import streamlit as st

def render_summary(bullets):
    for b in bullets:
        st.markdown(f"- {b}")

def render_action_items(items):
    if not items:
        st.write("No action items.")
        return
    for item in items:
        st.write(f"**Task:** {item.get('task')}")
        st.write(f"Assigned to: {item.get('assigned_to') or 'Unassigned'}")
        st.write(f"Deadline: {item.get('deadline') or 'None'}")
        st.markdown("---")

def render_timeline(timeline):
    if not timeline:
        st.write("No timeline items.")
        return
    for t in timeline:
        st.write(f"{t.get('timestamp')} — {t.get('topic')}")

def render_sentiment(sentiment_map):
    cols = st.columns(len(sentiment_map) or 1)
    i = 0
    for speaker, sentiment in sentiment_map.items():
        with cols[i % max(1, len(cols))]:
            if sentiment == "positive":
                st.success(f"{speaker}: {sentiment}")
            elif sentiment == "negative":
                st.error(f"{speaker}: {sentiment}")
            else:
                st.info(f"{speaker}: {sentiment}")
        i += 1
