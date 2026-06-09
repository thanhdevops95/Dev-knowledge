# 🤖 LLM là gì + Tokenization + Models 2026

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 07/06/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** Biết Python cơ bản + HTTP API; không cần học ML trước

> 🎯 *Bài đầu tiên của LLM cluster. Bạn nghe nhiều về ChatGPT/Claude/Gemini nhưng chưa hiểu **trong** nó hoạt động sao. Bài này dạy: LLM là gì + transformer cơ bản + tokenization + context window + temperature + top-p + models 2026 (Claude 4 / GPT-5 / Gemini 2 / Llama 4) + so sánh khi nào dùng cái nào. Không deep architecture (đó là deep-learning cluster).*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **LLM** là gì, khác classic NLP ra sao
- [ ] Hiểu **tokenization** — vì sao "GPT-4" là 1 token, "G", "P", "T", "-", "4" thường không
- [ ] Biết **context window** + cách tính cost theo token
- [ ] Hiểu **temperature, top-p, top-k, seed** — control output
- [ ] So sánh **Claude 4 / GPT-5 / Gemini 2 / Llama 4** 2026 + open vs proprietary
- [ ] Phân biệt **chat completion** vs **base model** vs **instruction-tuned**
- [ ] Setup API call đầu tiên (Anthropic/OpenAI) + Python SDK

---

## Tình huống — Sếp giao build chatbot

Sếp:

> *"Acme Shop muốn build chatbot trả lời câu hỏi sản phẩm + hỗ trợ checkout. Bạn build PoC trong 2 tuần. Dùng API LLM, không train từ đầu. Cost phải predictable. Tuần sau present design."*

Bạn bắt đầu tìm hiểu:
- LLM nào? ChatGPT? Claude? Open-source?
- API call ra sao? Pricing tính sao?
- Context window đủ không cho hỏi 1000 sản phẩm?
- Output có deterministic không?
- "Prompt engineering" là gì mà ai cũng nói?

Bài này map foundation — bài 01-04 sẽ dạy app patterns.

---

## 1️⃣ LLM — Large Language Model

🪞 **Ẩn dụ**: *LLM như **người đọc cả Internet + sách**, nhớ pattern ngôn ngữ, sau đó bạn hỏi gì cũng trả lời được (gần đúng) — không hiểu thật, mà "predict từ tiếp theo có khả năng nhất" dựa vào context.*

### Định nghĩa

**LLM** = Large Language Model — neural network (transformer architecture) train trên **lượng text khổng lồ** (hàng tỉ tỉ token) để dự đoán **token tiếp theo** trong sequence.

**Core mechanism**: Given input "The capital of France is", model predict next token = "Paris" (probability cao nhất).

→ Chỉ là **predict next token lặp đi lặp lại** — nhưng pattern đủ phong phú để trả lời conversation, code, reason.

### Lịch sử ngắn (2017-2026)

| Năm | Mốc |
|---|---|
| 2017 | Transformer paper "Attention is All You Need" (Google) |
| 2018 | BERT (Google), GPT-1 (OpenAI) |
| 2019 | GPT-2 — refuse open initially do "dangerous" |
| 2020 | GPT-3 175B params — emergent abilities |
| 2022 | ChatGPT launch (GPT-3.5) — mass adoption |
| 2023 | GPT-4, Claude 2, Llama 2 open |
| 2024 | GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 (1M context), Llama 3 |
| 2025 | Claude 4 (Opus/Sonnet/Haiku), GPT-5, Gemini 2 |
| 2026 | Multimodal default; agentic capability; longer context (10M+); cheaper inference |

### Khác classic NLP

| Classic NLP (pre-2018) | LLM 2026 |
|---|---|
| Specific task model (sentiment, NER, QA) | General — 1 model làm nhiều task |
| Need labeled training data per task | Zero/few-shot — chỉ prompt |
| Fine-tune cho mỗi domain | Prompt + RAG đủ cho 80% case |
| Smaller (MB-GB) | Large (GB-TB), API call cloud |
| Deterministic | Stochastic (random component) |

