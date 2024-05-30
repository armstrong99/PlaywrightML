from textblob import TextBlob

class SentimentAnalyzer:
    def analyse(self, reviews):
        sentiments = [self.get_sentiment(review) for review in reviews]
        return sentiments
    
    def get_sentiment(self, review):
        analysis = TextBlob(review)
        return analysis.sentiment.polarity