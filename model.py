import random
import pandas as pd
import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import model_selection
import tensorflow as tf
from tensorflow.keras.layers import AveragePooling2D, Dense, Input, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization, SpatialDropout2D
from tensorflow.keras.models import Model
from sklearn import preprocessing
from sklearn.utils import class_weight
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.svm import LinearSVC


train_file_name = "/Users/marynavek/Projects/LoRa_fingerprinting/signatures_train.csv"

test_file_name = "/Users/marynavek/Projects/LoRa_fingerprinting/signatures_test.csv"
signature_train = []
signature_test = []
train_file = open(train_file_name)
train_reader = csv.DictReader(train_file)

signature_train_features = []
signature_train_labels = []
train_r = []
for row in train_reader:
    train_r.append(row)
random.shuffle(train_r)
for item in train_r:
    signature = item["signature"]
    signature = signature.replace(']', "")
    signature = signature.replace('[', "")
    signature_list = signature.split()
    signature_array = np.asarray(signature_list)
    
    signature_array = signature_array.astype(dtype=np.float64)
    signature_train_features.append(signature_array)
    signature_train_labels.append(item["dev_addr"])

test_file = open(test_file_name)
test_reader = csv.DictReader(test_file)

signature_test_features = []
signature_test_labels = []
test_r = []
for row in test_reader:
    test_r.append(row)
random.shuffle(test_r)
for item in test_r:
    signature = item["signature"]
    signature = signature.replace(']', "")
    signature = signature.replace('[', "")
    signature_list = signature.split()
    signature_array = np.asarray(signature_list)
    signature_array = signature_array.astype(dtype=np.float64)
    signature_test_features.append(signature_array)
    signature_test_labels.append(item["dev_addr"])

signature_train_features = np.asarray(signature_train_features)
signature_test_features = np.asarray(signature_test_features)
le = preprocessing.LabelEncoder()
le.fit(signature_train_labels)

signature_train_labels = le.transform(signature_train_labels)
signature_test_labels = le.transform(signature_test_labels)

count_arr = np.bincount(signature_train_labels)
print('Total occurences of "0" in train dataset: ', count_arr[0])
print('Total occurences of "1" in train dataset: ', count_arr[1])
print('Total occurences of "2" in train dataset: ', count_arr[2])


count_arr_test = np.bincount(signature_test_labels)
print('Total occurences of "0" in test dataset: ', count_arr_test[0])
print('Total occurences of "1" in test dataset: ', count_arr_test[1])
print('Total occurences of "2" in test dataset: ', count_arr_test[2])



models = [
          ('LogReg', LogisticRegression(multi_class='multinomial', max_iter=3000)), 
        # #   // 0.6197183098591549
          ('RF', RandomForestClassifier()), 
        # #   //0.647887323943662
            ('RF', RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42)), 
        #     # // 0.6338028169014085
          ('KNN', KNeighborsClassifier()), 
        # #   // 0.5633802816901409
            ('OVR, SVC', OneVsRestClassifier(LinearSVC(random_state=42))), 
        #     # // 0.6197183098591549
            ('OVO SVC', OneVsOneClassifier(LinearSVC(random_state=42))), 
        #     # // 0.6197183098591549
        #   ('SVM', SVC()), 
          ('GNB', GaussianNB()), 
        #   \\ 0.6197183098591549
        #   ('XGB', SGDClassifier())
            ]
results = []
names = []
dfs = []
df_results = pd.DataFrame()
scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
for name, model in models:

    clf = model.fit(signature_train_features, signature_train_labels)

    y_pred = clf.predict(signature_test_features)
    print(name)
    accuracy = clf.score(signature_test_features, signature_test_labels)
    print(accuracy)
    print(classification_report(signature_test_labels, y_pred))


