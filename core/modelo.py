import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("data/dados.csv")

X = df["url"]
y = df["label"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

def prever(url):
    url_vec = vectorizer.transform([url])
    resultado = model.predict(url_vec)[0]

    return "phishing" if resultado == 1 else "seguro"