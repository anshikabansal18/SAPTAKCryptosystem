import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("crypto_eval_dataset.csv")
X = data[["plaintext_len", "bit_diff_ratio"]]

# Label: 1 = Good diffusion, 0 = Weak diffusion
y = (data["bit_diff_ratio"] >= 0.45).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Evaluation Model Accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, "saptak_crypto_evaluator.pkl")
print("Crypto evaluator model saved.")

