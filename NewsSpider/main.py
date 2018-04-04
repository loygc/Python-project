__author__ = "susmote"

import newspaper

sina_news = newspaper.build("http://www.bbc.com/news/world-europe-43588641")

for category in sina_news.category_urls():
    print(category)

article = sina_news.download()

print(type(article))

print(article.text)
print(article.title)