---

## 2️⃣ Transformer cơ bản (không deep)

🪞 **Ẩn dụ**: *Transformer như **đội phiên dịch đa người nhìn cả câu cùng lúc** — mỗi từ (token) "chú ý" (attention) đến mọi từ khác → hiểu context tốt hơn RNN cũ (đọc tuần tự).*

### Key concepts

| Concept | Mô tả ngắn |
|---|---|
| **Token** | Đơn vị input/output (sub-word, không phải char hoặc word) |
| **Embedding** | Vector representation của token (~1500-12000 dimensions) |
| **Attention** | Mechanism mỗi token "look at" tokens khác |
| **Layer / Head** | Transformer stack nhiều layer, mỗi layer nhiều attention head |
| **Decoder-only** | Architecture GPT/Claude (predict next token) |
| **Encoder-only** | BERT (classify/embed) |
| **Encoder-decoder** | T5 (translate) |

→ **LLM chat** (GPT/Claude/Gemini) = decoder-only, generative.

### Parameters

- **GPT-3**: 175B params.
- **GPT-4**: ~1.7T (rumored, mixture of experts).
- **Claude 4 Opus**: ~unknown (proprietary).
- **Llama 4**: kiến trúc MoE — Scout ~109B, Maverick ~400B total / 17B active (open).

Params = "memory" của model. Nhiều params = capable hơn (general) + đắt + chậm hơn.

---

## 3️⃣ Tokenization — Sao quan trọng

🪞 **Ẩn dụ**: *Tokenizer như **máy băm thịt** — text input bị băm thành **miếng nhỏ** (token) trước khi vào model. Miếng to/nhỏ ảnh hưởng cost + quality. "Hello world" có thể thành 2 token hoặc 5 token tùy tokenizer.*

### Token = sub-word

```python
# OpenAI tiktoken example
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode("Hello, world!")
# → [13225, 11, 1917, 0]  (4 tokens)

text = enc.decode([13225])  # → "Hello"
```

Common pattern:
- Common word = 1 token: `"hello"`, `"the"`, `"is"`.
- Rare/compound = nhiều token: `"unbelievable"` = `["un", "believ", "able"]`.
- Vietnamese: chưa quen tokenizer → **nhiều token hơn English** (1.5-3x).

### Tại sao token quan trọng

1. **Pricing**: API charge per token (input + output separate).
2. **Context window limit**: model có max token (e.g., 1M Claude Opus/Sonnet 4.6+, 128k GPT-4o, 1M Gemini 1.5/2).
3. **Latency**: nhiều token = chậm hơn.

### Token counting

| Text | Tokens (GPT-4) | Note |
|---|---|---|
| `"Hello, world!"` | 4 | |
| `"The quick brown fox"` | 4 | 1 token / từ |
| Đoạn 1000 từ English | ~1300 tokens | ratio ~1.3 |
| Đoạn 1000 từ Vietnamese | ~2000-3000 tokens | ratio ~2.5 (worse) |
| `"AAAAAAAAAA"` (10 chars) | 4-6 tokens | repeated chars OK |
| Code Python 100 dòng | ~800-1500 tokens | depends content |

### Vietnamese tokenizer pitfall

Vietnamese có dấu + đa âm tiết → tokenizer English-trained chia nhỏ:

```python
enc.encode("Chào bạn, hôm nay khỏe không?")
# → [12+ tokens] mặc dù 6 từ
```

→ App Việt: 1 message 100 từ ≈ 200-300 tokens. Pricing × 2-3 so với English.

→ Mitigation: Anthropic + OpenAI 2025+ improve multilingual tokenizer. Llama 3.1+ tốt hơn cho non-English.

---

## 4️⃣ Context window + token limit

🪞 **Ẩn dụ**: *Context window như **bàn làm việc trước mặt** — model chỉ nhìn vào những gì trên bàn. Bàn lớn (1M token) chứa nhiều giấy tờ hơn (cả cuốn sách), nhưng tìm 1 chi tiết cũng chậm hơn ("needle in haystack" problem).*

### Limits 2026

