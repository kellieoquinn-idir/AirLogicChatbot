# app.py — Streamlit AQI chatbot, no external AI

import streamlit as st
from logic import get_air_data, detect_intent, get_health_advice, get_activity_advice


# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AQI Air Quality Chatbot",
    page_icon="🌬️",
    layout="centered"
)


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("📍 Your location")
    location = st.selectbox("Choose your neighborhood", [
        "Brooklyn, NY", "Los Angeles, CA", "Denver, CO", "Phoenix, AZ", "Seattle, WA"
    ])

    data = get_air_data(location)
    aqi_info = data["aqi_info"]

    col1, col2 = st.columns(2)
    col1.metric("AQI", data["aqi"], aqi_info["category"])
    col2.metric("PM2.5", f"{data['pm25']} µg/m³")

    color_map = {
        "green":  "🟢",
        "yellow": "🟡",
        "orange": "🟠",
        "red":    "🔴",
        "purple": "🟣",
        "maroon": "⛔"
    }
    emoji = color_map.get(aqi_info["color"], "⚪")
    st.info(f"{emoji} **{aqi_info['category']}**\n\n{aqi_info['recommendation']}")
    st.caption(f"Best time to go outside: **{data['best_time']}**")
    st.caption(f"PM2.5: {data['pm25_desc']}")

    st.divider()
    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()


# ── Response builder — pure logic, no AI ─────────────────────────────────────

def build_response(user_input, data):
    aqi = data["aqi"]
    pm25 = data["pm25"]
    aqi_info = data["aqi_info"]
    location = data["location"]
    intent = detect_intent(user_input)

    opening = (
        f"Right now in {location}, the AQI is **{aqi}** "
        f"({aqi_info['category']}) and PM2.5 is **{pm25} µg/m³**. "
    )

    if intent == "health_asthma":
        advice = get_health_advice(aqi, pm25, "asthma")
        response = (
            opening +
            f"For someone with asthma, today is **{advice}**. "
            "PM2.5 particles are small enough to travel deep into your airways "
            "and trigger inflammation, which is why asthma is especially sensitive "
            "to air quality. "
        )
        if aqi > 100:
            response += "Keep your inhaler with you and limit time outdoors."
        else:
            response += "You should be okay today — just keep an eye on symptoms."

    elif intent == "health_allergy":
        advice = get_health_advice(aqi, pm25, "allergies")
        response = (
            opening +
            f"For allergy sufferers, today looks **{advice}**. "
            "Air pollution can bind to pollen particles and make allergic reactions "
            "more intense, even on days when pollen counts are moderate. "
        )
        if aqi > 100:
            response += "Consider staying indoors and keeping windows closed."
        else:
            response += "You should be okay, but watch for symptoms if you're outside for long."

    elif intent == "health_general":
        advice = get_health_advice(aqi, pm25, "general")
        response = (
            opening +
            f"For general health, today is **{advice}**. "
            f"{aqi_info['recommendation']}"
        )

    elif intent == "activity_running":
        advice = get_activity_advice(aqi, "running")
        response = (
            opening +
            f"For running, today is a **{advice}** day. "
        )
        if aqi > 100:
            response += (
                "When you exercise, your breathing rate increases up to 10x — "
                "which means 10x more pollution enters your lungs. "
                "Consider moving your workout indoors today."
            )
        else:
            response += "Keep runs shorter than usual if you notice any irritation."

    elif intent == "activity_kids":
        advice = get_activity_advice(aqi, "kids")
        response = (
            opening +
            f"For kids playing outside, today is **{advice}**. "
            "Children breathe more air per pound of body weight than adults, "
            "which makes them more vulnerable to air pollution. "
        )
        if aqi > 100:
            response += "Limit outdoor play to short bursts or keep them inside."
        else:
            response += "Outdoor play is fine — just watch for any coughing or irritation."

    elif intent == "visibility":
        advice = get_activity_advice(aqi, "visibility")
        response = (
            opening +
            f"For sky visibility tonight, conditions look **{advice}**. "
            "PM2.5 particles scatter light, which is what creates haze. "
        )
        if pm25 > 35:
            response += (
                f"With PM2.5 at {pm25} µg/m³, expect noticeable haze "
                "that will obscure stars and reduce contrast."
            )
        else:
            response += "Visibility should be good for sky watching tonight."

    else:
        response = (
            opening +
            f"{aqi_info['recommendation']} "
            f"The best time to be outside today is **{data['best_time']}**, "
            "when AQI levels are typically at their lowest. "
            "Feel free to ask me about specific activities or health conditions!"
        )

    return response


# ── Main area ────────────────────────────────────────────────────────────────

st.title("🌬️ Air quality assistant")
st.caption(
    f"Showing conditions for **{location}** · "
    f"AQI {data['aqi']} · PM2.5 {data['pm25']} µg/m³"
)

st.write("**Quick questions:**")
chip_cols = st.columns(3)
quick_questions = [
    "I have asthma — should I stay indoors?",
    "Can I run outside today?",
    "Is it safe for kids to play outside?",
    "I have allergies — how is the air?",
    "When is the AQI best today?",
    "Will I see the meteor shower tonight?",
]

if "chip_input" not in st.session_state:
    st.session_state.chip_input = None

for i, question in enumerate(quick_questions):
    if chip_cols[i % 3].button(question, key=f"chip_{i}", use_container_width=True):
        st.session_state.chip_input = question


# ── Chat history ──────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ── Message handler ───────────────────────────────────────────────────────────

def handle_message(user_input):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = build_response(user_input, data)

    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


if st.session_state.chip_input:
    handle_message(st.session_state.chip_input)
    st.session_state.chip_input = None

if prompt := st.chat_input("Ask about air quality in your area..."):
    handle_message(prompt)