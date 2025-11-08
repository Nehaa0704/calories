import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
df = pd.read_csv("dataset.csv")

# Select features
X = df[['Very_Active_Minutes', 'Fairly_Active_Minutes', 'Lightly_Active_Minutes', 'Steps']]
y = df['Calories_Burned']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Save Model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and model.pkl saved successfully!")
