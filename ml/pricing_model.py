import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# Sample training data (dummy values: time_of_day, duration, occupancy_rate)[cite: 25]
X_train = np.array([[8, 30, 0.8], [12, 60, 0.6], [18, 45, 0.9], [22, 20, 0.4]])
y_train = np.array([50, 90, 70, 30]) # Sample pricing (₹)

# Train model[cite: 25]
model = LinearRegression()
model.fit(X_train, y_train)

# Save model[cite: 25]
with open("pricing_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Pricing model saved as 'pricing_model.pkl'")