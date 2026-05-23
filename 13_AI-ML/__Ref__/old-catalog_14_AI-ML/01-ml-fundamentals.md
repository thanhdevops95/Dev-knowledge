# Machine Learning Fundamentals

> **Tags:** `ml` `supervised` `unsupervised` `classification` `regression` `neural-networks` `sklearn`
> **Level:** Intermediate | **Prerequisite:** `numpy-pandas basics`

---

## 1. ML Landscape

```
Artificial Intelligence
  └── Machine Learning
        ├── Supervised Learning        ← Labeled data, predict output
        │     ├── Classification       (output = category)
        │     └── Regression           (output = continuous number)
        ├── Unsupervised Learning      ← Unlabeled data, find patterns
        │     ├── Clustering
        │     └── Dimensionality Reduction
        ├── Semi-supervised Learning   ← Mix of labeled + unlabeled
        ├── Self-supervised Learning   ← Model creates its own labels (LLMs, BERT)
        └── Reinforcement Learning     ← Agent learns from rewards/penalties
```

---

## 2. Supervised Learning — Key Algorithms

### Linear Regression
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Data preparation
X = df[['bedrooms', 'bathrooms', 'sqft', 'location_score']].values
y = df['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")   # 1.0 = perfect
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

print(f"Coefficients: {model.coef_}")     # Feature importance
print(f"Intercept: {model.intercept_}")
```

**Equation**: `price = w1*bedrooms + w2*bathrooms + ... + bias`

Gradient Descent updates:
```
For each parameter w:
  w = w - learning_rate * ∂Loss/∂w

Loss = MSE = (1/n) * Σ(y_pred - y_actual)²
```

### Logistic Regression (Classification)
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Binary classification: spam or not spam
clf = LogisticRegression(C=1.0, max_iter=1000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]   # Probability of class 1

print(classification_report(y_test, y_pred))
# Output:
#               precision    recall  f1-score   support
#            0       0.95      0.98      0.96       952
#            1       0.89      0.73      0.80       200

print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
# [[TP, FP],
#  [FN, TN]]
```

**Sigmoid function**: `P(y=1) = 1 / (1 + e^(-z))` where `z = w·x + b`

### Decision Tree
```python
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

# Decision tree: interpretable, no scaling needed
tree = DecisionTreeClassifier(
    max_depth=5,           # Prevent overfitting
    min_samples_leaf=20,   # Minimum samples per leaf
    criterion='gini'       # gini or entropy
)
tree.fit(X_train, y_train)

# Visualize
print(export_text(tree, feature_names=feature_names))

plt.figure(figsize=(20, 10))
plot_tree(tree, feature_names=feature_names, class_names=['No', 'Yes'], filled=True)
plt.show()

# Feature importance
importances = dict(zip(feature_names, tree.feature_importances_))
sorted_importance = sorted(importances.items(), key=lambda x: x[1], reverse=True)
```

### Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

# Ensemble of decision trees — reduces overfitting
rf = RandomForestClassifier(
    n_estimators=100,     # 100 trees
    max_depth=10,
    min_samples_leaf=10,
    n_jobs=-1,            # Use all CPU cores
    random_state=42
)
rf.fit(X_train, y_train)

# Feature importance (more reliable than single tree)
feature_imp = pd.Series(
    rf.feature_importances_,
    index=feature_names
).sort_values(ascending=False)
```

### Gradient Boosting (XGBoost)
```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss',
    early_stopping_rounds=10,    # Stop if no improvement
    n_jobs=-1
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=50
)

# Best for tabular data competitions (Kaggle)
# XGBoost > LightGBM > CatBoost for different scenarios
```

---

## 3. Unsupervised Learning

### K-Means Clustering
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Scale features first!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal k using elbow method
inertias = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(k_range, inertias, 'bx-')
plt.xlabel('k'); plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()    # Look for "elbow" in curve

# Fit with chosen k
km = KMeans(n_clusters=3, n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)
df['cluster'] = labels

# Analyze clusters
df.groupby('cluster').mean()
```

### PCA — Principal Component Analysis
```python
from sklearn.decomposition import PCA

# Reduce 100-dim features to 2D for visualization
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)

print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {pca.explained_variance_ratio_.sum():.2%}")

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='viridis')

# For compression, choose n_components to retain 95% variance
pca_95 = PCA(n_components=0.95)   # Auto-select
X_compressed = pca_95.fit_transform(X_scaled)
print(f"Components needed for 95% variance: {pca_95.n_components_}")
```

---

## 4. ML Pipeline — scikit-learn

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Separate numeric and categorical features
numeric_features = ['age', 'income', 'score']
categorical_features = ['city', 'occupation', 'education']

# Preprocessing steps
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features),
])

# Full pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100)),
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate (preprocessing is applied automatically)
score = pipeline.score(X_test, y_test)

# Serialize (always serialize the full pipeline!)
import joblib
joblib.dump(pipeline, 'model.joblib')
pipeline = joblib.load('model.joblib')

# Predict on raw data (pipeline handles preprocessing)
prediction = pipeline.predict(new_raw_data)
```

---

## 5. Cross-Validation & Hyperparameter Tuning

```python
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from scipy.stats import randint, uniform

