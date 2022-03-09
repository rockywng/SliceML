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


model = pickle.load(open("comment_classifier2.sav", "rb"))
vectorizer = pickle.load(open("vectorizer2.sav", "rb"))
def scrape_predict(link):
    data=[]
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-gpu")
    with Chrome(executable_path=r'C:\Program Files\chromedriver.exe', options=options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(str(link))

        for item in range(20): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            #time.sleep(15)

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
scrape_predict("https://www.youtube.com/watch?v=5gqC4f24sd4")
