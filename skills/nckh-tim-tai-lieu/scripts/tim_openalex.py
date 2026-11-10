#!/usr/bin/env python3
"""Tìm bài báo trên OpenAlex và (tuỳ chọn) xuất BibTeX qua doi.org.

Chỉ dùng thư viện chuẩn của Python 3.9+.

Ví dụ:
  python3 tim_openalex.py "career decision AND adolescents" --tu-nam 2015 --so-luong 30
  python3 tim_openalex.py "career adaptability" --sap-xep trich-dan --bib ung-vien.bib
  python3 tim_openalex.py --trich-dan-boi W2741809807 --so-luong 50

--bib ghi THÊM vào file, không ghi đè: bài đã có trong file (trùng DOI) được bỏ qua, và mục mới nào
trùng khoá với mục đã có thì được đổi khoá (thêm a, b, c…).

Nếu OpenAlex đòi khoá API, đặt khoá vào biến môi trường OPENALEX_API_KEY rồi chạy lại.
Script không bao giờ in khoá ra.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"
UA = "nckh-skills/1.1 (literature search script)"
TOI_DA_MOT_LAN = 200          # OpenAlex trả tối đa 200 bài cho một lần gọi


def lay_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for lan in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            raise
        except urllib.error.URLError:
            if lan < 2:
                time.sleep(2 * (lan + 1))
                continue
            raise


def tom_tat(inv):
    """OpenAlex lưu tóm tắt dạng inverted index; dựng lại thành câu."""
    if not inv:
        return ""
    vi_tri = {}
    for tu, ds in inv.items():
        for i in ds or []:
            vi_tri[i] = tu
    return " ".join(vi_tri[i] for i in sorted(vi_tri))


def tim(args):
    """Gọi OpenAlex. Trả về (tổng số bài khớp, các bài, URL truy vấn để ghi log)."""
    loc = []
    if args.tu_nam:
        loc.append(f"from_publication_date:{args.tu_nam}-01-01")
    if args.den_nam:
        loc.append(f"to_publication_date:{args.den_nam}-12-31")
    if args.loai:
        loc.append(f"type:{args.loai}")
    if args.trich_dan_boi:
        loc.append(f"cites:{args.trich_dan_boi}")
    tham_so = {"per-page": max(1, min(args.so_luong, TOI_DA_MOT_LAN))}
    if args.tu_khoa:
        tham_so["search"] = args.tu_khoa
    if loc:
        tham_so["filter"] = ",".join(loc)
    if args.sap_xep == "trich-dan":
        tham_so["sort"] = "cited_by_count:desc"
    elif args.sap_xep == "moi-nhat":
        tham_so["sort"] = "publication_date:desc"
    url = API + "?" + urllib.parse.urlencode(tham_so)
    # Khoá API chỉ đi kèm yêu cầu gửi đi; URL trả về để ghi log thì không có khoá.
    khoa = os.environ.get("OPENALEX_API_KEY", "").strip()
    du_lieu = lay_json(url + ("&" + urllib.parse.urlencode({"api_key": khoa}) if khoa else "")) or {}
    return (du_lieu.get("meta") or {}).get("count", 0), (du_lieu.get("results") or [])[: args.so_luong], url


def rut_gon(w):
    tac_gia = [((a or {}).get("author") or {}).get("display_name") for a in (w.get("authorships") or [])]
    tac_gia = [t for t in tac_gia if t]
    if len(tac_gia) > 3:
        ten = ", ".join(tac_gia[:3]) + " et al."
    else:
        ten = ", ".join(tac_gia)
    nguon = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", w.get("doi") or "", flags=re.I)
    oa = (w.get("open_access") or {}).get("oa_url") or ""
    return {
        "openalex": (w.get("id") or "").rsplit("/", 1)[-1],
        "tac_gia": ten,
        "nam": w.get("publication_year"),
        "tieu_de": (w.get("display_name") or "").strip(),
        "nguon": nguon,
        "loai": w.get("type"),
        "trich_dan": w.get("cited_by_count") or 0,
        "doi": doi,
        "oa_url": oa,
        "tom_tat": tom_tat(w.get("abstract_inverted_index")),
    }


def o_bang(gia_tri):
    """Một ô của bảng Markdown: tiêu đề có dấu | hoặc xuống dòng sẽ làm vỡ bảng."""
    return " ".join(str("" if gia_tri is None else gia_tri).split()).replace("|", "\\|")


# ---------- BibTeX ----------

MAU_DAU_MUC = re.compile(r"\s*@(\w+)\s*\{\s*([^,\s{}]+)\s*,")
MAU_DOI = re.compile(r"\bdoi\s*=\s*[{\"]\s*([^}\"]+?)\s*[}\"]", re.I)


def chuan_doi(doi):
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", (doi or "").strip(), flags=re.I).lower()


def doc_bib_da_co(duong):
    """(các DOI, các khoá viết thường, nội dung) của file .bib đã có; chưa có file thì đều rỗng."""
    try:
        with open(duong, encoding="utf-8-sig", errors="replace") as f:
            van_ban = f.read()
    except FileNotFoundError:
        return set(), set(), ""
    doi = {chuan_doi(d) for d in MAU_DOI.findall(van_ban)}
    khoa = {m.group(2).casefold() for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s{}]+)\s*,", van_ban)}
    return doi, khoa, van_ban


def lay_bibtex(doi):
    """BibTeX của một DOI, lấy từ doi.org. Ném lỗi nếu không lấy được hoặc câu trả lời không phải BibTeX."""
    req = urllib.request.Request(
        "https://doi.org/" + urllib.parse.quote(doi, safe="/"),
        headers={"Accept": "application/x-bibtex; charset=utf-8", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        muc = r.read().decode("utf-8", errors="replace").strip()
    if not MAU_DAU_MUC.match(muc):
        raise ValueError("doi.org không trả về BibTeX")
    return muc


def dat_khoa_rieng(muc, da_dung):
    """Nếu khoá của mục đã có mục khác dùng thì thêm a, b, c… cho tới khi không trùng. Trả về mục đã sửa."""
    m = MAU_DAU_MUC.match(muc)
    goc = moi = m.group(2)
    hau_to = iter("abcdefghijklmnopqrstuvwxyz")
    so = 2
    while moi.casefold() in da_dung:
        chu = next(hau_to, None)
        if chu is None:                 # hết bảng chữ cái: chuyển sang đánh số
            moi, so = f"{goc}{so}", so + 1
        else:
            moi = goc + chu
    da_dung.add(moi.casefold())
    return muc[: m.start(2)] + moi + muc[m.end(2):]


def ghi_bib(bai, duong):
    """Ghi thêm BibTeX của các bài có DOI vào file. Trả về (số bài mới, số đã có, [(doi, lý do không lấy được)])."""
    doi_co, khoa_co, van_ban = doc_bib_da_co(duong)
    moi, da_co, hong = [], 0, []
    for b in bai:
        doi = chuan_doi(b["doi"])
        if not doi:
            continue
        if doi in doi_co:
            da_co += 1
            continue
        try:
            muc = lay_bibtex(b["doi"])
        except Exception as e:  # noqa: BLE001  (một DOI lỗi không được làm mất các bài còn lại)
            hong.append((b["doi"], str(e)))
        else:
            moi.append(dat_khoa_rieng(muc, khoa_co))
            doi_co.add(doi)
        time.sleep(0.2)
    if moi:
        with open(duong, "a", encoding="utf-8") as f:
            if van_ban and not van_ban.endswith("\n"):
                f.write("\n")
            f.write("".join(m + "\n\n" for m in moi))
    return len(moi), da_co, hong


# ---------- chương trình chính ----------

def in_utf8():
    """Windows dùng bảng mã cũ khi đầu ra bị chuyển hướng, in tiếng Việt sẽ lỗi. Ép UTF-8."""
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8", errors="replace")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tu_khoa", nargs="?", help="chuỗi tìm (OpenAlex hỗ trợ AND, OR, NOT, \"cụm từ\")")
    p.add_argument("--tu-nam", type=int)
    p.add_argument("--den-nam", type=int)
    p.add_argument("--loai", help="article, review, book-chapter, dissertation…")
    p.add_argument("--so-luong", type=int, default=25, help=f"số bài muốn lấy (tối đa {TOI_DA_MOT_LAN} mỗi lần chạy)")
    p.add_argument("--sap-xep", choices=["lien-quan", "trich-dan", "moi-nhat"], default="lien-quan")
    p.add_argument("--trich-dan-boi", metavar="OPENALEX_ID", help="liệt kê các bài trích dẫn bài này (snowballing tiến)")
    p.add_argument("--bib", metavar="FILE", help="ghi thêm BibTeX của các bài có DOI vào file này (không ghi đè)")
    p.add_argument("--json", metavar="FILE", help="ghi toàn bộ kết quả (kèm tóm tắt) ra JSON")
    p.add_argument("--tom-tat", action="store_true", help="in kèm 300 ký tự đầu của tóm tắt")
    a = p.parse_args()
    if not a.tu_khoa and not a.trich_dan_boi:
        p.error("cần chuỗi tìm hoặc --trich-dan-boi")
    if a.so_luong < 1:
        p.error("--so-luong phải từ 1 trở lên")

    tong, ds, url = tim(a)
    bai = [rut_gon(w) for w in ds]
    print(f"# OpenAlex: {tong} kết quả khớp, hiển thị {len(bai)}")
    print(f"# Truy vấn: {url}")
    print(f"# Ngày tìm: {time.strftime('%Y-%m-%d')}  (ghi dòng này vào tim-kiem.md)")
    if a.so_luong > TOI_DA_MOT_LAN:
        print(f"# Lưu ý: mỗi lần chạy chỉ lấy được {TOI_DA_MOT_LAN} bài, không phải {a.so_luong}. "
              "Muốn lấy hết thì chia theo khoảng năm (--tu-nam, --den-nam) và chạy nhiều lần.")
    print()
    print("| # | Tác giả | Năm | Tiêu đề | Nguồn | Trích dẫn | DOI | Truy cập mở |")
    print("|---|---|---|---|---|---|---|---|")
    for i, b in enumerate(bai, 1):
        oa = "có" if b["oa_url"] else ""
        print(f"| {i} | {o_bang(b['tac_gia'])} | {o_bang(b['nam'])} | {o_bang(b['tieu_de'])} | {o_bang(b['nguon'])} "
              f"| {b['trich_dan']} | {o_bang(b['doi'])} | {oa} |")
        if a.tom_tat and b["tom_tat"]:
            print(f"|   | _{o_bang(b['tom_tat'][:300])}…_ |||||||")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(bai, f, ensure_ascii=False, indent=2)
        print(f"\nĐã ghi {len(bai)} bài vào {a.json}")

    if a.bib:
        moi, da_co, hong = ghi_bib(bai, a.bib)
        khong_doi = sum(1 for b in bai if not b["doi"])
        print(f"\nĐã ghi thêm BibTeX của {moi} bài vào {a.bib} "
              f"(bỏ qua: {da_co} bài đã có trong file, {khong_doi} bài không có DOI).")
        if hong:
            print(f"KHÔNG lấy được BibTeX của {len(hong)} bài; các bài này CHƯA có trong file:")
            for doi, ly_do in hong:
                print(f"- {doi}: {ly_do}")


def chay():
    in_utf8()
    try:
        main()
    except urllib.error.HTTPError as e:
        goi_y = ""
        if e.code in (401, 403):
            goi_y = (" Nếu OpenAlex đòi khoá API: lấy khoá trong tài khoản của bạn trên openalex.org, "
                     "đặt vào biến môi trường OPENALEX_API_KEY rồi chạy lại.")
        elif e.code == 429:
            goi_y = " OpenAlex báo đã gọi quá nhiều; chờ rồi chạy lại, hoặc dùng khoá API (biến OPENALEX_API_KEY)."
        sys.exit(f"OpenAlex từ chối yêu cầu: HTTP {e.code} {e.reason}.{goi_y}")
    except urllib.error.URLError as e:
        sys.exit(f"Lỗi mạng khi gọi OpenAlex: {e.reason}")


if __name__ == "__main__":
    chay()
