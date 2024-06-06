# -*- coding: utf-8 -*-
"""TP_de_ML_RENOUX_Mathis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bn6kFp6K5BFs_6CgswSfUw8Y2l5J8dZt
"""

import pandas as pd
import matplotlib
import seaborn as sns

df=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/dataset.csv")
df.head()

print(len(df.columns))

"""Il y a 27 colonnes qu'on peu lire au dessus."""

print(len(df.index))

"""Il y a 55702 entrées"""

df=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/dataset.csv",on_bad_lines='skip')
df.isnull().sum()

"""il y a 12 badlines"""

df.describe()

fumeurs = df[df['smoking'] == 1]

print("la moyenne d'age des fumeur est")
print(fumeurs['age'].mean())
print("la moyenne de poid des fumeurs est")
print(fumeurs['weight(kg)'].mean())
print("la moyenne de taille des fumeurs est")
print(fumeurs['height(cm)'].mean())

print("la moyenne de taille des fumeurs est")
print(fumeurs['height(cm)'].mean())

df.describe()

"""l'écart type de l'hemoglobine est 1.564476.

y'a un gars qui a 40000 ans
"""

df[df['age'] > 85]

import matplotlib.pyplot as plt
fumeur_counts = df['smoking'].value_counts()

plt.figure(figsize=(8, 8))
fumeur_counts.plot.pie(autopct= '%1.1f%%', startangle=90, colors=['red', 'lightgreen'])
plt.title(' Fumeurs vs Non-Fumeurs')
plt.ylabel('')
plt.show()

h_fumeurs = fumeurs[fumeurs['gender'] == 'M']
f_fumeurs = fumeurs[fumeurs['gender'] == 'F']

fumeur_gender = fumeurs['gender'].value_counts()

plt.figure(figsize=(8, 6))
fumeur_gender.plot(kind='bar' )
plt.title('Nombre de Fumeurs par Sexe')
plt.xlabel('gender')
plt.ylabel('Nombre de Fumeurs')
plt.xticks(rotation=40)

h_fumeurs['age'].mean()

corr=df.corr()
sns.heatmap(corr)

"""
y'a des string dans les valeur du tableau.

"""

corr=df.corr()
sns.heatmap(corr)

print(df.dtypes)



"""j'ai choisie de suprimer les colones manquantes mais. Mais ca rend la matrices incomplete"""

from sklearn.preprocessing import OneHotEncoder
df=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/dataset.csv")

num_colon = df.select_dtypes(include=['float64', 'int64']).columns
lettre = df.select_dtypes(include=['object']).columns
encoder = OneHotEncoder(sparse=False)
encoded_categorical = encoder.fit_transform(df[lettre])
encoded_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(lettre))
dfenco = pd.concat([df[num_colon], encoded_df], axis=1)
correlation_matrix = dfenco.corr()
plt.figure(figsize=(27, 27))
sns.heatmap(correlation_matrix, annot=True , cmap='coolwarm',linewidths=0.5, linecolor='Black' )

dfenco.head()

df2=dfenco.dropna()

from sklearn.linear_model import LogisticRegression

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

X = df2.drop('smoking',axis=1)
y = df2['smoking']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

from sklearn.metrics import classification_report

clf = LogisticRegression(random_state = 0, solver = 'saga', max_iter=100).fit(X_train, y_train)

clf.score(X_test,y_test)

clf = LogisticRegression(random_state = 0, solver = 'lbfgs', max_iter=200).fit(X_train, y_train)
clf.score(X_test,y_test)

clf = LogisticRegression(random_state = 58,C= 100, solver = 'liblinear', max_iter=200).fit(X_train, y_train)
clf.score(X_test,y_test)

from sklearn.model_selection import GridSearchCV
param_grid_lr = {
    'C': [0.01, 0.1, 1, 10, 100],
    'max_iter': [100, 200, 300],
    'solver': ['liblinear', 'lbfgs']
}

# Créer une instance de LogisticRegression et GridSearchCV
model_lr = LogisticRegression()
grid_search_lr = GridSearchCV(estimator=model_lr, param_grid=param_grid_lr, cv=5, scoring='accuracy')

# Effectuer la recherche sur grille
grid_search_lr.fit(X_train, y_train)

