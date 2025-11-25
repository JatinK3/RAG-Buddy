import streamlit as st
import requests
import time

API_BASE = "http://localhost:8000"
RAG_URL = f"{API_BASE}/rag"
TOPIC_URL = f"{API_BASE}/topics"
INGEST_URL = f"{API_BASE}/ingest"
st.set_page_config(page_title="RAG-Buddy", page_icon="🤖", layout="wide")

st.title("RAG-Buddy")
st.write("Ask questions over your own documents (PDF-based RAG).")


@st.cache_data
def get_topics():
    try:
        r = requests.get(TOPIC_URL)
        if r.status_code == 200:
            return ["all"] + r.json().get("topics", [])
    except Exception as e:
        print("Error fetching topics:", e)
    return ["all"]


# ─── Sidebar: Upload & Ingest PDF ─────────────────────────────────────────────

st.sidebar.header("📤 Upload & Ingest PDF")

st.sidebar.markdown("---")
st.sidebar.header("Model selection")

model_choice = st.sidebar.radio(
    "Choose your desired model:",
    options=["Gemini (cloud)", "Local (LM Studio)"],
    index=0,
)

if model_choice.startswith("Gemini"):
    selected_backend = "gemini"
else:
    selected_backend = "local"

uploaded_file = st.sidebar.file_uploader("Choose a PDF", type=["pdf"])
topic_label = st.sidebar.text_input("Topic label", value="general", help="Used to group documents (e.g., dbms, ml, notes).")

if st.sidebar.button("Upload & Ingest"):
    if uploaded_file is None:
        st.sidebar.warning("Please select a PDF first.")
    else:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        data = {
            "topic": topic_label or "general"
        }

        progress = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        status_text.info("Uploading and ingesting...")

        try:
            # Fake-progress while waiting for the backend to finish
            for i in range(0, 90, 10):
                time.sleep(0.05)
                progress.progress(i)

            resp = requests.post(INGEST_URL, files=files, data=data)

            if resp.status_code == 200:
                progress.progress(100)
                resp_json = resp.json()
                st.sidebar.success(
                    f"Ingested {resp_json.get('pages_ingested', 0)} pages "
                    f"as topic '{resp_json.get('topic')}'."
                )
                # Refresh topics cache
                get_topics.clear()
            else:
                st.sidebar.error(f"Failed to ingest file: {resp.status_code}")
        except Exception as e:
            st.sidebar.error(f"Error during ingest: {e}")
        finally:
            time.sleep(0.2)
            progress.empty()
            status_text.empty()


# ─── Main: Query Interface ────────────────────────────────────────────────────

topics = get_topics()
col1, col2 = st.columns([1.5, 1])

with col2:
    st.subheader("Query Settings")
    selected_topic = st.selectbox("Filter by topic", topics)
    top_k = st.slider("Number of chunks to retrieve", 1, 10, 3)

with col1:
    st.subheader("💬 Ask a Question")
    question = st.text_input("Your question:")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            payload = {
            "question": question,
            "top_k": top_k,
            "backend": selected_backend,
            }
        if selected_topic != "all":
            payload["topic"] = selected_topic

            with st.spinner("Thinking..."):
                try:
                    r = requests.post(RAG_URL, json=payload)
                except Exception as e:
                    st.error(f"Error contacting backend: {e}")
                else:
                    if r.status_code == 200:
                        data = r.json()
                        st.success(data.get("answer", ""))

                        st.subheader("Sources")
                        for src in data.get("sources", []):
                            st.markdown(
                                f"- **{src.get('source', 'unknown')}**, "
                                f"page {src.get('page', '?')} "
                                f"(topic: `{src.get('topic', 'n/a')}`)"
                            )
                    else:
                        st.error(f"Backend error: {r.status_code}")
                        st.text(r.text)