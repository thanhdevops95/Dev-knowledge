# 🤖 Lộ trình AI / Machine Learning Engineer

> `[BEGINNER → ADVANCED]`
> **Prerequisite:** [00-overview.md](./00-overview.md) · Python basics · Toán cơ bản (đại số tuyến tính, xác suất)

---

## Tại sao AI/ML?

AI đang thay đổi mọi ngành — từ y tế, tài chính đến sáng tạo nội dung. Nhu cầu về kỹ sư AI/ML tăng vượt cung, và lương thuộc top ngành công nghệ.

### Các vai trò trong AI/ML

| Vai trò | Công việc chính | Công cụ thường dùng |
|---|---|---|
| **ML Engineer** | Train, deploy, optimize models | Python, PyTorch, MLflow, Docker |
| **Data Scientist** | Phân tích, thử nghiệm, prototype models | Python, Pandas, Sklearn, Jupyter |
| **AI Engineer** | Tích hợp AI vào sản phẩm (LLMs, APIs) | LangChain, OpenAI API, RAG |
| **MLOps Engineer** | Pipeline, monitoring, model serving | Kubeflow, MLflow, Seldon, K8s |

---

## Sơ đồ lộ trình

```
Math Foundations ──→ Python + Data Tools
                          │
          ┌───────────────┘
          ▼
   ML cổ điển (Sklearn) ──→ Deep Learning (PyTorch)
                                    │
          ┌────────┬────────────────┘
          ▼        ▼
        NLP    Computer Vision
          │        │
          └───┬────┘
              ▼
   LLMs & GenAI ──→ AI Agents
                        │
          ┌─────────────┘
          ▼
   LLM Eval & Inference ──→ MLOps
```

---

## Phase 1 — Math Foundations

> 📐 Không cần thành chuyên gia toán, nhưng cần hiểu đủ để đọc papers và debug models

- [ ] Linear Algebra: vectors, matrices, eigenvalues, dot product
- [ ] Calculus: derivatives, chain rule, gradient descent trực quan
- [ ] Probability & Statistics: distributions, Bayes' theorem, hypothesis testing
- [ ] Information Theory cơ bản: entropy, cross-entropy, KL divergence
- 📄 [Math for ML](../14-AI-ML/05-math-for-ml-fundamentals.md)

---

## Phase 2 — Python & Data Tools

- [ ] Python: list comprehensions, generators, decorators, OOP
- [ ] NumPy: array operations, broadcasting, linear algebra
- [ ] Pandas: DataFrames, groupby, merge, pivot, time series
- [ ] Matplotlib & Seaborn: visualization cho EDA
- [ ] Jupyter Notebooks workflow
- 📄 [Python Basics](../05-Languages/python/01-python-basics.md)
- 📄 [Python Advanced](../05-Languages/python/02-python-advanced.md)
- 📄 [NumPy & Pandas](../14-AI-ML/03-numpy-pandas-basics.md)
- 📄 [Data Visualization](../14-AI-ML/04-data-visualization-basics.md)

---

## Phase 3 — Machine Learning cổ điển

> 🎯 Hiểu vững ML cơ bản trước khi nhảy vào Deep Learning

- [ ] Supervised: Linear/Logistic Regression, Decision Trees, Random Forest, SVM
- [ ] Unsupervised: K-Means, DBSCAN, PCA, t-SNE
- [ ] Model evaluation: cross-validation, precision/recall, ROC-AUC, confusion matrix
- [ ] Feature engineering, feature selection, handling imbalanced data
- [ ] Hyperparameter tuning: Grid Search, Random Search, Optuna
- 📄 [ML Fundamentals](../14-AI-ML/01-ml-fundamentals.md)
- 📄 [Scikit-learn Advanced](../14-AI-ML/06-scikit-learn-advanced.md)

---

## Phase 4 — Deep Learning

- [ ] Neural Networks: forward/backpropagation, activation functions
- [ ] CNN: convolutions, pooling, architectures (ResNet, EfficientNet)
- [ ] Transformers: attention mechanism, self-attention, positional encoding
- [ ] PyTorch: tensors, autograd, DataLoaders, training loop
- [ ] Regularization: dropout, batch norm, early stopping
- [ ] Transfer learning & fine-tuning pre-trained models
- 📄 [Neural Networks Basics](../14-AI-ML/deep-learning/01-neural-networks-basics.md)
- 📄 [CNN](../14-AI-ML/deep-learning/02-cnn-basics.md)
- 📄 [Transformers](../14-AI-ML/deep-learning/03-transformers-basics.md)
- 📄 [PyTorch](../14-AI-ML/deep-learning/04-pytorch-basics.md)

