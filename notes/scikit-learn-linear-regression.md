# Linear Regression with Scikit-Learn

Linear Regression is a fundamental supervised machine learning algorithm used to model the relationship between a scalar dependent variable $y$ and one or more independent variables $X$.

## Mathematical Representation
The relationship is modeled as:
$$y = w X + b + \epsilon$$

Where:
- $w$ is the coefficient (slope).
- $b$ is the intercept.
- $\epsilon$ is the error term.

## Implementation Steps in Scikit-Learn

1. **Instantiation**: Create a regression object.
   ```python
   from sklearn.linear_model import LinearRegression
   model = LinearRegression()
   ```
2. **Fitting**: Train the model on the data matrix $X$ (which must be 2D) and target vector $y$.
   ```python
   model.fit(X, y)
   ```
3. **Prediction**: Predict values for new inputs.
   ```python
   predictions = model.predict(new_X)
   ```
4. **Evaluation**: Assess regression performance using metrics like Mean Squared Error (MSE) and Coefficient of Determination ($R^2$ score).

## Runnable Example
For a complete, runnable example using mock study hours to predict exam grades, refer to the source file at [linear_regression.py](file:///G:/dev-root-affinity/src/2022/linear_regression.py).

---
*Logged on 2022-01-23 12:35:00 (UTC)*
