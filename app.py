import os
import streamlit as st
from groq import Groq

# Configure Groq API key
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("AgriDiagnoX - Crop Fertilizer Recommendation")

# Inputs
crop_name = st.text_input("Enter the name of the crop:", "")

moisture = st.number_input(
    "Moisture Level (%)",
    min_value=0,
    max_value=100,
    value=55
)

ph_level = st.number_input(
    "pH Level",
    min_value=0.0,
    max_value=14.0,
    value=6.8
)

temperature = st.number_input(
    "Temperature (°C)",
    min_value=-30.0,
    max_value=50.0,
    value=22.5
)

# Button
if st.button("Get Fertilizer Recommendation"):

    if crop_name:
        user_input = f"""
Crop: {crop_name}
Moisture: {moisture}%
pH: {ph_level}
Temperature: {temperature}°C
"""
    else:
        user_input = f"""
Moisture: {moisture}%
pH: {ph_level}
Temperature: {temperature}°C
"""

    system_prompt = """
You are an agriculture expert.

Recommend fertilizers based on:
- crop name
- soil moisture
- pH level
- temperature

If crop name missing ask for it.

Provide:
- fertilizer name
- quantity
- application method
- reason
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.6,
        max_completion_tokens=1024,
        top_p=0.95
    )

    response = completion.choices[0].message.content

    st.markdown("### Recommendation:")
    st.write(response)
