from newsdataapi import NewsDataApiClient
import pandas as pd


def run():
    api = NewsDataApiClient(apikey="newsdata.io - api_key")  #Enter your news API key

    page = None
    finalcount = 0

    while finalcount <= 10:
        count = 0   
        while count < 10:
            try:
                try:
                    df = pd.read_csv("data-tsv-file/raw-data.tsv", sep="\t")
                except FileNotFoundError:
                    df = pd.DataFrame(columns=["headline", "description", "source", "url", "date"])

                response = api.latest_api(page=page, language="en")

                if "results" not in response or not response["results"]:
                    print("No more results available.")
                    return

            except Exception as e:
                print(f"Exception occurred: {e}")
                return

            row = pd.DataFrame([
                {
                    "headline": i.get("title"),
                    "description": i.get("description"),
                    "source": i.get("source_id"),
                    "url": i.get("link"),
                    "date": i.get("pubDate")
                }
                for i in response["results"]
            ])

            df = pd.concat([df, row]).drop_duplicates(subset=["headline"])

            df.to_csv("data-tsv-file/raw-data.tsv", encoding="utf-8", index=False, sep="\t")

            print("credits used:", count)
            count += 1

            page = response.get("nextPage", None)
            print("Next page token:", page)

            if not page:  
                print("No next page")
                break

        finalcount += 1

    print("Finished data collection (raw-data.py)")


if __name__ == "__main__":
    run()
