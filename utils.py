"""
utils.py – Helper functions for summary calculation and data export.
"""
import csv
import io
from datetime import datetime


def calculate_summary(selections: dict, guest_count: int, menu_data: dict, upsells: list) -> dict:
    """Return a summary dict with total_dishes count and per-category breakdown."""
    breakdown = {}
    total = 0

    for category in menu_data:
        chosen = selections.get(category, [])
        breakdown[category] = chosen
        total += len(chosen)

    return {
        "total_dishes": total,
        "breakdown": breakdown,
        "guest_count": guest_count,
    }


def export_to_csv(
    selections: dict,
    dietary_notes: dict,
    guest_count: int,
    couple_name: str,
    menu_data: dict,
    upsells: list,
) -> str:
    """Generate a CSV string ready for download."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header block
    writer.writerow(["KONFIGURATOR MENU WESELNEGO"])
    writer.writerow(["Para Młoda:", couple_name or "—"])
    writer.writerow(["Liczba gości:", guest_count])
    writer.writerow(["Data eksportu:", datetime.now().strftime("%Y-%m-%d %H:%M")])
    writer.writerow([])

    # Selected dishes
    writer.writerow(["KATEGORIA", "DANIE", "PORCJE", "ALERGENY"])
    for category, items in menu_data.items():
        chosen = selections.get(category, [])
        for dish_name in chosen:
            dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
            allergens = ", ".join(dish.get("allergens", [])) if dish else ""
            writer.writerow([category, dish_name, guest_count, allergens])

    writer.writerow([])

    # Dietary
    writer.writerow(["ZESTAWIENIE DIET"])
    writer.writerow(["Dieta", "Liczba gości"])
    writer.writerow(["Wegetariańska", dietary_notes.get("vegetarian", 0)])
    writer.writerow(["Wegańska", dietary_notes.get("vegan", 0)])
    writer.writerow(["Bezglutenowa", dietary_notes.get("gluten_free", 0)])
    if dietary_notes.get("other"):
        writer.writerow(["Inne uwagi", dietary_notes["other"]])

    writer.writerow([])

    # Upsells
    chosen_upsells = selections.get("_upsells", [])
    if chosen_upsells:
        writer.writerow(["DODATKI PREMIUM"])
        for u in chosen_upsells:
            upsell = next((x for x in upsells if x["name"] == u), None)
            price = upsell.get("price", "—") if upsell else "—"
            writer.writerow([u, f"od {price} zł"])

    return output.getvalue()
