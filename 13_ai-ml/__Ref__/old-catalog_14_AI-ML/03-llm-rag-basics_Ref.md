# 🤖 AI/ML thực hành — LLM, RAG, và Prompt Engineering

> `[INTERMEDIATE]` — Ứng dụng AI vào sản phẩm thực tế

---

## 1. LLM APIs — Tích hợp AI vào ứng dụng

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Basic completion
async function askAI(prompt) {
    const response = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [
            { role: 'system', content: 'You are a helpful assistant. Reply in Vietnamese.' },
            { role: 'user', content: prompt },
        ],
        temperature: 0.7,        // 0=deterministic, 1=creative
        max_tokens: 1000,
    });
    return response.choices[0].message.content;
}

// Streaming — hiện text real-time
async function streamAI(prompt, onChunk) {
    const stream = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [{ role: 'user', content: prompt }],
        stream: true,
    });

    for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || '';
        onChunk(content);  // Gửi từng phần về client
    }
}

// Function Calling — AI gọi functions
const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Thời tiết Hà Nội hôm nay?' }],
    tools: [{
        type: 'function',
        function: {
            name: 'get_weather',
            description: 'Get weather for a city',
            parameters: {
                type: 'object',
                properties: {
                    city: { type: 'string', description: 'City name' },
                },
                required: ['city'],
            },
        },
    }],
});

// AI trả về: { function: 'get_weather', arguments: { city: 'Hanoi' } }
// → App gọi weather API → trả kết quả về cho AI → AI format response
```

---

## 2. Prompt Engineering — Viết prompt hiệu quả

```
❌ Bad prompt:
"Viết code cho tôi"

✅ Good prompt:
"Viết function JavaScript nhận array numbers, trả về
top 3 số lớn nhất. Function phải:
- Handle array rỗng (return [])
- Handle array < 3 items
- Không duplicate
- Time complexity: O(n)"

Kỹ thuật:
```

### Few-shot — Cho ví dụ

```
Convert product names to slugs:

Input: "iPhone 16 Pro Max"
Output: "iphone-16-pro-max"

Input: "Samsung Galaxy S25 Ultra"
Output: "samsung-galaxy-s25-ultra"

Input: "MacBook Pro 16 inch M4"
Output:
```

### Chain of Thought — Suy nghĩ từng bước

```
Bài toán: Cửa hàng có 50 áo, bán 15, nhập thêm 20, bán tiếp 10.
Còn lại bao nhiêu?

Hãy giải TỪNG BƯỚC:
1. Ban đầu: 50 áo
2. Bán 15: 50 - 15 = 35 áo
3. Nhập 20: 35 + 20 = 55 áo
4. Bán 10: 55 - 10 = 45 áo
→ Đáp án: 45 áo
```

### System Prompt — Định hình persona

```javascript
const messages = [
    {
        role: 'system',
        content: `You are a senior code reviewer.
When reviewing code:
1. Check for bugs and security issues
2. Suggest performance improvements
3. Rate code quality 1-10
4. Be constructive, not critical
Format: use markdown with ✅ ❌ emojis`,
    },
    {
        role: 'user',
        content: 'Review this code:\n```js\napp.get("/users", (req, res) => {...})\n```',
    },
];
```

---

## 3. RAG — Retrieval-Augmented Generation

```
Problem: LLM không biết data riêng của bạn (docs, DB)
Solution: Tìm context liên quan → đưa vào prompt → AI trả lời

User Question
    │
    ▼
┌──────────┐     ┌──────────────┐     ┌──────────┐
│ Embedding│ ──► │ Vector Search│ ──► │  Top K   │
│ (query)  │     │ (similarity) │     │ Results  │
└──────────┘     └──────────────┘     └────┬─────┘
                                            │
                                  ┌─────────▼─────────┐
                                  │   LLM Prompt       │
                                  │ Context: [results] │
                                  │ Question: [query]  │
                                  └─────────┬──────────┘
                                            │
                                        AI Answer
```

```javascript
import { OpenAIEmbeddings } from '@langchain/openai';
import { PineconeStore } from '@langchain/pinecone';

