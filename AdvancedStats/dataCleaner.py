import pandas as pd

df = pd.read_csv("AdvancedStats/merged_stats_n_scorecards.csv")


# use to determine which cols need to be cleaned




OF_COLUMNS = {
    "red_fighter_sig_str",
    "blue_fighter_sig_str",
    "red_fighter_total_str",
    "blue_fighter_total_str",
    "red_fighter_TD",
    "blue_fighter_TD",
    "red_fighter_sig_str_head",
    "blue_fighter_sig_str_head",
    "red_fighter_sig_str_body",
    "blue_fighter_sig_str_body",
    "red_fighter_sig_str_leg",
    "blue_fighter_sig_str_leg",
    "red_fighter_sig_str_distance",
    "blue_fighter_sig_str_distance",
    "red_fighter_sig_str_clinch",
    "blue_fighter_sig_str_clinch",
    "red_fighter_sig_str_ground",
    "blue_fighter_sig_str_ground",
}

def clean_row(row):
    for col in row.index:

        val = row[col]

        if pd.isna(val):
            continue

        # Handle "X of Y"
        if col in OF_COLUMNS and isinstance(val, str):
            if " of " in val:
                row[col] = int(val.split(" of ")[0])
            elif val == "---":
                row[col] = 0

    return row

df = df.apply(clean_row, axis=1)
cols = list(df.columns)
for col in cols:
    df = df[df[col] != "---"]
    
df.to_csv("AdvancedStats/scoreCardTrainingData.csv", index=False)

STAT_NAMES = {
    "KD",
    "sig_str",
    "sig_str_pct",
    "total_str",
    "TD",
    "TD_pct",
    "sub_att",
    "sig_str_head",
    "sig_str_body",
    "sig_str_leg",
    "sig_str_distance",
    "sig_str_clinch",
    "sig_str_ground",
    "sig_str_head_pct",
    "sig_str_body_pct",
    "sig_str_leg_pct",
    "sig_str_distance_pct",
    "sig_str_clinch_pct",
    "sig_str_ground_pct"
}
df.replace({"-": 0, "---": 0}, inplace=True)



learningReady = pd.DataFrame()
learningReady["winner"] = df["red_fighter_result"]
learningReady["ref"] = df['referee']
for name in STAT_NAMES:
    red = "red_fighter_" + name
    blue = "blue_fighter_" + name
    df[red] = df[red].astype(float)
    df[blue] = df[blue].astype(float)
    learningReady["diff_" + name] = df[red] - df[blue]

feature_cols = [col for col in learningReady.columns if col.startswith("diff_")]

# keep only rows where at least one feature is non-zero
learningReady = learningReady[learningReady[feature_cols].any(axis=1)]

learningReady.to_csv("AdvancedStats/learningReadyData.csv", index=False)

    






