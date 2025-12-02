import pandas as pd
import random

# Constants
sri_lankan_names = {
    "male": [
        "Chaminda", "Kasun", "Rohan", "Thilan", "Pradeep", "Nuwan", "Mahesh", "Sanjeewa",
        "Dinesh", "Lakshman", "Sunil", "Wasantha", "Arjuna", "Gayan", "Ruwan", "Ajith",
        "Nihal", "Bandula", "Nalin", "Janaka", "Chatura", "Ananda", "Prasanna", "Upul",
        "Jayantha", "Tharindu", "Sampath", "Chamara", "Asanka", "Priyantha", "Chandana",
        "Ranil", "Mahinda", "Janith", "Anil", "Nishantha", "Sumith", "Asela", "Susantha",
        "Ranjith", "Buddhika", "Gamini", "Niroshan", "Sarath", "Lalith", "Piyal", "Palitha",
        "Dhananjaya", "Jayasinghe", "Samantha", "Tharaka", "Dilshan", "Lasantha", "Udaya",
        "Ravi", "Kumara", "Chandimal", "Thisara", "Viraj", "Dilan", "Chathura", "Lahiru"
    ],
    "female": [
        "Dilini", "Nimalka", "Shalini", "Amaya", "Sewwandi", "Rashmi", "Chandani", "Iresha",
        "Malini", "Kumari", "Nilmini", "Pramila", "Sanduni", "Chathurika", "Nethmi", "Samanthi",
        "Shanika", "Charuni", "Ayesha", "Manjula", "Dilhani", "Sachini", "Nadeeka", "Hansika",
        "Madushi", "Anusha", "Thilini", "Geethika", "Oshadi", "Priyani", "Kamani", "Gayathri",
        "Menaka", "Nimali", "Dilrukshi", "Chandrika", "Deepika", "Hasini", "Kaushalya", "Erandi",
        "Shashika", "Ishara", "Ruvini", "Nadeesha", "Tharindi", "Chathumini", "Pavithra", "Lakmini",
        "Ireshani", "Thilanka", "Sandya", "Hiruni", "Oshini", "Madhavi", "Menaka", "Dilini"
    ],
    "surnames": [
        "Perera", "Fernando", "Silva", "Jayawardena", "Wickramasinghe", "Rajapaksa", "Gunasekara",
        "Dissanayake", "Bandara", "Kumari", "Herath", "Liyanage", "Senanayake", "Wijesinghe",
        "Rodrigo", "Jayasuriya", "Samaraweera", "Mendis", "Amarasinghe", "Ranasinghe", "Ekanayake",
        "Wickremaratne", "Pathirana", "Wijesuriya", "Gamage", "De Silva", "Karunaratne", "Siriwardena",
        "Gunathilaka", "Jayakody", "Samarakoon", "Fonseka", "Gunawardena", "Welikala", "Ranatunga",
        "Yapa", "Hettiarachchi", "Madushani", "Vithanage", "Rajapaksha", "Abeysinghe", "Wickramage",
        "Cooray", "Rathnayake", "De Alwis", "Jayasundara", "Kumarasinghe", "Seneviratne", "Wickramaratne"
    ]
}

mental_conditions = [
    "PTSD", "Panic Disorder / Severe Anxiety", "Mild Anxiety", "Clinical Depression",
    "Mild Depression", "Autism", "Bipolar Disorder", "Schizophrenia", "OCD – Severe",
    "Loneliness", "Emotional Support"
]

def generate_name(gender):
    first_name = random.choice(sri_lankan_names[gender])
    surname = random.choice(sri_lankan_names["surnames"])
    return f"{first_name} {surname}"

