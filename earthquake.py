import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
import pickle
warnings.filterwarnings("ignore")

data = pd.read_csv('earthquake_dataset.csv')
X = data.drop(['Richter Category', 'Mag', 'Depth(km)', 'City', 'Province', 'Distance(km)'], axis=1)
y = data['Richter Category']


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.30,random_state=0)
from sklearn.metrics import accuracy_score

gb_classifier = RandomForestClassifier(n_estimators=100)
gb_classifier.fit(X_train, y_train)

#make predictions and store data for later
y_pred_gb = gb_classifier.predict(X_test)

#get the accuracy score
acc_gb = round(accuracy_score(y_test,y_pred_gb)*100,2)

pickle.dump(gb_classifier, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))

print(f'Accuracy: {acc_gb}')