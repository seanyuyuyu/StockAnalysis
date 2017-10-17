#!/usr/bin/python  
# coding: UTF-8  

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.preprocessing import scale
from sklearn.cross_validation import train_test_split
from sklearn import neighbors,linear_model


if __name__ == '__main__':  

	data=pd.read_excel('newstock.xlsx')

	x=data.drop(u'新股名称',1)
	x=x.drop(u'涨停数',1)
	x=x.drop(u'破板涨幅',1)
	X=x.values

	X=scale(X)

	y=data[u'涨停数'].values

	X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

	knn=neighbors.KNeighborsClassifier(n_neighbors=5)
	knn_model=knn.fit(X_train,y_train)

	y_true,y_pred=y_test,knn_model.predict(X_test)
	print knn_model.score(X_test,y_test)
	print classification_report(y_true,y_pred)