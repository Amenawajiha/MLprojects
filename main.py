import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
import re
from nltk.corpus import stopwords
import string
from collections import Counter

data = pd.read_csv("C:\\Users\\shahe\\OneDrive\\Desktop\\tinder_google_play_reviews.csv")

data = data[["content"]]

data.isnull().sum()

data = data.dropna()

nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))


def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\. \S+', '', text)
    text = re.sub('<.?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\\n', '', text)
    text = re.sub('\\w*\\d\\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text


data["content"] = data["content"].apply(clean)

# text = " ".join(i for i in data.content)
# stopwords = set(STOPWORDS)
# wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
# plt.figure(figsize=(15, 10))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()

text = " ".join(data["content"])
words = text.split()
word_counts = Counter(words)
top_n = 20
common_words = word_counts.most_common(top_n)
words, counts = zip(*common_words)

plt.figure(figsize=(12, 8))
plt.barh(words, counts, color="skyblue")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.title(f"Top {top_n} Most Common Words in Reviews")
plt.gca().invert_yaxis()
# plt.show()


nltk.download('vader_lexicon')
sentiments = SentimentIntensityAnalyzer()
data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["content"]]
data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["content"]]
data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["content"]]
data = data[["content", "Positive", "Negative", "Neutral"]]
print(data.head())


positive = ' '.join([i for i in data['content'][data['Positive'] > data['Negative']]])
stopwords = set(STOPWORDS)
if positive:
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(positive)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
else:
    print("No positive reviews to generate a word cloud")


negative = ' '.join([i for i in data['content'][data['Negative'] > data['Positive']]])
stopwords = set(STOPWORDS)
if negative:
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(negative)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
else:
    print("No negative reviews to generate a word cloud")


x = sum(data["Positive"])
y = sum(data["Negative"])
z = sum(data["Neutral"])

def sentiment_score(a,b,c):
    if(a>b) and (a>c):
        print("Positive 😊")
    elif(b>a) and (b>c):
        print("Negative 😠")
    else:
        print("Neutral 🙂 ")


sentiment_score(x, y, z)

print("Positive: ", x)
print("Negative: ", y)
print("Neutral: ", z)

