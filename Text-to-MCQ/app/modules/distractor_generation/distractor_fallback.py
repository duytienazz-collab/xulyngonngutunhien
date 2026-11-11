"""Sinh distractor theo luật khi pool trong văn bản không đủ."""
import random
import re

PROVINCES = ["Quảng Trị", "Quảng Bình", "Quảng Ngãi", "Quảng Ninh", "Nghệ An", "Hà Tĩnh", "Thanh Hóa", "Lào Cai", "Lạng Sơn", "Cao Bằng", "Ninh Bình", "Hưng Yên", "Phú Thọ", "Thái Nguyên", "Tuyên Quang", "Sơn La", "Điện Biên", "Lai Châu", "Khánh Hòa", "Lâm Đồng", "Gia Lai", "Đắk Lắk", "Đồng Nai", "Tây Ninh", "Vĩnh Long", "Đồng Tháp", "An Giang", "Cà Mau", "Bình Định", "Quảng Nam"]
CITIES = ["Hà Nội", "Hải Phòng", "Huế", "Đà Nẵng", "Cần Thơ", "Hồ Chí Minh"]
COUNTRIES = ["Việt Nam", "Lào", "Campuchia", "Thái Lan", "Myanmar", "Malaysia", "Indonesia", "Philippines", "Singapore", "Trung Quốc", "Nhật Bản", "Hàn Quốc", "Ấn Độ", "Nga", "Pháp", "Đức", "Anh", "Hoa Kỳ", "Úc", "Canada"]
REGIONS = ["miền Bắc", "miền Trung", "miền Nam", "Tây Nguyên", "Đông Nam Bộ", "Tây Nam Bộ", "Bắc Trung Bộ", "Nam Trung Bộ", "Tây Bắc", "Đông Bắc"]
RIVERS = ["sông Hồng", "sông Đà", "sông Mã", "sông Cả", "sông Gianh", "sông Thạch Hãn", "sông Hương", "sông Thu Bồn", "sông Trà Khúc", "sông Đồng Nai", "sông Tiền", "sông Hậu", "sông Sài Gòn"]
LAKES = ["hồ Hoàn Kiếm", "hồ Tây", "hồ Ba Bể", "hồ Hòa Bình", "hồ Trị An", "hồ Dầu Tiếng", "hồ Thác Bà", "hồ Núi Cốc"]
MINISTRIES = ["Bộ Quốc phòng", "Bộ Công an", "Bộ Y tế", "Bộ Giáo dục và Đào tạo", "Bộ Tài chính", "Bộ Ngoại giao", "Bộ Xây dựng", "Bộ Tư pháp", "Bộ Giao thông vận tải", "Bộ Khoa học và Công nghệ"]
UNIVERSITIES = ["Đại học Quốc gia Hà Nội", "Đại học Bách khoa Hà Nội", "Đại học Kinh tế Quốc dân", "Đại học Huế", "Đại học Đà Nẵng", "Đại học Cần Thơ", "Đại học Y Hà Nội", "Đại học Ngoại thương"]
GENERIC_ORGS = ["Liên Hợp Quốc", "Ngân hàng Thế giới", "Tổ chức Y tế Thế giới", "Quốc hội", "Chính phủ", "Ngân hàng Nhà nước Việt Nam", "Đài Truyền hình Việt Nam", "Hội Chữ thập đỏ Việt Nam", "Hội Liên hiệp Phụ nữ Việt Nam"]
SURNAMES = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
MALE_MIDDLES = ["Văn", "Đức", "Minh", "Quốc", "Hữu", "Thanh", "Xuân"]
MALE_GIVENS = ["Anh", "Bình", "Cường", "Dũng", "Hải", "Hùng", "Khánh", "Long", "Nam", "Phong", "Quang", "Sơn", "Tuấn", "Việt"]
FEMALE_GIVENS = ["Lan", "Hoa", "Mai", "Hương", "Linh", "Thảo", "Trang", "Ngọc", "Hạnh", "Yến"]


