"""Badge / achievement system for CaloriQ gamification."""

BADGE_DEFINITIONS = [
    {
        "id": "first_burn", "emoji": "🔥",
        "name_id": "First Burn", "name_en": "First Burn",
        "desc_id": "Lakukan prediksi pertama Anda",
        "desc_en": "Make your first prediction",
        "category": "milestone",
    },
    {
        "id": "century", "emoji": "💯",
        "name_id": "Century", "name_en": "Century",
        "desc_id": "Akumulasi total 100 kcal terbakar",
        "desc_en": "Accumulate 100 kcal burned total",
        "category": "calorie",
    },
    {
        "id": "half_k", "emoji": "🏅",
        "name_id": "Half K", "name_en": "Half K",
        "desc_id": "Bakar 500 kcal dalam satu sesi",
        "desc_en": "Burn 500 kcal in a single session",
        "category": "calorie",
    },
    {
        "id": "bullseye", "emoji": "🎯",
        "name_id": "Bullseye", "name_en": "Bullseye",
        "desc_id": "Capai target kalori harian",
        "desc_en": "Achieve daily calorie target",
        "category": "target",
    },
    {
        "id": "streak_3", "emoji": "📅",
        "name_id": "Streak 3", "name_en": "Streak 3",
        "desc_id": "Olahraga 3 hari berturut-turut",
        "desc_en": "Exercise 3 consecutive days",
        "category": "streak",
    },
    {
        "id": "streak_7", "emoji": "🔥",
        "name_id": "Streak 7", "name_en": "Streak 7",
        "desc_id": "Olahraga 7 hari berturut-turut",
        "desc_en": "Exercise 7 consecutive days",
        "category": "streak",
    },
    {
        "id": "ten_sessions", "emoji": "🔟",
        "name_id": "Ten Sessions", "name_en": "Ten Sessions",
        "desc_id": "Lakukan 10 kali prediksi",
        "desc_en": "Make 10 predictions",
        "category": "milestone",
    },
    {
        "id": "fifty_sessions", "emoji": "💪",
        "name_id": "Fifty Sessions", "name_en": "Fifty Sessions",
        "desc_id": "Lakukan 50 kali prediksi",
        "desc_en": "Make 50 predictions",
        "category": "milestone",
    },
    {
        "id": "heat_wave", "emoji": "🌡️",
        "name_id": "Heat Wave", "name_en": "Heat Wave",
        "desc_id": "Suhu tubuh > 40°C saat olahraga",
        "desc_en": "Body temperature above 40°C during exercise",
        "category": "extreme",
    },
    {
        "id": "heart_racer", "emoji": "💓",
        "name_id": "Heart Racer", "name_en": "Heart Racer",
        "desc_id": "Heart rate lebih dari 150 bpm",
        "desc_en": "Heart rate above 150 bpm",
        "category": "extreme",
    },
]


def get_badge_def(badge_id: str) -> dict | None:
    """Return badge definition by ID."""
    for b in BADGE_DEFINITIONS:
        if b["id"] == badge_id:
            return b
    return None


def get_all_badges() -> list:
    """Return all badge definitions."""
    return BADGE_DEFINITIONS


def check_badges(prediction_data: dict, db) -> list:
    """Check which new badges should be unlocked after a prediction.

    Args:
        prediction_data: dict with keys like calories, heart_rate, body_temp
        db: the database module (utils.database)

    Returns:
        List of newly earned badge definition dicts.
    """
    earned = {b['badge_id'] for b in db.get_earned_badges()}
    newly = []

    def _award(bid):
        d = get_badge_def(bid)
        if d:
            db.save_badge(bid)
            newly.append(d)

    if "first_burn" not in earned:
        _award("first_burn")

    if "century" not in earned and db.get_total_calories() >= 100:
        _award("century")

    if "half_k" not in earned and prediction_data.get('calories', 0) >= 500:
        _award("half_k")

    if "bullseye" not in earned:
        target = db.get_target()
        if target and db.get_today_total_calories() >= target:
            _award("bullseye")

    streak = db.get_streak()
    if "streak_3" not in earned and streak >= 3:
        _award("streak_3")
    if "streak_7" not in earned and streak >= 7:
        _award("streak_7")

    count = db.get_prediction_count()
    if "ten_sessions" not in earned and count >= 10:
        _award("ten_sessions")
    if "fifty_sessions" not in earned and count >= 50:
        _award("fifty_sessions")

    if "heat_wave" not in earned and prediction_data.get('body_temp', 0) > 40:
        _award("heat_wave")
    if "heart_racer" not in earned and prediction_data.get('heart_rate', 0) > 150:
        _award("heart_racer")

    return newly


def get_badge_progress(db) -> list:
    """Return all badges with progress info for display."""
    earned_map = {b['badge_id']: b['earned_at'] for b in db.get_earned_badges()}
    total_cal = db.get_total_calories()
    max_cal = db.get_max_calories_single()
    count = db.get_prediction_count()
    streak = db.get_streak()

    results = []
    for badge in BADGE_DEFINITIONS:
        bid = badge["id"]
        is_earned = bid in earned_map
        earned_at = earned_map.get(bid)

        progress = 1.0 if is_earned else 0.0
        progress_text = ""

        if not is_earned:
            if bid == "first_burn":
                progress = min(count / 1, 1.0) if count else 0
                progress_text = f"{count}/1"
            elif bid == "century":
                progress = min(total_cal / 100, 1.0)
                progress_text = f"{total_cal:.0f}/100 kcal"
            elif bid == "half_k":
                progress = min(max_cal / 500, 1.0)
                progress_text = f"{max_cal:.0f}/500 kcal"
            elif bid == "bullseye":
                progress_text = "Capai target harian"
            elif bid == "streak_3":
                progress = min(streak / 3, 1.0)
                progress_text = f"{streak}/3 hari"
            elif bid == "streak_7":
                progress = min(streak / 7, 1.0)
                progress_text = f"{streak}/7 hari"
            elif bid == "ten_sessions":
                progress = min(count / 10, 1.0)
                progress_text = f"{count}/10"
            elif bid == "fifty_sessions":
                progress = min(count / 50, 1.0)
                progress_text = f"{count}/50"
            elif bid == "heat_wave":
                progress_text = "> 40°C"
            elif bid == "heart_racer":
                progress_text = "> 150 bpm"

        results.append({
            **badge,
            "is_earned": is_earned,
            "earned_at": earned_at,
            "progress": progress,
            "progress_text": progress_text,
        })

    return results
