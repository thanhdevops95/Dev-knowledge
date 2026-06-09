export const meta = {
  name: 'fix-security-aiml',
  description: 'Fix findings 12_security/13_ai-ml + restructure owasp-top-10 sang OWASP 2025, schema-free per-file',
  phases: [{ title: 'Fix' }],
}
const ROOT = '04_Knowledge/dev-knowledge'
const OWASP = [
  '12_security/owasp-top-10/lessons/01_basic/00_what-is-owasp-and-application-security.md',
  '12_security/owasp-top-10/lessons/01_basic/01_injection-and-access-control.md',
  '12_security/owasp-top-10/lessons/01_basic/02_crypto-failures-and-secure-design.md',
  '12_security/owasp-top-10/lessons/01_basic/03_misconfig-vulnerable-components-supply-chain.md',
  '12_security/owasp-top-10/lessons/01_basic/04_auth-failures-logging-and-ssrf.md',
]
const OTHER = [
  '12_security/authentication/lessons/01_basic/01_password-and-mfa.md',
  '12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md',
  '12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md',
  '12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md',
  '12_security/authorization/lessons/01_basic/00_what-is-authorization.md',
  '12_security/cloud-security/lessons/01_basic/00_what-is-cloud-security.md',
  '12_security/container-security/lessons/01_basic/00_what-is-container-security.md',
  '12_security/cryptography/lessons/01_basic/00_what-is-cryptography.md',
  '12_security/pentesting-fundamentals/lessons/01_basic/00_what-is-pentesting-fundamentals.md',
  '13_ai-ml/README.md',
  '13_ai-ml/deep-learning/lessons/01_basic/00_what-is-deep-learning.md',
  '13_ai-ml/llm/lessons/01_basic/00_what-is-llm-and-tokenization.md',
  '13_ai-ml/llm/lessons/01_basic/01_prompt-engineering-and-context.md',
  '13_ai-ml/llm/lessons/01_basic/02_function-calling-and-tools.md',
  '13_ai-ml/llm/lessons/01_basic/03_rag-fundamentals.md',
  '13_ai-ml/llm/lessons/01_basic/04_llm-app-cost-eval-and-production.md',
  '13_ai-ml/math-for-ml/lessons/01_basic/00_what-is-math-for-ml.md',
  '13_ai-ml/ml-fundamentals/lessons/01_basic/00_what-is-ml-fundamentals.md',
  '13_ai-ml/rag-and-ai-agent/lessons/01_basic/00_what-is-rag-and-ai-agent.md',
  '13_ai-ml/vector-search-and-embeddings/lessons/01_basic/00_what-is-vector-search-and-embeddings.md',
]

const fixPrompt = (file) => `Bạn là chuyên gia QA kỹ thuật (persona Mr.Rom). Sửa lỗi cho FILE: \`${ROOT}/${file}\`.

ĐỌC: \`${ROOT}/_workspace/_audit-secai-findings.json\` — LỌC các finding có "file" chứa "${file.split('/').pop()}" và đúng đường dẫn này.

Với MỖI finding: VERIFY lại (đọc vị trí, đối chiếu kiến thức 2026). Nếu CHẮC đúng là lỗi → sửa (Edit). Nếu false-positive → bỏ qua. Loại lỗi: code-error (vd argon2 ph.verify() RAISE VerifyMismatchError chứ không return False → phải try/except; biến chưa định nghĩa như PUBLIC_KEYS), factual-error (số liệu/version/giá sai), content-gap (cụt/thiếu), broken-content (bảng vỡ/artifact).

BẢO TOÀN: nội dung kỹ thuật đúng, code trong fence (chỉ sửa chỗ sai). KHÔNG đụng nav/heading/time/de-meta (đã sync). KHÔNG để lọt tag tool-call (</content>...).

METADATA: bump version (+0.1.0 nếu chỉ fix), "Cập nhật: 07/06/2026", changelog TĂNG DẦN thêm dòng cuối. Xong trả 2-3 dòng text tóm tắt (lỗi đã fix + false-positive bỏ qua). KHÔNG gọi tool ở cuối.`

const owaspPrompt = (file) => `Bạn là chuyên gia bảo mật (persona Mr.Rom). Cập nhật bài này sang OWASP Top 10:2025. FILE: \`${ROOT}/${file}\`.

ĐỌC BẮT BUỘC: \`${ROOT}/_workspace/_owasp-2025-ref.md\` (thứ tự + mapping 2025 chính thức) + \`${ROOT}/_workspace/_audit-secai-findings.json\` (lọc finding của file này).

NHIỆM VỤ:
1) Cập nhật MỌI tham chiếu OWASP từ 2021 → 2025: số hiệu (A01-A10) + tên category theo bản 2025. Bỏ mọi câu coi 2021 là "current" / 2025 là "preview/expected/draft" — 2025 LÀ bản hiện hành (final release).
2) Thay đổi then chốt phải phản ánh: **A02 Security Misconfiguration** lên #2; **A03 Software Supply Chain Failures** (mới, mở rộng từ Vulnerable & Outdated Components); **Injection** xuống A05; **Insecure Design** xuống A06; **A10 Mishandling of Exceptional Conditions** (MỚI); **SSRF gộp vào A01** (không còn category riêng).
3) Nếu là bài 00 (intro): thêm/ cập nhật **bảng mapping 2021↔2025**. Đảm bảo toàn cluster có nhắc 2 category mới (A03 Supply Chain, A10 Mishandling) và việc SSRF gộp A01.
4) Áp các finding của file (code/factual: PBKDF2 600k là OWASP không phải NIST; SLSA L4 là "deferred ở v1.0" không phải "merged L3"; argon2 verify try/except; số liệu IBM $4.88M / 194+64 ngày; bảng vỡ).

BẢO TOÀN: nội dung kỹ thuật + code mẫu (chỉ sửa numbering/tên/chỗ sai). GIỮ NGUYÊN tên file (đừng rename — vỡ link). KHÔNG đụng nav/time/de-meta (đã sync). KHÔNG lọt tag tool-call.

METADATA: bump MAJOR (vd v1.1.0 → v2.0.0 vì cập nhật chuẩn lớn), "Cập nhật: 07/06/2026", changelog TĂNG DẦN. Xong trả 2-3 dòng tóm tắt. KHÔNG gọi tool ở cuối.`

phase('Fix')
const all = [...OWASP.map(f => ({f, owasp:true})), ...OTHER.map(f => ({f, owasp:false}))]
const res = await parallel(all.map(({f, owasp}) => () =>
  agent(owasp ? owaspPrompt(f) : fixPrompt(f), { label: `${owasp?'owasp':'fix'}:${f.split('/').slice(1,2)}/${f.split('/').pop()}`, phase: 'Fix' })
    .then(t => ({ f, t })).catch(() => ({ f, t: 'ERROR' }))
))
const ok = res.filter(s => s && s.t !== 'ERROR')
log(`Fix xong ${ok.length}/${all.length} file.`)
return { processed: ok.length, total: all.length, summaries: res.map(s => ({ file: s.f, summary: (s.t||'').slice(0,220) })) }