# K-Fold Cross-Validation
scores = cross_val_score(
    RandomForestClassifier(n_estimators=100),
    X, y,
    cv=5,              # 5-fold
    scoring='f1_macro',
    n_jobs=-1
)
print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.3f} ± {scores.std():.3f}")

# Grid Search
param_grid = {
    'classifier__n_estimators': [100, 200, 500],
    'classifier__max_depth': [5, 10, None],
    'classifier__min_samples_leaf': [1, 5, 20],
}
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1_macro', n_jobs=-1)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")

# Randomized Search (faster for large search space)
param_distributions = {
    'classifier__n_estimators': randint(50, 500),
    'classifier__max_depth': randint(3, 20),
    'classifier__learning_rate': uniform(0.01, 0.3),
}
random_search = RandomizedSearchCV(
    pipeline, param_distributions,
    n_iter=50, cv=5, scoring='f1_macro', n_jobs=-1
)
random_search.fit(X_train, y_train)

# Optuna (modern Bayesian optimization — more efficient)
import optuna

def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 500)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    learning_rate = trial.suggest_float('learning_rate', 0.01, 0.3, log=True)
    
    model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, 
                          learning_rate=learning_rate)
    score = cross_val_score(model, X_train, y_train, cv=3, scoring='f1_macro').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
print(f"Best: {study.best_params}")
```

---

## 6. Neural Networks — PyTorch

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Data
X_tensor = torch.FloatTensor(X_train)
y_tensor = torch.LongTensor(y_train)
dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Model definition
class MLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dims: list[int], output_dim: int):
        super().__init__()
        layers = []
        prev_dim = input_dim
        for dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, dim),
                nn.BatchNorm1d(dim),    # Batch normalization
                nn.ReLU(),
                nn.Dropout(0.3),        # Regularization
            ])
            prev_dim = dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

# Training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MLP(input_dim=20, hidden_dims=[256, 128, 64], output_dim=2).to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)
criterion = nn.CrossEntropyLoss()

for epoch in range(100):
    model.train()
    for batch_X, batch_y in loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        
        # Gradient clipping (prevents exploding gradients)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
    
    # Validation
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val_tensor.to(device))
        val_loss = criterion(val_outputs, y_val_tensor.to(device))
    scheduler.step(val_loss)
```

---

## 7. Evaluation Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, average_precision_score,
    confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

# Classification metrics
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall:    {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.3f}")
print(f"PR-AUC:    {average_precision_score(y_test, y_pred_proba):.3f}")

# Confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred))
disp.plot()

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr, label=f'ROC (AUC={roc_auc_score(y_test, y_pred_proba):.3f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
```

**Chọn metric:**
- **Balanced data**: Accuracy
- **Imbalanced, FP costly** (spam filter): Precision
- **Imbalanced, FN costly** (cancer detection): Recall
- **Balance both**: F1 Score
- **Ranking/probability**: ROC-AUC, PR-AUC

---

## 8. MLflow — Experiment Tracking

```python
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("house-price-prediction")

with mlflow.start_run(run_name="random-forest-v2"):
    # Log parameters
    mlflow.log_params({
        "n_estimators": 200,
        "max_depth": 10,
        "min_samples_leaf": 5,
    })
    
    # Train model
    rf = RandomForestClassifier(n_estimators=200, max_depth=10)
    rf.fit(X_train, y_train)
    
    # Log metrics
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, rf.predict(X_test)),
        "f1_score": f1_score(y_test, rf.predict(X_test)),
        "roc_auc": roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1]),
    })
    
    # Log model
    mlflow.sklearn.log_model(rf, "model", registered_model_name="house-price")
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_artifact("confusion_matrix.png")

# Compare runs in MLflow UI: mlflow ui --port 5000
```

---

## 9. Overfitting & Regularization

```python
# Signs of overfitting:
# Train accuracy = 99%, Test accuracy = 75% → big gap = overfitting

# Solutions:

# 1. More data
# 2. Feature selection (remove irrelevant features)
# 3. Cross-validation (detect before deployment)

# 4. Regularization
from sklearn.linear_model import Ridge, Lasso, ElasticNet

# Ridge (L2): penalize large weights → keeps all features, reduces magnitude
ridge = Ridge(alpha=1.0)   # alpha = regularization strength

# Lasso (L1): penalize sum of |weights| → sets some weights to 0 (feature selection)
lasso = Lasso(alpha=0.1)

# ElasticNet: combination of L1 + L2
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # l1_ratio: 0 = Ridge, 1 = Lasso

# 5. Early stopping (for iterative models)
# 6. Dropout (neural networks)
# 7. Reduce model complexity (depth, hidden layers)
```

---

## 10. Bài tập

1. **Titanic**: Predict survival trên Titanic dataset. Goal: F1 score > 0.80.
2. **Customer segmentation**: Dùng K-Means để segment khách hàng từ e-commerce dataset.
3. **House prices**: Regression problem — điều chỉnh hyperparameters XGBoost để đạt RMSE < 30000.
4. **Pipeline**: Tạo complete sklearn pipeline với preprocessing + model + cross-validation.
5. **MLflow tracking**: Log 5 model variants với different hyperparameters, compare trong UI.

---

*Tài liệu liên quan: `ai-ml/02-numpy-pandas.md` | `ai-ml/03-deep-learning.md` | `ai-ml/04-nlp-transformers.md`*
