# 🤖 RAG & LangChain — Xây dựng AI Apps với dữ liệu riêng

> `[INTERMEDIATE → ADVANCED]` — Kết hợp LLM với knowledge base của bạn

---

## Tại sao cần RAG?

LLMs (GPT, Claude, Gemini) rất thông minh nhưng có **2 giới hạn lớn**:

1. **Knowledge cutoff**: Không biết thông tin sau ngày training. Hỏi "giá Bitcoin hôm nay?" → không trả lời được.
2. **No private data**: Không biết gì về docs nội bộ công ty, sản phẩm của bạn, hay database riêng.

**RAG (Retrieval-Augmented Generation)** giải quyết bằng cách: tìm thông tin liên quan từ dữ liệu của bạn → đưa vào prompt → LLM trả lời dựa trên data thực.

```
Không RAG:
  User: "Chính sách hoàn tiền của công ty là gì?"
  LLM:  "Tôi không có thông tin về công ty bạn." ❌

Có RAG:
  User: "Chính sách hoàn tiền?"
  → Search docs → Tìm file policy.pdf → Extract đoạn liên quan
  → Đưa vào prompt: "Dựa trên tài liệu sau: [chính sách]... Trả lời câu hỏi..."
  LLM:  "Theo chính sách công ty, bạn được hoàn tiền trong 30 ngày..." ✅
```

---

## 1. RAG Pipeline — Luồng xử lý

### Giai đoạn 1: Indexing (chuẩn bị data, chạy 1 lần)

```
Documents (PDF, MD, HTML...)
    │
    ▼
Chunking: Chia thành đoạn nhỏ (500-1000 tokens)
    │
    ▼
Embedding: Chuyển text → vector số (1536 dimensions)
    │                    "Chính sách hoàn tiền" → [0.12, -0.45, 0.87, ...]
    ▼
Vector DB: Lưu vectors (Pinecone, Chroma, Weaviate)
```

**Tại sao chunking?** Vì LLM có giới hạn context window (4K-128K tokens). Nếu document 100 trang, bạn không thể nhét hết vào prompt. Chunking giúp tìm đúng đoạn cần thiết.

**Tại sao embedding?** Vì text search thường dùng keyword matching ("hoàn tiền" ≠ "refund"). Embedding biến text thành vector — các câu có **nghĩa giống nhau** sẽ có vector gần nhau, bất kể ngôn ngữ hay cách nói.

### Giai đoạn 2: Retrieval + Generation (mỗi query)

```
User Question: "Bao lâu được hoàn tiền?"
    │
    ▼
Embed question → vector
    │
    ▼
Search Vector DB → Top 3 chunks gần nhất
    │
    ▼
Build prompt:
  "Dựa trên tài liệu sau:
   [chunk 1: ...hoàn tiền trong 30 ngày...]
   [chunk 2: ...yêu cầu hóa đơn gốc...]
   [chunk 3: ...liên hệ support@...]
   
   Câu hỏi: Bao lâu được hoàn tiền?"
    │
    ▼
LLM generates answer: "Bạn được hoàn tiền trong 30 ngày kể từ ngày mua.
Cần cung cấp hóa đơn gốc. Liên hệ support@company.com."
```

---

## 2. Implementation với LangChain

### Setup & Document Loading

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { OpenAIEmbeddings } from '@langchain/openai';
import { MemoryVectorStore } from 'langchain/vectorstores/memory';
import { PDFLoader } from 'langchain/document_loaders/fs/pdf';
import { DirectoryLoader } from 'langchain/document_loaders/fs/directory';

// 1. Load documents
const loader = new DirectoryLoader('./docs', {
    '.pdf': (path) => new PDFLoader(path),
    '.md': (path) => new TextLoader(path),
});
const docs = await loader.load();

// 2. Chunking
// RecursiveCharacterTextSplitter: chia theo paragraph → sentence → word
// Giữ context tốt hơn chia cứng theo số ký tự
const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,      // ~250 words per chunk
    chunkOverlap: 200,    // Overlap để không mất context ở ranh giới
    separators: ['\n\n', '\n', '. ', ' '],  // Ưu tiên chia tại paragraph, sentence
});
const chunks = await splitter.splitDocuments(docs);
console.log(`${docs.length} documents → ${chunks.length} chunks`);

// 3. Embed & Store
const embeddings = new OpenAIEmbeddings({
    model: 'text-embedding-3-small',  // Rẻ & nhanh, 1536 dims
});
const vectorStore = await MemoryVectorStore.fromDocuments(chunks, embeddings);
// Production: dùng Pinecone, Chroma, hoặc pgvector thay MemoryVectorStore
```

### Query & Generate

```typescript
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { createRetrievalChain } from 'langchain/chains/retrieval';
import { createStuffDocumentsChain } from 'langchain/chains/combine_documents';

