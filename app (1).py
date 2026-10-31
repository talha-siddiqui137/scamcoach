import streamlit as st
from scam_engine import analyze, QUIZ, RULES_OF_THUMB

st.set_page_config(page_title="ScamCoach", page_icon="🛡️", layout="centered")
st.markdown("""<style>
html, body, [class*="css"] {font-size: 20px;}
.stButton>button {font-size: 22px; padding: 0.6em 1.4em; border-radius: 12px;}
textarea {font-size: 20px !important;}
</style>""", unsafe_allow_html=True)

st.title("🛡️ ScamCoach")
st.write("Learn to spot fake messages. Practice here. Nothing here can hurt you.")

tab1, tab2, tab3 = st.tabs(["🔍 Check a message", "🎯 Practice", "📌 5 Simple Rules"])

with tab1:
    st.subheader("Got a message that feels strange?")
    st.write("Copy it and paste it below. I will show you what looks wrong, and why.")
    msg = st.text_area("Paste the message here", height=150)
    if st.button("Check it", type="primary"):
        if not msg.strip():
            st.info("Please paste a message first.")
        else:
            level, found = analyze(msg)
            if level == "danger":
                st.error("🚨 DANGER. This looks like a scam. Do not reply or click.")
            elif level == "careful":
                st.warning("⚠️ BE CAREFUL. It has warning signs. Check with someone you trust.")
            else:
                st.success("✅ No clear warning signs. If you are still unsure, ask your family.")
            for f in found:
                with st.container(border=True):
                    st.markdown(f"**❗ {f['name']}**")
                    st.write(f"Why this matters: {f['why']}")
                    st.write(f"What to do: {f['todo']}")
            if found:
                st.caption("Tip: show this screen to your son or daughter.")

with tab2:
    st.subheader("Is this message real or a scam?")
    s = st.session_state
    s.setdefault("i", 0); s.setdefault("score", 0); s.setdefault("answered", None)
    if s.i >= len(QUIZ):
        st.balloons()
        st.success(f"Well done! You got {s.score} out of {len(QUIZ)} right.")
        if st.button("Play again"):
            s.i, s.score, s.answered = 0, 0, None
            st.rerun()
    else:
        text, is_scam, why = QUIZ[s.i]
        st.progress(s.i / len(QUIZ), text=f"Question {s.i + 1} of {len(QUIZ)}")
        st.info(text)
        if s.answered is None:
            c1, c2 = st.columns(2)
            if c1.button("🚨 It is a SCAM", use_container_width=True):
                s.answered = True
                s.score += int(is_scam); st.rerun()
            if c2.button("✅ It is REAL", use_container_width=True):
                s.answered = False
                s.score += int(not is_scam); st.rerun()
        else:
            right = (s.answered == is_scam)
            (st.success if right else st.error)("Correct! 👏" if right else "Not quite. That is okay, this is practice.")
            st.write(f"**Answer:** {'Scam' if is_scam else 'Real'}. {why}")
            if st.button("Next ➡️"):
                s.i += 1; s.answered = None; st.rerun()

with tab3:
    st.subheader("Remember these 5 things")
    for r in RULES_OF_THUMB:
        st.markdown(f"### {r}")
