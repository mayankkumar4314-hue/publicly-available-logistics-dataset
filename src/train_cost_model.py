"""Train and evaluate a linear model for simulated transportation cost."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from prepare_model_data import load_model_data


def main() -> None:
    X, y = load_model_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Features:", list(X.columns))
    print("Training records:", len(X_train))
    print("Test records:", len(X_test))
    print("MAE:", mean_absolute_error(y_test, predictions))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, predictions)))
    print("R2:", r2_score(y_test, predictions))


if __name__ == "__main__":
    main()
