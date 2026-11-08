#!/usr/bin/env bash
# Cài bộ skill NCKH cho Claude Code. Mặc định chỉ cài cho MỘT dự án.
#
#   ./install.sh                      cài vào dự án ở thư mục hiện tại (<thư mục>/.claude/skills)
#   ./install.sh "/đường/dẫn/đề-tài"   cài vào dự án đó
#   ./install.sh --go [thư mục]       gỡ bộ skill khỏi dự án đó
#   ./install.sh --link [thư mục]     tạo symlink thay vì sao chép (sửa skill ở bản clone là dự án thấy ngay)
#   ./install.sh --global             cài cho MỌI dự án (~/.claude/skills); chỉ dùng khi bạn thật sự muốn
set -euo pipefail

NGUON="$(cd "$(dirname "$0")" && pwd)/skills"
CHE_DO="copy"
GO=0
TOAN_CUC=0
DU_AN=""

for a in "$@"; do
  case "$a" in
    --link) CHE_DO="link" ;;
    --go) GO=1 ;;
    --global) TOAN_CUC=1 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    -*) echo "Không hiểu tuỳ chọn: $a (xem --help)" >&2; exit 2 ;;
    *) DU_AN="$a" ;;
  esac
done

if [ "$TOAN_CUC" = 1 ]; then
  DICH="$HOME/.claude/skills"
else
  DU_AN="$(cd "${DU_AN:-$PWD}" && pwd)"
  if [ "$DU_AN" = "$HOME" ]; then
    echo "Bạn đang ở thư mục home: cài ở đây cũng là cài cho MỌI dự án." >&2
    echo "Hãy cd vào thư mục đề tài rồi chạy lại, hoặc thêm --global nếu bạn thật sự muốn." >&2
    exit 1
  fi
  DICH="$DU_AN/.claude/skills"
fi

# Gỡ: chỉ xoá những gì bộ này đã cài (symlink, hoặc thư mục có file đánh dấu .nckh-skills).
if [ "$GO" = 1 ]; then
  so=0
  for d in "$NGUON"/*/; do
    ten="$(basename "$d")"
    dich="$DICH/$ten"
    if [ -L "$dich" ] || [ -f "$dich/.nckh-skills" ]; then
      rm -rf "$dich"
      echo "– đã gỡ $ten"
      so=$((so + 1))
    fi
  done
  echo
  echo "Đã gỡ $so skill khỏi $DICH"
  exit 0
fi

mkdir -p "$DICH"
for d in "$NGUON"/*/; do
  ten="$(basename "$d")"
  dich="$DICH/$ten"
  if [ -e "$dich" ] || [ -L "$dich" ]; then
    if [ -L "$dich" ] || [ -f "$dich/.nckh-skills" ]; then
      rm -rf "$dich"
    else
      echo "Bỏ qua $ten: $dich đã tồn tại và không phải do bộ này cài."
      continue
    fi
  fi
  if [ "$CHE_DO" = "link" ]; then
    ln -s "${d%/}" "$dich"
  else
    cp -R "${d%/}" "$dich"
    touch "$dich/.nckh-skills"
  fi
  echo "✓ $ten"
done

echo
echo "Đã cài vào $DICH"
echo "Mở Claude Code trong thư mục đề tài và gõ: /nckh khoi-tao"
