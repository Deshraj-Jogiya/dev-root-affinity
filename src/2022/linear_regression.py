import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Mock dataset: Study Hours vs. Exam Score
# X: Study hours (independent variable, reshaped to 2D array for scikit-learn)
# y: Exam score (dependent variable)
X = np.array([1.5, 2.0, 3.0, 4.0, 4.5, 5.0, 6.0, 7.0, 8.5, 9.0]).reshape(-1, 1)
y = np.array([45, 50, 62, 70, 72, 78, 85, 89, 95, 98])

def train_linear_model():
    # Instantiate the linear regression model
    model = LinearRegression()
    
    # Fit the model
    model.fit(X, y)
    
    # Predict exam scores based on study hours
    predictions = model.predict(X)
    
    # Model parameters
    slope = model.coef_[0]
    intercept = model.intercept_
    
    # Metrics
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    
    print("=== Scikit-Learn Linear Regression model ===")
    print(f"Regression Equation: y = {slope:.3f} * x + {intercept:.3f}")
    print(f"Mean Squared Error (MSE): {mse:.3f}")
    print(f"R-squared (R2) Score: {r2:.3f}")
    
    # Predict score for a student studying 6.5 hours
    test_hour = [[6.5]]
    predicted_score = model.predict(test_hour)[0]
    print(f"\nPredicted score for 6.5 hours of study: {predicted_score:.2f}%")

if __name__ == "__main__":
    train_linear_model()
