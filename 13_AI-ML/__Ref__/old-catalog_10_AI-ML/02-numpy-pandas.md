# 🐍 NumPy & Pandas — Data Manipulation

> `[BEGINNER → INTERMEDIATE]` — Nền tảng của mọi Data Science workflow Python

---

## NumPy — Numerical Computing

```bash
pip install numpy
```

### Array cơ bản

```python
import numpy as np

# Tạo arrays
a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 4))           # Ma trận 0s: 3x4
c = np.ones((2, 3))            # Ma trận 1s: 2x3
d = np.eye(4)                  # Ma trận đơn vị 4x4
e = np.arange(0, 10, 0.5)     # [0, 0.5, 1.0, ..., 9.5]
f = np.linspace(0, 1, 100)    # 100 điểm đều nhau từ 0 đến 1

# Từ list lồng nhau → 2D array
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Properties
print(matrix.shape)    # (3, 3)
print(matrix.dtype)    # int64
print(matrix.ndim)     # 2
print(matrix.size)     # 9
```

### Indexing & Slicing

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Basic indexing
arr[0]          # [1, 2, 3] — hàng đầu
arr[1][2]       # 6
arr[1, 2]       # 6 (cách ngắn hơn)

# Slicing
arr[0:2]        # 2 hàng đầu
arr[:, 1]       # Cột thứ 2: [2, 5, 8]
arr[1:3, 0:2]   # Submatrix: [[4,5],[7,8]]

# Boolean indexing
arr[arr > 5]    # [6, 7, 8, 9]
arr[(arr > 2) & (arr < 7)]  # [3, 4, 5, 6]

# Fancy indexing
arr[[0, 2], :]  # Hàng 0 và 2
```

### Operations & Broadcasting

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Element-wise operations
a + b           # [5, 7, 9]
a * b           # [4, 10, 18]
a ** 2          # [1, 4, 9]
np.sqrt(a)      # [1, 1.41, 1.73]

# Broadcasting — tự mở rộng shape để compatible
matrix = np.array([[1,2,3],[4,5,6]])
row = np.array([10, 20, 30])
matrix + row    # [[11,22,33],[14,25,36]] — broadcast theo hàng

# Matrix operations
A = np.random.randn(3, 4)
B = np.random.randn(4, 2)
C = A @ B                    # Matrix multiply: (3,4) @ (4,2) → (3,2)
C = np.dot(A, B)             # Tương đương

# Aggregation
arr = np.array([[1,2,3],[4,5,6]])
arr.sum()          # 21
arr.sum(axis=0)    # [5, 7, 9] — sum theo cột
arr.sum(axis=1)    # [6, 15] — sum theo hàng
arr.mean()         # 3.5
arr.std()          # Độ lệch chuẩn
arr.max(axis=0)    # [4, 5, 6]
arr.argmax()       # Index của max value = 5
```

### Random

```python
rng = np.random.default_rng(seed=42)  # Reproducible

rng.random((3, 3))              # Uniform [0, 1)
rng.integers(0, 10, size=(4,))  # Random ints
rng.normal(mean=0, std=1, size=(1000,))  # Normal distribution
rng.choice([1, 2, 3, 4], size=100, replace=True)  # Sample with replacement
rng.shuffle(arr)                # Shuffle in place
```

---

## Pandas — Data Analysis

```bash
pip install pandas
```

### Series

```python
import pandas as pd

# Series = 1D array với labels
prices = pd.Series(
    [25000, 35000, 15000, 45000],
    index=["apple", "mango", "banana", "durian"],
    name="price_vnd"
)

prices["mango"]         # 35000
prices[["mango", "apple"]]  # Lấy nhiều
prices[prices > 20000]  # Filter
prices * 1.1            # Tăng 10%
prices.mean()           # 30000
prices.describe()       # count, mean, std, min, max, ...
```

### DataFrame

```python
# DataFrame = 2D table, như Excel sheet
data = {
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 28],
    "salary": [15_000_000, 25_000_000, 35_000_000, 20_000_000],
    "department": ["Tech", "Marketing", "Tech", "Sales"],
    "active": [True, True, False, True]
}
df = pd.DataFrame(data)

# Basic info
df.shape        # (4, 5)
df.dtypes       # Kiểu dữ liệu mỗi cột
df.info()       # Overview: shape, dtypes, null counts
df.describe()   # Thống kê mô tả cho numeric columns
df.head(3)      # 3 dòng đầu
df.tail(2)      # 2 dòng cuối
```

### Selection & Filtering

```python
# Chọn cột
df["name"]              # Series
df[["name", "salary"]]  # DataFrame

# Chọn theo vị trí — iloc
df.iloc[0]          # Hàng đầu tiên
df.iloc[1:3]        # Hàng 1-2
df.iloc[:, 0:2]     # 2 cột đầu
df.iloc[0, 1]       # Hàng 0, cột 1

# Chọn theo label — loc
df.loc[0, "name"]            # "Alice"
df.loc[:, ["name", "age"]]   # Nhiều cột
df.loc[df["age"] > 28]       # Filter

# Boolean filtering
active_tech = df[(df["active"]) & (df["department"] == "Tech")]
high_salary = df[df["salary"] > 20_000_000]

# Query syntax (dễ đọc hơn)
result = df.query("age > 28 and department == 'Tech'")
```

