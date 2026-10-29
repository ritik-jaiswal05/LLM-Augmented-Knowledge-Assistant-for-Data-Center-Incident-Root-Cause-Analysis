import streamlit as st
from rca import load_docs, chunk_docs, Index, analyze

st.set_page_config(page_title="RCA Knowledge Assistant", layout="wide")
st.title("LLM-Augmented Knowledge Assistant for Data Center Incident RCA")
st.caption("Prototype on SYNTHETIC data. Decision support only: a human engineer must validate all suggestions.")

@st.cache_resource
def get_index():
    return Index(chunk_docs(load_docs()))
index = get_index()
st.sidebar.write(f"Retrieval backend: {index.backend}")
st.sidebar.write(f"Chunks indexed: {len(index.chunks)}")
k = st.sidebar.slider("Top-k", 1, 8, 4)

incident = st.text_area("Describe the incident / paste log text", height=150,
    placeholder="e.g. Users report API timeouts; logs show 'timeout waiting for connection from pool'")
if st.button("Analyze") :
    if not incident.strip():
        st.error("Please enter an incident description.")
    else:
        out, hits = analyze(incident, index, k)
        st.info(f"Mode: {out.get('mode')}" + (f" | LLM error, fell back: {out['llm_error']}" if out.get("llm_error") else ""))
        st.subheader("Summary"); st.write(out.get("summary", ""))
        if out.get("insufficient_evidence"): st.warning("Evidence may be insufficient; KB may not contain a relevant match.")
        st.subheader("Ranked root-cause hypotheses")
        for h in out.get("hypotheses", []):
            st.markdown(f"**#{h.get('rank')} {h.get('root_cause')}**  \nConfidence (qualitative): `{h.get('confidence')}`  \n"
                        f"Evidence: {', '.join(h.get('evidence_ids', []))}  \n{h.get('reasoning','')}")
        st.subheader("Suggested diagnostic steps")
        for s in out.get("diagnostic_steps", []): st.write("- " + s)
        if out.get("missing_info"):
            st.subheader("Missing information"); [st.write("- " + m) for m in out["missing_info"]]
        for p in out.get("validation_problems", []): st.error(p)
        st.subheader("Retrieved evidence")
        for h in hits: st.expander(f"{h['chunk_id']} (score {h['score']:.3f})").write(h["text"])
