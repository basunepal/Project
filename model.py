import pandas as pd
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from nltk.tokenize import word_tokenize 
from sklearn import preprocessing 

import re
import warnings
warnings.filterwarnings("ignore")

import nltk
nltk.download('stopwords')
nltk.download('punkt')

data = pd.read_csv("data.csv")


def process_text(text):
    text = text.lower().replace('\n',' ').replace('\r','').strip()
    text = re.sub(' +', ' ', text)
    text = re.sub(r'[^\w\s]','',text)
    
    
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    
    text = " ".join(filtered_sentence)
    return text

data['Text_parsed'] = data['Text'].apply(process_text)



label_encoder = preprocessing.LabelEncoder() 
data['Category_target']= label_encoder.fit_transform(data['Category'])


X_train, X_test, y_train, y_test = train_test_split(data['Text_parsed'], 
                                                    data['Category_target'], 
                                                    test_size=0.2, 
                                                    random_state=8)

ngram_range = (1,2)
min_df = 10
max_df = 1.
max_features = 300

tfidf = TfidfVectorizer(encoding='utf-8',
                        decode_error='ignore',
                        ngram_range=ngram_range,
                        stop_words=None,
                        lowercase=False,
                        max_df=max_df,
                        min_df=min_df,
                        max_features=max_features,
                        norm='l2',
                        sublinear_tf=True)
                        
features_train = tfidf.fit_transform(X_train).toarray()

#FEATURE EXTRACTOR DUMPED
pickle.dump(tfidf,open('feature.pkl','wb'))

labels_train = y_train

features_test = tfidf.transform(X_test).toarray()
labels_test = y_test


LR = LogisticRegression(C=1)
LR.fit(features_train, labels_train)

#PREDICTIONS

#THIS IS THE INPUT TO THE MODEL
#input = pd.read_csv("input.csv",encoding_errors='replace')
#processed input
#processed_input = input.apply(process_text)

#EXTRACTING THE FEATURES FROM THE INPUT DATA
#input_features = tfidf.transform(processed_input).toarray()

#prediction = LR.predict(input_features)
#print(prediction)

pickle.dump(LR,open('model.pkl','wb'))

# model = pickle.load(open('model.pkl','rb'))