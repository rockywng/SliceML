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
# open model and vectorizer
model = pickle.load(open("app/models/comment_classifier5.sav", "rb"))
vectorizer = pickle.load(open("app/models/vectorizer5.sav", "rb"))

# video unavailable site pattern, to be used for link verification
pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'

# check if a given link is valid
def validate_link(link):
    # check if link does not follow standard youtube link formatting
    if not (link[0:32] == "https://www.youtube.com/watch?v="):
        return False         
    request = requests.get(link)
    # check if the video unavailable pattern appears, if True then the link is not valid
    return False if pattern in request.text else True

def scrape_predict(link):
    data=[]
    # set scraper options for Heroku
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-gpu")
    # begin scraping with path to Heroku chromedriver
    with Chrome(executable_path=("/app/.chromedriver/bin/chromedriver"), options=options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(str(link))

        for item in range(4): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            
        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            data.append(comment.text)
            
    clean_features = []
    df = pd.DataFrame(data, columns=['comment'])
    # clean comments collected 
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
    # use vectorizer to transform comments to appropriate input format
    clean_features = vectorizer.transform(clean_features).toarray()
    # make predictions
    val = model.predict(clean_features)
    pos = 0
    neg = 0
    # count positive and negative labels
    for i in range(len(val)):
        if (val[i] == 'Positive'):
            pos += 1
        elif (val[i] == 'Negative'):
            neg += 1
    if (pos + neg == 0):
        return -1
    rat = pos/(pos + neg)
    print(rat)
    print(neg)
    return rat

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=["GET", "POST"])
def predict():
    link = request.form['entry']
    # inform user if link is not valid
    if not (validate_link(link)):
        return render_template("index.html", prediction_text = 'Please enter a valid video link of the form https://www.youtube.com/watch?v=VIDEOID')
    # make predictions if link is valid
    rat = scrape_predict(str(link))
    # handle edge cases (-1, 0, 1)
    if (rat == -1):
        return render_template("index.html", prediction_text = "The model failed to identify sentiment for this video.")
    if (rat == 1):
        return render_template("index.html", prediction_text = "The comments on this video were almost 100% positive.")
    if (rat == 0):
        return render_template("index.html", prediction_text = "The comments on this video were almost 0% positive.")
    # convert from float to int and multiply by 100 to get percentage value
    percent = int(rat * 100)
    # return percent to user
    return render_template("index.html", prediction_text = "The comments on this video were " + str(percent) + "% positive.")

if __name__ == '__main__':
    #app.debug = True
    app.run(debug=True) 
