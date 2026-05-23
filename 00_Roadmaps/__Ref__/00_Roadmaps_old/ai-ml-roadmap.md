# 🗺️ Lộ trình AI/ML Engineer

> `[INTERMEDIATE → ADVANCED]` — Từ Machine Learning đến production AI systems

---

## AI/ML Engineer là gì?

AI/ML Engineer xây dựng và deploy **hệ thống AI** vào production — từ training model đến serving, monitoring và cải tiến.

```
Data          →    Model         →    Production
Collect            Train              Deploy (API)
Clean              Evaluate           Monitor
Transform          Iterate            Retrain
```

---

## Khác biệt với Data Scientist

| | Data Scientist | ML Engineer |
|---|---|---|
| **Focus** | Research, experiments | Production systems |
| **Skills** | Stats, ML algorithms | ML + Software Eng |
| **Output** | Notebooks, insights | Deployed models, APIs |
| **Work with** | Business analysts | DevOps, Backend teams |

---

## Giai đoạn 1 — Toán học & Python

- [ ] **Python mạnh** → [../02-Languages/python/](../02-Languages/python/)
- [ ] **Numpy & Pandas** — Data manipulation
- [ ] **Đại số tuyến tính** — Vectors, Matrices, Dot product
- [ ] **Xác suất & Thống kê** — Distribution, Bayes, Hypothesis testing
- [ ] **Giải tích** — Đạo hàm, Gradient descent

---

## Giai đoạn 2 — Machine Learning cơ bản

→ [../10-AI-ML/01-ml-fundamentals.md](../10-AI-ML/01-ml-fundamentals.md)

- [ ] Supervised: Linear/Logistic Regression, Decision Tree, Random Forest
- [ ] Unsupervised: K-Means, DBSCAN, PCA
- [ ] Scikit-learn workflow: Train → Evaluate → Tune
- [ ] Feature Engineering & Selection
- [ ] Cross-validation, Overfitting/Underfitting
- [ ] Metrics: Accuracy, F1, AUC-ROC, RMSE

---

## Giai đoạn 3 — Deep Learning

- [ ] **Neural Networks** — Perceptron, Backpropagation, Activation functions
- [ ] **PyTorch** (hoặc TensorFlow/Keras)
- [ ] **CNN** — Computer Vision (Image classification, Object detection)
- [ ] **RNN/LSTM** — Sequence data, Time series
- [ ] **Transformer** — Attention mechanism, BERT, GPT basics

---

## Giai đoạn 4 — Chuyên sâu (chọn 1)

### Natural Language Processing (NLP)
- [ ] Text preprocessing, Tokenization
- [ ] Embeddings: Word2Vec, FastText, Sentence Transformers
- [ ] Hugging Face ecosystem
- [ ] Fine-tuning LLMs
- [ ] RAG (Retrieval Augmented Generation)

### Computer Vision (CV)
- [ ] Image preprocessing, Augmentation
- [ ] CNN architectures: ResNet, EfficientNet, ViT
- [ ] Object Detection: YOLO, Detectron2
- [ ] Segmentation, Pose Estimation

### Tabular / Structured Data
- [ ] XGBoost, LightGBM, CatBoost
- [ ] Feature stores
- [ ] AutoML

---

## Giai đoạn 5 — MLOps (Production)

- [ ] **Experiment tracking** — MLflow, Weights & Biases
- [ ] **Model serving** — FastAPI + model, TorchServe, Triton
- [ ] **Model monitoring** — Data drift, Performance degradation
- [ ] **Pipeline orchestration** — Airflow, Kubeflow, ZenML
- [ ] **Feature Store** — Feast, Hopsworks
- [ ] **Docker & Kubernetes** → [../06-DevOps/docker/](../06-DevOps/docker/)
- [ ] **Cloud ML** — AWS SageMaker, GCP Vertex AI, Azure ML

---

## Working with LLMs & Generative AI

- [ ] **Prompt engineering** — Few-shot, Chain-of-thought, ReAct
- [ ] **LangChain / LlamaIndex** — LLM application frameworks
- [ ] **Vector databases** — Pinecone, Weaviate, Chroma (cho RAG)
- [ ] **Fine-tuning** — LoRA, QLoRA
- [ ] **Evaluations** — LLM-as-judge, RAGAS

---

## 📦 Project thực hành

| Project | Kỹ năng |
|---|---|
| Titanic / House Prices (Kaggle) | ML fundamentals |
| Image classifier với CNN | Deep Learning, PyTorch |
| Chatbot với OpenAI API + RAG | LLMs, Vector DB |
| Fraud detection system | Feature engineering, Imbalanced data |
| Deploy ML model dưới dạng API | MLOps, FastAPI, Docker |

---

## Tài nguyên thêm

- [fast.ai](https://www.fast.ai/) — Practical DL (top-down approach)
- [Andrej Karpathy YouTube](https://www.youtube.com/@AndrejKarpathy) — Deep Learning từ đầu
- [Hugging Face Course](https://huggingface.co/learn) — NLP & Transformers miễn phí
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/) — ML + Production
- [Made With ML](https://madewithml.com/) — MLOps focused
