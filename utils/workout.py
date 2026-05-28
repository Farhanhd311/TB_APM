"""Weekly workout program generator based on BMI, target, and fitness level."""


def get_workout_program(bmi: float, target_calories: float,
                        fitness_level: str = "beginner", lang: str = "id") -> list:
    """Generate a 7-day workout program.

    Returns list of dicts with keys: day, exercise, duration, est_cal, tips
    """
    programs = {
        "beginner": {
            "id": [
                {"day": "Senin",   "exercise": "🚶 Jalan Cepat",       "duration": 30, "est_cal": 150, "tips": "Mulai dengan pemanasan 5 menit"},
                {"day": "Selasa",  "exercise": "🧘 Yoga Dasar",        "duration": 30, "est_cal": 120, "tips": "Fokus pada pernapasan"},
                {"day": "Rabu",    "exercise": "🏊 Berenang Santai",   "duration": 25, "est_cal": 180, "tips": "Istirahat setiap 5 lap"},
                {"day": "Kamis",   "exercise": "😴 Istirahat Aktif",   "duration": 20, "est_cal":  60, "tips": "Stretching ringan & jalan santai"},
                {"day": "Jumat",   "exercise": "🚴 Bersepeda Santai",  "duration": 30, "est_cal": 170, "tips": "Jaga kecepatan konstan"},
                {"day": "Sabtu",   "exercise": "🏃 Jogging Ringan",    "duration": 20, "est_cal": 160, "tips": "Jaga heart rate 100-120 bpm"},
                {"day": "Minggu",  "exercise": "😴 Istirahat Total",   "duration":  0, "est_cal":   0, "tips": "Recovery & hidrasi cukup"},
            ],
            "en": [
                {"day": "Monday",    "exercise": "🚶 Brisk Walking",    "duration": 30, "est_cal": 150, "tips": "Start with 5-min warm-up"},
                {"day": "Tuesday",   "exercise": "🧘 Basic Yoga",       "duration": 30, "est_cal": 120, "tips": "Focus on breathing"},
                {"day": "Wednesday", "exercise": "🏊 Casual Swimming",  "duration": 25, "est_cal": 180, "tips": "Rest every 5 laps"},
                {"day": "Thursday",  "exercise": "😴 Active Rest",      "duration": 20, "est_cal":  60, "tips": "Light stretching & walking"},
                {"day": "Friday",    "exercise": "🚴 Casual Cycling",   "duration": 30, "est_cal": 170, "tips": "Keep constant speed"},
                {"day": "Saturday",  "exercise": "🏃 Light Jogging",    "duration": 20, "est_cal": 160, "tips": "Keep HR 100-120 bpm"},
                {"day": "Sunday",    "exercise": "😴 Full Rest",        "duration":  0, "est_cal":   0, "tips": "Recovery & hydration"},
            ],
        },
        "intermediate": {
            "id": [
                {"day": "Senin",   "exercise": "🏃 Lari Interval",       "duration": 35, "est_cal": 300, "tips": "Sprint 1 menit, jog 2 menit"},
                {"day": "Selasa",  "exercise": "💪 Bodyweight Training",  "duration": 40, "est_cal": 280, "tips": "Push-up, squat, plank, lunges"},
                {"day": "Rabu",    "exercise": "🏊 Berenang Aktif",      "duration": 35, "est_cal": 320, "tips": "Variasi gaya setiap 10 menit"},
                {"day": "Kamis",   "exercise": "🧘 Power Yoga",          "duration": 45, "est_cal": 200, "tips": "Fokus kekuatan & fleksibilitas"},
                {"day": "Jumat",   "exercise": "🚴 Bersepeda Cepat",     "duration": 40, "est_cal": 350, "tips": "Tanjakan untuk challenge ekstra"},
                {"day": "Sabtu",   "exercise": "⚽ Olahraga Tim",        "duration": 60, "est_cal": 400, "tips": "Futsal, basket, atau badminton"},
                {"day": "Minggu",  "exercise": "😴 Istirahat Aktif",     "duration": 20, "est_cal":  80, "tips": "Stretching & foam rolling"},
            ],
            "en": [
                {"day": "Monday",    "exercise": "🏃 Interval Running",    "duration": 35, "est_cal": 300, "tips": "Sprint 1 min, jog 2 min"},
                {"day": "Tuesday",   "exercise": "💪 Bodyweight Training",  "duration": 40, "est_cal": 280, "tips": "Push-ups, squats, planks, lunges"},
                {"day": "Wednesday", "exercise": "🏊 Active Swimming",     "duration": 35, "est_cal": 320, "tips": "Vary styles every 10 min"},
                {"day": "Thursday",  "exercise": "🧘 Power Yoga",          "duration": 45, "est_cal": 200, "tips": "Focus on strength & flexibility"},
                {"day": "Friday",    "exercise": "🚴 Fast Cycling",        "duration": 40, "est_cal": 350, "tips": "Add hills for extra challenge"},
                {"day": "Saturday",  "exercise": "⚽ Team Sports",         "duration": 60, "est_cal": 400, "tips": "Futsal, basketball, badminton"},
                {"day": "Sunday",    "exercise": "😴 Active Rest",         "duration": 20, "est_cal":  80, "tips": "Stretching & foam rolling"},
            ],
        },
        "advanced": {
            "id": [
                {"day": "Senin",   "exercise": "🔥 HIIT Training",       "duration": 45, "est_cal": 500, "tips": "Burpee, box jump, mountain climber"},
                {"day": "Selasa",  "exercise": "🏋️ Weight Training",     "duration": 60, "est_cal": 400, "tips": "Deadlift, squat, bench press"},
                {"day": "Rabu",    "exercise": "🏃 Lari Jarak Jauh",     "duration": 50, "est_cal": 550, "tips": "Pace 5:30-6:00 /km"},
                {"day": "Kamis",   "exercise": "💪 Calisthenics",        "duration": 50, "est_cal": 380, "tips": "Pull-up, muscle-up, handstand"},
                {"day": "Jumat",   "exercise": "🥊 Boxing / Muay Thai",  "duration": 60, "est_cal": 600, "tips": "Kombinasi pukulan & tendangan"},
                {"day": "Sabtu",   "exercise": "🚴 Cycling Endurance",   "duration": 90, "est_cal": 700, "tips": "Long ride, variasi intensitas"},
                {"day": "Minggu",  "exercise": "🧘 Recovery Yoga",       "duration": 30, "est_cal": 100, "tips": "Yin yoga untuk pemulihan total"},
            ],
            "en": [
                {"day": "Monday",    "exercise": "🔥 HIIT Training",       "duration": 45, "est_cal": 500, "tips": "Burpees, box jumps, mountain climbers"},
                {"day": "Tuesday",   "exercise": "🏋️ Weight Training",     "duration": 60, "est_cal": 400, "tips": "Deadlift, squat, bench press"},
                {"day": "Wednesday", "exercise": "🏃 Long Distance Run",   "duration": 50, "est_cal": 550, "tips": "Pace 5:30-6:00 /km"},
                {"day": "Thursday",  "exercise": "💪 Calisthenics",        "duration": 50, "est_cal": 380, "tips": "Pull-ups, muscle-ups, handstands"},
                {"day": "Friday",    "exercise": "🥊 Boxing / Muay Thai",  "duration": 60, "est_cal": 600, "tips": "Punch & kick combinations"},
                {"day": "Saturday",  "exercise": "🚴 Cycling Endurance",   "duration": 90, "est_cal": 700, "tips": "Long ride, intensity variations"},
                {"day": "Sunday",    "exercise": "🧘 Recovery Yoga",       "duration": 30, "est_cal": 100, "tips": "Yin yoga for full recovery"},
            ],
        },
    }

    level = fitness_level.lower()
    if level not in programs:
        level = "beginner"

    program = [d.copy() for d in programs[level].get(lang, programs[level]["id"])]

    # Adjust estimated calories based on BMI
    if bmi > 30:
        factor = 1.15
    elif bmi > 25:
        factor = 1.08
    elif bmi < 18.5:
        factor = 0.85
    else:
        factor = 1.0

    for day in program:
        day["est_cal"] = round(day["est_cal"] * factor)

    return program


