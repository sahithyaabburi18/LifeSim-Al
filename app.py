import streamlit as st
import google.generativeai as genai
import os

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="LifeSim AI",
    page_icon="🧠",
    layout="wide"
)

# ---------------- API KEY ----------------
API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------- UI ----------------
st.title("🧠 LifeSim AI")
st.subheader("RAG-Powered Intelligent Real-World Decision Simulation System")

st.write(
    "Describe a real-world decision, and LifeSim AI will "
    "compare possible choices, risks, benefits and outcomes."
)

st.divider()

category = st.selectbox(
    "Select Decision Category",
    [
        "Career",
        "Education",
        "Financial Planning",
        "Purchase Decision"
    ]
)

situation = st.text_area(
    "Describe your situation",
    placeholder=(
        "Example: I have 6 months to prepare for placements. "
        "Should I choose Data Analyst or Software Developer?"
    ),
    height=150
)

# ---------------- SIMULATION ----------------
if st.button("🚀 Simulate Decision"):

    if not situation.strip():
        st.warning("Please describe your situation first.")

    elif not API_KEY:
        st.error(
            "Gemini API key is not configured. "
            "Please set GEMINI_API_KEY in the terminal."
        )

    else:
        try:
            genai.configure(api_key=API_KEY)

            model = genai.GenerativeModel("gemini-2.5-flash")

            prompt = f"""
You are LifeSim AI, an intelligent real-world decision
simulation system.

Decision Category:
{category}

User Situation:
{situation}

Analyze the situation and provide a clear decision simulation.

Give the response in this structure:

1. Situation Analysis
2. Option 1
   - Advantages
   - Disadvantages
   - Skills/Requirements
   - Possible Outcome
3. Option 2
   - Advantages
   - Disadvantages
   - Skills/Requirements
   - Possible Outcome
4. Risk Analysis
5. Comparison Table
6. Recommended Option
7. Why this option is recommended
8. Short-Term Action Plan

Be practical and suitable for a beginner/fresher.
Do not make unrealistic guarantees about salary or success.
"""

            with st.spinner("🤖 AI is simulating your decision..."):

                response = model.generate_content(prompt)

            st.success("✅ Decision simulation completed!")

            st.write("### 📌 Selected Category")
            st.write(category)

            st.write("### 📝 Your Situation")
            st.write(situation)

            st.divider()

            st.write("## 🤖 LifeSim AI Analysis")
            st.markdown(response.text)

        except Exception as e:
            st.error("Something went wrong while generating the simulation.")
            st.code(str(e))
