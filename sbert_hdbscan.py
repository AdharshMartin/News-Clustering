import pandas as pd
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def get_keywords(texts, top_n=5):
    vectorizer = CountVectorizer(stop_words='english', max_features=5000)
    X = vectorizer.fit_transform(texts)
    sums = np.array(X.sum(axis=0)).flatten()
    words = vectorizer.get_feature_names_out()
    keywords = [words[i] for i in sums.argsort()[-top_n:][::-1]]
    return keywords


def run():
    df = pd.read_csv("data-tsv-file/raw-data.tsv", sep="\t")
    df["text"] = df["headline"].fillna('') + " " + df["description"].fillna('')
    texts = df["text"].tolist()

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, show_progress_bar=True)

    reducer = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine', random_state=42)
    reduced_embeddings = reducer.fit_transform(embeddings)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom')
    cluster_labels = clusterer.fit_predict(reduced_embeddings)
    df["cluster"] = cluster_labels

    print(df.groupby("cluster").size())

    for cluster_id in np.unique(cluster_labels):
        if cluster_id == -1:
            continue
        cluster_texts = df[df["cluster"] == cluster_id]["text"].tolist()
        print(f"\nCluster {cluster_id} top keywords:", get_keywords(cluster_texts))


if __name__ == "__main__":
    run()
