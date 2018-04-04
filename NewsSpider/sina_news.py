__author__ = "susmote"

__author__ = "susmote"

from newspaper import Article

url = 'http://tech.sina.com.cn/i/2018-03-29/doc-ifysqfni2090726.shtml'
article = Article(url)
article.download()

print("*"*40)
print(article.html)
print("*"*40)
print(article.parse())

print(article.authors)

print(article.publish_date)

print(article.text)

print(article.top_image)

print(article.movies)


print(article.keywords)

print(article.summary)

