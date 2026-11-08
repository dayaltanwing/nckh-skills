#!/usr/bin/env bash
# Tải bản mới nhất của bộ skill NCKH từ GitHub và cài vào MỘT dự án.
#
# Chạy trong thư mục đề tài:
#   curl -fsSL https://raw.githubusercontent.com/dayaltanwing/nckh-skills/main/get.sh | bash
# Thêm tuỳ chọn của install.sh sau "bash -s --", ví dụ gỡ khỏi dự án:
#   curl -fsSL https://raw.githubusercontent.com/dayaltanwing/nckh-skills/main/get.sh | bash -s -- --go
set -euo pipefail

REPO="dayaltanwing/nckh-skills"
NHANH="${NCKH_NHANH:-main}"

for a in "$@"; do
  if [ "$a" = "--link" ]; then
    echo "--link chỉ dùng với bản clone của repo (bản tải về đây sẽ bị xoá sau khi cài)." >&2
    exit 2
  fi
done

TAM="$(mktemp -d)"
trap 'rm -rf "$TAM"' EXIT

echo "Đang tải $REPO ($NHANH)…"
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$NHANH" | tar -xz -C "$TAM"
GOC="$(ls -d "$TAM"/*/ | head -1)"
bash "${GOC}install.sh" "$@"
