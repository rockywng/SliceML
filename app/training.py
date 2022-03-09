import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from sklearn.pipeline import Pipeline

nltk.download('stopwords')
training_path = "C:\Projects\sentiment\\betternlp.csv"
training_set = pd.read_csv(training_path)
training_set = training_set[['comment_text', 'Sentiment']]
training_set = training_set.head(100000)
#training_set.columns = ['Comment', 'Sentiment']
#print(training_set)
features = training_set.iloc[:, 0]
labels = training_set.iloc[:, 1]
clean_features = []
for comment in range(0, len(features)):
    # remove special chars
    clean = re.sub(r'\W', ' ', str(features[comment]))
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

vectorizer = TfidfVectorizer(max_features = 2500, min_df = 7, max_df = 0.8, stop_words = stopwords.words('english'))
#print(vectorizer.get_feature_names())
print(clean_features)
clean_features = vectorizer.fit_transform(clean_features).toarray()
print(len(clean_features[0]))
print(len(clean_features[1]))
X_train, X_test, Y_train, Y_test = train_test_split(clean_features, labels, test_size = 0.2, random_state = 0)
print(X_test)
classifier = RandomForestClassifier(n_estimators = 200, random_state = 0)
classifier.fit(X_train, Y_train)
predictions = classifier.predict(X_test)
print(predictions)
print(confusion_matrix(Y_test,predictions))
print(classification_report(Y_test,predictions))
print(accuracy_score(Y_test, predictions))
# accuracy of .775!
# save w/ pickle
filename = 'comment_classifier2.sav'
vecname = 'vectorizer2.sav'
pickle.dump(classifier, open(filename, 'wb'))
pickle.dump(vectorizer, open(vecname, 'wb'))
#pickle.dump(classifier, open(filename, 'wb'))
#pickle.dump(vectorizer, open(vecname, 'wb'))
#with open(filename, 'rb') as file:
    #loaded_pickle = pickle.load(file)
#yval = loaded_pickle.predict(new_test)
#print(yval)

""" import time
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
options.add_argument("--mute-audio") """


""" with Chrome(executable_path=r'C:\Program Files\chromedriver.exe', options=options) as driver:
    wait = WebDriverWait(driver,15)
    driver.get("https://www.youtube.com/watch?v=pz52gPH3ou4")

    for item in range(10): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)
 """
""" clean_features2 = []
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
    clean_features2.append(clean)
for i in range(1, 10):
    print(clean_features2[i])
#vectorizer = TfidfVectorizer(max_features = 2500, min_df = 7, max_df = 0.8, stop_words = stopwords.words('english'))
#vectorizer.fit(clean_features)
clean_features2 = vectorizer.transform(clean_features2).toarray()

filename = 'comment_classifier.sav'

with open(filename, 'rb') as file:
    loaded_pickle = pickle.load(file)
#print(clean_features[1])
#print(clean_features[0])
print(len(clean_features2[1]))

print(len(clean_features2[2]))
print(len(clean_features2[3]))

val = loaded_pickle.predict(clean_features2)
print(val)
 """