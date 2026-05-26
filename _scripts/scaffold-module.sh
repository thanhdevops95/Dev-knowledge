#!/usr/bin/env bash

# ==============================================================================
# Tên script: scaffold-module.sh
# Tác giả: Mr.Rom
# Phiên bản: v1.0.0
# Mô tả: Tự động khởi tạo cấu trúc thư mục L2 chuẩn 7 lõi linh hoạt theo Blueprint
#        và sao chép các tệp mẫu (templates) với metadata điền sẵn.
# Sử dụng: ./_scripts/scaffold-module.sh <L1_Folder> <L2_Name>
# Ví dụ: ./_scripts/scaffold-module.sh 02_Tools docker
# ==============================================================================

set -euo pipefail

# 1. Đường dẫn gốc dự án (Repository Root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${REPO_ROOT}/_Blueprint/templates"

# 2. Hướng dẫn sử dụng
usage() {
    echo -e "❌ Sử dụng chưa đúng!"
    echo -e "👉 Cú pháp: $0 <L1_Folder> <L2_Name>"
    echo -e "👉 Ví dụ:   $0 02_Tools docker"
    echo -e "👉 Ví dụ:   $0 10_DevOps kubernetes"
    exit 1
}

# Kiểm tra số lượng tham số đầu vào
if [ "$#" -ne 2 ]; then
    usage
fi

L1_DIR="$1"
L2_NAME="$(echo "$2" | tr '[:upper:]' '[:lower:]')" # Chuẩn hóa lowercase cho L2

L1_PATH="${REPO_ROOT}/${L1_DIR}"
L2_PATH="${L1_PATH}/${L2_NAME}"

# 3. Kiểm tra tính hợp lệ của L1
if [ ! -d "${L1_PATH}" ]; then
    echo -e "❌ Lỗi: Thư mục L1 '${L1_DIR}' không tồn tại tại gốc kho!"
    echo -e "Vui lòng kiểm tra lại tên thư mục (ví dụ: 02_Tools, 10_DevOps...)"
    exit 1
fi

# 4. Kiểm tra sự tồn tại của các Template
if [ ! -d "${TEMPLATE_DIR}" ]; then
    echo -e "❌ Lỗi: Thư mục templates của Blueprint không tồn tại tại: ${TEMPLATE_DIR}"
    exit 1
fi

echo -e "🏗️  Đang khởi tạo cấu trúc L2 cho mô-đun: \033[1;32m${L2_NAME}\033[0m nằm trong \033[1;34m${L1_DIR}\033[0m..."

# 5. Tạo các thư mục 7 lõi linh hoạt theo chuẩn Blueprint
declare -a SUBDIRS=(
    "lessons/01_basic"
    "lessons/02_intermediate"
    "lessons/03_advanced"
    "setup"
    "exercises/01_basic"
    "exercises/02_intermediate"
    "exercises/03_advanced"
    "projects"
    "recipes"
)

# Tạo thư mục cha L2
mkdir -p "${L2_PATH}"

# Tạo các thư mục con
for sub in "${SUBDIRS[@]}"; do
    mkdir -p "${L2_PATH}/${sub}"
done

echo -e "✅ Đã tạo cấu trúc thư mục 7 lõi chuẩn."

# 6. Hàm sao chép file an toàn (Idempotent — không ghi đè nếu file đã có sẵn)
copy_template_safe() {
    local template_file="$1"
    local dest_file="$2"
    local desc="$3"

    if [ -f "${dest_file}" ]; then
        echo -e "🟡 Bỏ qua: ${desc} đã tồn tại, không ghi đè."
    else
        cp "${template_file}" "${dest_file}"
        echo -e "🟢 Đã tạo: ${desc}"
    fi
}

# Tên viết hoa chữ cái đầu cho tiêu đề (Capitalize)
L2_CAPITALIZED="$(echo "${L2_NAME:0:1}" | tr '[:lower:]' '[:upper:]')${L2_NAME:1}"
CURRENT_DATE="$(date +'%d/%m/%Y')"

# 7. Hàm thay thế chuỗi tương thích cả Linux và macOS (Idempotent & Safe)
replace_placeholder() {
    local target_str="$1"
    local replacement_str="$2"
    local target_file="$3"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|${target_str}|${replacement_str}|g" "${target_file}"
    else
        sed -i "s|${target_str}|${replacement_str}|g" "${target_file}"
    fi
}

