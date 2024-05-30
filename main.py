import os
from scrappers.review import ReviewScrapper
from ml.sentiment import SentimentAnalyzer
import pandas as pd

def main():
    config_path = "scrappers/sources.yml"
    config = ReviewScrapper.loadConfig(config_path)
    results = []

    for product in config['products']:
        scraper = ReviewScrapper(product)
        reviews = scraper.scrape_reviews()
         
        if reviews:
            analyzer = SentimentAnalyzer()
            sentiments = analyzer.analyse(reviews)
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            results.append({
                "product": product["name"],
                "average_sentiment": avg_sentiment,
                "reviews": reviews
            })
        
    results_df = pd.DataFrame(results)
    results_df.to_csv("anaylsis_results.csv", index=False)
    print("Analysis completed, Results saved to -> anaylsis_results.csv")




if __name__ ==  "__main__":
    main()

