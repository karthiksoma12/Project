import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import cohere

# Initialize Cohere Client
COHERE_API_KEY = ""  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

# Load the processed CSV file
data = pd.read_csv("analyzed_reviews.csv")

# Prepare Context for Chatbot
def prepare_context(data):
    """Combine product name, rating, and review into a single context."""
    context = []
    for _, row in data.iterrows():
        context.append(
            f"Product: {row['product_name']}\n"
            f"Rating: {row['rating']}\n"
            f"Review: {row['review']}\n"
        )
    return "\n".join(context)

context = prepare_context(data)

# Streamlit App Title
st.title("Sentiment Analysis, Recommendations, and Chatbot")

# Sidebar
st.sidebar.title("Options")
visualization_choice = st.sidebar.selectbox(
    "Choose Visualization",
    ["Sentiment Distribution", "Chatbot"]
)
sentiment_filter = st.sidebar.selectbox(
    "Filter Sentiment for Recommendations",
    ["Positive", "Negative", "Neutral"]
)
top_n = st.sidebar.slider("Number of Top Products to Recommend", min_value=1, max_value=5, value=3)

# Visualization: Sentiment Distribution
if visualization_choice == "Sentiment Distribution":
    st.subheader("Sentiment Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### TextBlob Sentiments")
        fig, ax = plt.subplots()
        sns.countplot(data['textblob_sentiment'], palette="viridis", ax=ax)
        ax.set_title("TextBlob Sentiment Distribution")
        st.pyplot(fig)

    with col2:
        st.markdown("### Hugging Face Sentiments")
        fig, ax = plt.subplots()
        sns.countplot(data['huggingface_sentiment'], palette="magma", ax=ax)
        ax.set_title("Hugging Face Sentiment Distribution")
        st.pyplot(fig)

# Recommendation System
def recommend_top_products(data, sentiment_filter="Positive", top_n=5):
    filtered_data = data[data['textblob_sentiment'] == sentiment_filter]
    recommended_products = (
        filtered_data.groupby('product_name')
        .agg(average_score=('rating', 'mean'), review_count=('review', 'count'))
        .sort_values(by='average_score', ascending=False)
        .head(top_n)
    )
    return recommended_products

if visualization_choice == "Sentiment Distribution":
    st.subheader(f"Top {top_n} Recommended Products ({sentiment_filter} Sentiments)")
    top_products = recommend_top_products(data, sentiment_filter, top_n)

    if not top_products.empty:
        st.dataframe(top_products)

        # Visualization: Top Recommended Products
        st.markdown(f"### Top {top_n} Recommended Products (Bar Chart)")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x=top_products['average_score'],
            y=top_products.index,
            palette="Blues_d",
            ax=ax
        )
        ax.set_title(f"Top {top_n} Recommended Products ({sentiment_filter} Sentiments)")
        ax.set_xlabel("Average Product Score")
        ax.set_ylabel("Product Name")
        st.pyplot(fig)
    else:
        st.write(f"No products found with {sentiment_filter} sentiment.")

# Chatbot Section
if visualization_choice == "Chatbot":
    st.subheader("Chat with AI")
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User Input
    user_input = st.text_input("You: ", placeholder="Ask about product ratings or reviews...")

    if user_input:
        # Include context in the prompt
        query = (
            "You are an assistant that answers questions based on the following product reviews:\n\n"
            f"{context}\n\n"
            "User Query: " + user_input
        )

        try:
            # Generate response using Cohere
            response = co.generate(
                prompt=query,
                model="command-xlarge-nightly",  # Use a suitable Cohere model
                max_tokens=300,
                temperature=0.7
            )
            ai_response = response.generations[0].text.strip()

            # Append messages
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "ai", "content": ai_response})
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"
            st.session_state.messages.append({"role": "ai", "content": ai_response})

    # Display Chat
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")
