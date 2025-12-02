document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('result');
    const resultIcon = document.getElementById('resultIcon');
    const predictionText = document.getElementById('predictionText');
    const resultDescription = document.getElementById('resultDescription');
    const resetBtn = document.getElementById('resetBtn');

    // API Endpoint
    const API_URL = 'https://pet-prediction-f477d70f900c.herokuapp.com/predict';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        // Collect data
        const formData = new FormData(form);
        const data = {
            "Gender": formData.get('Gender'),
            "Age": parseInt(formData.get('Age')),
            "Salary": parseInt(formData.get('Salary')),
            "Mental Condition": formData.get('Mental Condition'),
            "Allergies": formData.get('Allergies')
        };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            showResult(result.recommended_pet);

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to get prediction. Please try again.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    });

    function showResult(pet) {
        // Normalize pet string
        const petLower = pet.toLowerCase();

        // Breed Lists
        const dogBreeds = ['german shepherd', 'golden retriever', 'labrador retriever', 'pomeranian', 'dog'];
        const catBreeds = ['persian', 'siamese', 'himalayan', 'cat'];

        const isDog = dogBreeds.some(breed => petLower.includes(breed));
        const isCat = catBreeds.some(breed => petLower.includes(breed));

        if (isDog) {
            resultIcon.textContent = '🐶';
            predictionText.textContent = pet; // Show the specific breed
            resultDescription.textContent = `A loyal and energetic ${pet} would be your perfect companion!`;
        } else if (isCat) {
            resultIcon.textContent = '🐱';
            predictionText.textContent = pet; // Show the specific breed
            resultDescription.textContent = `A independent and cuddly ${pet} matches your lifestyle perfectly!`;
        } else {
            resultIcon.textContent = '🐾';
            predictionText.textContent = pet;
            resultDescription.textContent = 'This unique pet is the one for you!';
        }

        // Cost Display Logic
        const costContainer = document.getElementById('costContainer');
        let costHtml = '';

        if (isDog) {
            costHtml = `
                <div class="cost-info">
                    <h4>Estimated Monthly Cost</h4>
                    <div class="cost-grid">
                        <div class="cost-item">
                            <span class="cost-label">Small Dog</span>
                            <span class="cost-value">LKR 7,000 – 12,000</span>
                        </div>
                        <div class="cost-item">
                            <span class="cost-label">Medium Dog</span>
                            <span class="cost-value">LKR 9,000 – 15,000</span>
                        </div>
                        <div class="cost-item">
                            <span class="cost-label">Large Dog</span>
                            <span class="cost-value">LKR 13,000 – 25,000</span>
                        </div>
                    </div>
                </div>
            `;
        } else if (isCat) {
            costHtml = `
                <div class="cost-info">
                    <h4>Estimated Monthly Cost</h4>
                    <div class="cost-single">
                        <span class="cost-value">LKR 6,000 – 12,000</span>
                    </div>
                </div>
            `;
        }

        costContainer.innerHTML = costHtml;

        // Show result overlay
        resultContainer.classList.remove('hidden');
        // Small delay to allow display:block to apply before opacity transition
        setTimeout(() => {
            resultContainer.classList.add('active');
        }, 10);
    }

    resetBtn.addEventListener('click', () => {
        resultContainer.classList.remove('active');
        setTimeout(() => {
            resultContainer.classList.add('hidden');
            form.reset();
        }, 400); // Wait for transition
    });
});
