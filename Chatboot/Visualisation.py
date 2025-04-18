import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from wordcloud import WordCloud

def visualize_sentiment(source="reddit", viz="pie"):
    # Load data depending on source
    if source == "reddit":
        df = pd.read_csv("../reddit_tesla_sentiment.csv")
    elif source == "news":
        df = pd.read_csv("../tesla_news_emotion_summary.csv")
    else:
        print("Error: source must be either 'reddit' or 'news'")
        return

    # Pie chart visualization
    if viz == "pie":
        if source == "reddit":
            counts = df["sentiment_label"].value_counts()
        else:
            counts = df["emotion"].value_counts()

        plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
        plt.title(f"{source.title()} Sentiment Distribution")
        plt.show()

    # Bar chart visualization
    elif viz == "bar":
        if source == "reddit":
            counts = df["sentiment_label"].value_counts()
        else:
            counts = df["emotion"].value_counts()

        plt.bar(counts.index, counts.values, color='lightblue')
        plt.title(f"{source.title()} Sentiment Counts")
        plt.ylabel("Number of Posts")
        plt.xticks(rotation=30)
        plt.show()

    # Line plot for reddit sentiment over time
    elif viz == "line":
        if source != "reddit":
            print("Line chart is only available for Reddit data.")
            return

        df["date"] = pd.to_datetime(df["date"])
        daily_sentiment = df.groupby("date")["sentiment_label"].value_counts(normalize=True).unstack().fillna(0)

        daily_sentiment.plot(figsize=(10, 5), marker='o')
        plt.title("Reddit Sentiment Over Time")
        plt.xlabel("Date")
        plt.ylabel("Sentiment Proportion")
        plt.grid(True)
        plt.show()

    # Word cloud of text data
    elif viz == "wordcloud":
        if source == "reddit":
            text_data = " ".join(df["title"].dropna()) + " " + " ".join(df["comments"].dropna())
        else:
            text_data = " ".join(df["title"].dropna()) + " " + " ".join(df["text"].dropna())

        wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(text_data)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(f"Word Cloud - {source.title()}")
        plt.show()

    else:
        print("Error: viz must be one of 'pie', 'bar', 'line', or 'wordcloud'")
