import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
from joblib import dump

df = pd.read_csv("AdvancedStats/learningReadyData.csv")



features = ["diff_KD",
    "diff_sig_str",
    "diff_sig_str_pct",
    "diff_total_str",
    "diff_TD",
    "diff_TD_pct",
    "diff_sub_att",
    "diff_sig_str_head",
    "diff_sig_str_body",
    "diff_sig_str_leg",
    "diff_sig_str_distance",
    "diff_sig_str_clinch",
    "diff_sig_str_ground",
    "diff_sig_str_head_pct",
    "diff_sig_str_body_pct",
    "diff_sig_str_leg_pct",
    "diff_sig_str_distance_pct",
    "diff_sig_str_clinch_pct",
    "diff_sig_str_ground_pct", 'ref']

catFeatures = ['ref']
x = df[features]
y = df["winner"]
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=.2, random_state=42)


#catboost handles categorical features, could prove useful for referee encoding and other stats
classifier = CatBoostClassifier(iterations=500,
    depth=6,
    learning_rate=0.05,
    loss_function="Logloss",
    verbose=False)


classifier.fit(xTrain, yTrain, cat_features=catFeatures)


#determines the outcome of a fight based on the stats in the fight and the referee
predictions = classifier.predict(xTest)
accuracy = accuracy_score(yTest, predictions)
print(accuracy)

dump(classifier, 'outcomePredictor.joblib')