| Model | Context window | Input limit | Output limit |
|---|---|---|---|
| Claude Opus (4.6/4.7/4.8) | 1M tokens | 1M | 128k (cần streaming) |
| Claude Sonnet 4.6 | 1M | 1M | 64k |
| Claude Haiku 4.5 | 200k | 200k | 64k |
| GPT-5 | 256k | 256k | 16k |
| GPT-4o | 128k | 128k | 16k |
| Gemini 2 Pro | 2M | 2M | 8k |
| Gemini 2 Flash | 1M | 1M | 8k |
| Llama 4 (Maverick) | ~1M | ~1M | — |

### "Lost in the middle" problem

Model có 1M context không = retrieve đều khắp. Research shows:
- Tokens **đầu** + **cuối** context recall tốt.
- Tokens **giữa** dễ bị "miss".

→ Khi build app, **đặt instruction quan trọng** ở đầu + cuối prompt, không giữa.

### Cost theo token

| Model | Input ($/1M token) | Output ($/1M token) | Notes |
|---|---|---|---|
| Claude Opus (4.6+) | $5 | $25 | Smartest, đắt nhất |
| Claude Sonnet 4.6 | $3 | $15 | Default workhorse |
| Claude Haiku 4.5 | $1 | $5 | Fast, cheap |
| GPT-5 | $5 | $15 | (giả định) |
| GPT-4o | $2.50 | $10 | |
| Gemini 2 Pro | $3.50 | $10.50 | |
| Llama 4 (host) | self-host | self-host | GPU cost |

### Cost calc example

App Acme Shop chatbot:
- 1000 user/ngày × 10 message/user = 10k message.
- Mỗi message: 500 token input (history + context) + 200 token output.
- Tổng: 5M input + 2M output / ngày.
- Claude Sonnet 4.6: 5M × $3 + 2M × $15 = $15 + $30 = **$45/ngày** = $1,350/tháng.
- Claude Haiku 4.5: 5M × $1 + 2M × $5 = $5 + $10 = **$15/ngày** = $450/tháng.

→ Chọn model theo task: simple Q&A dùng Haiku/Flash; complex reasoning dùng Sonnet/GPT-5.

---

## 5️⃣ Generation parameters — Control output

### Temperature (default 1.0)

Control **randomness**:
- `0` = deterministic (most likely token).
- `1` = balanced (recommended for chat).
- cao hơn = creative, có khi vô lý.

> ⚠️ **Range khác nhau theo provider**: Claude dùng `0-1`, OpenAI dùng `0-2` (truyền >1 vào Claude sẽ lỗi). Các model Claude đời mới (Opus 4.7+) còn **gỡ hẳn** `temperature/top_p/top_k` (truyền vào → 400 error) — điều khiển output bằng prompt + tham số `effort` thay thế.

```python
# Code generation: temperature=0 (consistent)
# Creative writing: temperature=0.7-1.0
# Brainstorm: temperature=1.2-1.5
```

### Top-p (nucleus sampling, 0-1)

Chỉ chọn từ top tokens với cumulative probability ≤ p.
- `top_p=0.1` = chỉ top 10% probable.
- `top_p=1.0` = không filter.

→ Thường **tune temperature hoặc top_p**, không cả 2.

### Top-k

Chỉ chọn từ k tokens probable nhất. Less commonly used than top_p.

### Max tokens

Limit output length:
```python
max_tokens=500  # Stop after 500 output tokens
```

### Stop sequences

Stop khi gặp string cụ thể:
```python
stop=["\nUser:", "---END---"]
```

### Seed (deterministic)

```python
seed=42  # Same input + seed → same output (gần đúng)
```

→ Vẫn không hoàn toàn deterministic do GPU floating point.

### Streaming

Nhận output token-by-token (low latency UX):
```python
for chunk in client.messages.stream(...):
    print(chunk.delta.text, end="", flush=True)
```

→ User thấy text appear progressively, không đợi response complete.

---

## 6️⃣ Models 2026 — Compare + chọn

