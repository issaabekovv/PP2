import re
import json


def read_receipt(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def money_to_float(s: str) -> float:
    # "1 526,00" -> 1526.00
    return float(s.replace(" ", "").replace(",", "."))


def extract_datetime(text: str) -> str | None:
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})", text)
    return m.group(1) if m else None


def extract_total_from_receipt(text: str) -> str | None:
    m = re.search(r"ИТОГО:\n([\d ]+,\d{2})", text)
    return m.group(1) if m else None


def extract_payment_method(text: str) -> str | None:
    m = re.search(r"(Банковская карта|Наличные)", text)
    return m.group(1) if m else None


def parse_items(text: str) -> list[dict]:
    """
    Парсим блоки товаров вида:
    1.
    Название
    2,000 x 154,00
    308,00
    Стоимость
    308,00
    """
    item_re = re.compile(
        r"(?m)^\s*(\d+)\.\s*\n"          # номер
        r"(.+?)\n"                      # название (1 строка)
        r"(\d+,\d{3})\s*x\s*"           # количество: 2,000
        r"(\d{1,3}(?: \d{3})*,\d{2})\n" # цена за шт: 1 200,00
        r"(\d{1,3}(?: \d{3})*,\d{2})\n" # сумма по строке: 308,00
    )

    items = []
    for m in item_re.finditer(text):
        idx = int(m.group(1))
        name = m.group(2).strip()
        qty_str = m.group(3)
        unit_price_str = m.group(4)
        line_total_str = m.group(5)

        qty = float(qty_str.replace(",", "."))  # 2,000 -> 2.0
        unit_price = money_to_float(unit_price_str)
        line_total = money_to_float(line_total_str)

        items.append({
            "index": idx,
            "name": name,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total,
        })

    return items


def main():
    text = read_receipt("raw.txt")

    items = parse_items(text)
    calculated_total = round(sum(i["line_total"] for i in items), 2)

    total_from_receipt_str = extract_total_from_receipt(text)
    total_from_receipt = money_to_float(total_from_receipt_str) if total_from_receipt_str else None

    data = {
        "date_time": extract_datetime(text),
        "payment_method": extract_payment_method(text),
        "items": items,
        "calculated_total": calculated_total,
        "total_from_receipt": total_from_receipt,
        "totals_match": (total_from_receipt == calculated_total) if total_from_receipt is not None else None,
    }

    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()