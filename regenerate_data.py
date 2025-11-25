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
    dog_probability = 0.5

    # Rule 1: Allergies
    if allergies == "yes":
        dog_probability -= 0.8

    # Rule 2: Age
    if age < 35:
        dog_probability += 0.3
    elif age > 60:
        dog_probability -= 0.3

    # Rule 3: Salary
    if salary > 120000:
        dog_probability += 0.2

    # Rule 4: Mental Condition
    if "Depression" in mental_condition or "Loneliness" in mental_condition:
        dog_probability += 0.3
    if "Anxiety" in mental_condition or "Autism" in mental_condition or "Stress" in mental_condition:
        dog_probability -= 0.2

    # Clamp
    dog_probability = max(0, min(1, dog_probability))

    owned_pet = "dog" if random.random() < dog_probability else "cat"
    # --- NEW LOGIC END ---

    satisfied = "yes" if random.random() > 0.15 else "no"

    data.append([name, gender, age, salary, owned_pet, mental_condition, allergies, satisfied])

df = pd.DataFrame(data, columns=["Name", "Gender", "Age", "Salary", "Pet", "Mental Condition", "Allergies", "Satisfaction"])
df.to_csv('pet_data.csv', index=False)
print("✅ Regenerated pet_data.csv with improved logic.")
