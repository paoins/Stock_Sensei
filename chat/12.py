import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import StringIO
from contextlib import redirect_stdout
def capture_printed_recap(func, *args, **kwargs):
    buffer = StringIO()
    with redirect_stdout(buffer):
        func(*args, **kwargs)
    return buffer.getvalue()

from text import get_tesla_sentiment_insight, recap


# Set page config
st.set_page_config(
    page_title="Tesla Sentiment Analysis",
    page_icon="🚗",
    layout="wide"
)



def streamlit_visualize_sentiment(df, source="reddit", viz="pie"):
    if viz == "pie":
        column = "sentiment_label" if source == "reddit" else "emotion"
        counts = df[column].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index)
        ax.set_title(f"{source.title()} Sentiment Distribution")
        st.pyplot(fig)

    elif viz == "bar":
        column = "sentiment_label" if source == "reddit" else "emotion"
        counts = df[column].value_counts()
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values, color='lightblue')
        ax.set_title(f"{source.title()} Sentiment Counts")
        ax.set_ylabel("Number of Posts")
        plt.xticks(rotation=30)
        st.pyplot(fig)

    elif viz == "line":
        if source != "reddit":
            st.error("Line chart is only available for Reddit data.")
            return

        df["date"] = pd.to_datetime(df["date"])
        daily_sentiment = df.groupby("date")["sentiment_label"].value_counts(normalize=True).unstack().fillna(0)

        fig, ax = plt.subplots(figsize=(10, 5))
        daily_sentiment.plot(ax=ax, marker='o')
        ax.set_title("Reddit Sentiment Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sentiment Proportion")
        ax.grid(True)
        st.pyplot(fig)

    elif viz == "wordcloud":
        if source == "reddit":
            text_data = " ".join(df["title"].dropna().astype(str)) + " " + " ".join(df["comments"].dropna().astype(str))
        else:
            text_data = " ".join(df["title"].dropna().astype(str)) + " " + " ".join(df["text"].dropna().astype(str))

        wordcloud = WordCloud().generate(text_data)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"Word Cloud - {source.title()}")
        st.pyplot(fig)

    else:
        st.error(f"Visualization type '{viz}' not supported")



def load_data():
        reddit_df = pd.read_csv("../Data/reddit_tesla_sentiment.csv")
        news_df = pd.read_csv("../Data/tesla_news_emotion_summary.csv")

        return reddit_df, news_df




def show_sentiment_summary(reddit_df, news_df):
    # Get sentiment summary and full report
    summary, reddit_main_emotion, news_main_emotion = get_tesla_sentiment_insight(reddit_df, news_df)
    full_report = capture_printed_recap(recap, reddit_df, news_df)

    # Infer signal from summary content
    signal = "mixed"
    if "bearish" in summary.lower():
        signal = "bearish"
    elif "bullish" in summary.lower():
        signal = "bullish"

    # Page Title
    st.markdown("# Tesla Sentiment Dashboard")

    # Layout with columns
    col1, col2 = st.columns(2)

    with col1:
        signal_color = {
            "bullish": "green",
            "bearish": "red",
            "mixed": "orange"
        }[signal]

        st.markdown(f"""
        ##  Overall Market Signal
        <div style='background-color: {signal_color}; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
            <h1>{signal.upper()}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("##  Sentiment Breakdown")
        st.markdown(summary)

    # Full Report
    with st.expander("View Full Sentiment Report"):
        try:
            st.markdown(full_report, unsafe_allow_html=True)
        except:
            st.write(full_report)


def show_reddit_analysis(reddit_df):
    st.markdown("##  Reddit Sentiment Analysis")

    # Filter options
    sentiment_filter = st.selectbox(
        "Filter by sentiment:",
        ["All"] + list(reddit_df["sentiment_label"].unique())
    )

    filtered_df = reddit_df
    if sentiment_filter != "All":
        filtered_df = reddit_df[reddit_df["sentiment_label"] == sentiment_filter]

    # Sort by upvotes
    filtered_df = filtered_df.sort_values(by="upvotes", ascending=False)

    # Show top posts
    st.markdown("### Top Reddit Posts")
    for idx, row in filtered_df.head(5).iterrows():
        with st.expander(f" {row['title']} ({row['sentiment_label']})"):
                post_data = {
                    "title": row['title'],
                    "url": row['url'],
                    "upvotes": row['upvotes'],
                    "sentiment": row['sentiment_label'],
                    "emotion": row.get('emotion', 'n/a'),
                    "summary": row.get('thread_summary', '')[:300] + "..."
                }
                st.markdown(f"**Upvotes:** {post_data['upvotes']}")
                st.markdown(f"**Sentiment:** {post_data['sentiment']}")
                st.markdown(f"**URL:** {post_data['url']}")
                st.markdown(f"**Summary:** {post_data['summary']}")


def show_news_analysis(news_df):
    st.markdown("##  News Sentiment Analysis")

    # Filter options
    emotion_filter = st.selectbox(
        "Filter by emotion:",
        ["All"] + list(news_df["emotion"].unique())
    )

    filtered_df = news_df
    if emotion_filter != "All":
        filtered_df = news_df[news_df["emotion"] == emotion_filter]

    # Show top news
    st.markdown("### Top News Articles")
    for idx, row in filtered_df.head(5).iterrows():
        with st.expander(f" {row['title']} ({row['emotion']})"):
                article_data = {
                    "title": row['title'],
                    "source": row['url'],
                    "emotion": row['emotion'],
                    "summary": row['summary'][:300] + "..."
                }
                st.markdown(f"**Emotion:** {article_data['emotion']}")
                st.markdown(f"**Source:** {article_data['source']}")
                st.markdown(f"**Summary:** {article_data['summary']}")


def show_visualizations(reddit_df, news_df):
    st.markdown("##  Visualizations")

    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.markdown("### Data Source")
        data_source = st.radio(
            "Select data source:",
            ["Reddit", "News"]
        )

        df = reddit_df if data_source == "Reddit" else news_df
        source = data_source.lower()

    with viz_col2:
        st.markdown("### Chart Type")
        chart_types = ["pie", "bar", "wordcloud"]
        if data_source == "Reddit":
            chart_types.append("line")

        chart_type = st.radio(
            "Select chart type:",
            chart_types
        )

    # Generate visualization
    streamlit_visualize_sentiment(df, source=source, viz=chart_type)


if __name__ == "__main__":
    # 1. Load your data
    reddit_df, news_df = load_data()

    # 2. Sidebar for navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio(
        "Choose a section:",
        ["Sentiment Summary", "Reddit Analysis", "News Analysis", "Visualizations"]
    )

    # 3. Content
    if app_mode == "Sentiment Summary":
        show_sentiment_summary(reddit_df, news_df)
    elif app_mode == "Reddit Analysis":
        show_reddit_analysis(reddit_df)
    elif app_mode == "News Analysis":
        show_news_analysis(news_df)
    elif app_mode == "Visualizations":
        show_visualizations(reddit_df, news_df)