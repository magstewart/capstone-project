import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import log_loss, confusion_matrix
#import pipeline
import pickle

class Model():
    def __init__(self, model_type, **kwargs):
        '''
        Instantiates the model.

        Input:
        ------
        model_type: string specifying the type of model to be used:
                    'gbc': Gradient Boosting Classifier
                    'logistic' : Logistic Regression
                    'rf': Random Forest
        kwargs: Key word arguments for model hyperparameters

        Output:
        -------
        None
        '''
        self.type = model_type
        if self.type == 'gbc':
            self.model = GradientBoostingClassifier(**kwargs)
        self.fit_model = None

    def fit(self, X, y):
        '''
        Takes in numpy array of features and a numpy array of labels
        and and returns a probability prediction

        Input:
        ------
        X: numpy array of features
        y: numpy array of labels

        Output:
        -------
        None
        '''
        self.fit_model = self.model.fit(X,y)

    def predict(self, X, staged=False):
        '''
        Takes in numpy array of features and returns a probability prediction
        for the positive class

        Input:
        ------
        X: numpy array of features

        Output:
        -------
        y: numpy array predicted probabilities
        '''
        return self.fit_model.predict_proba(X)[:,1]

    def cross_validate(self, n_folds, X, y, stages=False):
        '''
        Performs n_fold cross-validation on the model.
        Returns arrays of model metrics

        Input:
        ------
        n_folds: number of cross-validation folds
        X: numpy array of features
        y: numpy array of labels
        stages: if True, perform staged predictions

        Output:
        -------
        loss: numpy array containing the final log-loss of each fold
        loss_optimal: numpy array of the log-loss at the optimal_n_trees f
                      or each fold
        staged_loss: numpy array of log_loss for the staged_predict_proba
        optimal_n_trees: numpy array of optimal n_trees for each fold
        '''
        loss = []
        loss_optimal_n_all_folds = []
        optimal_n_trees_all_folds = []
        staged_loss_all_folds = []
        kf = KFold(n_splits=n_folds, random_state=225, shuffle=True)
        fold = 1
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            self.fit(X_train, y_train)
            predictions = self.predict(X_test)
            fold_loss = log_loss(y_test, predictions)
            loss.append(fold_loss)

            if stages:
                staged_loss, optimal_n_trees, loss_optimal = self.staged_predictions(X_test)
                staged_loss_all_folds.append(staged_loss)
                optimal_n_trees_all_folds.append(optimal_n_trees)
                loss_optimal_n_all_folds.append(loss_optimal)

                print("fold: {}, optimal number of trees: {}, \
                log-loss at n_optimal: {:.2f}, final log-loss: {:.2f}".format(
                    fold, optimal_n_trees, loss_optimal, fold_loss))
            else:
                print("fold: {}, log-loss: {:.2f}".format(fold, fold_loss))

            fold +=1
        return loss, loss_optimal_n_all_folds, staged_loss_all_folds, optimal_n_trees_all_folds

    def staged_predictions(self, X_test, y_test):
        '''
        Performs n_fold cross-validation on the model.
        Returns arrays

        Input:
        ------
        X_test: numpy array of features
        y_test: numpy array of labels

        Output:
        -------
        staged_loss: numpy array of the log-loss at each stage
        optimal_n_trees: optimal number of tress based on log-loss
        loss_optimal: log-loss calculated at the optimal number of trees
        '''
        staged_loss = np.zeros(len(self.fit_model.estimators_))
        staged_preds = self.fit_model.staged_predict_proba(X_test)
        for i, preds in enumerate(staged_preds):
            staged_loss[i] = log_loss(y_test, preds[:,1])
        optimal_n_trees = np.argmin(staged_loss)
        loss_optimal = staged_loss[optimal_n_trees][fold-1]
        return staged_loss, optimal_n_trees, loss_optimal

    def final_model(self, X, y):
        '''
        Performs n_fold cross-validation on the model.
        Returns arrays

        Input:
        ------
        n_folds: number of cross-validation folds

        Output:
        -------
        None
        '''
        self.fit_model = self.model.fit(X,y)
        with open('model.pkl', 'wb') as f:
            pickle.dump(self.fit_model, f)