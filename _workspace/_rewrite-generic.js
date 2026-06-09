export const meta = {
  name: 'lesson-rewrite-fix',
  description: 'Rewrite Việt-hoá (nếu điện tín-EN) + fix theo gold-standard cho danh sách file, schema-free + verify cơ học',
  phases: [{ title: 'Rewrite' }],
}

const ROOT = '04_Knowledge/dev-knowledge'
const FILES = [
  '10_devops/iac/lessons/01_basic/03_modules-and-workspaces.md',
  '10_devops/iac/lessons/02_intermediate/01_terragrunt-dry-multi-env.md',
  '10_devops/iac/lessons/02_intermediate/02_atlantis-gitops-for-iac.md',
  '10_devops/iac/lessons/02_intermediate/03_state-advanced-and-drift.md',
  '10_devops/iac/lessons/02_intermediate/04_pulumi-cdk-crossplane.md',
  '10_devops/observability/lessons/02_intermediate/01_promql-deep-and-alerting.md',
  '10_devops/observability/lessons/02_intermediate/02_loki-logql-deep.md',
  '10_devops/observability/lessons/02_intermediate/03_opentelemetry-instrumentation.md',
]

const prompt = (file) => `Bạn là chuyên gia nội dung kỹ thuật tiếng Việt (persona Mr.Rom), hoàn thiện 1 bài trong kho dev-knowledge.

FILE: \`${ROOT}/${file}\`

ĐỌC TRƯỚC: gold-standard \`${ROOT}/10_devops/docker/lessons/02_intermediate/01_buildkit-and-multistage-advanced.md\` (chuẩn văn phong intermediate) + \`${ROOT}/_workspace/lesson-qa-checklist.md\` (checklist).

ĐÁNH GIÁ prose rồi quyết:
- NẾU có đoạn "điện tín tiếng Anh" (bullet/bảng/Q&A khô, "**Pros**:/**Cons**:" thuần EN, "**You manage**:", định nghĩa cụt tiếng Anh, nhảy thẳng vào bảng/code không lời dẫn) → VIẾT LẠI sang tiếng Việt narrative đúng gold-standard: lời dẫn 2-3 câu trước mỗi bảng/code/list, ẩn dụ khi cần, mạch WHY→WHAT→HOW, câu phân tích sau. Label "**Pros**:"→"**Ưu điểm**:", "**Cons**:"→"**Nhược điểm**:".
- NẾU prose đã là tiếng Việt narrative tốt → chỉ áp fix, KHÔNG viết lại.

BẢO TOÀN TUYỆT ĐỐI: mọi nội dung kỹ thuật, số liệu, mọi code/lệnh/config trong fence (giữ tiếng Anh), tên công cụ/dịch vụ EN, cấu trúc 8 phần + diagram.

ÁP FIX (đối chiếu checklist):
- Heading framework canonical 1:1: \`## 🧠 Tự kiểm tra (Self-check)\`, \`## ⚡ Tra cứu nhanh (Cheatsheet)\`, \`## 💡 Cạm bẫy thường gặp & Best practice\`.
- "**Prerequisites:**" → "**Yêu cầu trước:**". Glossary → 3 cột \`| Thuật ngữ | Tiếng Việt | Giải thích |\`.
- Nav (🔗 Liên kết & Tài nguyên): marker \`⬅️ Bài trước / ➡️ Bài tiếp theo / ↑ Về cụm\`, link-text = tiêu đề H1 thực; 3 sub \`🧭 Định hướng lộ trình học / 🧩 Các chủ đề liên quan / 🌐 Tài nguyên tham khảo khác\`. XOÁ nhãn "(sắp viết)" cho bài đã tồn tại. SỬA link gãy nếu tìm được đích đúng (sai số ../).
- Lỗi code/lệnh sai/deprecated/factual rõ ràng (đối chiếu kiến thức 2026): chỉ fix nếu CHẮC sai.

VÙNG CẤM: KHÔNG nhắc ngôn ngữ/đối tượng/phương pháp/persona trong thân bài; KHÔNG bịa nhân vật (dùng "bạn"); KHÔNG ước tính thời gian (tháng/tuần/giờ/phút).

METADATA: bump version (rewrite→major; fix-only→minor +0.1.0), "Cập nhật: 07/06/2026". Changelog TĂNG DẦN, thêm dòng CUỐI: \`- **vX.Y.Z (07/06/2026)** — <mô tả>.\`

ĐỊNH DẠNG: dùng Edit/Write. TUYỆT ĐỐI không để lọt tag tool-call (</content>, </invoke>...) vào file. Xong thì trả lời 2-3 dòng text tóm tắt (rewritten/fixed-only + version + điểm chính). KHÔNG gọi tool ở cuối.`

phase('Rewrite')
const summaries = await parallel(
  FILES.map((file) => () =>
    agent(prompt(file), { label: `${file.split('/').slice(1, 2)}/${file.split('/').pop()}`, phase: 'Rewrite' })
      .then((text) => ({ file, text }))
      .catch(() => ({ file, text: 'ERROR' }))
  )
)
const ok = summaries.filter((s) => s && s.text !== 'ERROR')
log(`Hoàn thiện ${ok.length}/${FILES.length} file.`)
return { processed: ok.length, total: FILES.length, summaries: summaries.map((s) => ({ file: s.file, summary: (s.text || '').slice(0, 250) })) }
