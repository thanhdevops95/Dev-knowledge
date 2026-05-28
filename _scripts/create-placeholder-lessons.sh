#!/usr/bin/env bash

# ==============================================================================
# Tên script: create-placeholder-lessons.sh
# Tác giả: Mr.Rom
# Phiên bản: v1.0.0
# Mô tả: Tạo placeholder lesson files tối giản cho 21 L2 modules
#        chưa có nội dung bài học. Giúp các links từ Career Roadmaps
#        trỏ đến target thật (không còn "chưa có").
# Sử dụng: bash _scripts/create-placeholder-lessons.sh
# ==============================================================================

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CURRENT_DATE="$(date +'%d/%m/%Y')"

create_placeholder() {
    local module_path="$1"
    local title="$2"
    local desc="$3"

    local target_dir="${REPO_ROOT}/${module_path}/lessons/01_basic"
    local basename_clean
    basename_clean="$(basename "$module_path")"
    local target_file="${target_dir}/00_what-is-${basename_clean}.md"

    # Idempotent check
    if [[ -f "$target_file" ]]; then
        echo "🟡 Bỏ qua: ${module_path} — bài học đã tồn tại."
        return
    fi

    # Ensure directory exists
    mkdir -p "$target_dir"

    cat > "$target_file" << HEREDOC
# ${title}

> **Tác giả:** Mr.Rom\\
> **Phiên bản:** v0.1.0 (placeholder)\\
> **Tạo lúc:** ${CURRENT_DATE}\\
> **Cập nhật:** ${CURRENT_DATE}\\
> **Level:** Basic\\
> **Thời lượng đọc:** ~15 phút\\
> **Status:** 🚧 Placeholder — nội dung chi tiết sẽ được bổ sung sau

> 🎯 *${desc}*

---

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu ${title} là gì và tại sao nó quan trọng
- [ ] Biết các khái niệm cốt lõi và thuật ngữ chính
- [ ] Hiểu khi nào nên sử dụng ${title}
- [ ] Sẵn sàng cho các bài thực hành tiếp theo

---

## 🚧 Nội dung đang được xây dựng

> Bài học này đang trong giai đoạn phát triển. Nội dung chi tiết sẽ được bổ sung theo chuẩn
> [Writing Style Guide](../../../../_blueprint/03_writing-style.md) của dự án.
>
> Trong thời gian chờ, bạn có thể tham khảo:
> - 📐 [Sitemap Detail](../../../../_blueprint/01_sitemap-detail.md) — xem cấu trúc dự kiến
> - 📚 Tài liệu chính thức của ${title}

---

## 📌 Changelog

- **v0.1.0 (${CURRENT_DATE})** — Placeholder — khung bài học được tạo tự động.
HEREDOC

    echo "🟢 Đã tạo: ${target_file}"
}

echo "🏗️  Bắt đầu tạo placeholder lessons cho 21 L2 modules trống..."
echo ""

# === 03_languages ===
create_placeholder "03_languages/csharp" \
    "C# là gì?" \
    "C# (C-Sharp) là ngôn ngữ lập trình hướng đối tượng do Microsoft phát triển, sử dụng rộng rãi trong game dev (Unity), desktop app (.NET) và web backend."

create_placeholder "03_languages/javascript-typescript" \
    "JavaScript & TypeScript là gì?" \
    "JavaScript là ngôn ngữ lập trình web phổ biến nhất thế giới, chạy trên cả browser và server. TypeScript là phiên bản có kiểu dữ liệu tĩnh của JavaScript."

# === 06_databases ===
create_placeholder "06_databases/database-design" \
    "Database Design là gì?" \
    "Database Design (Thiết kế cơ sở dữ liệu) là quá trình xác định cấu trúc bảng, quan hệ, khóa và ràng buộc để lưu trữ dữ liệu hiệu quả và nhất quán."

create_placeholder "06_databases/redis" \
    "Redis là gì?" \
    "Redis là hệ thống lưu trữ dữ liệu in-memory (trong RAM), thường dùng làm cache, message broker, và session store với tốc độ cực nhanh."

# === 08_mobile ===
create_placeholder "08_mobile/react-native" \
    "React Native là gì?" \
    "React Native là framework cross-platform cho phép bạn xây dựng ứng dụng iOS và Android bằng JavaScript/TypeScript với cùng một codebase."

