import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from html import unescape

def download_nltk_resources():
    """Ensure necessary NLTK resources are downloaded."""
    try:
        # Check if the 'stopwords' resource is available, otherwise download it
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        # Check if the 'vader_lexicon' for SentimentIntensityAnalyzer is available, otherwise download it
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

# Call the download function to ensure resources are available
download_nltk_resources()

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def preprocess_text_for_sentiment(text):
    """Clean text for sentiment analysis by removing HTML tags, URLs, and decoding HTML entities."""
    html_tag_pattern = re.compile(r'<.*?>')
    hyperlink_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = unescape(text)
    text = html_tag_pattern.sub('', text)
    text = hyperlink_pattern.sub('', text)
    return text.lower().strip()

def remove_stopwords(text):
    """Remove stopwords from text."""
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word not in stop_words])

def analyze_sentiment(text):
    """Analyze the sentiment of the given text using NLTK's VADER."""
    return sia.polarity_scores(text)['compound']

def categorize_sentiment(score):
    """Categorize sentiment based on the sentiment score."""
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def preprocessing_analysing():
    # downloding nltk 
    download_nltk_resources()

    preprocess_text_for_sentiment()