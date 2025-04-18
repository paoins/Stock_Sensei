from collections import Counter
from datetime import datetime

# === Sentiment Logic ===

# Finds the most common emotion in a given column
def dominant_emotion(series):
    if not series.empty:
        counts = Counter(series.dropna())
        return counts.most_common(1)[0][0]
    return "neutral"

# Maps emotion labels to sentiment
def map_emotion_to_sentiment(emotion):
    emotion_map = {
        "joy": "positive",
        "surprise": "positive",
        "positive": "positive",
        "anger": "negative",
        "fear": "negative",
        "sadness": "negative",
        "disgust": "negative",
        "negative": "negative",
        "neutral": "neutral"
    }
    return emotion_map.get(emotion, "neutral")

# Gets sentiment overview from both Reddit and News
def get_tesla_sentiment_insight(reddit_df, news_df):
    reddit_main_emotion = dominant_emotion(reddit_df["sentiment_label"])
    news_main_emotion = dominant_emotion(news_df["emotion"])

    reddit_sentiment = map_emotion_to_sentiment(reddit_main_emotion)
    news_sentiment = map_emotion_to_sentiment(news_main_emotion)

    if reddit_sentiment == "positive" and news_sentiment == "positive":
        signal = "bullish"
    elif reddit_sentiment == "negative" and news_sentiment == "negative":
        signal = "bearish"
    else:
        signal = "mixed"

    reddit_total = reddit_df["sentiment_label"].dropna().shape[0]
    news_total = news_df["emotion"].dropna().shape[0]

    summary = f"""📈 **Overall Sentiment: {signal.upper()}**
Reddit: {reddit_main_emotion} ({reddit_sentiment}) – based on {reddit_total} posts  
News: {news_main_emotion} ({news_sentiment}) – based on {news_total} articles"""

    return summary, reddit_main_emotion, news_main_emotion

# === Format Output ===

# Build a markdown block for Reddit posts
def format_post(row):
    return f"""**🔗 {row['title']}**
- URL: {row['url']}
- Upvotes: {row['upvotes']}
- Sentiment: {row['sentiment_label']}
- Emotion: {row.get('emotion', 'n/a')}
- Summary: {row.get('thread_summary', '')[:300]}..."""

# Build a markdown block for News articles
def format_news(row):
    return f"""**📰 {row['title']}**
- Source: {row['url']}
- Emotion: {row['emotion']}
- Summary: {row['summary'][:300]}..."""

# === Generate Daily Report ===

def recap(reddit_df, news_df):
    # Get the overall signal and main emotions
    summary_text, top_emotion_reddit, top_emotion_news = get_tesla_sentiment_insight(reddit_df, news_df)

    # Get top Reddit posts by emotion
    top_reddit = reddit_df[reddit_df["sentiment_label"] == top_emotion_reddit]
    top_reddit = top_reddit.sort_values(by="upvotes", ascending=False).head(3)

    # Get top news articles by emotion
    top_news = news_df[news_df["emotion"] == top_emotion_news].head(3)

    # Create date header
    today = datetime.now().strftime("%Y-%m-%d")

    # Start report
    report = f"# 🚗 Tesla Daily Sentiment Report – {today}\n\n"
    report += "## 📊 Summary\n" + summary_text + "\n\n"

    # Add Reddit threads
    report += "## 🔥 Top Reddit Threads\n"
    for _, row in top_reddit.iterrows():
        report += format_post(row) + "\n\n"

    # Add News headlines
    report += "## 📰 Top News Articles\n"
    for _, row in top_news.iterrows():
        report += format_news(row) + "\n\n"

    print(report)
