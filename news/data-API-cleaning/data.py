from newsdataapi import NewsDataApiClient
import pandas as pd


def run():
    api = NewsDataApiClient(apikey="pub_8a7c2d312f6647a6b6be50ea7372703f")

    page = None
    finalcount = 0

    while finalcount <= 10:
        count = 0   # reset each outer loop
        while count < 13:
            try:
                # Load existing file if it exists, otherwise start fresh
                try:
                    df = pd.read_csv("data-tsv-file/raw-data.tsv", sep="\t")
                except FileNotFoundError:
                    df = pd.DataFrame(columns=["headline", "description", "source", "url", "date"])

                # Call API
                response = api.latest_api(page=page, language="en")

                # Stop if API has no results
                if "results" not in response or not response["results"]:
                    print("⚠️ No more results available, stopping.")
                    return

            except Exception as e:
                print(f"⚠️ Exception occurred: {e}")
                return

            # Convert API response to DataFrame
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

            # Merge and remove duplicates
            df = pd.concat([df, row]).drop_duplicates(subset=["headline"])

            # Save updated dataset
            df.to_csv("data-tsv-file/raw-data.tsv", encoding="utf-8", index=False, sep="\t")

            print("credits used:", count)
            count += 1

            # Update next page token
            page = response.get("nextPage", None)
            print("Next page token:", page)

            if not page:  # no more pages
                print("⚠️ No next page, breaking inner loop.")
                break

        finalcount += 1

    print("✅ Finished data collection (raw-data.py)")


if __name__ == "__main__":
    run()
