import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print("▶️ Loading training data from src/data/train.csv ...")
train = pd.read_csv("src/data/train.csv")

print("\n🔎 Train head:")
print(train.head())

# --- simple preprocessing (keep it transparent & reproducible) ---
print("\n🧹 Preprocessing...")
cols_needed = ["Survived", "Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
missing = [c for c in cols_needed if c not in train.columns]
if missing:
    raise ValueError(f"Expected columns missing from train.csv: {missing}")

df = train[cols_needed].copy()

# Encode categoricals
df["Sex"] = (df["Sex"] == "male").astype(int)
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0])
df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2}).astype(int)

# Impute numerics
for c in ["Age", "Fare"]:
    df[c] = df[c].fillna(df[c].median())

X_cols = ["Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
X = df[X_cols].values
y = df["Survived"].values

print(f"✅ Features ready. Shape X={X.shape}, y={y.shape}")

# --- train logistic regression ---
print("\n🤖 Training LogisticRegression...")
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# --- training accuracy ---
train_pred = model.predict(X)
train_acc = accuracy_score(y, train_pred)
print(f"📈 Training accuracy: {train_acc:.4f}")

# --- test set ---
print("\n▶️ Loading test data from src/data/test.csv ...")
test = pd.read_csv("src/data/test.csv")

# If your test has no Survived column (Kaggle style), we'll still run predictions
has_label = "Survived" in test.columns
test_proc = test.copy()

# same transforms as train
need_test = ["Pclass", "Sex", "Age", "Fare", "SibSp", "Parch", "Embarked"]
missing_t = [c for c in need_test if c not in test_proc.columns]
if missing_t:
    raise ValueError(f"Expected columns missing from test.csv: {missing_t}")

test_proc["Sex"] = (test_proc["Sex"] == "male").astype(int)
test_proc["Embarked"] = test_proc["Embarked"].fillna(test_proc["Embarked"].mode().iloc[0])
test_proc["Embarked"] = test_proc["Embarked"].map({"S": 0, "C": 1, "Q": 2}).astype(int)
for c in ["Age", "Fare"]:
    test_proc[c] = test_proc[c].fillna(test_proc[c].median())

X_test = test_proc[X_cols].values
test_pred = model.predict(X_test)
print("\n🔮 First 20 predictions on test:")
print(test_pred[:20])

if has_label:
    test_acc = accuracy_score(test_proc["Survived"].values, test_pred)
    print(f"✅ Test accuracy: {test_acc:.4f}")
else:
    print("ℹ️ Test file has no 'Survived' column; printed predictions only.")
