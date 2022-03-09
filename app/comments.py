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
import pickle
import re
import pandas as pd   


data=[]
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--mute-audio")


with Chrome(executable_path=r'C:\Program Files\chromedriver.exe', options=options) as driver:
    wait = WebDriverWait(driver,15)
    driver.get("https://www.youtube.com/watch?v=pz52gPH3ou4")

    for item in range(20): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)

clean_features = []
df = pd.DataFrame(data, columns=['comment'])
def clean(comment):
    clean = re.sub(r'\W', ' ', comment)
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
for i in range(1, 10):
    print(clean_features[i])
vectorizer = pickle.load(open("vectorizer.sav", "rb"))
loaded_pickle = pickle.load(open("comment_classifier.sav", "rb"))

#vectorizer = TfidfVectorizer(max_features = 2500, min_df = 7, max_df = 0.8, stop_words = stopwords.words('english'))
#vectorizer.fit(clean_features)
clean_features = vectorizer.transform(clean_features).toarray()

#filename = 'comment_classifier.sav'

print(len(clean_features[1]))

print(len(clean_features[2]))
print(len(clean_features[3]))
val = loaded_pickle.predict(clean_features)
print(val)
pos = 0
neg = 0
for i in range(len(val)):
    if (val[i] == 'P'):
        pos += 1
    elif (val[i] == 'N'):
        neg += 1
rat = pos/(pos + neg)
print(rat)