🪞 **Ẩn dụ**: *Chọn LLM như **chọn ô tô** — Claude Opus là **Mercedes S** (cao cấp, đắt), Claude Sonnet là **Camry** (balanced), Haiku là **Yaris** (rẻ, nhanh), Llama open là **xe tự lắp ráp** (kiểm soát, công ops, có thể customize hơn).*

### Proprietary (API only)

| Model | Strength | Weakness | When |
|---|---|---|---|
| **Claude 4 Opus** | Smart reasoning, long context, code | Đắt, slower | Hard reasoning, code, agent main |
| **Claude 4 Sonnet** | Balanced (smart + fast + reasonable cost) | — | Default workhorse |
| **Claude 4 Haiku** | Fast, cheap, multimodal | Less smart | High-volume, simple |
| **GPT-5** | Smart, multimodal, plugins ecosystem | Đắt, OpenAI ecosystem lock | Microsoft stack, general |
| **GPT-4o** | Cheap, multimodal, fast | Plateau | Cost-sensitive general |
| **Gemini 2 Pro** | 2M context, Google ecosystem | Hallucination concerns | bạn doc analysis |
| **Gemini 2 Flash** | Free tier rộng, multimodal | — | Beginner, prototyping |

### Open-source (self-host or via API providers)

| Model | Size | Strength | When |
|---|---|---|---|
| **Llama 4** (Meta) | MoE: Scout ~109B / Maverick ~400B | Quality close to proprietary, open weights | Self-host, fine-tune, data privacy |
| **Mistral Large 2** | 123B | Multilingual tốt | EU compliance, RAG |
| **Qwen 3** (Alibaba) | 7B/72B | Chinese + English | China market |
| **DeepSeek V3** | 671B MoE | Math + code | Code task, cheap (cùng FP) |
| **Gemma 3** (Google open) | 2B/9B/27B | Small, on-device | Edge, mobile |

### Hosted open-source

Không tự host? Dùng:
- **Together.ai** — multi-model hosting
- **Groq** — fast inference (custom chip)
- **Replicate** — managed model deploy
- **Fireworks.ai** — fast inference
- **Hugging Face Inference API** — community

### Decision matrix

| Need | Pick |
|---|---|
| Best reasoning + complex agent | Claude 4 Opus / GPT-5 |
| Daily workhorse for app | Claude 4 Sonnet / GPT-4o |
| High volume + cheap | Claude 4 Haiku / Gemini 2 Flash |
| Long context (book, codebase) | Claude 4 / Gemini 2 |
| Self-host, data privacy | Llama 4 70B+ |
| Code generation | Claude 4 / DeepSeek V3 |
| Multilingual (Vietnamese) | Claude / GPT / Gemini (đều OK 2026) |
| Mobile / on-device | Gemma 3 / Phi 3 |

### Chat completion vs Base vs Instruction-tuned

| Type | Description | Use |
|---|---|---|
| **Base model** | Trained on raw text, predict next token raw | Research, fine-tune từ đầu |
| **Instruction-tuned** | Fine-tune trên (instruction, response) pairs | Follow instruction, Q&A |
| **Chat-tuned (RLHF)** | Fine-tune + RLHF + RLAIF | Conversation, helpful, safe |

→ API LLM bạn dùng = **chat-tuned**. Base model hiếm khi access.

---

## 7️⃣ First API call — Anthropic + OpenAI

### Anthropic Claude

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Giải thích Big-O notation trong 3 câu."},
    ],
)
print(response.content[0].text)
# → Big-O đánh giá phức tạp thuật toán... [output]
```

### OpenAI

```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Giải thích Big-O notation trong 3 câu."},
    ],
)
print(response.choices[0].message.content)
```

### Multi-turn

```python
messages = [
    {"role": "user", "content": "Tôi muốn build chatbot."},
    {"role": "assistant", "content": "OK, chatbot cho domain gì?"},
    {"role": "user", "content": "E-commerce, trả lời câu hỏi sản phẩm."},
]
response = client.messages.create(model="claude-sonnet-4-6", max_tokens=512, messages=messages)
```

→ Model **không nhớ** giữa request — bạn phải gửi lại lịch sử mỗi lần.

### System prompt

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    system="Bạn là trợ lý support Acme Shop. Trả lời ngắn gọn, tiếng Việt.",
    messages=[{"role": "user", "content": "Order #123 ở đâu?"}],
)
```

