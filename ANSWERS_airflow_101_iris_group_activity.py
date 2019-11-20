#####################################################################################
#
#
# 	Airflow 101 Group Activity: WMP_ML_iris_group_activity 
#  
#	Author: Sam Showalter 
#	Date: 10-29-2019
#
#####################################################################################


#####################################################################################
# External Library and Module Imports
#####################################################################################

# System and OS
import os
import sys
# Airflow DAG
from airflow import DAG
#Airflow Operators
from airflow.operators.python_operator import PythonOperator

#Datetime information
from datetime import datetime, timedelta

## Import pandas
import pandas as pd

## Load iris data from sklearn
from sklearn.datasets import load_iris

## Import statements for Sklearn train_test_split
from sklearn.model_selection import train_test_split

## Import statements for SKLEARN.LINEAR_MODEL.LOGISTIC
from sklearn.linear_model.logistic import LogisticRegression

## Import statements for SKLEARN.METRICS.CLASSIFICATION
from sklearn.metrics.classification import accuracy_score


#####################################################################################
# Core functionality
#####################################################################################

def read_iris_data_operation(params, dag, **kwargs):

	ti = kwargs['ti']

	df = pd.DataFrame(load_iris().data, columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"])
	df['flower_label'] = load_iris().target

	ti.xcom_push(key = 'data', value = df)

def fit_operation(params, dag, **kwargs):
	#if not _is_fitted(params['model']):
	ti = kwargs['ti']

	X_train = ti.xcom_pull(key = "X_train")
	y_train = ti.xcom_pull(key = "y_train")

	model = params['model'](**params['params'])
	model.fit(X_train, y_train)

	return model

def impute_median_operation(params, dag, **kwargs):
	#if not _is_fitted(params['model']):
	ti = kwargs['ti']

	
	data = ti.xcom_pull(key = "data")

	data = data.fillna(data.median())

	ti.xcom_push(key = 'preprocessed_data', value = data)

def predict_operation(params, dag, **kwargs):
	ti = kwargs['ti']

	X_test = ti.xcom_pull(key = "X_test")

	model = ti.xcom_pull(task_ids = params['model'])
	
	predictions = model.predict(X_test)

	return predictions

def evaluation_operation(params, dag, **kwargs):

	ti = kwargs['ti']

	preds = ti.xcom_pull(task_ids = params['model_id'])
	y_test = ti.xcom_pull(key = 'y_test')

	return params['func'](y_test, preds, **params['params'])

def split_operation(params, dag, **kwargs):

	ti = kwargs['ti']

	data = ti.xcom_pull(key = 'preprocessed_data')

	train = data.loc[:,data.columns != params['target']]
	test = data.loc[:,params['target']]

	X_train, X_test, y_train, y_test = train_test_split(train,test, **params['params'])

	ti.xcom_push(key = 'X_train', value = X_train)
	ti.xcom_push(key = 'y_train', value = y_train)
	ti.xcom_push(key = 'X_test', value = X_test)
	ti.xcom_push(key = 'y_test', value = y_test)

#####################################################################################
# DAG Construction
#####################################################################################

default_args = {
    "owner": "Sam Showalter",
    "depends_on_past": False,
    "email": [
        "sshowalter@wmp.com"
    ],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "op_args": {},
    "op_kwargs": {},
    "params": {}
}

dag = DAG( 'WMP_ML_iris_group_activity', 
		   default_args=default_args,
		   start_date = datetime.today(), 
		   schedule_interval='@once')

#####################################################################################
# Operators Construction
#####################################################################################




iris_demo_csv_read_csv = PythonOperator( 
							task_id='iris_demo_csv_read_csv',
							provide_context=True,
							python_callable=read_iris_data_operation,
							params = {},
							dag=dag)

impute_median_operation = PythonOperator( 
							task_id='impute_median_operation',
							provide_context=True,
							python_callable=impute_median_operation,
							params = {},
							dag = dag)			

sklearn_train_test_split = PythonOperator( 
							task_id='sklearn_train_test_split',
							provide_context=True,
							python_callable=split_operation,
							params = {'func': train_test_split,
							'target': 'flower_label',
							 'params': {'random_state': 42, 'test_size': 0.25}},
							dag = dag)

					
LOG_fit = PythonOperator( 
							task_id='LOG_fit',
							provide_context=True,
							python_callable=fit_operation,
							params = {'model': LogisticRegression,
							 'params': {}},
							dag = dag)

					
LOG_predict = PythonOperator( 
							task_id='LOG_predict',
							provide_context=True,
							python_callable=predict_operation,
							params = {'model': 'LOG_fit', 'params': {}},
							dag = dag)


LOG_predict_acc = PythonOperator( 
							task_id='LOG_predict_acc',
							provide_context=True,
							python_callable=evaluation_operation,
							params = {'func': accuracy_score,
							 'model_id': 'LOG_predict',
							 'params': {}},
							dag = dag)

					

#####################################################################################
# Associate operators
#####################################################################################


iris_demo_csv_read_csv >> impute_median_operation >> sklearn_train_test_split >> LOG_fit
LOG_fit >> LOG_predict
LOG_predict >> LOG_predict_acc