data = []
for _ in range(1000):
    gender = "male" if random.random() > 0.5 else "female"
    name = generate_name(gender)
    age = random.randint(18, 100)
    salary = random.randint(68000, 150000)
    mental_condition = random.choice(mental_conditions)
    allergies = "yes" if random.random() > 0.85 else "no"

    # --- NEW LOGIC START ---
    # Breeds
    dog_breeds = ["German Shepherd", "Golden Retriever", "Labrador Retriever", "Pomeranian"]
    cat_breeds = ["Persian", "Siamese", "Himalayan"]

    # Scores for each breed
    breed_scores = {breed: 0 for breed in dog_breeds + cat_breeds}

    # 1. Allergies (Cats are generally worse for allergies, but we'll assume "yes" means avoid pets or prefer hypoallergenic - let's simplify: if allergies, reduce all pets, maybe prefer fish? But we only have dogs/cats. Let's reduce all, but maybe some dogs are better? Let's just reduce probability of any pet, but if they MUST have one (which this script assumes they have one), maybe no strong preference change between breeds for now, or maybe hairless cats? We don't have those. Let's assume allergies -> lower chance of high-shedding breeds.)
    # For this synthetic data, let's say Allergies = 'yes' makes them less likely to be 'Satisfied' with high shedding pets, but here we are predicting the BEST pet.
    # Let's assume if Allergies=Yes, we might prefer "Pomeranian" (smaller) or "Siamese" (shorter hair) over "German Shepherd" or "Persian".
    if allergies == "yes":
        breed_scores["Pomeranian"] += 2
        breed_scores["Siamese"] += 2
        breed_scores["German Shepherd"] -= 2
        breed_scores["Persian"] -= 2

    # 2. Age
    if age < 30:
        # Young people might like active dogs
        breed_scores["German Shepherd"] += 3
        breed_scores["Golden Retriever"] += 2
        breed_scores["Labrador Retriever"] += 2
    elif age > 60:
        # Elderly might prefer calmer/smaller pets
        breed_scores["Pomeranian"] += 4
        breed_scores["Persian"] += 4
        breed_scores["Himalayan"] += 3
        breed_scores["German Shepherd"] -= 3 # Too active/strong

    # 3. Salary
    # Larger dogs might cost more to feed/maintain
    if salary > 120000:
        breed_scores["German Shepherd"] += 1
        breed_scores["Golden Retriever"] += 1
        breed_scores["Persian"] += 1 # Grooming costs
    elif salary < 80000:
        breed_scores["Pomeranian"] += 1 # Smaller, less food
        breed_scores["Siamese"] += 1

    # 4. Mental Condition
    if "Anxiety" in mental_condition or "PTSD" in mental_condition:
        # Protective or comforting
        breed_scores["German Shepherd"] += 2 # Protective
        breed_scores["Golden Retriever"] += 3 # Comforting
        breed_scores["Labrador Retriever"] += 3
    elif "Depression" in mental_condition or "Loneliness" in mental_condition:
        # Companionship
        breed_scores["Golden Retriever"] += 3
        breed_scores["Labrador Retriever"] += 3
        breed_scores["Pomeranian"] += 2
        breed_scores["Siamese"] += 2 # Talkative
    elif "Autism" in mental_condition:
        # Gentle, predictable
        breed_scores["Golden Retriever"] += 3
        breed_scores["Labrador Retriever"] += 3
        breed_scores["Himalayan"] += 2

    # Select breed with highest score + some randomness
    # Add random noise to scores to ensure variety
    for breed in breed_scores:
        breed_scores[breed] += random.uniform(-1, 1)

    owned_pet = max(breed_scores, key=breed_scores.get)
    # --- NEW LOGIC END ---

    satisfied = "yes" if random.random() > 0.15 else "no"

    data.append([name, gender, age, salary, owned_pet, mental_condition, allergies, satisfied])

df = pd.DataFrame(data, columns=["Name", "Gender", "Age", "Salary", "Pet", "Mental Condition", "Allergies", "Satisfaction"])
df.to_csv('pet_data.csv', index=False)
print("✅ Regenerated pet_data.csv with improved logic.")
