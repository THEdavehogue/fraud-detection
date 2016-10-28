from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
import random
random.seed(1)
from scrub_data_no_dummies import scrub_df
import cPickle as pickle

def roc_curve(probabilities, labels):
    '''
    INPUT: numpy array, numpy array
    OUTPUT: list, list, list
    Take a numpy array of the predicted probabilities and a numpy array of the
    true labels.
    Return the True Positive Rates, False Positive Rates and Thresholds for the
    ROC curve.
    '''

    thresholds = np.sort(probabilities)

    tprs = []
    fprs = []

    num_positive_cases = sum(labels)
    num_negative_cases = len(labels) - num_positive_cases

    for threshold in thresholds:
        # With this threshold, give the prediction of each instance
        predicted_positive = probabilities >= threshold
        # Calculate the number of correctly predicted positive cases
        true_positives = np.sum(predicted_positive * labels)
        # Calculate the number of incorrectly predicted positive cases
        false_positives = np.sum(predicted_positive) - true_positives
        # Calculate the True Positive Rate
        tpr = true_positives / float(num_positive_cases)
        # Calculate the False Positive Rate
        fpr = false_positives / float(num_negative_cases)

        fprs.append(fpr)
        tprs.append(tpr)

    return tprs, fprs, thresholds.tolist()

def build_model(df):
    y = df.pop('fraud').values
    X = df.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y)

    #Change model here
    #regressor = GradientBoostingClassifier(n_estimators=100)
    #regressor = AdaBoostClassifier(n_estimators=100)
    regressor = RandomForestClassifier(n_estimators=100)

    model = regressor.fit(X_train, y_train)
    print "Model score: ", model.score(X_test,y_test)
    print "ROC AUC score: ", roc_auc_score(y_test, model.predict(X_test))
    figure_text = "Accuracy: "+str(model.score(X_test,y_test)) + '\n' + '\n' + 'ROC AUC: ' + str(roc_auc_score(y_test, model.predict(X_test)))
    probabilities = model.predict_proba(X_test)[:, 1]

    tpr, fpr, thresholds = roc_curve(probabilities, y_test)

    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity, Recall)")
    plt.title("ROC plot of fraud data")
    plt.annotate(figure_text, xy=(1, 0), xycoords='axes fraction', fontsize=12,
                xytext=(-5, 5), textcoords='offset points',
                ha='right', va='bottom')
    plt.show()

    return model

if __name__ == '__main__':
    plt.style.use('ggplot')
    df = pd.read_json('data/data.json')
    df = scrub_df(df)
    model = build_model(df)

    with open("model_no_dummies.pkl", 'w') as f:
        pickle.dump(model, f)