# Afficher les meilleurs paramètres trouvés et la précision
print("Best parameters for Logistic Regression: ", grid_search_lr.best_params_)
best_model_lr = grid_search_lr.best_estimator_
y_pred_lr = best_model_lr.predict(X_test)
print(f"Logistic Regression Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")

"""apres avoir testé  
Best parameters for Logistic Regression:  {'C': 10, 'max_iter': 100, 'solver': 'liblinear'}

Logistic Regression Accuracy: 0.7184
"""

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train, y_train)
y_pred=knn.predict(X_test)
confusion_mat_result = confusion_matrix(y_pred, y_test)

accuracy_score(y_test, y_pred)

# Définir les hyperparamètres à tester pour K-NN
param_grid_knn = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

# Créer une instance de KNeighborsClassifier et GridSearchCV
knn2 = KNeighborsClassifier()
grid_search_knn = GridSearchCV(estimator=knn2, param_grid=param_grid_knn, cv=5, scoring='accuracy')

# Effectuer la recherche sur grille
grid_search_knn.fit(X_train, y_train)

# Afficher les meilleurs paramètres trouvés et la précision
print("Best parameters for K-NN: ", grid_search_knn.best_params_)
best_model_knn = grid_search_knn.best_estimator_
y_pred_knn = best_model_knn.predict(X_test)
print(f"K-NN Accuracy: {accuracy_score(y_test, y_pred_knn):.4f}")

"""les fonctions sont tres longue à faire tourner alors j'ecrit ici ce qu'elles renvoient :

Best parameters for K-NN:  {'metric': 'manhattan', 'n_neighbors': 9, 'weights': 'distance'}

K-NN Accuracy: 0.6770
"""



from sklearn import tree
DT = tree.DecisionTreeClassifier()

DT.fit(X_train, y_train)
y_pred=DT.predict(X_test)

accuracy_score(y_test, y_pred)

# Définir les hyperparamètres à tester pour l'arbre de décision
param_grid_dt = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Créer une instance de DecisionTreeClassifier et GridSearchCV
model_dt = tree.DecisionTreeClassifier()
grid_search_dt = GridSearchCV(estimator=model_dt, param_grid=param_grid_dt, cv=5, scoring='accuracy')

# Effectuer la recherche sur grille
grid_search_dt.fit(X_train, y_train)

# Afficher les meilleurs paramètres trouvés et la précision
print("Best parameters for Decision Tree: ", grid_search_dt.best_params_)
best_model_dt = grid_search_dt.best_estimator_
y_pred_dt = best_model_dt.predict(X_test)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, y_pred_dt):.4f}")

"""Run time : 3min50

Best parameters for Decision Tree:  {'criterion': 'entropy', 'max_depth': None, 'min_samples_leaf': 1, 'min_samples_split': 2}

Decision Tree Accuracy: 0.7742

On remarque que changer les hyperparametre n'ameliore pas beaucoup, mais que les decisions tree sont plus accurate que les autres modèles testé.
"""

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier()
gb.fit(X_train, y_train)
y_pred=gb.predict(X_test)
accuracy_score(y_test, y_pred)

# Définir les hyperparametres à tester pour Gradient Boosting
param_grid_gb = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}

# Créer une instance de GradientBoostingClassifier et GridSearchCV
model_gb = GradientBoostingClassifier()
grid_search_gb = GridSearchCV(estimator=model_gb, param_grid=param_grid_gb, cv=5, scoring='accuracy')

# Effectuer la recherche sur grille
grid_search_gb.fit(X_train, y_train)

# Afficher les meilleurs paramètres trouvés et la précision
print("Best parameters for Gradient Boosting: ", grid_search_gb.best_params_)
best_model_gb = grid_search_gb.best_estimator_
y_pred_gb = best_model_gb.predict(X_test)
print(f"Gradient Boosting Accuracy: {accuracy_score(y_test, y_pred_gb):.4f}")

"""ici le modele est encore meilleurs et jouer avec les hyper parametre apporte des amélioration scinificatives

Best parameters for Gradient Boosting:  {'learning_rate': 0.2, 'max_depth': 7, 'n_estimators': 200}

Gradient Boosting Accuracy: 0.8057

on vas maintenant relancer chaque algo avec les meilleurs hyper parametres pour en étudier l'acuracy la precision le f1 score les faux positif et le recall
"""