### Async + Streaming

```python
# Streaming
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Viết bài blog 500 từ về Docker."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Async
import asyncio
async_client = anthropic.AsyncAnthropic()
async def main():
    r = await async_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(r.content[0].text)
asyncio.run(main())
```

> ⚠️ **Lưu ý SDK**: với Anthropic SDK, `max_tokens` là tham số **bắt buộc** trong mọi `messages.create` (khác OpenAI — vốn cho phép bỏ trống).

---

## 🛠️ Hands-on — Build "explain code" CLI tool

### Mục tiêu

CLI nhận file Python, gọi Claude explain → output Vietnamese explanation.

### Code

```python
#!/usr/bin/env python3
# explain.py — Mr.Rom
import sys
import anthropic

client = anthropic.Anthropic()

def explain_code(code: str, model: str = "claude-sonnet-4-6") -> str:
    response = client.messages.create(
        model=model,
        max_tokens=1500,
        system="Bạn là senior engineer. Giải thích code bằng tiếng Việt, ngắn gọn, focus WHAT + WHY.",
        messages=[
            {"role": "user", "content": f"Giải thích code sau:\n\n```python\n{code}\n```"},
        ],
        temperature=0.3,  # consistent
    )
    return response.content[0].text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: explain.py <file.py>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        code = f.read()
    print(explain_code(code))
```

### Test

```bash
# Tạo file test
cat > sample.py <<'EOF'
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
EOF

python explain.py sample.py
# → "Hàm fib() tính số Fibonacci bằng đệ quy..."
```

### Estimate cost

- Input: ~50 lines code = ~600 tokens.
- Output: ~300 tokens.
- Cost per call (Sonnet): 600 × $3/M + 300 × $15/M ≈ **$0.0063** = 0.16 cents.
- 1000 call = $6.30.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Token = char

**Sai**: "Context 200k = 200k characters."

**Đúng**: Token ≈ 0.75 word English ≈ 1.5 char tiếng Việt. 200k token ≈ 150k words English ≈ 400 trang sách.

### 2. Forget conversation history

**Sai**: Gửi mỗi message độc lập, model trả lời không context.

**Đúng**: Gửi lại full message history mỗi turn (chịu cost input).

### 3. Use Opus cho mọi task

**Sai**: Default model max ($25/M output).

**Đúng**: Sonnet/Haiku cho 80% task; Opus cho hard reasoning thật sự.

### 4. Temperature=0 = same answer

**Sai**: `temperature=0` ⇒ deterministic.

**Đúng**: Vẫn có small variance do GPU. Dùng `seed` parameter (OpenAI) nếu cần tightly reproducible.

### 5. Trust LLM output 100%

**Sai**: Bot bảo "đáp án là X" → believe.

**Đúng**: LLM **hallucinate** (bịa). Critical info → verify nguồn (RAG + citation) hoặc fact-check API.

### 6. Send PII/secrets vào prompt

**Sai**: Send full user PII + API key vào API → vendor có thể log.

**Đúng**: Sanitize prompt; dùng vendor có **zero data retention** option (Anthropic/OpenAI enterprise tier).

### 7. Forget streaming → UX chậm

**Sai**: Đợi full response → user wait 10s thấy trống.

**Đúng**: Streaming = UX feel instant.

### 8. Vietnamese cost không tính

**Sai**: Quote app cost theo English token count.

