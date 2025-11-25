import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# ==========================================
# 1. Load and Filter Data
# ==========================================

# Load the dataset (Assuming it's a CSV based on your schema image)
# Replace 'pet_data.csv' with your actual file path
df = pd.read_csv('pet_data.csv')

print(f"Total records before filtering: {len(df)}")

# FILTER LOGIC: Keep only users who are 'Satisfied'
# (Adjust 'Satisfied' to match the exact text or score in your dataset)
df_satisfied = df[df['Satisfaction'] == 'yes'].copy()

print(f"Records after filtering for satisfaction: {len(df_satisfied)}")

# ==========================================
# 2. Define Features and Target
# ==========================================

# We drop 'Name' because it doesn't predict pet suitability
# We drop 'Satisfaction' because we've already used it for filtering
X = df_satisfied[['Gender', 'Age', 'Salary', 'Mental Condition', 'Allergies']]
y = df_satisfied['Pet']  # Target variable (Cat or Dog)

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 3. Build the Preprocessing Pipeline
# ==========================================

# Define which columns are which type
categorical_features = ['Gender', 'Mental Condition', 'Allergies']
numeric_features = ['Age', 'Salary']

# Create transformers
# 1. Numeric: Standardize them (scale to mean 0, variance 1)
numeric_transformer = StandardScaler()

# 2. Categorical: One-Hot Encode them (convert 'Male'/'Female' to 0/1 columns)
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Combine them into a single ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# ==========================================
# 4. Train the Random Forest Model
# ==========================================

# Create a full pipeline: Preprocessor -> Classifier
# This ensures that any new data (from the website) goes through the exact same steps
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
])

print("Training model...")
clf.fit(X_train, y_train)
print("Model training complete.")

# Evaluate accuracy
accuracy = clf.score(X_test, y_test)
print(f"Model Accuracy on Test Set: {accuracy:.2f}")

# ==========================================
# 5. Save the Model
# ==========================================

# Save the entire pipeline (includes the preprocessor and the model)
joblib.dump(clf, 'pet_suggestion_model.pkl')

print("✅ Model saved as 'pet_suggestion_model.pkl'")