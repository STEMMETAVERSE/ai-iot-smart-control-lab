import streamlit as st
import requests
import os
from huggingface_hub import InferenceClient
# =========================
# CONFIG
# =========================
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)
ARDUINO_IP = "http://192.168.1.50"  # change this to your device IP
st.set_page_config(
    page_title="AI IoT Smart Control Lab",
    layout="centered"
)
st.title("🏠 AI IoT Smart Control Lab (HF Hub Powered)")
st.info(
    "Convert natural language into IoT device commands."
)
# =========================
# VALID COMMANDS
# =========================
VALID_COMMANDS = {
    "LIGHT_ON",
    "LIGHT_OFF",
    "FAN_ON",
    "FAN_OFF",
    "ALARM_ON",
    "ALARM_OFF",
    "PUMP_ON",
    "PUMP_OFF"
}
# =========================
# AI FUNCTION (STANDARD ARCHITECTURE)
# =========================
def get_ai_command(user_text):
    prompt = f"""
You are an IoT command assistant.

Convert the user instruction into ONLY valid commands:
LIGHT_ON
LIGHT_OFF
FAN_ON
FAN_OFF
ALARM_ON
ALARM_OFF
PUMP_ON
PUMP_OFF

RULES:
- Return ONLY commands
- One command per line
- No explanations
- No extra text
Instruction:
{user_text}
"""
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-1B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=120,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
# =========================
# ARDUINO SENDER
# =========================
def send_to_arduino(command):
    try:
        requests.get(f"{ARDUINO_IP}/{command}", timeout=2)
    except:
        st.error("Arduino not reachable")
# =========================
# UI
# =========================
user_input = st.text_input("Enter Smart Home Command")
if st.button("Execute"):
    if not user_input.strip():
        st.warning("Please enter a command")
        st.stop()

    if not HF_TOKEN:
        st.error("HF_TOKEN is missing in environment variables")
        st.stop()
    with st.spinner("AI processing command..."):
        ai_output = get_ai_command(user_input)
    st.subheader("🧠 AI Generated Commands")
    st.code(ai_output)
    commands = ai_output.split("\n")
    st.subheader("📡 Execution Log")
    for cmd in commands:
        cmd = cmd.strip()
        if cmd in VALID_COMMANDS:
            st.write(f"Sending: {cmd}")
            send_to_arduino(cmd)
        elif cmd:
            st.warning(f"Ignored invalid command: {cmd}")
    st.success("Execution completed successfully 🚀")