# === 10_devops ===
create_placeholder "10_devops/gitops" \
    "GitOps là gì?" \
    "GitOps là phương pháp quản lý hạ tầng và triển khai ứng dụng sử dụng Git làm single source of truth. Mọi thay đổi đều đi qua Git (commit/PR)."

# === 12_security ===
create_placeholder "12_security/authorization" \
    "Authorization là gì?" \
    "Authorization (Phân quyền) là quá trình xác định user ĐÃ xác thực được phép làm gì. Bao gồm các mô hình RBAC, ABAC, ACL."

create_placeholder "12_security/cloud-security" \
    "Cloud Security là gì?" \
    "Cloud Security là tập hợp các chính sách, công nghệ và công cụ bảo vệ dữ liệu, ứng dụng và hạ tầng trên nền tảng đám mây."

create_placeholder "12_security/container-security" \
    "Container Security là gì?" \
    "Container Security bao gồm quét image (Trivy), runtime security, network policies và các best practice bảo mật cho Docker/Kubernetes."

create_placeholder "12_security/cryptography" \
    "Cryptography là gì?" \
    "Cryptography (Mật mã học) là khoa học mã hóa và giải mã thông tin. Bao gồm symmetric, asymmetric encryption, hashing và digital signatures."

create_placeholder "12_security/pentesting-fundamentals" \
    "Pentesting Fundamentals là gì?" \
    "Penetration Testing là quy trình kiểm thử xâm nhập bảo mật có phương pháp: reconnaissance → scanning → exploitation → post-exploitation → report."

# === 13_ai-ml ===
create_placeholder "13_ai-ml/deep-learning" \
    "Deep Learning là gì?" \
    "Deep Learning là nhánh con của Machine Learning sử dụng neural networks nhiều tầng (deep) để học các pattern phức tạp từ dữ liệu."

create_placeholder "13_ai-ml/math-for-ml" \
    "Toán cho Machine Learning là gì?" \
    "Nền tảng toán học cần thiết cho ML: Linear Algebra (vector, matrix), Calculus (gradient, optimization), Probability & Statistics."

create_placeholder "13_ai-ml/ml-fundamentals" \
    "Machine Learning Fundamentals là gì?" \
    "Machine Learning là phương pháp cho máy tính học từ dữ liệu thay vì lập trình rõ ràng. Bao gồm Supervised, Unsupervised và Reinforcement Learning."

create_placeholder "13_ai-ml/rag-and-ai-agent" \
    "RAG & AI Agent là gì?" \
    "RAG (Retrieval-Augmented Generation) kết hợp search + LLM. AI Agent là hệ thống tự động lập kế hoạch và thực thi task sử dụng tools."

create_placeholder "13_ai-ml/vector-search-and-embeddings" \
    "Vector Search & Embeddings là gì?" \
    "Embeddings biểu diễn dữ liệu (text, image) dưới dạng vector số. Vector Search tìm kiếm theo độ tương đồng ngữ nghĩa thay vì keyword chính xác."

# === 14_data-engineering ===
create_placeholder "14_data-engineering/airflow-and-orchestration" \
    "Airflow & Data Orchestration là gì?" \
    "Apache Airflow là nền tảng quản lý và lập lịch data pipeline. Data Orchestration điều phối các bước ETL/ELT theo thứ tự và điều kiện."

create_placeholder "14_data-engineering/data-lake" \
    "Data Lake là gì?" \
    "Data Lake là hệ thống lưu trữ dữ liệu thô ở mọi định dạng (structured, semi-structured, unstructured) với chi phí thấp và khả năng mở rộng cao."

create_placeholder "14_data-engineering/dbt" \
    "dbt là gì?" \
    "dbt (data build tool) là công cụ transform dữ liệu trong warehouse bằng SQL. Hỗ trợ version control, testing, documentation cho data pipeline."

create_placeholder "14_data-engineering/streaming" \
    "Data Streaming là gì?" \
    "Data Streaming xử lý dữ liệu real-time khi nó phát sinh (Kafka, Pulsar, Kinesis), thay vì batch processing theo lịch cố định."

# === 15_specialized ===
create_placeholder "15_specialized/blockchain" \
    "Blockchain là gì?" \
    "Blockchain là công nghệ sổ cái phân tán (distributed ledger), nền tảng của Bitcoin, Ethereum và smart contracts."

echo ""
echo "🎉 Hoàn thành! Đã tạo placeholder lessons cho tất cả L2 modules trống."
echo "👉 Các file đều tuân theo template chuẩn của _blueprint."
