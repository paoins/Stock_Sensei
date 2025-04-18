from newspaper import Article

url = "https://www.cnn.com/2023/12/15/business/tesla-stock-news.html"
article = Article(url)

article.download()
article.parse()

print("📰 Title:", article.title)
print("🧑 Author(s):", article.authors)
print("📅 Published:", article.publish_date)
print("📝 Text:\n", article.text[:500], "...")