def get_nutrition_tips(fitness_level: str, lang: str = "id") -> list:
    """Return nutrition tips matching the fitness level."""
    tips = {
        "beginner": {
            "id": [
                "🥤 Minum minimal 2 liter air putih per hari",
                "🍎 Konsumsi buah & sayur setiap hari (5 porsi)",
                "🍗 Protein cukup: telur, ayam, ikan, tahu/tempe",
                "🚫 Kurangi makanan olahan dan fast food",
                "⏰ Makan teratur 3× sehari + snack sehat",
            ],
            "en": [
                "🥤 Drink at least 2 liters of water daily",
                "🍎 Eat fruits & vegetables daily (5 servings)",
                "🍗 Adequate protein: eggs, chicken, fish, tofu",
                "🚫 Reduce processed and fast food",
                "⏰ Eat regularly 3× daily + healthy snacks",
            ],
        },
        "intermediate": {
            "id": [
                "🥩 Tingkatkan protein (1.5-2 g per kg BB)",
                "🍚 Karbohidrat kompleks: nasi merah, oat, ubi",
                "🥑 Lemak sehat: alpukat, kacang, olive oil",
                "🕐 Makan 1-2 jam sebelum olahraga",
                "🍌 Post-workout: protein + buah dalam 30 menit",
                "🥤 Pre-workout: pisang + kopi hitam",
            ],
            "en": [
                "🥩 Increase protein (1.5-2 g per kg BW)",
                "🍚 Complex carbs: brown rice, oats, sweet potato",
                "🥑 Healthy fats: avocado, nuts, olive oil",
                "🕐 Eat 1-2 hours before exercise",
                "🍌 Post-workout: protein + fruit within 30 min",
                "🥤 Pre-workout: banana + black coffee",
            ],
        },
        "advanced": {
            "id": [
                "🥩 Protein tinggi: 2-2.5 g per kg BB per hari",
                "📊 Track makro: 40% karbo, 30% protein, 30% lemak",
                "🔄 Carb cycling: tinggi di hari latihan berat",
                "💊 Suplemen: creatine, BCAA, multivitamin",
                "🍌 Intra-workout: BCAA atau air kelapa",
                "🥤 Post-workout: 40 g whey + 60 g dextrose",
                "😴 Tidur 7-9 jam untuk pemulihan optimal",
            ],
            "en": [
                "🥩 High protein: 2-2.5 g per kg BW daily",
                "📊 Track macros: 40% carb, 30% protein, 30% fat",
                "🔄 Carb cycling: high on heavy training days",
                "💊 Supplements: creatine, BCAA, multivitamin",
                "🍌 Intra-workout: BCAA or coconut water",
                "🥤 Post-workout: 40 g whey + 60 g dextrose",
                "😴 Sleep 7-9 hours for optimal recovery",
            ],
        },
    }

    level = fitness_level.lower()
    if level not in tips:
        level = "beginner"
    return tips[level].get(lang, tips[level]["id"])