from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

gb = GradientBoostingClassifier(learning_rate = 0.2, max_depth = 7, n_estimators = 200)
gb.fit(X_train, y_train)
y_pred_gb=gb.predict(X_test)

accuracy_gb = accuracy_score(y_test, y_pred_gb)
precision_gb = precision_score(y_test, y_pred_gb, average='weighted')
recall_gb = recall_score(y_test, y_pred_gb, average='weighted')
f1_gb = f1_score(y_test, y_pred_gb, average='weighted')
cm_gb = confusion_matrix(y_test, y_pred_gb)
false_positives_gb = cm_gb.sum(axis=0) - np.diag(cm_gb)

print(f"Gradient Boosting - Accuracy: {accuracy_gb:.4f}, Precision: {precision_gb:.4f}, Recall: {recall_gb:.4f}, F1 Score: {f1_gb:.4f}, False Positives: {false_positives_gb}")

"""Gradient Boosting - Accuracy: 0.8027, Precision: 0.8035, Recall: 0.8027, F1 Score: 0.8031, False Positives: [1058 1140]"""

dt = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = None, min_samples_leaf = 1, min_samples_split = 2)
dt.fit(X_train, y_train)
y_pred_dt=dt.predict(X_test)

accuracy_dt = accuracy_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt, average='weighted')
recall_dt = recall_score(y_test, y_pred_dt, average='weighted')
f1_dt = f1_score(y_test, y_pred_dt, average='weighted')
cm_dt = confusion_matrix(y_test, y_pred_dt)
false_positives_dt = cm_dt.sum(axis=0) - np.diag(cm_dt)

print(f"Decision Tree - Accuracy: {accuracy_dt:.4f}, Precision: {precision_dt:.4f}, Recall: {recall_dt:.4f}, F1 Score: {f1_dt:.4f}, False Positives: {false_positives_dt}")

"""Decision Tree - Accuracy: 0.7774, Precision: 0.7761, Recall: 0.7774, F1 Score: 0.7766, False Positives: [1304 1176]"""

knn = KNeighborsClassifier(metric = 'manhattan', n_neighbors = 9, weights = 'distance')
knn.fit(X_train, y_train)
y_pred_knn=knn.predict(X_test)

accuracy_knn = accuracy_score(y_test, y_pred_knn)
precision_knn = precision_score(y_test, y_pred_knn, average='weighted')
recall_knn = recall_score(y_test, y_pred_knn, average='weighted')
f1_knn = f1_score(y_test, y_pred_knn, average='weighted')
cm_knn = confusion_matrix(y_test, y_pred_knn)
false_positives_knn = cm_knn.sum(axis=0) - np.diag(cm_knn)

print(f"Knn - Accuracy: {accuracy_knn:.4f}, Precision: {precision_knn:.4f}, Recall: {recall_knn:.4f}, F1 Score: {f1_knn:.4f}, False Positives: {false_positives_knn}")

"""Knn - Accuracy: 0.6770, Precision: 0.6653, Recall: 0.6770, F1 Score: 0.6639, False Positives: [2357 1241]"""

lr = LogisticRegression(C = 10, max_iter=100, solver='liblinear')
lr.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred_lr = lr.predict(X_test)

# Calculer les métriques
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr, average='weighted')
recall_lr = recall_score(y_test, y_pred_lr, average='weighted')
f1_lr = f1_score(y_test, y_pred_lr, average='weighted')
cm_lr = confusion_matrix(y_test, y_pred_lr)
false_positives_lr = cm_lr.sum(axis=0) - np.diag(cm_lr)

print(f"Logistic Regression - Accuracy: {accuracy_lr:.4f}, Precision: {precision_lr:.4f}, Recall: {recall_lr:.4f}, F1 Score: {f1_lr:.4f}, False Positives: {false_positives_lr}")

"""Logistic Regression - Accuracy: 0.7184, Precision: 0.7119, Recall: 0.7184, F1 Score: 0.7120, False Positives: [1925 1212]

On constate donc que l'algorythme qui obtien les meilleur resultats est l'algorythme de gradient boosting avec plus de 80% d'accuracy de precision de recall et de F1 score.
"""