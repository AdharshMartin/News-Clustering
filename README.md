# 📝 News Clustering and Keyword Extraction 

This project performs **unsupervised clustering** on news text data and extracts top keywords for each cluster 🚀

---

## ✨ Features
- 🌐 Collect news data using a news newsdata.io
- 📰 Combine `headline` and `description` into a single text field.
- 🤖 Generate embeddings using `SentenceTransformer`.
- 🔽 Reduce embeddings with **UMAP**.
- 📊 Cluster texts using **HDBSCAN**.
- 🏷️ Display cluster sizes and top keywords.


---

Run the following commands to install required Python packages:

```bash
pip install --user -U nltk
pip install -U sentence-transformers
pip install hf_xet
pip install hdbscan
pip install umap-learn
pip install requests
