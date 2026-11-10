"""Tiện ích cho bộ kiểm thử: nạp script trong skills/ như một module và chạy nó như một lệnh."""
import importlib.util
import os
import subprocess
import sys

# Không sinh __pycache__ trong skills/: install.sh sao chép nguyên thư mục skill vào dự án người dùng.
sys.dont_write_bytecode = True

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRIPT = {
    "kiem_trich_dan": "skills/nckh-kiem-trich-dan/scripts/kiem_trich_dan.py",
    "kiem_thong_ke": "skills/nckh-phan-bien/scripts/kiem_thong_ke.py",
    "tim_openalex": "skills/nckh-tim-tai-lieu/scripts/tim_openalex.py",
}


def duong_dan(ten):
    return os.path.join(GOC, SCRIPT[ten])


def nap(ten):
    """Nạp script thành module mới (mỗi lần gọi một bản riêng, để test thay hàm mạng mà không ảnh hưởng nhau)."""
    spec = importlib.util.spec_from_file_location(ten, duong_dan(ten))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chay(ten, *doi_so, cwd=None, env=None):
    """Chạy script như người dùng chạy. Trả về (mã thoát, stdout, stderr)."""
    moi_truong = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    moi_truong.update(env or {})
    kq = subprocess.run(
        [sys.executable, duong_dan(ten), *doi_so],
        capture_output=True, text=True, encoding="utf-8", cwd=cwd, env=moi_truong, timeout=120,
    )
    return kq.returncode, kq.stdout, kq.stderr


def ghi(thu_muc, ten_file, noi_dung):
    duong = os.path.join(thu_muc, ten_file)
    os.makedirs(os.path.dirname(duong), exist_ok=True)
    with open(duong, "w", encoding="utf-8") as f:
        f.write(noi_dung)
    return duong
