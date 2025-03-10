Sentiment Analysis, Recommendations, and Chatbot
This project is a Streamlit web application that performs sentiment analysis on product reviews, provides product recommendations, and includes a chatbot to answer questions based on the reviews.

Features
Sentiment Analysis: Visualize the distribution of sentiments using TextBlob and Hugging Face models.
Product Recommendations: Recommend top products based on sentiment filters.
Chatbot: Interact with an AI chatbot to ask questions about product ratings and reviews.
Project Structure
analyzed_reviews.csv: Processed CSV file containing product reviews and sentiment analysis results.
flipkart_reviews.csv: Raw CSV file containing Flipkart product reviews.
rec1.py: Main Streamlit application file.
requirements.txt: List of dependencies required for the project.
scrap.py: Script for scraping product reviews.
senti.py: Script for performing sentiment analysis on the reviews.


Installation
Clone the repository:

Create a virtual environment and activate it:

Install the required dependencies:

Replace the placeholder API key in rec1.py with your actual Cohere API key:

Usage
Run the Streamlit application:

Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

Use the sidebar to choose between visualizing sentiment distribution or interacting with the chatbot.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Streamlit
Cohere
TextBlob
Hugging Face
Feel free to contribute to this project by submitting issues or pull requests.
