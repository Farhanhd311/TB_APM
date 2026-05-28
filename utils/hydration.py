"""Hydration calculator based on weight and calories burned."""


def calculate_hydration(weight_kg: float, calories_burned: float) -> dict:
    """Calculate recommended water intake.

    Formula:
      - Base need: ~33 ml per kg body weight
      - Exercise extra: ~500 ml per 500 kcal burned

    Returns dict with total_liters, total_ml, glasses, base_liters, exercise_extra_ml.
    """
    base_ml = weight_kg * 33
    exercise_ml = (calories_burned / 500) * 500 if calories_burned > 0 else 0
    total_ml = base_ml + exercise_ml
    total_liters = round(total_ml / 1000, 1)
    glasses = round(total_ml / 250)  # 250 ml per glass

    return {
        "total_liters": total_liters,
        "total_ml": round(total_ml),
        "glasses": glasses,
        "base_liters": round(base_ml / 1000, 1),
        "exercise_extra_ml": round(exercise_ml),
    }