def _in(pool, text):
    t = text.strip().casefold()
    return any(t == p.casefold() for p in pool)


def _time(answer):
    a = answer.strip()
    m = re.search(r"(\d+)(?!.*\d)", a)
    if not m:
        return []
    num = int(m.group(1))
    before = a[:m.start()].split()
    kw = before[-1].lower() if before else ("năm" if len(m.group(1)) == 4 else "")
    if kw == "năm":
        values = [num + d for d in (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)]
    elif kw == "tháng":
        values = list(range(1, 13))
    elif kw == "ngày":
        values = list(range(1, 29))
    elif kw == "kỷ":
        values = [num + d for d in (-3, -2, -1, 1, 2, 3)]
    else:
        return []
    values = [v for v in values if v > 0 and v != num]
    return [a[:m.start()] + str(v) + a[m.end():] for v in values]


def _num(answer):
    """Xử lý số liệu (450 MW -> 400 MW, 500 MW, 350 MW...)."""
    a = answer.strip()
    m = re.search(r"(\d+(?:[\.,]\d+)?)", a)
    if not m:
        return []
    try:
        num = float(m.group(1).replace(",", "."))
    except ValueError:
        return []
    # Tạo các số lân cận (giữ nguyên đơn vị)
    offsets = [-200, -150, -100, -50, -20, -10, 10, 20, 50, 100, 150, 200]
    result = []
    for d in offsets:
        new_num = num + d
        if new_num <= 0 or new_num == num:
            continue
        # Format số nguyên nếu có thể
        if new_num == int(new_num):
            new_str = str(int(new_num))
        else:
            new_str = f"{new_num:g}"
        new_text = a[:m.start()] + new_str + a[m.end():]
        result.append(new_text)
    return result


def _loc(answer):
    a = answer.strip()
    low = a.lower()
    if low.startswith("tỉnh "):
        return ["tỉnh " + p for p in PROVINCES]
    if low.startswith("thành phố "):
        return ["thành phố " + p for p in CITIES]
    if low.startswith("sông "):
        return list(RIVERS)
    if low.startswith("hồ "):
        return list(LAKES)
    if _in(REGIONS, a) or low.startswith("miền "):
        return list(REGIONS)
    if _in(COUNTRIES, a):
        return list(COUNTRIES)
    if _in(PROVINCES, a) or _in(CITIES, a):
        return PROVINCES + CITIES
    return []


def _org(answer):
    a = answer.strip()
    low = a.lower()
    m = re.match(r"^(.*\b(?:tỉnh|thành phố))\s+(.+)$", a, flags=re.IGNORECASE)
    if m:
        head, place = m.group(1), m.group(2)
        pool = CITIES if head.lower().endswith("thành phố") else PROVINCES
        return [f"{head} {p}" for p in pool if p.casefold() != place.casefold()]
    if low.startswith("bộ "):
        return list(MINISTRIES)
    if low.startswith(("đại học", "trường đại học")):
        return list(UNIVERSITIES)
    return list(GENERIC_ORGS)


def _person(answer):
    words = answer.split()
    if len(words) not in (2, 3) or words[0] not in SURNAMES:
        return []
    female = "Thị" in words
    givens = FEMALE_GIVENS if female else MALE_GIVENS
    names = set()
    for _ in range(40):
        s, g = random.choice(SURNAMES), random.choice(givens)
        if len(words) == 3:
            mid = "Thị" if female else random.choice(MALE_MIDDLES)
            names.add(f"{s} {mid} {g}")
        else:
            names.add(f"{s} {g}")
    return list(names)


_HANDLERS = {
    "TIME": _time,
    "LOC": _loc,
    "ORG": _org,
    "PER": _person,
    "NUM": _num,
}


def fallback_distractors(answer: str, answer_type: str) -> list:
    """Trả về danh sách distractor ứng viên (đã xáo trộn)."""
    handler = _HANDLERS.get(answer_type)
    if not handler:
        return []
    pool = handler(answer)
    random.shuffle(pool)
    return pool