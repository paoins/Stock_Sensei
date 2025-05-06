import requests
import csv
from newspaper import Article
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


important_keywords = [
    # Market movement
    "drop", "crash", "soars", "surge", "plunge", "rally", "bounce", "dip",

    # Financial events
    "earnings", "revenue", "forecast", "guidance", "beat", "miss", "record",

    # Legal and company risk
    "lawsuit", "SEC", "fine", "fraud", "investigation", "recall", "layoffs",

    # Corporate news
    "merger", "acquisition", "partnership", "IPO", "stock split", "buyback",

    # Hype or risk signals
     "short squeeze", "trending", "viral", "AI", "FSD", "autopilot"
]


def fetch_news_api(query="Tesla", api_key="YOUR_NEWSAPI_KEY"):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    return data.get("articles", [])

def fetch_gnews(query="Tesla", api_key="YOUR_GNEWS_KEY"):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": "en",
        "max": 100,
        "token": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])

# Check if article contains any important keyword
def is_important(article, keywords):
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()

    text = f"{title} {description}"
    for kw in keywords:
        if kw.lower() in text:
            return True
    return False

# Scrape full text
def scrape_articles(articles):
    scraped = []
    for i, item in enumerate(articles):
        url = item.get("url", "")
        if not url:
            continue

        source = item.get("source", "")
        source_name = source.get("name", "") if isinstance(source, dict) else source

        try:
            a = Article(url)
            a.download()
            a.parse()
            scraped.append({
                "title": a.title,
                "text": a.text,
                "published": a.publish_date,
                "source": source_name,
                "url": url
            })
            print(f"[{i + 1}] Scraped: {a.title}")
        except Exception as e:
            print(f"[{i + 1}] Failed to scrape {url}: {e}")

    return scraped

def save_to_csv(articles, filename="tesla_news_collected.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["source", "title", "description", "text", "url", "publishedAt"])

        for article in articles:
            writer.writerow([
                article.get("source", ""),
                article.get("title", ""),
                article.get("description", ""),
                article.get("text", ""),
                article.get("url", ""),
                article.get("published", "")
            ])

newsapi_articles = fetch_news_api(api_key=NEWS_API_KEY)
gnews_articles = fetch_gnews(api_key=GNEWS_API_KEY)

print(len(newsapi_articles))
print(len(gnews_articles))

all_articles = newsapi_articles + gnews_articles

# Filter only important articles
filtered_articles = [article for article in all_articles if is_important(article, important_keywords)]

print("Important articles found:", len(filtered_articles))

full_articles = scrape_articles(filtered_articles)
save_to_csv(full_articles)
print(f"Saved {len(full_articles)} articles to 'tesla_news_collected.csv'")

