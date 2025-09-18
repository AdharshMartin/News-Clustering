import data
import data_cleaning
import sbert_hdbscan

# Collect news from API
data.run()

# Clean the collected data
data_cleaning.run()

# Cluster the cleaned news
sbert_hdbscan.run()
