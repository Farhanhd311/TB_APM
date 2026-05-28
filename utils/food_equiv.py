"""Food calorie equivalents — mostly Indonesian foods."""

FOOD_DATABASE = [
    {"name_id": "Nasi Putih (1 porsi)",        "name_en": "White Rice (1 serving)",       "calories": 204, "emoji": "🍚"},
    {"name_id": "Nasi Goreng",                  "name_en": "Fried Rice",                   "calories": 450, "emoji": "🍛"},
    {"name_id": "Mie Goreng",                   "name_en": "Fried Noodles",                "calories": 390, "emoji": "🍜"},
    {"name_id": "Indomie Goreng",               "name_en": "Instant Fried Noodles",        "calories": 380, "emoji": "🍜"},
    {"name_id": "Rendang (1 porsi)",            "name_en": "Rendang (1 serving)",          "calories": 340, "emoji": "🥩"},
    {"name_id": "Ayam Goreng (1 potong)",       "name_en": "Fried Chicken (1 piece)",      "calories": 260, "emoji": "🍗"},
    {"name_id": "Sate Ayam (10 tusuk)",         "name_en": "Chicken Satay (10 skewers)",   "calories": 350, "emoji": "🍢"},
    {"name_id": "Bakso (1 mangkuk)",            "name_en": "Meatball Soup (1 bowl)",       "calories": 300, "emoji": "🍲"},
    {"name_id": "Gado-gado",                    "name_en": "Gado-gado Salad",              "calories": 270, "emoji": "🥗"},
    {"name_id": "Martabak Manis (1 potong)",    "name_en": "Sweet Martabak (1 slice)",     "calories": 320, "emoji": "🥞"},
    {"name_id": "Pizza (1 slice)",              "name_en": "Pizza (1 slice)",              "calories": 285, "emoji": "🍕"},
    {"name_id": "Burger",                       "name_en": "Burger",                       "calories": 354, "emoji": "🍔"},
    {"name_id": "Donat",                        "name_en": "Donut",                        "calories": 253, "emoji": "🍩"},
    {"name_id": "Es Krim (1 scoop)",            "name_en": "Ice Cream (1 scoop)",          "calories": 137, "emoji": "🍦"},
    {"name_id": "Coklat (1 bar)",               "name_en": "Chocolate (1 bar)",            "calories": 230, "emoji": "🍫"},
    {"name_id": "Boba Milk Tea",                "name_en": "Boba Milk Tea",                "calories": 400, "emoji": "🧋"},
    {"name_id": "Kopi Susu Gula Aren",          "name_en": "Palm Sugar Latte",             "calories": 250, "emoji": "☕"},
    {"name_id": "Nasi Padang (1 paket)",        "name_en": "Nasi Padang (1 set)",          "calories": 550, "emoji": "🍛"},
]


def get_food_equivalents(calories: float, lang: str = "id") -> list:
    """Return foods closest to the calorie value burned.

    Returns up to 5 items sorted by closest match.
    """
    results = []
    name_key = "name_id" if lang == "id" else "name_en"

    for food in FOOD_DATABASE:
        ratio = calories / food["calories"] if food["calories"] > 0 else 0
        if 0.2 <= ratio <= 4.0:
            results.append({
                "name": food[name_key],
                "emoji": food["emoji"],
                "food_cal": food["calories"],
                "ratio": round(ratio, 2),
                "portions": round(ratio, 1),
            })

    results.sort(key=lambda x: abs(x["ratio"] - 1))
    return results[:5]


def get_burn_time_for_food(food_calories: float, duration_minutes: int,
                           session_calories: float) -> float:
    """Estimate minutes needed to burn off a food item at the same intensity."""
    if session_calories <= 0 or duration_minutes <= 0:
        return 0
    cal_per_min = session_calories / duration_minutes
    return round(food_calories / cal_per_min, 1) if cal_per_min > 0 else 0