### Data Cleaning

```python
# Dữ liệu thực tế thường "bẩn"
df_raw = pd.read_csv("employees.csv")

# Kiểm tra missing values
df_raw.isnull().sum()          # Số null mỗi cột
df_raw.isnull().mean() * 100   # % null mỗi cột

# Xử lý missing
df_raw.dropna()                          # Xóa hàng có null
df_raw.dropna(subset=["email"])          # Xóa hàng nếu email null
df_raw["age"].fillna(df_raw["age"].median())  # Điền bằng median
df_raw.fillna({"name": "Unknown", "salary": 0})  # Điền theo cột

# Duplicates
df_raw.duplicated().sum()  # Số hàng trùng
df_raw.drop_duplicates()   # Xóa trùng
df_raw.drop_duplicates(subset=["email"])  # Trùng theo email

# Data types
df_raw["hire_date"] = pd.to_datetime(df_raw["hire_date"])
df_raw["salary"] = df_raw["salary"].str.replace(",", "").astype(float)
df_raw["department"] = df_raw["department"].astype("category")

# Rename columns
df_raw.rename(columns={"emp_id": "id", "dept": "department"}, inplace=True)

# String operations
df_raw["email"] = df_raw["email"].str.lower().str.strip()
df_raw["name"] = df_raw["name"].str.title()
```

### GroupBy & Aggregation

```python
# GroupBy — như SQL GROUP BY
by_dept = df.groupby("department")

by_dept["salary"].mean()              # Lương trung bình theo dept
by_dept["salary"].agg(["mean", "min", "max", "count"])  # Multiple agg

# Nhiều columns
df.groupby(["department", "active"]).agg(
    avg_salary=("salary", "mean"),
    count=("name", "count"),
    max_age=("age", "max")
).reset_index()

# Pivot table
pivot = df.pivot_table(
    values="salary",
    index="department",
    columns="active",
    aggfunc="mean"
)
```

### Merge & Join

```python
employees = pd.DataFrame({...})
departments = pd.DataFrame({"dept_id": [1, 2, 3], "dept_name": [...]})

# Inner join
merged = employees.merge(departments, on="dept_id", how="inner")

# Left join — giữ tất cả employees
merged = employees.merge(departments, on="dept_id", how="left")

# Merge trên nhiều keys
merged = df1.merge(df2, left_on=["year", "month"], right_on=["yr", "mo"])

# Concat — stack DataFrames
combined = pd.concat([df_2023, df_2024], ignore_index=True)
combined = pd.concat([df1, df2], axis=1)  # Gộp theo cột
```

### Apply & Transform

```python
# Apply function lên column
df["salary_eur"] = df["salary"].apply(lambda x: x / 25000)

# Apply lên hàng (axis=1)
def categorize(row):
    if row["salary"] > 30_000_000:
        return "Senior"
    elif row["salary"] > 20_000_000:
        return "Mid"
    return "Junior"

df["level"] = df.apply(categorize, axis=1)

# Vectorized approach (nhanh hơn apply)
df["level"] = pd.cut(
    df["salary"],
    bins=[0, 20_000_000, 30_000_000, float('inf')],
    labels=["Junior", "Mid", "Senior"]
)

# map — thay thế giá trị
df["dept_code"] = df["department"].map({"Tech": "T", "Marketing": "M", "Sales": "S"})
```

### Time Series

```python
# Làm việc với dates
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

df.loc["2024"]              # Tất cả năm 2024
df.loc["2024-01"]           # Tháng 1/2024
df.loc["2024-01":"2024-06"] # H1 2024

# Resample — aggregate theo thời gian
daily_revenue = df["revenue"].resample("D").sum()        # Ngày
monthly_revenue = df["revenue"].resample("ME").sum()     # Tháng
weekly_avg = df["sales"].resample("W").mean()            # Tuần

# Rolling window
df["7d_avg"] = df["sales"].rolling(window=7).mean()     # MA7
df["30d_std"] = df["price"].rolling(window=30).std()
```

### Xuất dữ liệu

```python
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False, sheet_name="Data")
df.to_json("output.json", orient="records", indent=2)
df.to_parquet("output.parquet")  # Efficient binary format
```

---

## Pattern thực tế: EDA (Exploratory Data Analysis)

```python
import pandas as pd
import numpy as np

def quick_eda(df: pd.DataFrame):
    """Báo cáo EDA nhanh"""
    print(f"Shape: {df.shape}")
    print(f"\nDtypes:\n{df.dtypes}")
    print(f"\nMissing:\n{df.isnull().sum()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")
    print(f"\nDescribe:\n{df.describe()}")
    
    for col in df.select_dtypes("object").columns:
        print(f"\n{col} value counts (top 10):")
        print(df[col].value_counts().head(10))

quick_eda(df)
```

---

## Bài tập thực hành

- [ ] Load và clean dataset thực từ [Kaggle](https://www.kaggle.com/datasets)
- [ ] EDA: Tìm 5 insights thú vị từ một dataset
- [ ] GroupBy: So sánh doanh thu theo region và sản phẩm
- [ ] Time series: Plot doanh thu 12 tháng với rolling average

---

## Tài nguyên thêm

- [NumPy Docs](https://numpy.org/doc/)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Kaggle Pandas Course (free)](https://www.kaggle.com/learn/pandas)
