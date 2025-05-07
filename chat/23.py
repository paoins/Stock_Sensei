import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import StringIO
from contextlib import redirect_stdout

from Chatboot.text import get_tesla_sentiment_insight, recap

# --- Settings ---
st.set_page_config(page_title="Tesla Sentiment Bot", page_icon="🚗", layout="wide")


# --- Load Data ---
@st.cache_data
def load_data():
    reddit = pd.read_csv("../reddit_tesla_sentiment.csv")
    news = pd.read_csv("../tesla_news_emotion_summary.csv")
    return reddit, news


# --- Capture Printed Recap ---
def get_full_report():
    buffer = StringIO()
    with redirect_stdout(buffer):
        recap(reddit_df, news_df)
    return buffer.getvalue()


# --- Show Summary ---
def show_summary():
    st.title("🚗 Tesla Sentiment Dashboard")

    summary, reddit_emotion, news_emotion = get_tesla_sentiment_insight(reddit_df, news_df)
    signal = "bullish" if "bullish" in summary.lower() else "bearish" if "bearish" in summary.lower() else "mixed"

    st.subheader("📊 Market Signal:")
    st.success(f"Signal: {signal.upper()}")

    st.subheader("📈 Summary:")
    st.markdown(summary)

    with st.expander("📑 Full Report"):
        report = get_full_report()
        st.text(report if report.strip() else "No report generated.")


# --- Visualization ---
def show_visuals():
    st.title("📊 Sentiment Visualizations")
    data_source = st.radio("Choose data:", ["Reddit", "News"])
    chart_type = st.selectbox("Chart type:", ["Pie", "Bar", "Wordcloud", "Line (Reddit Only)"])

    df = reddit_df if data_source == "Reddit" else news_df
    source = data_source.lower()
    column = "sentiment_label" if source == "reddit" else "emotion"

    if chart_type == "Pie":
        fig, ax = plt.subplots()
        df[column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    elif chart_type == "Bar":
        fig, ax = plt.subplots()
        df[column].value_counts().plot.bar(color="skyblue", ax=ax)
        st.pyplot(fig)

    elif chart_type == "Line" and source == "reddit":
        df["date"] = pd.to_datetime(df["date"])
        trend = df.groupby("date")[column].value_counts(normalize=True).unstack().fillna(0)
        fig, ax = plt.subplots()
        trend.plot(ax=ax)
        st.pyplot(fig)

    elif chart_type == "Wordcloud":
        text = " ".join(df["title"].fillna("").astype(str))
        if source == "reddit" and "comments" in df.columns:
            text += " " + " ".join(df["comments"].fillna("").astype(str))
        wc = WordCloud(width=800, height=400).generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)


# --- Main ---
reddit_df, news_df = load_data()

st.sidebar.title("🧭 Navigation")
choice = st.sidebar.radio("Go to:", ["Summary", "Visualizations"])

if choice == "Summary":
    show_summary()
else:
    show_visuals()

st.sidebar.markdown("---")
st.sidebar.caption("Made by a 2nd-year student 🤖")
