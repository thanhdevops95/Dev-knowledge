# 🤖 13_ai-ml

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** 🟢 Active — 1/10 cluster có basic content (llm)

> 🎯 *AI / ML knowledge: LLM (ChatGPT/Claude/Gemini), RAG, AI Agents, Vector Search, Embeddings, Fine-tuning, classical ML, Deep Learning, Math for ML, MLOps, NLP, Computer Vision. LLM cluster là cluster đầu tiên — cross-cuts mọi dev role 2026.*

---

## 🎯 Chủ đề này có gì

LLM (Large Language Models), RAG (Retrieval Augmented Generation), AI Agents, Vector Search, Embeddings, Fine-tuning, classical ML, Deep Learning fundamentals, Math for ML, MLOps, NLP, Computer Vision.

---

## 📂 Sub-clusters

| Cluster | Status | Basic | Intermediate |
|---|---|---|---|
| [llm](llm/) | ✅ Active | 5/5 ✅ | ⏳ |
| [rag-and-ai-agent](rag-and-ai-agent/) | 🟡 Skeleton | ⏳ | ⏳ |
| [vector-search-and-embeddings](vector-search-and-embeddings/) | 🟡 Skeleton | ⏳ | ⏳ |
| [math-for-ml](math-for-ml/) | 🟡 Skeleton | ⏳ | ⏳ |
| [ml-fundamentals](ml-fundamentals/) | 🟡 Skeleton | ⏳ | ⏳ |
| [deep-learning](deep-learning/) | 🟡 Skeleton | ⏳ | ⏳ |
| [nlp](nlp/) | 🟡 Skeleton | ⏳ | ⏳ |
| [computer-vision](computer-vision/) | 🟡 Skeleton | ⏳ | ⏳ |
| [fine-tuning-and-training](fine-tuning-and-training/) | 🟡 Skeleton | ⏳ | ⏳ |
| [mlops](mlops/) | 🟡 Skeleton | ⏳ | ⏳ |

> Chi tiết sitemap → [`../_blueprint/01_sitemap-detail.md`](../_blueprint/01_sitemap-detail.md).

---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đi theo |
|---|---|
| 🟢 **Beginner muốn build LLM app** | [llm/01_basic/](llm/lessons/01_basic/) — không cần math/ML trước |
| 🟡 **Backend dev integrate AI** | llm → rag-and-ai-agent → vector-search-and-embeddings |
| 🟠 **ML Engineer truyền thống** | math-for-ml → ml-fundamentals → deep-learning → nlp/cv |
| 🔵 **AI Engineer 2026** | llm → rag-and-ai-agent → fine-tuning → mlops |

→ **2026 reality**: Đa số dev chỉ cần `llm` + `rag-and-ai-agent` để build AI app. Math/classical ML cho ML engineer truyền thống.

---

## 📖 Active cluster — llm basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [LLM intro + tokenization](llm/lessons/01_basic/00_what-is-llm-and-tokenization.md) | MUST-KNOW | ~18p |
| 01 | [Prompt engineering](llm/lessons/01_basic/01_prompt-engineering-and-context.md) | MUST-KNOW | ~22p |
| 02 | [Function calling + tools](llm/lessons/01_basic/02_function-calling-and-tools.md) | MUST-KNOW | ~22p |
| 03 | [RAG fundamentals](llm/lessons/01_basic/03_rag-fundamentals.md) | MUST-KNOW | ~22p |
| 04 | [Production LLM app](llm/lessons/01_basic/04_llm-app-cost-eval-and-production.md) | MUST-KNOW | ~22p |

→ **Tổng ~106 phút**. Foundation cho mọi AI app 2026.

---

## 🔗 Liên kết

### Trong workspace
- 🐍 [Python](../03_languages/python/)
- 🌐 [HTTP API](../05_networking/http-https/)
- 🛡️ [OWASP LLM Top 10](../12_security/owasp-top-10/)
- 🐘 [pgvector + Postgres](../06_databases/sql/postgresql/)
- 🐳 [Docker + K8s](../10_devops/)
- ☁️ [11_cloud](../11_cloud/)
- 💰 [Cloud cost management](../11_cloud/cloud-cost-management/)

### Tài nguyên ngoài 2026
- 📖 [Anthropic Docs](https://docs.anthropic.com/)
- 📖 [OpenAI Docs](https://platform.openai.com/docs)
- 📖 [Hugging Face](https://huggingface.co/)
- 📖 [Andrej Karpathy YouTube](https://www.youtube.com/@AndrejKarpathy)
- 📖 [LangChain](https://python.langchain.com/)
- 📖 [LlamaIndex](https://docs.llamaindex.ai/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Cluster **llm basic 5/5 hoàn chỉnh**. Cluster đầu tiên của 13_ai-ml branch. 1/10 sub-clusters active. Foundation cho dev build AI app — không cần math/classical ML trước.
- **v0.1.0 (16/05/2026)** — Skeleton ban đầu.