// Step 1: Index documents (chạy 1 lần)
const embeddings = new OpenAIEmbeddings();
const vectorStore = await PineconeStore.fromDocuments(
    documents,  // Chia nhỏ docs thành chunks
    embeddings,
    { pineconeIndex: index }
);

// Step 2: Query (mỗi user request)
async function askWithContext(question) {
    // Tìm documents liên quan
    const relevantDocs = await vectorStore.similaritySearch(question, 4);
    const context = relevantDocs.map(d => d.pageContent).join('\n\n');

    // Đưa vào prompt
    const response = await openai.chat.completions.create({
        model: 'gpt-4o',
        messages: [
            {
                role: 'system',
                content: `Answer based on the following context. 
                         If the answer is not in the context, say "I don't know".
                         Context: ${context}`,
            },
            { role: 'user', content: question },
        ],
    });

    return {
        answer: response.choices[0].message.content,
        sources: relevantDocs.map(d => d.metadata.source),
    };
}
```

---

## 4. AI trong Production

### Caching responses

```javascript
async function cachedAI(prompt, cacheKey) {
    const cached = await redis.get(`ai:${cacheKey}`);
    if (cached) return JSON.parse(cached);

    const response = await askAI(prompt);
    await redis.set(`ai:${cacheKey}`, JSON.stringify(response), 'EX', 3600);
    return response;
}
```

### Rate limiting + Cost control

```javascript
// Track usage per user
async function aiWithLimits(userId, prompt) {
    const usage = await redis.incr(`ai:usage:${userId}`);
    if (usage === 1) await redis.expire(`ai:usage:${userId}`, 86400);

    const FREE_LIMIT = 20;
    if (usage > FREE_LIMIT) throw new Error('Daily AI limit reached');

    const response = await askAI(prompt);

    // Log cost
    const tokens = response.usage.total_tokens;
    const cost = tokens * 0.00001;  // ~$0.01 per 1K tokens
    await db.aiLogs.create({ userId, tokens, cost, prompt: prompt.slice(0, 100) });

    return response;
}
```

### Evaluation — Đánh giá AI output

```
Metrics:
• Accuracy:     Output đúng không? (so với ground truth)
• Latency:      Bao lâu? (p50, p95, p99)
• Cost:         Bao nhiêu $/request?
• Hallucination: AI bịa không? (kiểm tra sources)
• User satisfaction: Thumbs up/down

A/B Testing:
• Model A (GPT-4o) vs Model B (Claude)
• Prompt A vs Prompt B
• Temperature 0.3 vs 0.7
```

---

## 5. AI Stack 2026

```
┌───────────────────────────────────────┐
│           Application Layer           │
│  (Chatbot, Search, Code Assistant)    │
├───────────────────────────────────────┤
│         Orchestration Layer           │
│   LangChain │ LlamaIndex │ Vercel AI │
├───────────────────────────────────────┤
│            Model Layer                │
│  OpenAI │ Claude │ Gemini │ Local LLM │
├───────────────────────────────────────┤
│           Vector Database             │
│  Pinecone │ Weaviate │ pgvector      │
├───────────────────────────────────────┤
│              Data Layer               │
│  Documents │ Database │ APIs          │
└───────────────────────────────────────┘
```

---

## Các lỗi thường gặp

```
❌ Sai: Gửi toàn bộ database vào prompt → token limit + đắt
✅ Đúng: RAG — chỉ gửi chunks liên quan (top 3-5)

❌ Sai: Tin tưởng AI output 100% → hallucination
✅ Đúng: Verify output, thêm guardrails, fact-checking

❌ Sai: Không cache → mỗi request giống nhau gọi API lại
✅ Đúng: Cache responses → giảm cost + latency
```

---

## Bài tập thực hành

- [ ] Tích hợp OpenAI API: chatbot đơn giản với streaming
- [ ] Prompt Engineering: viết system prompt cho code reviewer
- [ ] RAG: index 10 documents → hỏi đáp dựa trên context
- [ ] Production: thêm caching + rate limiting + usage tracking

---

## Tài nguyên thêm

- [OpenAI Docs](https://platform.openai.com/docs) — Official
- [LangChain Docs](https://docs.langchain.com/) — Orchestration
- [Prompt Engineering Guide](https://www.promptingguide.ai/) — Comprehensive
