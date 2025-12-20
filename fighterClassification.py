#gradient boost algorithm to classify fighters
import pandas as pd
from pandas.core.frame import treat_as_nested
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
from joblib import dump


# Suppress all warnings
warnings.filterwarnings("ignore")


#load the data
df = pd.read_csv('cleanedFighterFinalTrainingData.csv')

#some columns represent percentages --> convert to a proper numerical format
percent_columns = ["Str_Acc", "Str_Def", "TD_Acc", "TD_Def"]

for col in percent_columns:
    # Convert to string first, remove %, then cast to float
    df[col] = df[col].astype(str).str.replace('%', '', regex=False).astype(float)

numeric_columns = ["SLpM", "SApM", "TD_Avg", "Sub_Avg"]

for col in numeric_columns:
    df[col] = df[col].astype(float)




allFeatures = [
    "SLpM","Str_Acc","SApM","Str_Def","TD_Avg","TD_Acc","TD_Def","Sub_Avg",
]

new_features = ['SLpM', 'Str_Acc', 'SApM', "TD_Acc","TD_Def"]

#converts classifications from training data into numerical format
def numerical(row):
    if(row['classification'] == 'grappler'):
        return 0
    else:
        return 1


df['classification'] = df.apply(numerical, axis=1)

x = df[new_features]
y = df['classification']

xTrain, xTest, yTrain, yTest = train_test_split(x,y, test_size =.2, random_state = 42)

classifier = RandomForestClassifier(n_estimators=500, max_depth = 5, min_samples_leaf=5,random_state=42)

classifier.fit(xTrain,yTrain)

predictions = classifier.predict(xTest)
accuracy = accuracy_score(yTest, predictions)
print(accuracy)

dump(classifier, 'fighter_classifier_model.joblib')

#code to measure if a fighter is more of a grappler than a striker or vice versa
'''
for i in range(len(df['classification'])):
    X_new = df.iloc[[i]][new_features]
    numerical_class = sum(([tree.predict(X_new)[0] for tree in classifier.estimators_]))/len(classifier.estimators_)
    print(f"Fighter lean score: {numerical_class} vs classification: {df.iloc[[i]]['classification'].values[0]}")
'''
