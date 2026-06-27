# logic.py — AQI categories, health logic, intent detection


# ── AQI category lookup ──────────────────────────────────────────────────────

def get_aqi_info(aqi):
    if aqi <= 50:
        return {
            "category": "Good",
            "color": "green",
            "recommendation": "Safe for all activities outdoors."
        }
    elif aqi <= 100:
        return {
            "category": "Moderate",
            "color": "yellow",
            "recommendation": "Safe for most people. Sensitive groups should use caution."
        }
    elif aqi <= 150:
        return {
            "category": "Unhealthy for Sensitive Groups",
            "color": "orange",
            "recommendation": "Avoid intense outdoor exercise. Kids should limit outdoor time."
        }
    elif aqi <= 200:
        return {
            "category": "Unhealthy",
            "color": "red",
            "recommendation": "Stay indoors if possible. Wear a mask outdoors."
        }
    elif aqi <= 300:
        return {
            "category": "Very Unhealthy",
            "color": "purple",
            "recommendation": "Avoid all outdoor activity. Stay indoors."
        }
    else:
        return {
            "category": "Hazardous",
            "color": "maroon",
            "recommendation": "Emergency conditions. Stay indoors with windows closed."
        }


# ── PM2.5 category lookup ────────────────────────────────────────────────────

def get_pm25_info(pm25):
    if pm25 <= 12.0:
        return "Good — clean air, safe for everyone including sensitive groups."
    elif pm25 <= 35.4:
        return "Moderate — acceptable air quality. Sensitive groups should limit prolonged outdoor exertion."
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups — people with asthma or allergies should reduce outdoor time."
    elif pm25 <= 150.4:
        return "Unhealthy — everyone may feel effects. Avoid strenuous outdoor activity."
    elif pm25 <= 250.4:
        return "Very Unhealthy — significant health risk. Stay indoors and wear a mask if going out."
    else:
        return "Hazardous — dangerous air quality. Stay indoors with windows closed."


# ── Health-specific advice ───────────────────────────────────────────────────

def get_health_advice(aqi, pm25, condition):
    if condition == "asthma":
        if aqi <= 50:
            return "safe"
        elif aqi <= 100:
            return "use caution — keep your inhaler handy"
        elif aqi <= 150:
            return "risky — PM2.5 particles irritate airways and can trigger flare-ups"
        else:
            return "unsafe — stay indoors"

    elif condition == "allergies":
        if aqi <= 50:
            return "safe — low pollution today"
        elif aqi <= 100:
            return "mild concern — pollution can worsen allergy symptoms"
        elif aqi <= 150:
            return "risky — pollutants bind to pollen and intensify reactions"
        else:
            return "unsafe — stay indoors and keep windows closed"

    else:
        if aqi <= 100:
            return "safe for most people"
        elif aqi <= 150:
            return "use caution if you have any respiratory sensitivities"
        else:
            return "limit outdoor exposure"


# ── Activity-specific advice ─────────────────────────────────────────────────

def get_activity_advice(aqi, activity_type):
    if activity_type == "running":
        if aqi <= 50:
            return "great day for a run — no restrictions"
        elif aqi <= 100:
            return "short runs are fine — skip long or intense workouts"
        elif aqi <= 150:
            return "not recommended — consider moving your workout indoors"
        else:
            return "do not run outdoors today"

    elif activity_type == "kids":
        if aqi <= 50:
            return "great day — kids can play outside freely"
        elif aqi <= 100:
            return "outdoor play is fine — watch for symptoms in kids with asthma"
        elif aqi <= 150:
            return "limit outdoor play to short periods"
        else:
            return "keep kids indoors today"

    elif activity_type == "visibility":
        if aqi <= 50:
            return "excellent — great conditions for sky watching"
        elif aqi <= 100:
            return "decent — some haze possible"
        elif aqi <= 150:
            return "poor — noticeable haze will obscure the sky"
        else:
            return "very poor — heavy haze will block most sky views"

    else:
        if aqi <= 100:
            return "safe for outdoor activities"
        elif aqi <= 150:
            return "moderate outdoor activity is okay — avoid intense exertion"
        else:
            return "limit time outdoors"


# ── Intent detection ─────────────────────────────────────────────────────────

def detect_intent(message):
    msg = message.lower()

    asthma_words = ["asthma", "inhaler", "copd", "breathing issue",
                    "shortness of breath", "wheez", "bronch"]
    if any(w in msg for w in asthma_words):
        return "health_asthma"

    allergy_words = ["allerg", "hay fever", "pollen", "sinus",
                     "sneez", "itchy eyes", "runny nose"]
    if any(w in msg for w in allergy_words):
        return "health_allergy"

    health_words = ["cough", "sick", "sensitive", "lung", "respiratory",
                    "health", "safe to go out", "stay indoors"]
    if any(w in msg for w in health_words):
        return "health_general"

    running_words = ["run", "jog", "sprint", "marathon", "workout",
                     "exercise", "cycling", "bike"]
    if any(w in msg for w in running_words):
        return "activity_running"

    kids_words = ["kid", "child", "children", "baby", "toddler",
                  "school", "playground", "play outside"]
    if any(w in msg for w in kids_words):
        return "activity_kids"

    visibility_words = ["sunset", "sunrise", "meteor", "star", "firework",
                        "sky", "visibility", "see tonight", "view"]
    if any(w in msg for w in visibility_words):
        return "visibility"

    return "general"


# ── Air data (mock — swap for real API later) ────────────────────────────────

def get_air_data(location="Brooklyn, NY"):
    mock_data = {
        "Brooklyn, NY":    {"aqi": 72,  "pm25": 18.2, "best_time": "6–9 AM"},
        "Los Angeles, CA": {"aqi": 148, "pm25": 51.0, "best_time": "5–8 AM"},
        "Denver, CO":      {"aqi": 38,  "pm25": 8.1,  "best_time": "anytime"},
        "Phoenix, AZ":     {"aqi": 162, "pm25": 62.3, "best_time": "5–7 AM"},
        "Seattle, WA":     {"aqi": 22,  "pm25": 4.5,  "best_time": "anytime"},
    }

    data = mock_data.get(location, {"aqi": 75, "pm25": 20.0, "best_time": "morning"})
    data["location"] = location
    data["aqi_info"] = get_aqi_info(data["aqi"])
    data["pm25_desc"] = get_pm25_info(data["pm25"])
    return data