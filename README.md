# 🚢 Titanic Survival Prediction (Python + R)

This project trains logistic regression models in **Python** and **R** to predict Titanic passenger survival.  
Both scripts run inside **Docker containers** and save predictions to the shared `src/data/` folder.

---

## 📁 Repository Structure

```plaintext
titanic-disaster/
├─ src/
│  ├─ app/                 # Python code
│  │  └─ main.py
│  ├─ r-app/               # R code
│  │  └─ main.R
│  └─ data/                # Place CSV files here
│     ├─ train.csv
│     ├─ test.csv
│     ├─ predictions.csv       # Python output
│     └─ predictions_r.csv     # R output
├─ Dockerfile              # Python Dockerfile
├─ Dockerfile.r            # R Dockerfile
├─ install_packages.R      # R package install script
├─ requirements.txt        # Python packages
└─ README.md

## 📥 Step 1 — Download Data

Place the following files in `src/data/`:

- `train.csv`
- `test.csv`

⚠️ These files are **NOT stored in the repo**. You must add them manually.

---

## 🐍 Step 2 — Build & Run Python Model (Docker)

### Build the Python image

```bash
docker build -t titanic-python .

---

## 📊 Step 3 — Build & Run R Model (Docker)

### ✅ Build the R Docker image
```bash
docker build -f Dockerfile.r -t titanic-r .
▶️ Run the R container
docker run --rm \
  -v "$PWD/src/data:/app/src/data" \
  titanic-r


✔️ Prints model accuracy
✔️ Creates src/data/predictions_r.csv

## 🧠 Modeling Notes

| Pipeline Step | Description                          |
| ------------- | ------------------------------------ |
| Input         | `train.csv`, `test.csv`              |
| Encoding      | `Sex` (0/1), `Embarked` (0/1/2)      |
| Missing Data  | Median imputation for `Age` & `Fare` |
| Model         | Logistic Regression                  |
| Output        | `.csv` predictions for Python & R    |

## 🧪 Optional — Run Without Docker

🐍 Python Local Run

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python src/app/main.py

## 📦 R Local Run

install.packages(c("readr", "dplyr"))

source("src/r-app/main.R")

## ✅ Submission Checklist

| Task                             | Complete |
| -------------------------------- | -------- |
| Python Docker working            | ✅        |
| R Docker working                 | ✅        |
| Predictions saved to `src/data/` | ✅        |
| README written with instructions | ✅        |
| Pull Request submitted           | ✅        |

## 🤝 Notes For Grader

To reproduce results:

docker build -t titanic-python .

docker run --rm -v "$PWD/src/data:/app/src/data" titanic-python

docker build -f Dockerfile.r -t titanic-r .

docker run --rm -v "$PWD/src/data:/app/src/data" titanic-r

OUPUT to verify:

src/data/predictions.csv

src/data/predictions_r.csv

Amy Wang