# Tên viết hoa chữ cái đầu cho tiêu đề (Capitalize)
L2_CAPITALIZED="$(echo "${L2_NAME:0:1}" | tr '[:lower:]' '[:upper:]')${L2_NAME:1}"
CURRENT_DATE="$(date +'%d/%m/%Y')"

# 8. Sao chép và tiền xử lý các file mẫu (Template processing)

# A. README chính của mô-đun L2
dest_readme="${L2_PATH}/README.md"
copy_template_safe "${TEMPLATE_DIR}/topic-readme_template.md" "${dest_readme}" "README chính"
if [ -f "${dest_readme}" ]; then
    replace_placeholder "<Tên chủ đề>" "${L2_CAPITALIZED}" "${dest_readme}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_readme}"
fi

# B. 00_overview.md
dest_overview="${L2_PATH}/00_overview.md"
copy_template_safe "${TEMPLATE_DIR}/overview_template.md" "${dest_overview}" "00_overview.md"
if [ -f "${dest_overview}" ]; then
    replace_placeholder "<Tên mô-đun>" "${L2_CAPITALIZED}" "${dest_overview}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_overview}"
fi

# C. Bài học đầu tiên: lessons/01_basic/00_what-is-<module>.md
lesson_filename="00_what-is-${L2_NAME}.md"
dest_lesson="${L2_PATH}/lessons/01_basic/${lesson_filename}"
copy_template_safe "${TEMPLATE_DIR}/lesson_template.md" "${dest_lesson}" "${lesson_filename}"
if [ -f "${dest_lesson}" ]; then
    replace_placeholder "<Tên bài học>" "${L2_CAPITALIZED} là gì?" "${dest_lesson}"
    replace_placeholder "<Level>" "Basic" "${dest_lesson}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_lesson}"
fi

# D. Setup README
dest_setup="${L2_PATH}/setup/README.md"
copy_template_safe "${TEMPLATE_DIR}/setup_template.md" "${dest_setup}" "setup/README.md"
if [ -f "${dest_setup}" ]; then
    replace_placeholder "<Tên công cụ>" "${L2_CAPITALIZED}" "${dest_setup}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_setup}"
fi

# E. Bài trắc nghiệm đầu tiên: exercises/01_basic/quiz_basic-concepts.md
dest_quiz="${L2_PATH}/exercises/01_basic/quiz_basic-concepts.md"
copy_template_safe "${TEMPLATE_DIR}/exercise_template.md" "${dest_quiz}" "exercises/01_basic/quiz_basic-concepts.md"
if [ -f "${dest_quiz}" ]; then
    replace_placeholder "<Chủ đề bài học>" "Khái niệm cơ bản về ${L2_CAPITALIZED}" "${dest_quiz}"
    replace_placeholder "<Level>" "Basic" "${dest_quiz}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_quiz}"
fi

# F. Bài thực hành đầu tiên: exercises/01_basic/lab_first-steps.md
dest_lab="${L2_PATH}/exercises/01_basic/lab_first-steps.md"
copy_template_safe "${TEMPLATE_DIR}/lab_template.md" "${dest_lab}" "exercises/01_basic/lab_first-steps.md"
if [ -f "${dest_lab}" ]; then
    replace_placeholder "<Tên bài thực hành>" "Từng bước đầu tiên chinh phục ${L2_CAPITALIZED}" "${dest_lab}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_lab}"
fi

# G. Recipes README
dest_recipes="${L2_PATH}/recipes/README.md"
copy_template_safe "${TEMPLATE_DIR}/recipe_template.md" "${dest_recipes}" "recipes/README.md"
if [ -f "${dest_recipes}" ]; then
    replace_placeholder "<Tên lỗi>" "Lỗi thường gặp" "${dest_recipes}"
    replace_placeholder "DD/MM/YYYY" "${CURRENT_DATE}" "${dest_recipes}"
fi

echo -e "\n🎉 \033[1;32mHoàn thành cấu trúc mô-đun '${L2_NAME}' thành công!\033[0m"
echo -e "👉 Đường dẫn mô-đun mới: ${L2_PATH}"
echo -e "👉 Bạn có thể bắt đầu chỉnh sửa nội dung bài học tại: ${dest_lesson}"
echo -e "👉 Hãy làm theo các quy tắc viết của Mr.Rom tại _Blueprint/03_writing-style.md!"
