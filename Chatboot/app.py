# app.py
import streamlit as st
import pandas as pd
from Chatboot import get_tesla_sentiment_insight, dominant_emotion, recap
from Visualisation import visualize_sentiment

# Load data
@st.cache_data
def load_data():
    reddit_df = pd.read_csv("../reddit_tesla_sentiment.csv")
    news_df = pd.read_csv("../tesla_news_emotion_summary.csv")
    return reddit_df, news_df

reddit_df, news_df = load_data()

# Sidebar
st.sidebar.title("Chatboot Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Sentiment Summary", "Visualize", "Chat Mode"])

st.title("🤖 Tesla Sentiment Chatboot")

# Overview Section
if section == "Overview":
    st.header("🗞️ Dataset Overview")
    st.subheader("Reddit Posts")
    st.write(reddit_df.head())

    st.subheader("News Articles")
    st.write(news_df.head())

# Sentiment Summary
elif section == "Sentiment Summary":
    st.header("📊 Sentiment Summary")

    source = st.selectbox("Choose data source", ["Reddit", "News"])
    if source == "Reddit":
        insight = get_tesla_sentiment_insight(reddit_df)
        st.markdown(insight)
    else:
        insight = get_tesla_sentiment_insight(news_df)
        st.markdown(insight)

    st.markdown("### 🧠 Dominant Emotion")
    emotion = dominant_emotion(news_df if source == "News" else reddit_df)
    st.success(f"Dominant Emotion: **{emotion}**")

    st.markdown("### 🔁 Recap")
    summary = recap(news_df if source == "News" else reddit_df)
    st.info(summary)

# Visualization
elif section == "Visualize":
    st.header("📈 Sentiment Visualization")
    chart_type = st.radio("Choose chart type", ["Pie", "Bar", "WordCloud"])
    source = st.selectbox("Choose data source", ["Reddit", "News"], key="viz_source")

    try:
        visualize_sentiment(source=source, viz=chart_type.lower())
    except Exception as e:
        st.error(f"Visualization error: {e}")

# Chat Mode
elif section == "Chat Mode":
    st.header("💬 Chat with Tesla Sentiment Bot")
    user_input = st.text_input("You:", "")
    if user_input:
        if "news" in user_input.lower():
            st.markdown(get_tesla_sentiment_insight(news_df))
        elif "reddit" in user_input.lower():
            st.markdown(get_tesla_sentiment_insight(reddit_df))
        else:
            st.warning("Ask me something about Tesla, news, or Reddit!")