const llm = new ChatOpenAI({
    model: 'gpt-4o-mini',
    temperature: 0,  // Deterministic cho Q&A (không cần creativity)
});

// Prompt template
const prompt = ChatPromptTemplate.fromTemplate(`
Bạn là assistant trả lời câu hỏi dựa trên tài liệu được cung cấp.
Nếu không tìm thấy câu trả lời trong tài liệu, nói "Tôi không tìm thấy thông tin này."
KHÔNG bịa thông tin.

Tài liệu tham khảo:
{context}

Câu hỏi: {input}
`);

// Chain: retriever → stuff docs → LLM
const retriever = vectorStore.asRetriever({
    k: 4,  // Lấy top 4 chunks liên quan nhất
});
const documentChain = await createStuffDocumentsChain({ llm, prompt });
const retrievalChain = await createRetrievalChain({
    combineDocsChain: documentChain,
    retriever,
});

// Query!
const result = await retrievalChain.invoke({
    input: 'Chính sách hoàn tiền như thế nào?',
});

console.log(result.answer);
// "Theo chính sách công ty, bạn được hoàn tiền trong 30 ngày..."

// Xem sources (traceability!)
result.context.forEach(doc => {
    console.log(`Source: ${doc.metadata.source}, Page: ${doc.metadata.page}`);
});
```

---

## 3. Vector Databases — So sánh

| DB | Type | Hosting | Free tier | Khi nào dùng |
|---|---|---|---|---|
| **Chroma** | Embedded | Self-hosted | ✅ Open source | Prototype, local dev |
| **Pinecone** | Managed | Cloud | ✅ 100K vectors | Production, serverless |
| **Weaviate** | Managed/Self | Both | ✅ Open source | Multi-modal (text+image) |
| **pgvector** | PostgreSQL extension | Self-hosted | ✅ Open source | Already use PostgreSQL |
| **Qdrant** | Self-hosted | Both | ✅ Open source | High performance, Rust |

**Lời khuyên:**
- Mới bắt đầu → **Chroma** (đơn giản nhất)
- Đã có PostgreSQL → **pgvector** (không thêm infra)
- Production scale → **Pinecone** (managed, không lo ops)

---

## 4. Advanced RAG Techniques

### Chunking Strategy

Cách chunk ảnh hưởng lớn đến chất lượng:

```
❌ Fixed-size chunking: cắt cứng 500 chars → cắt giữa câu, mất context
✅ Semantic chunking: chia theo paragraph, section, heading
✅ Parent-child: chunk nhỏ để search, trả parent chunk lớn hơn cho LLM

Chunk size trade-off:
  Nhỏ (200 tokens) → Search chính xác hơn, ít context
  Lớn (2000 tokens) → Nhiều context, search kém chính xác hơn
  Sweet spot: 500-1000 tokens + overlap 10-20%
```

### Hybrid Search (keyword + semantic)

```typescript
// Chỉ semantic search có thể miss khi query chứa keywords đặc biệt
// (tên sản phẩm, mã code, số điện thoại)
// → Kết hợp BM25 (keyword) + Vector (semantic)

const results = await vectorStore.similaritySearch(query, 4);
const keywordResults = await bm25Search(query, documents, 4);

// Merge & rerank
const combined = rerank([...results, ...keywordResults], query);
```

### Evaluation — Đo chất lượng RAG

Không đo = không biết có tốt không. 3 metrics quan trọng:

```
1. Faithfulness: Câu trả lời có đúng với source documents không?
   (Không hallucinate/bịa)

2. Relevancy: Retrieved chunks có liên quan đến câu hỏi không?
   (Search đúng, không lấy nhầm)

3. Answer Correctness: So với ground truth, đúng bao nhiêu %?
```

---

## 5. Production Considerations

```
✅ Caching: Cache embeddings (tốn tiền!), cache frequent queries
✅ Rate limiting: OpenAI API có limits (TPM, RPM)
✅ Cost control: text-embedding-3-small ($0.02/1M tokens) thay large
✅ Monitoring: log retrieved chunks + user feedback (thumbs up/down)
✅ Security: sanitize input (prompt injection!), filter PII from context
✅ Updates: re-index khi documents thay đổi (incremental > full rebuild)
```

---

## Bài tập thực hành

- [ ] RAG cơ bản: Q&A chatbot cho README.md files trong project
- [ ] Chunking comparison: fixed vs recursive, đo chất lượng
- [ ] Production: pgvector + Express API + React frontend
- [ ] Evaluation: tạo test set 20 questions, đo faithfulness

---

## Tài nguyên thêm

- [LangChain Docs](https://js.langchain.com/docs/) — JavaScript/TypeScript
- [LlamaIndex](https://www.llamaindex.ai/) — Alternative framework (Python-focused)
- [RAG From Scratch (DeepLearning.AI)](https://www.deeplearning.ai/short-courses/) — Free course
- [Pinecone Learning Center](https://www.pinecone.io/learn/) — Vector DB concepts
