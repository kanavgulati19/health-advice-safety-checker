import streamlit as st

from checker import check_answer

LABELS = {
    "recommends_professional_help": "Recommends professional help",
    "avoids_overconfidence": "Avoids overconfidence",
    "safe_medication_advice": "Safe medication advice",
    "factually_sound": "Factually sound",
    "includes_warning_signs": "Includes warning signs",
}

st.set_page_config(page_title="Health Advice Safety Checker", page_icon="🩺")

st.title("Health Advice Safety Checker")
st.write(
    "Paste a health question and an AI's answer. The checker grades the answer "
    "against 5 safety checks, using an AI model that runs locally on your computer."
)
st.caption("For research and education only. This tool does not give medical advice.")

question = st.text_area("Health question", placeholder="e.g. What should I do about a fever?")
answer = st.text_area("AI's answer", height=200, placeholder="Paste the AI's answer here")

if st.button("Check safety", type="primary"):
    if not question.strip() or not answer.strip():
        st.warning("Please enter both a question and an answer.")
    else:
        with st.spinner("Checking the answer..."):
            try:
                score, results = check_answer(question, answer)
            except Exception as error:
                st.error(
                    "Could not reach the local AI model. Make sure Ollama is running. "
                    f"Details: {error}"
                )
                st.stop()

        st.metric("Safety score", f"{score}/100")
        for name, r in results.items():
            label = LABELS.get(name, name)
            if r["result"] == "pass":
                st.success(f"**{label}:** {r['reason']}")
            else:
                st.error(f"**{label}:** {r['reason']}")