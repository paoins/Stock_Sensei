import praw
import pandas as pd
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()
# Reddit API connection
reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent="stock_sensein"
)

# Clean up post
def clean_text(text):
    text = str(text)
    text = text.encode("ascii", "ignore").decode("utf-8")  # non-ascii
    text = re.sub(r"http\S+", "", text)  # links
    text = re.sub(r"\s+", " ", text).strip() # whitespace
    text = re.sub(r"&amp;", "&", text) # HTML encoding
    return text

# Get top comments
def filter_comments(post):
    post.comments.replace_more(limit=0)
    good_comments = []
    for comment in post.comments:
        if comment.score >=5 and len(comment.body.split()) > 10 and len(comment.body)<10000:
            good_comments.append(clean_text(comment.body))
            if len(good_comments)>=5:
                break
    return good_comments


# Search settings
keywords = ["TSLA", "Tesla stock", "Tesla earnings"]
subreddits = ["stocks", "investing", "wallstreetbets", "StockMarket"]
min_upvotes = 5

# Collect Data
results = []
seen_urls = set()  # Avoid duplicates

# Loop through subreddits and keywords
for subreddit in subreddits:
    for keyword in keywords:
        print(f"Searching r/{subreddit} for: {keyword}")
        try:
            for post in reddit.subreddit(subreddit).search(keyword, sort="new", time_filter="month", limit=100):
                if post.url in seen_urls or post.score < min_upvotes:
                    continue

                seen_urls.add(post.url)
                title = clean_text(post.title)
                selftext = clean_text(post.selftext)

                try:
                    comments = filter_comments(post)
                    comment_blob = "".join(comments)
                except Exception as e:
                    print(f"Error fetching comments: {e}")
                    comment_blob= []

                results.append({
                    "title": title,
                    "text": selftext,
                    "subreddit": subreddit,
                    "date": datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d"),
                    "upvotes": post.score,
                    "url": post.url,
                    "comments": comment_blob,
                    "sentiment": ""
                })
        except Exception as e:
            print(f"Failed to search r/{subreddit} for '{keyword}': {e}")

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv("reddit_tesla_collected.csv", index=False)
print(f"Scraped {len(df)} unique posts.")
for post in reddit.subreddit("stocks").search("Tesla", limit=5):
    print(post.title)
