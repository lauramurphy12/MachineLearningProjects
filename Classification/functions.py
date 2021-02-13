import plotly.graph_objects as go
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.classifier import ClassificationReport

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn import metrics

def class_distribution(df, label, title, x_labels):
	counts = df[label].value_counts()
	print(counts)
	
	sns.set(rc={'figure.figsize':(11.7,8.27),
            'axes.labelsize':25,
            'xtick.labelsize':20,
            'ytick.labelsize':20})
			
	cplot = sns.countplot(df[label])
	cplot.set_xticklabels(x_labels)
	plt.show()

	labels = df[label].value_counts().keys().tolist()
	values = df[label].value_counts().values.tolist()
	colors = ['rgb(17, 98, 182)', 'rgb(164, 58, 100)']
	pie_figure = go.Figure(data=[go.Pie(labels=labels, 
              values= values,
              marker_colors=colors                            
    )]) 
	pie_figure.update_layout(
		title= title,
		font=dict(
			family="Courier New, monospace",
			size=20,
			color="#7f7f7f"
		)
	)
	pie_figure.show()

def mult_var_counts(label, hue_value, df):
	sns.set(rc={'figure.figsize':(11.7,8.27),
            'axes.labelsize':25,
            'xtick.labelsize':20,
            'ytick.labelsize':20})

	ax = sns.countplot(x=label, hue=hue_value, data=df)
	plt.setp(ax.get_legend().get_texts(), fontsize='22')
	plt.show()

def one_hot_encode(df, feature, prefix):
	ohe_df = pd.get_dummies(df.feature, prefix=prefix)
	df = df.drop(feature, axis=1)
	df = df.join(ohe_df)
	return df

def model_accuracy_df(features, labels, ml_models, classes):
	accuracies = []
	model_names = []
	for ml_name, ml_model in ml_models:
		model_names.append(ml_name)
		print(ml_model)
		X_train, X_test, y_train, y_test = train_test_split(
		features, labels, test_size=0.20, random_state=42, stratify=labels,
		)
		ml_model.fit(X_train, y_train)
		ml_pred = ml_model.predict(X_test)
		#np.sum(predictions==y_test)/len(y_test)
		
		visualizer = ClassificationReport(ml_model, classes=classes, support=True)
		visualizer.fit(X_train, y_train)      
		visualizer.score(X_test, y_test)       
		visualizer.show()
		
		ml_accuracy = metrics.accuracy_score(y_test, ml_pred)
		accuracies.append(ml_accuracy)
		precision = metrics.precision_score(y_test, ml_pred)
		recall = metrics.recall_score(y_test, ml_pred)
		f1 = metrics.f1_score(y_test, ml_pred)
			
	horizontal_bar(accuracies, model_names)

def horizontal_bar(metrics, model_names):
	fig = go.Figure(go.Bar(
            x=metrics,
            y=model_names,
            orientation='h'
			))
	fig.update_layout(title_text='Classification Model Accuracy')
	fig.show()
	
def generate_confusion_matrix(test_values, predicted_values, title):	
	cnf_matrix = pd.crosstab(test_values, predicted_values, rownames=['Actual'], colnames=['Predicted'])
	matrix_states = ['True Negative', 'False Positive', 'False Negative', 'True Positive']
	counts = cnf_matrix.values.flatten()
	labels = [f'{v1}\n{v2}' for v1, v2 in zip(matrix_states, counts)]
	labels = np.asarray(labels).reshape(2,2)
	plt.figure(figsize=(10, 8))
	plt.title(title)
	return sns.heatmap(cnf_matrix, fmt='', annot=labels, annot_kws={"fontsize":15})