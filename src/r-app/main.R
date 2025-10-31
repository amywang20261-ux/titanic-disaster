# src/r-app/main.R
# Minimal, clear R version of your Python script

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

message("Loading train.csv ...")
train <- read_csv("src/data/train.csv", show_col_types = FALSE)

needed <- c("Survived","Pclass","Sex","Age","Fare","SibSp","Parch","Embarked")
miss <- setdiff(needed, names(train))
if (length(miss)) stop("Missing columns in train.csv: ", paste(miss, collapse=", "))

df <- train[, needed]

# encode + impute
df$Sex <- ifelse(df$Sex == "male", 1L, 0L)

# Embarked: fill NA with mode, then map S=0, C=1, Q=2
mode_emb <- names(sort(table(df$Embarked), decreasing=TRUE))[1]
df$Embarked[is.na(df$Embarked)] <- mode_emb
emap <- c(S=0L, C=1L, Q=2L)
df$Embarked <- unname(emap[as.character(df$Embarked)])

# median impute
for (c in c("Age","Fare")) df[[c]][is.na(df[[c]])] <- median(df[[c]], na.rm=TRUE)

x_cols <- c("Pclass","Sex","Age","Fare","SibSp","Parch","Embarked")

message("Training logistic regression ...")
# glm binomial (logistic)
fit <- glm(Survived ~ ., data = df[, c("Survived", x_cols)], family = binomial())

# training accuracy
p_tr  <- ifelse(predict(fit, type="response") >= 0.5, 1L, 0L)
acc_tr <- mean(p_tr == df$Survived)
message(sprintf("Training accuracy: %.4f", acc_tr))

# ---------- test ----------
message("Loading test.csv ...")
test <- read_csv("src/data/test.csv", show_col_types = FALSE)
need_t <- x_cols
miss_t <- setdiff(need_t, names(test))
if (length(miss_t)) stop("Missing columns in test.csv: ", paste(miss_t, collapse=", "))

tp <- test

tp$Sex <- ifelse(tp$Sex == "male", 1L, 0L)
mode_emb_t <- names(sort(table(tp$Embarked), decreasing=TRUE))[1]
tp$Embarked[is.na(tp$Embarked)] <- mode_emb_t
tp$Embarked <- unname(emap[as.character(tp$Embarked)])
for (c in c("Age","Fare")) tp[[c]][is.na(tp[[c]])] <- median(tp[[c]], na.rm=TRUE)

p_te <- ifelse(predict(fit, newdata = tp[, x_cols], type="response") >= 0.5, 1L, 0L)

if ("Survived" %in% names(test)) {
  acc_te <- mean(p_te == test$Survived)
  message(sprintf("Test accuracy: %.4f", acc_te))
} else {
  message("Test file has no 'Survived' column; outputting predictions only.")
}

# ---------- write predictions next to train/test ----------
if ("PassengerId" %in% names(test)) {
  out <- tibble(PassengerId = test$PassengerId, Survived = p_te)
} else {
  out <- tibble(Id = seq_len(length(p_te)), Survived = p_te)
}
out_path <- "src/data/predictions_r.csv"
write_csv(out, out_path)
message(sprintf("Saved predictions to %s", out_path))
