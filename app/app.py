import numpy as np
from flask import Flask, flash, request, render_template
import pickle 
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.preprocessing import OneHotEncoder
import re
import pandas as pd
import numpy as np
import requests
import os

app = Flask(__name__)
model = pickle.load(open("app/models/comment_classifier3.sav", "rb"))
vectorizer = pickle.load(open("app/models/vectorizer3.sav", "rb"))

pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'

def validate_link(link):
# check if link is actually a youtube link
    # https://www.youtube.com/watch?v=v8o_hA2eMzI
    if not (link[0:32] == "https://www.youtube.com/watch?v="):
        #print("linkfail")
        return False         
    request = requests.get(link)
    return False if pattern in request.text else True

def scrape_predict(link):
    data=[]
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-gpu")
    with Chrome(executable_path=("/app/.chromedriver/bin/chromedriver"), options=options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(str(link))

        for item in range(3): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(15)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            data.append(comment.text)
    clean_features = []
    df = pd.DataFrame(data, columns=['comment'])
    for index, row in df.iterrows():
        clean = re.sub(r'\W', ' ', row['comment'])
        # remove single chars
        clean = re.sub(r'\s+[a-zA-Z]\s+', ' ', clean)
        # remove starting single chars
        clean = re.sub(r'\^[a-zA-Z]\s+', ' ', clean)
        # replace multiple consecutive spaces with single space
        clean = re.sub(r'\s+', ' ', clean, flags=re.I)
        # remove prefix b
        clean = re.sub(r'^b\s+', '', clean)
        # make all lowercase
        clean = clean.lower()
        clean_features.append(clean)
    clean_features = vectorizer.transform(clean_features).toarray()
    val = model.predict(clean_features)
    pos = 0
    neg = 0
    for i in range(len(val)):
        if (val[i] == 'P'):
            pos += 1
        elif (val[i] == 'N'):
            neg += 1
    rat = pos/(pos + neg)
    print(rat)
    print(neg)
    return rat

def zscore(mean, sd, val):
    return (val - mean)/sd

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=["GET", "POST"])
def predict():
    link = request.form['entry']
    if not (validate_link(link)):
        #flash("i got bad input bro")
        return render_template("index.html", prediction_text = 'Please enter a valid video link of the form https://www.youtube.com/watch?v=VIDEOID')
    print("got link!")
    rat = scrape_predict(str(link))
    print("done scrape")
    #rat = scrape_predict("https://www.youtube.com/watch?v=AK3HxCOZZ6w")
    z = zscore(0.94, 0.01666, rat)
    print("predictions made!")
    if (z > 1.645):
        return render_template("index.html", prediction_text = "The reception to this video was very positive. Its reception was in the top 5% of YouTube videos.")
    elif (z > 0.675):
        return render_template("index.html", prediction_text = "The reception to this video was mostly positive. Its reception was in the top 25% of YouTube videos")
    elif (z > 0):
        return render_template("index.html", prediction_text = "The reception to this video was neutral. Its reception was in the top 50% of YouTube videos.")
    elif (z > -0.675):
        return render_template("index.html", prediction_text = "The reception to this video was mostly negative. Its reception was in the bottom 25% of YouTube videos.")
    else:
        return render_template("index.html", prediction_text = "The reception to this video was very negative. Its reception was in the bottom 5% of YouTube videos.")

# WORKING BASE CASE HERE!
""" @app.route('/', methods=["GET", "POST"])
def home():
    rat = scrape_predict("https://www.youtube.com/watch?v=AK3HxCOZZ6w")
    return str(rat) """

if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True) 
