import pandas as pd
import io
from menu_data import MENU_DATA, UPSELLS


def calculate_summary(selections, guest_count, menu_data, upsells):
    breakdown = {}
    total_dishes = 0
    estimated_cost = 0

    for category, items in menu_data.items():
        chosen = selections.get(category, [])
        breakdown[category] = chosen
        total_dishes += len(chosen)
        for dish_name in chosen:
            dish = next((d for d in items["dishes"] if d["name"] == dish_name), None)
            if dish and "price_per_person" in dish:
                estimated_cost += dish["price_per_person"] * guest_count

    # Add upsells cost
    chosen_upsells = selections.get("_upsells", [])
    for upsell_name in chosen_upsells:
        upsell = next((u for u in upsells if u["name"] == upsell_name), None)
        if upsell and "price" in upsell:
            estimated_cost += upsell["price"]

    return {
        "breakdown": breakdown,
        "total_dishes": total_dishes,
        "estimated_cost": estimated_cost,
    }


def export_to_csv(selections, dietary_notes, guest_count, couple_name, menu_data, upsells):
    rows = []
    for category, dishes in selections.items():
        if category == "_upsells":
            continue
        for dish_name in dishes:
            items = menu_data.get(category, {})
            dish = next((d for d in items.get("dishes", []) if d["name"] == dish_name), None)
            rows.append({
                "Para": couple_name,
                "Kategoria": category,
                "Danie": dish_name,
                "Porcje": guest_count,
                "Cena/os (zł)": dish.get("price_per_person", "-") if dish else "-",
                "Suma (zł)": dish.get("price_per_person", 0) * guest_count if dish else "-",
                "Alergeny": ", ".join(dish.get("allergens", [])) if dish else "",
            })

    for upsell_name in selections.get("_upsells", []):
        upsell = next((u for u in upsells if u["name"] == upsell_name), None)
        rows.append({
            "Para": couple_name,
            "Kategoria": "Dodatek Premium",
            "Danie": upsell_name,
            "Porcje": "-",
            "Cena/os (zł)": "-",
            "Suma (zł)": upsell.get("price", "-") if upsell else "-",
            "Alergeny": "",
        })

    rows.append({
        "Para": couple_name,
        "Kategoria": "DIETY",
        "Danie": (
            f"Wegetarianie: {dietary_notes.get('vegetarian', 0)}, "
            f"Weganie: {dietary_notes.get('vegan', 0)}, "
            f"Bezglutenowi: {dietary_notes.get('gluten_free', 0)}"
        ),
        "Porcje": "",
        "Cena/os (zł)": "",
        "Suma (zł)": "",
        "Alergeny": dietary_notes.get("other", ""),
    })

    df = pd.DataFrame(rows)
    output = io.StringIO()
    df.to_csv(output, index=False, encoding="utf-8-sig")
    return output.getvalue()