---

## Phase 5 — Computer Vision

- [ ] Image classification, object detection (YOLO, Faster R-CNN)
- [ ] Semantic segmentation, instance segmentation
- [ ] Image generation: GANs, Diffusion Models
- [ ] OpenCV cho image preprocessing
- 📄 [Computer Vision](../14-AI-ML/07-computer-vision-basics.md)

---

## Phase 6 — LLMs & Generative AI

> 🔥 Lĩnh vực nóng nhất hiện tại — nhu cầu tuyển dụng cực cao

- [ ] Prompt Engineering: techniques, chain-of-thought, few-shot
- [ ] RAG (Retrieval-Augmented Generation): vector DBs, embeddings, chunking
- [ ] Fine-tuning: LoRA, QLoRA, PEFT cho domain-specific models
- [ ] AI Agents: tool use, planning, multi-agent systems
- 📄 [Prompt Engineering](../14-AI-ML/llm/01-prompt-engineering-practices.md)
- 📄 [RAG & LangChain](../14-AI-ML/llm/02-rag-langchain-basics.md)
- 📄 [Fine-tuning](../14-AI-ML/llm/03-fine-tuning-basics.md)
- 📄 [AI Agents](../14-AI-ML/llm/04-ai-agents-basics.md)

---

## Phase 7 — LLM Evaluation & Inference

- [ ] LLM Evaluation: benchmarks, human eval, automated metrics
- [ ] Inference optimization: quantization, KV-cache, speculative decoding
- [ ] Serving: vLLM, TGI, Triton Inference Server
- [ ] Cost optimization: batching, model distillation, caching
- 📄 [LLM Evaluation](../14-AI-ML/llm/05-llm-evaluation-basics.md)
- 📄 [LLM Inference](../14-AI-ML/llm/06-llm-inference-basics.md)

---

## Phase 8 — MLOps

> 🔄 Đưa model từ notebook vào production

- [ ] Experiment tracking: MLflow, Weights & Biases
- [ ] Model registry, versioning, reproducibility
- [ ] Model serving: REST API, gRPC, batch inference
- [ ] Feature stores: Feast, Tecton
- [ ] Monitoring: data drift, model drift, performance degradation
- [ ] CI/CD cho ML: automated retraining pipelines
- 📄 [MLOps Basics](../14-AI-ML/mlops/01-mlops-basics.md)
- 📄 [Model Serving](../14-AI-ML/mlops/02-model-serving-basics.md)
- 📄 [Feature Store](../14-AI-ML/mlops/03-feature-store-basics.md)

---

## 📦 Project thực hành

| Phase | Project | Độ khó |
|---|---|---|
| ML cơ bản | House price prediction với feature engineering (Kaggle) | ⭐⭐ |
| ML nâng cao | Fraud detection system với imbalanced dataset | ⭐⭐ |
| Deep Learning | Image classifier với PyTorch + transfer learning | ⭐⭐⭐ |
| NLP | Sentiment analysis trên Vietnamese text | ⭐⭐⭐ |
| LLM / RAG | Chatbot hỏi đáp tài liệu nội bộ công ty (RAG + LangChain) | ⭐⭐⭐ |
| AI Agents | Agent tự động research + tóm tắt papers từ arXiv | ⭐⭐⭐⭐ |
| MLOps | End-to-end: train → track → serve → monitor với MLflow + FastAPI | ⭐⭐⭐⭐ |

---

## 📚 Tài nguyên

| Loại | Tên | Ghi chú |
|---|---|---|
| Khóa học | [fast.ai — Practical Deep Learning](https://course.fast.ai) | Top-down approach, miễn phí |
| Khóa học | [Andrew Ng — ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction) | Nền tảng ML vững chắc |
| Khóa học | [Andrej Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) | Xây neural net từ scratch |
| Practice | [Kaggle](https://kaggle.com) | Competitions + datasets + notebooks |
| Papers | [Papers with Code](https://paperswithcode.com) | SOTA papers kèm implementation |
| Sách | *Hands-On ML with Scikit-Learn & TensorFlow* — Aurélien Géron | Thực hành-first approach |
| Sách | *Deep Learning* — Ian Goodfellow | "Bible" của Deep Learning |
| Community | [Hugging Face](https://huggingface.co) | Models, datasets, spaces |
