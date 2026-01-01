from fastapi import FastAPI
import uvicorn
from joblib import load
import pandas as pd
from pydantic import BaseModel
from typing import List
import os


base_dir = os.path.dirname(__file__)  # folder where the python file is
fighterClassifier = load(os.path.join(base_dir, "fighterClassifier.joblib"))
outcomeClassifier = load(os.path.join(base_dir, "outcomePredictor.joblib"))

app = FastAPI()


class OutcomeRequest(BaseModel):
    fighter1Name: str
    fighter2Name: str
    features: List[float]
    ref: str

@app.get("/")
def read_root():
    return "This is the model accessor API, used only for internal usage by shelling api"

@app.get("/fighterStylePercentage")
def fighterStylePercentage(fighterName: str, SLpM: float, Str_Acc: float, SApM: float, TD_Acc: float, TD_Def: float):
    X = pd.DataFrame([[SLpM, Str_Acc, SApM, TD_Acc, TD_Def]], 
                 columns=["SLpM", "Str_Acc", "SApM", "TD_Acc", "TD_Def"])
    X_new = X.iloc[[0]][['SLpM', 'Str_Acc', 'SApM', "TD_Acc","TD_Def"]]
    numerical_class = sum(([tree.predict(X_new)[0] for tree in fighterClassifier.estimators_]))/len(fighterClassifier.estimators_)
    return numerical_class


#'SLpM', 'Str_Acc', 'SApM', "TD_Acc","TD_Def"
@app.get("/classifyFighter")
def classifyFighter(fighterName: str, SLpM: float, Str_Acc: float, SApM: float, TD_Acc: float, TD_Def: float):
    X = pd.DataFrame([[SLpM, Str_Acc, SApM, TD_Acc, TD_Def]], 
                 columns=["SLpM", "Str_Acc", "SApM", "TD_Acc", "TD_Def"])
    prediction = (fighterClassifier.predict(X)[0])
    return "striker" if prediction == 1 else "grappler"

#potential that outcomes are reversed but could be due to model error
@app.post("/predictOutcome")
def predictOutcome(data: OutcomeRequest):
    X = pd.DataFrame([data.features], 
                 columns=["diff_KD","diff_sig_str","diff_sig_str_pct","diff_total_str","diff_TD",
                          "diff_TD_pct","diff_sub_att","diff_sig_str_head","diff_sig_str_body",
                          "diff_sig_str_leg","diff_sig_str_distance","diff_sig_str_clinch",
                          "diff_sig_str_ground","diff_sig_str_head_pct","diff_sig_str_body_pct",
                          "diff_sig_str_leg_pct","diff_sig_str_distance_pct","diff_sig_str_clinch_pct",
                          "diff_sig_str_ground_pct"])
    X['ref'] = data.ref
    prediction = outcomeClassifier.predict(X)[0]
    return data.fighter1Name if prediction == "W" else data.fighter2Name


if __name__ == "__main__":
    # host="0.0.0.0" allows access from other devices on the network if needed
    uvicorn.run("modelAccessor:app", host="127.0.0.1", port=8000, reload=True)
