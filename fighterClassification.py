#gradient boost algorithm to classify fighters
import pandas as pd
from pandas.core.frame import treat_as_nested
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import requests





#load the data
df = pd.read_csv('cleanedFighterStatsClassifications.csv')
writer = open("cleanedFighterTrainingData.csv","w")
reader = open('cleanedFighterStatsClassifications.csv', "r")
for line in reader.readlines():
    line = line.strip().split(",")
    writer.write(",".join(line[:-1]) + "\n")


percent_columns = ["Str_Acc", "Str_Def", "TD_Acc", "TD_Def"]

for col in percent_columns:
    # Convert to string first, remove %, then cast to float
    df[col] = df[col].astype(str).str.replace('%', '', regex=False).astype(float)

numeric_columns = ["SLpM", "SApM", "TD_Avg", "Sub_Avg"]

for col in numeric_columns:
    df[col] = df[col].astype(float)

    
x = df[["SLpM","Str_Acc","SApM","Str_Def","TD_Avg","TD_Acc","TD_Def","Sub_Avg"]]
y = df['classification']
xTrain, xTest, yTrain, yTest = train_test_split(x,y, test_size =.8, random_state = 42)

classifier = GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, max_depth = 10)

classifier.fit(xTrain,yTrain)

predictions = classifier.predict(xTest)
accuracy = accuracy_score( yTest, predictions)
print(accuracy)

test_fighters = pd.DataFrame([
    [4.5, 55, 3.8, 70, 5.0, 90, 0, 0.5],
    [3.8, 50, 4.0, 65, 4.8, 85, 0, 0.6],
    [5.0, 60, 3.5, 68, 5.2, 88, 0, 0.7],
    [4.2, 52, 4.1, 72, 4.9, 82, 0, 0.5],
    [3.5, 48, 4.3, 70, 4.5, 80, 0, 0.4],
    [4.8, 55, 3.9, 75, 5.0, 86, 0, 0.6],
    [4.0, 50, 4.5, 68, 4.7, 84, 0, 0.5],
    [3.9, 53, 4.2, 70, 4.8, 82, 0, 0.4],
    [4.5, 57, 3.8, 72, 5.1, 85, 0, 0.6],
    [4.3, 54, 4.0, 68, 4.9, 83, 0, 0.5]
], columns=["SLpM","Str_Acc","SApM","Str_Def","TD_Avg","TD_Acc","TD_Def","Sub_Avg"])

# Predict with your classifier
predictions = classifier.predict(test_fighters)

for i, pred in enumerate(predictions, start=1):
    print(f"Fighter {i} predicted class: {pred}") 

