# 🤖 AI & Machine Learning — Bắt đầu từ đâu?

> `[INTERMEDIATE]` — Từ toán học nền tảng đến xây dựng model thực tế

---

## Lộ trình học AI/ML

```
Toán học nền tảng
    ↓
Python + Numpy + Pandas
    ↓
Machine Learning cơ bản (Scikit-learn)
    ↓
Deep Learning (PyTorch / TensorFlow)
    ↓
NLP / Computer Vision / Tabular (chọn 1)
    ↓
MLOps (deploy model ra production)
```

---

## Toán học cần thiết (Không cần chuyên sâu ban đầu)

| Môn | Cần biết |
|---|---|
| **Đại số tuyến tính** | Vectors, Matrices, Dot product, Eigenvectors |
| **Giải tích** | Đạo hàm, Chain rule (cho backpropagation) |
| **Xác suất & Thống kê** | Mean, Variance, Distribution, Bayes theorem |

---

## Machine Learning là gì?

```
Traditional Programming:
  Input + Rules → Output

Machine Learning:
  Input + Output → Rules (Model)
```

**3 loại học chính:**
1. **Supervised Learning** — Học từ dữ liệu có nhãn (classification, regression)
2. **Unsupervised Learning** — Tìm pattern trong dữ liệu không nhãn (clustering)
3. **Reinforcement Learning** — Học qua thử-sai với reward/penalty

---

## Python cho AI/ML

```bash
pip install numpy pandas scikit-learn matplotlib seaborn jupyter
```

```python
import numpy as np
import pandas as pd

# Numpy — Tính toán ma trận hiệu quả
arr = np.array([1, 2, 3, 4, 5])
matrix = np.zeros((3, 3))
dot = np.dot(A, B)
mean = np.mean(arr)

# Pandas — Xử lý dữ liệu dạng bảng
df = pd.read_csv("data.csv")
df.head()                           # Xem 5 dòng đầu
df.info()                           # Thông tin cột, dtype
df.describe()                       # Thống kê cơ bản
df["age"].fillna(df["age"].mean())  # Điền giá trị thiếu
df.dropna()                         # Xóa row có NaN
df.groupby("category")["sales"].sum()
```

---

## Scikit-learn — ML cơ bản

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load và chia dữ liệu
X = df.drop("target", axis=1)   # Features
y = df["target"]                 # Labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Preprocessing
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)   # Không fit lại trên test!

# 3. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))

# 5. Predict
new_data = scaler.transform([[25, 50000, 1]])
prediction = model.predict(new_data)
```

---

## Các thuật toán ML quan trọng

### Regression (Dự đoán số)
| Thuật toán | Khi nào dùng |
|---|---|
| Linear Regression | Quan hệ tuyến tính đơn giản |
| Ridge/Lasso | Có regularization chống overfitting |
| Random Forest | Dữ liệu phức tạp, nhiều features |
| XGBoost/LightGBM | Competition, tabular data |

### Classification (Phân loại)
| Thuật toán | Khi nào dùng |
|---|---|
| Logistic Regression | Baseline đơn giản |
| SVM | High-dimensional data |
| Random Forest | Mạnh với mọi loại data |
| Neural Network | Ảnh, text, âm thanh |

### Clustering
| Thuật toán | Khi nào dùng |
|---|---|
| K-Means | Biết số cluster |
| DBSCAN | Cluster hình dạng bất kỳ |
| Hierarchical | Không biết số cluster |

---

## Deep Learning với PyTorch

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# 1. Định nghĩa model
class MLP(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

# 2. Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MLP(input_size=10, hidden_size=64, output_size=1).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.BCEWithLogitsLoss()

# 3. Training loop
def train(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    
    for batch_X, batch_y in dataloader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_X).squeeze()
        loss = criterion(outputs, batch_y.float())
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(dataloader)

# 4. Eval
def evaluate(model, dataloader, device):
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for batch_X, batch_y in dataloader:
            batch_X = batch_X.to(device)
            outputs = model(batch_X).squeeze()
            predicted = (torch.sigmoid(outputs) > 0.5).cpu()
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)
    
    return correct / total
```

---

## Working with LLMs (Large Language Models)

```python
# OpenAI API
from openai import OpenAI

client = OpenAI()

# Chat Completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Bạn là trợ lý lập trình."},
        {"role": "user", "content": "Giải thích recursion bằng ví dụ Python"}
    ],
    temperature=0.7,
    max_tokens=1000
)
print(response.choices[0].message.content)

# Embeddings — Vector representation of text
embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="Machine learning là gì?"
)
vector = embedding.data[0].embedding  # List[float] độ dài 1536
```

---

## MLOps Cơ bản

```python
# Lưu và load model
import joblib

# Save
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

# Load
model = joblib.load("model.pkl")

# MLflow — Experiment tracking
import mlflow

mlflow.set_experiment("my-classification")

with mlflow.start_run():
    mlflow.log_params({
        "n_estimators": 100,
        "max_depth": 5,
        "learning_rate": 0.01
    })
    
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
```

---

## Bài tập thực hành

- [ ] **Titanic** — Classification với Scikit-learn (Kaggle)
- [ ] **Housing Prices** — Regression (Kaggle)
- [ ] **Image Classifier** — CIFAR-10 với CNN (PyTorch)
- [ ] **Sentiment Analysis** — Phân tích review phim
- [ ] **Chatbot đơn giản** — Dùng OpenAI API

---

## Tài nguyên thêm

- [fast.ai](https://www.fast.ai/) — Practical Deep Learning (top-down approach)
- [Kaggle Learn](https://www.kaggle.com/learn) — Khóa học miễn phí ngắn gọn
- [3Blue1Brown Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) — Hiểu neural network trực quan
- [Andrej Karpathy's YouTube](https://www.youtube.com/@AndrejKarpathy) — Nội dung chất lượng cao
