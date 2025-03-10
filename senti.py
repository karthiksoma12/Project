import pandas as pd
from textblob import TextBlob
from transformers import pipeline

# Load the CSV file
input_file = "flipkart_reviews.csv"  # Replace with your file path
data = pd.read_csv(input_file)

# Check the structure of the dataset
print(data.head())

# Initialize Hugging Face sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Function to perform sentiment analysis using TextBlob
def sentiment_analysis_textblob(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity  # Range: [-1.0, 1.0]
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, polarity

# Function to perform sentiment analysis using Hugging Face Transformers
def sentiment_analysis_transformers(text):
    try:
        result = sentiment_pipeline(text)[0]
        return result['label'], result['score']
    except Exception as e:
        return "Unknown", 0.0

# Perform sentiment analysis on reviews and save results in new columns
data['textblob_sentiment'], data['textblob_polarity'] = zip(*data['review'].apply(sentiment_analysis_textblob))
data['huggingface_sentiment'], data['huggingface_confidence'] = zip(*data['review'].apply(sentiment_analysis_transformers))

# Save the processed data to a new CSV file
output_file = "analyzed_reviews.csv"
data.to_csv(output_file, index=False)

print(f"Sentiment analysis complete. Results saved to {output_file}.")
