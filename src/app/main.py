# src/app/main.py
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ---------- load train ----------
print("Loading train.csv ...")
train = pd.read_csv("src/data/train.csv")

# keep only needed columns
cols = ["Survived", "Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
missing = [c for c in cols if c not in train.columns]
if missing:
    raise ValueError(f"Missing columns in train.csv: {missing}")
df = train[cols].copy()

# encode + impute
df["Sex"] = (df["Sex"] == "male").astype(int)
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0]).map({"S":0,"C":1,"Q":2}).astype(int)
for c in ["Age", "Fare"]:
    df[c] = df[c].fillna(df[c].median())

X_cols = ["Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
X = df[X_cols].to_numpy()
y = df["Survived"].to_numpy()
print(f"Train shape: X={X.shape}, y={y.shape}")

# ---------- fit model ----------
print("Training logistic regression ...")
model = LogisticRegression(max_iter=1000)
model.fit(X, y)
train_acc = accuracy_score(y, model.predict(X))
print(f"Training accuracy: {train_acc:.4f}")

# ---------- load test + predict ----------
print("Loading test.csv ...")
test = pd.read_csv("src/data/test.csv")
need = ["Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
missing_t = [c for c in need if c not in test.columns]
if missing_t:
    raise ValueError(f"Missing columns in test.csv: {missing_t}")

test_proc = test.copy()
test_proc["Sex"] = (test_proc["Sex"] == "male").astype(int)
test_proc["Embarked"] = test_proc["Embarked"].fillna(test_proc["Embarked"].mode().iloc[0]).map({"S":0,"C":1,"Q":2}).astype(int)
for c in ["Age", "Fare"]:
    test_proc[c] = test_proc[c].fillna(test_proc[c].median())

X_test = test_proc[X_cols].to_numpy()
test_pred = model.predict(X_test)

# optional test accuracy if label is present
if "Survived" in test_proc.columns:
    test_acc = accuracy_score(test_proc["Survived"].to_numpy(), test_pred)
    print(f"Test accuracy: {test_acc:.4f}")

print("First 20 predictions:", test_pred[:20])

# ---------- write predictions ----------
if "PassengerId" in test.columns:
    out = pd.DataFrame({"PassengerId": test["PassengerId"], "Survived": test_pred.astype(int)})
else:
    out = pd.DataFrame({"Id": np.arange(1, len(test_pred)+1), "Survived": test_pred.astype(int)})

out_path = "src/data/predictions.csv"
out.to_csv(out_path, index=False)
print(f"Saved predictions to {out_path}")