**Đúng**: Tiếng Việt ~2-3x token count. Budget gấp đôi.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] LLM khác classic NLP 5 điểm?
- [ ] Token vs character vs word — phân biệt?
- [ ] Tính context window 200k cho doc tiếng Việt ~?
- [ ] Temperature vs top_p — khi nào tune cái nào?
- [ ] So sánh Claude 4 Opus/Sonnet/Haiku — chọn cho 3 use case?
- [ ] Code Python gọi Claude API + system prompt + streaming?
- [ ] Estimate cost cho chatbot 1000 user/ngày?
- [ ] 5 pitfall + fix mỗi cái?

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Term | Vietnamese / Explanation |
|---|---|
| **LLM** | Large Language Model |
| **Transformer** | Architecture (2017) — attention-based |
| **Token** | Đơn vị input/output sub-word |
| **Tokenizer** | Tool chuyển text ↔ tokens |
| **Context window** | Max tokens model handle (input + output) |
| **Parameters** | Trainable weights (175B, 1.7T, ...) |
| **Decoder-only** | Architecture GPT/Claude — predict next token |
| **Encoder-only** | Architecture BERT — classify/embed |
| **Embedding** | Vector representation của token |
| **Attention** | Mechanism cross-token interaction |
| **Temperature** | Control randomness (Claude 0-1, OpenAI 0-2) |
| **Top-p** | Nucleus sampling cutoff |
| **System prompt** | Instruction toàn cuộc chat |
| **Multi-turn** | Conversation với history |
| **Streaming** | Token-by-token output |
| **Hallucination** | LLM bịa fact |
| **Base model** | Pre-train, không instruction-tune |
| **Instruction-tuned** | Fine-tune để follow instruction |
| **RLHF** | Reinforcement Learning from Human Feedback |
| **Chat completion** | API endpoint cho chat (vs completion legacy) |
| **MoE** | Mixture of Experts (architecture) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ➡️ **Bài tiếp theo:** [Prompt Engineering + Context Strategies](01_prompt-engineering-and-context.md) *(sắp viết)*
- ↑ **Về cụm:** [LLM README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- ↑ **Về cụm:** [RAG + AI Agent](../../../rag-and-ai-agent/) — sibling cluster
- 🔢 [Vector search + Embeddings](../../../vector-search-and-embeddings/) — sibling
- 🐍 [Python](../../../../03_languages/python/) — language for LLM apps
- 🌐 [HTTP API](../../../../05_networking/http-https/) — API calls
- 🛡️ [OWASP](../../../../12_security/owasp-top-10/) — LLM security (OWASP LLM Top 10)

### Tài nguyên ngoài (2026)
- 📖 [Anthropic Docs](https://docs.anthropic.com/)
- 📖 [OpenAI Docs](https://platform.openai.com/docs)
- 📖 [Google AI Studio](https://aistudio.google.com/)
- 📖 [Hugging Face](https://huggingface.co/)
- 📖 [Transformer paper](https://arxiv.org/abs/1706.03762) — "Attention is all you need"
- 📖 [tiktoken](https://github.com/openai/tiktoken) — OpenAI tokenizer
- 📖 [LMSYS Chatbot Arena](https://chat.lmsys.org/) — model leaderboard
- 📖 [Artificial Analysis](https://artificialanalysis.ai/) — pricing + benchmark comparison
- 📖 [Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- 📖 [Karpathy's "Let's build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) — from scratch
- 📖 [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 00 LLM basic cluster. LLM định nghĩa + transformer cơ bản + tokenization (token vs char) + context window 2026 (200k-2M) + parameters (temperature/top-p/seed/streaming) + models 2026 compare (Claude 4 / GPT-5 / Gemini 2 / Llama 4) + decision matrix + first API call Anthropic + OpenAI + hands-on "explain code" CLI + 8 pitfalls.
- **v1.1.0 (07/06/2026)** — Sửa số liệu Claude 2026: context window Opus/Sonnet 4.6+ lên 1M (output 128k/64k); giá Opus $5/$25, Sonnet $3/$15, Haiku $1/$5; tính lại cost Haiku $15/ngày; pitfall #3 sửa $25/M output; temperature range Claude 0-1 vs OpenAI 0-2 + lưu ý Opus 4.7+ gỡ temperature/top_p/top_k; Llama 4 sửa sang kiến trúc MoE (Scout/Maverick); hoàn thiện ví dụ async + ghi chú max_tokens bắt buộc.
