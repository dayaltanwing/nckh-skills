#!/usr/bin/env python3
"""Tìm bài báo trên OpenAlex và (tuỳ chọn) xuất BibTeX qua doi.org.

Chỉ dùng thư viện chuẩn của Python 3.9+.

Ví dụ:
  python3 tim_openalex.py "career decision AND adolescents" --tu-nam 2015 --so-luong 30
  python3 tim_openalex.py "career adaptability" --sap-xep trich-dan --bib ung-vien.bib
  python3 tim_openalex.py --trich-dan-boi W2741809807 --so-luong 50
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.openalex.org/works"
UA = "nckh-skills/1.0 (literature search script)"


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
        for i in ds:
            vi_tri[i] = tu
    return " ".join(vi_tri[i] for i in sorted(vi_tri))


def tim(args):
    loc = []
    if args.tu_nam:
        loc.append(f"from_publication_date:{args.tu_nam}-01-01")
    if args.den_nam:
        loc.append(f"to_publication_date:{args.den_nam}-12-31")
    if args.loai:
        loc.append(f"type:{args.loai}")
    if args.trich_dan_boi:
        loc.append(f"cites:{args.trich_dan_boi}")
    tham_so = {"per-page": min(args.so_luong, 200)}
    if args.tu_khoa:
        tham_so["search"] = args.tu_khoa
    if loc:
        tham_so["filter"] = ",".join(loc)
    if args.sap_xep == "trich-dan":
        tham_so["sort"] = "cited_by_count:desc"
    elif args.sap_xep == "moi-nhat":
        tham_so["sort"] = "publication_date:desc"
    url = API + "?" + urllib.parse.urlencode(tham_so)
    du_lieu = lay_json(url)
    return du_lieu.get("meta", {}).get("count", 0), du_lieu.get("results", [])[: args.so_luong], url


def rut_gon(w):
    tac_gia = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
    if len(tac_gia) > 3:
        ten = ", ".join(tac_gia[:3]) + " et al."
    else:
        ten = ", ".join(tac_gia)
    nguon = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    oa = (w.get("open_access") or {}).get("oa_url") or ""
    return {
        "openalex": w.get("id", "").rsplit("/", 1)[-1],
        "tac_gia": ten,
        "nam": w.get("publication_year"),
        "tieu_de": (w.get("display_name") or "").strip(),
        "nguon": nguon,
        "loai": w.get("type"),
        "trich_dan": w.get("cited_by_count", 0),
        "doi": doi,
        "oa_url": oa,
        "tom_tat": tom_tat(w.get("abstract_inverted_index")),
    }


def bibtex(doi):
    req = urllib.request.Request(
        "https://doi.org/" + urllib.parse.quote(doi, safe="/"),
        headers={"Accept": "application/x-bibtex; charset=utf-8", "User-Agent": UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8").strip()
    except Exception as e:  # noqa: BLE001
        return f"% KHÔNG LẤY ĐƯỢC BibTeX cho {doi}: {e}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tu_khoa", nargs="?", help="chuỗi tìm (OpenAlex hỗ trợ AND, OR, NOT, \"cụm từ\")")
    p.add_argument("--tu-nam", type=int)
    p.add_argument("--den-nam", type=int)
    p.add_argument("--loai", help="article, review, book-chapter, dissertation…")
    p.add_argument("--so-luong", type=int, default=25)
    p.add_argument("--sap-xep", choices=["lien-quan", "trich-dan", "moi-nhat"], default="lien-quan")
    p.add_argument("--trich-dan-boi", metavar="OPENALEX_ID", help="liệt kê các bài trích dẫn bài này (snowballing tiến)")
    p.add_argument("--bib", metavar="FILE", help="ghi BibTeX của các bài có DOI vào file này")
    p.add_argument("--json", metavar="FILE", help="ghi toàn bộ kết quả (kèm tóm tắt) ra JSON")
    p.add_argument("--tom-tat", action="store_true", help="in kèm 300 ký tự đầu của tóm tắt")
    a = p.parse_args()
    if not a.tu_khoa and not a.trich_dan_boi:
        p.error("cần chuỗi tìm hoặc --trich-dan-boi")

    tong, ds, url = tim(a)
    bai = [rut_gon(w) for w in ds]
    print(f"# OpenAlex: {tong} kết quả khớp, hiển thị {len(bai)}")
    print(f"# Truy vấn: {url}")
    print(f"# Ngày tìm: {time.strftime('%Y-%m-%d')}  (ghi dòng này vào tim-kiem.md)\n")
    print("| # | Tác giả | Năm | Tiêu đề | Nguồn | Trích dẫn | DOI | Truy cập mở |")
    print("|---|---|---|---|---|---|---|---|")
    for i, b in enumerate(bai, 1):
        oa = "có" if b["oa_url"] else ""
        print(f"| {i} | {b['tac_gia']} | {b['nam']} | {b['tieu_de']} | {b['nguon']} | {b['trich_dan']} | {b['doi']} | {oa} |")
        if a.tom_tat and b["tom_tat"]:
            print(f"|   | _{b['tom_tat'][:300]}…_ |||||||")

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(bai, f, ensure_ascii=False, indent=2)
        print(f"\nĐã ghi {len(bai)} bài vào {a.json}")

    if a.bib:
        co_doi = [b for b in bai if b["doi"]]
        with open(a.bib, "w", encoding="utf-8") as f:
            for b in co_doi:
                f.write(bibtex(b["doi"]) + "\n\n")
                time.sleep(0.2)
        print(f"Đã ghi BibTeX của {len(co_doi)}/{len(bai)} bài (bài không có DOI bị bỏ qua) vào {a.bib}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as e:
        sys.exit(f"Lỗi mạng khi gọi OpenAlex: {e}")
