import pandas as pd


reader = open("cleanedFighterTrainingData.csv", "r")
writer = open("cleanedFighterFinalTrainingData.csv", "w")

writer.write("fighter_name,Height,Weight,Reach,Stance,DOB,SLpM,Str_Acc,SApM,Str_Def,TD_Avg,TD_Acc,TD_Def,Sub_Avg,classification\n")

#apply classification function to each fighter and create final cleaned fighter training data for model
import pandas as pd

# Step 1: Load the CSV file
df = pd.read_csv('cleanedFighterStatsClassifications.csv')  # replace with your filename

# Step 2: Create classification based on selected stats
# We'll classify as: striker, grappler, submission specialist
def classify_fighter(row):
    # Strong grappling signal
    if row['TD_Avg'] >= 2.0 and row['Sub_Avg'] >= 0.7:
        return 'grappler'
    
    # Strong striking signal
    if row['SLpM'] >= 3.5 and row['TD_Avg'] < 1.5:
        return 'striker'
    
    # Default: assign based on dominant tendency
    if row['TD_Avg'] > row['SLpM'] / 2:
        return 'grappler'
    else:
        return 'striker'

# Apply classification
df['classification'] = df.apply(classify_fighter, axis=1)



print(df["Sub_Avg"].mean())
print(df["TD_Avg"].mean())
print(df['classification'].value_counts())

i = 0;
for line in reader.readlines()[1:]:
    writer.write(line.strip() + "," + df['classification'].iloc[i] + '\n')
    i+=1
