'''
import pandas as pd
from text import get_tesla_sentiment_insight, dominant_emotion, recap
from Visualisation import visualize_sentiment

# Load data
reddit_df = pd.read_csv("../reddit_tesla_sentiment.csv")
news_df = pd.read_csv("../tesla_news_emotion_summary.csv")

print("🤖 Tesla Sentiment Bot is ready to help! Ask about Reddit, news, sentiment, or charts. Type 'exit' to quit.\n")

# Bot state variables
awaiting_source = False
awaiting_chart_type = False
chart_source = None

while True:
    user_input = input("You: ").strip().lower()

    if user_input in ["exit", "quit", "bye"]:
        print("Bot: 👋 Bye! Stay informed, trader!")
        break

    # Start visualization flow
    if user_input in ["chart", "graph", "visual"]:
        print("Bot: 📊 What source do you want to visualize? (reddit / news)")
        awaiting_source = True
        continue

    # Ask for chart source
    if awaiting_source:
        if "reddit" in user_input:
            chart_source = "reddit"
        elif "news" in user_input:
            chart_source = "news"
        else:
            print("Bot: ❗ Please type either 'reddit' or 'news'")
            continue

        awaiting_source = False
        awaiting_chart_type = True
        chart_options = "pie / bar / line / wordcloud" if chart_source == "reddit" else "pie / bar / wordcloud"
        print(f"Bot: ✅ Source selected. What chart type? ({chart_options})")
        continue

    # Ask for chart type and show it
    if awaiting_chart_type:
        chart_types = ["pie", "bar", "wordcloud"]
        if chart_source == "reddit":
            chart_types.append("line")

        selected_type = next((t for t in chart_types if t in user_input), None)
        if selected_type:
            print(f"Bot: 🛠 Creating {selected_type} chart for {chart_source.title()}...")
            visualize_sentiment(source=chart_source, viz=selected_type)
            awaiting_chart_type = False
            chart_source = None
        else:
            print(f"Bot: ❗ Please choose a valid chart type: {', '.join(chart_types)}")
        continue

    # Sentiment overview
    if any(word in user_input for word in ["sentiment", "summary", "tesla"]):
        summary, _, _ = get_tesla_sentiment_insight(reddit_df, news_df)
        print(f"\n📈 Bot Insight:\n{summary}\n")
        continue

    # Reddit emotion
    if "reddit" in user_input:
        emotion = dominant_emotion(reddit_df["sentiment_label"])
        print(f"📕 Reddit Emotion: {emotion}")
        continue

    # News emotion
    if "news" in user_input:
        emotion = dominant_emotion(news_df["emotion"])
        print(f"📰 News Emotion: {emotion}")
        continue

    # Market signal
    if "signal" in user_input or "market" in user_input:
        summary, _, _ = get_tesla_sentiment_insight(reddit_df, news_df)
        if "BEARISH" in summary:
            signal = "bearish"
        elif "BULLISH" in summary:
            signal = "bullish"
        else:
            signal = "mixed"
        print(f"📊 Market Signal: {signal.upper()}")
        continue

    # Top news titles
    if "headline" in user_input or "top news" in user_input:
        top = news_df[['title', 'emotion']].head(3)
        for _, row in top.iterrows():
            print(f"📰 [{row['emotion'].upper()}] {row['title']}")
        continue

    # Full report
    if "full" in user_input or "report" in user_input:
        recap(reddit_df, news_df)
        continue

    # Fallback
    print("Bot: 🤖 I can show Tesla sentiment, Reddit emotions, news vibes, or charts! Try asking about 'summary', 'chart', 'market', or 'report'.")'''
