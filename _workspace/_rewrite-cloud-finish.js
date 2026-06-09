export const meta = {
  name: 'cloud-rewrite-finish',
  description: 'Hoàn thiện 28 file 11_cloud còn dở (rewrite Việt-hoá + fix), KHÔNG schema để tránh lỗi StructuredOutput',
  phases: [{ title: 'Rewrite' }],
}

const ROOT = '04_Knowledge/dev-knowledge'
const FILES = [
  '11_cloud/cloudflare/lessons/01_basic/00_what-is-cloudflare-overview.md',
  '11_cloud/cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md',
  '11_cloud/cloudflare/lessons/01_basic/03_r2-and-d1-and-queues.md',
  '11_cloud/cloudflare/lessons/01_basic/04_security-zero-trust-and-waf.md',
  '11_cloud/digitalocean/README.md',
  '11_cloud/digitalocean/lessons/01_basic/00_what-is-digitalocean-overview.md',
  '11_cloud/digitalocean/lessons/01_basic/01_droplets-and-volumes.md',
  '11_cloud/digitalocean/lessons/01_basic/02_spaces-object-storage-and-cdn.md',
  '11_cloud/digitalocean/lessons/01_basic/03_managed-databases.md',
  '11_cloud/digitalocean/lessons/01_basic/04_app-platform-and-functions.md',
  '11_cloud/gcp/README.md',
  '11_cloud/gcp/lessons/01_basic/00_what-is-gcp-overview.md',
  '11_cloud/gcp/lessons/01_basic/01_compute-engine-and-disks.md',
  '11_cloud/gcp/lessons/01_basic/02_cloud-storage-and-iam.md',
  '11_cloud/gcp/lessons/01_basic/03_cloud-sql-and-firestore.md',
  '11_cloud/gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md',
  '11_cloud/multi-cloud-strategies/README.md',
  '11_cloud/multi-cloud-strategies/lessons/01_basic/00_what-is-multi-cloud-overview.md',
  '11_cloud/multi-cloud-strategies/lessons/01_basic/01_vendor-lock-in-and-portability.md',
  '11_cloud/multi-cloud-strategies/lessons/01_basic/02_multi-cloud-network-and-identity.md',
  '11_cloud/multi-cloud-strategies/lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md',
  '11_cloud/multi-cloud-strategies/lessons/01_basic/04_disaster-recovery-and-architecture-patterns.md',
  '11_cloud/serverless/README.md',
  '11_cloud/serverless/lessons/01_basic/00_what-is-serverless-overview.md',
  '11_cloud/serverless/lessons/01_basic/01_function-as-a-service-deep.md',
  '11_cloud/serverless/lessons/01_basic/02_event-driven-and-triggers.md',
  '11_cloud/serverless/lessons/01_basic/03_serverless-patterns-and-anti-patterns.md',
  '11_cloud/serverless/lessons/01_basic/04_serverless-cost-cold-start-and-observability.md',
]

const prompt = (file) => `Bạn là chuyên gia nội dung kỹ thuật tiếng Việt (persona Mr.Rom), hoàn thiện 1 bài trong kho dev-knowledge.

FILE: \`${ROOT}/${file}\`

ĐỌC TRƯỚC: gold-standard \`${ROOT}/10_devops/docker/lessons/01_basic/00_what-is-docker.md\` (chuẩn văn phong) + checklist \`${ROOT}/_workspace/lesson-qa-checklist.md\` + findings audit \`${ROOT}/_workspace/_audit-11cloud-findings.json\` (LỌC finding có "file"=="${file}").

ĐÁNH GIÁ prose rồi quyết:
- NẾU "điện tín tiếng Anh" (vd "**You manage**:", "**Pros**:/**Cons**:", bullet/Q&A thuần EN) → VIẾT LẠI sang tiếng Việt narrative đúng gold-standard: lời dẫn 2-3 câu trước mỗi bảng/code/list, ẩn dụ khi cần, mạch WHY→WHAT→HOW, câu phân tích sau.
- NẾU đã là tiếng Việt narrative tốt → chỉ áp fix bên dưới, KHÔNG viết lại.

BẢO TOÀN TUYỆT ĐỐI: mọi nội dung kỹ thuật, số liệu (giữ nguyên con số như "95%", "20 dịch vụ"...), mọi code/lệnh/config trong fence (giữ tiếng Anh), tên dịch vụ EN. Cấu trúc 8 phần + diagram.

ÁP FIX:
- Heading framework canonical 1:1: \`## 🧠 Tự kiểm tra (Self-check)\`, \`## ⚡ Tra cứu nhanh (Cheatsheet)\`, \`## 💡 Cạm bẫy thường gặp & Best practice\`.
- "**Prerequisites:**" → "**Yêu cầu trước:**". Glossary → 3 cột \`| Thuật ngữ | Tiếng Việt | Giải thích |\`.
- Nav (🔗 Liên kết & Tài nguyên): marker \`⬅️ Bài trước / ➡️ Bài tiếp theo / ↑ Về cụm\`, link-text = tiêu đề H1 thực; 3 sub \`🧭 Định hướng lộ trình học / 🧩 Các chủ đề liên quan / 🌐 Tài nguyên tham khảo khác\`; XOÁ nhãn "(sắp viết)" cho bài đã tồn tại.
- code-error/factual-error trong findings: VERIFY từng cái, chỉ fix nếu CHẮC sai (vd GCP không có "S3" mà là "Cloud Storage/GCS"); false-positive thì bỏ qua.

VÙNG CẤM: KHÔNG nhắc ngôn ngữ/đối tượng/phương pháp/persona trong thân bài; KHÔNG bịa nhân vật (dùng "bạn"); KHÔNG ước tính thời gian.

METADATA: bump version (rewrite→major vd v1.1.0→v2.0.0; fix-only→minor +0.1.0), "Cập nhật: 01/06/2026". Changelog TĂNG DẦN, thêm dòng CUỐI: \`- **vX.Y.Z (01/06/2026)** — <mô tả>.\`

QUAN TRỌNG VỀ ĐỊNH DẠNG: dùng Edit/Write để sửa file. TUYỆT ĐỐI không để lọt tag tool-call (</content>, </invoke>...) vào nội dung file. Khi xong, trả lời bằng 2-3 dòng text tóm tắt (rewritten hay fixed-only + version + điểm chính). KHÔNG cần gọi tool nào ở cuối.`

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
return { processed: ok.length, total: FILES.length, summaries: summaries.map((s) => ({ file: s.file, summary: (s.text || '').slice(0, 300) })) }
