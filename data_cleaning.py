import pandas as pd
import re


def clean_text(val: str) -> str:
    val = re.sub(r"[^a-zA-Z]", " ", val)
    return val.strip()


def run():
    df = pd.read_csv("data-tsv-file/raw-data.tsv", sep="\t")

    df["text"] = df["headline"].fillna("") + " " + df["description"].fillna("")
    df["text"] = df["text"].apply(clean_text)

    df = df[["text", "headline", "description", "source", "url", "date"]]

    df.to_csv("data-tsv-file/data-news.tsv", sep="\t", index=False)

    print("Finished cleaning data")


if __name__ == "__main__":
    run()
