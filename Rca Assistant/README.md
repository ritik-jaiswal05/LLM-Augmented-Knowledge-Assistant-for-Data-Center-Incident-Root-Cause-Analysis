# LLM-Augmented Knowledge Assistant for Data Center Incident RCA (prototype)
Synthetic data only. Decision support; human validates everything.

## Run
pip install -r requirements.txt
python make_data.py          # creates synthetic KB + test cases
python evaluate.py           # retrieval evaluation -> results/results.json
streamlit run app.py         # UI

## Optional LLM (any OpenAI-compatible API, e.g. Groq free tier)
export LLM_API_KEY=...       # Windows: set LLM_API_KEY=...
export LLM_MODEL=llama-3.3-70b-versatile
Without a key the app uses a clearly-labelled heuristic (retrieval-ranked) fallback.
Force TF-IDF retrieval (no model download): export RCA_EMBED=tfidf
