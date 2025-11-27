import requests

url = "http://localhost:11434/api/generate"
reader = open("cleanedFighterTrainnigData.csv", "r")
writer = open("cleanedFighterFinalTrainingData.csv", "w")
#dont use the name stick to above prompt since llm is limited on ufc info
for line in reader.readlines()[:5]:
    fighter = line.strip().split(",")[7:-1]  
    print(fighter)
    '''
    payload = {
        "model": "gemma3:4b",
        "prompt": "Classify the ufc fighter that is given by the following stats that follow the format (SLpM,Str_Acc,SApM,Str_Def,TD_Avg,TD_Acc,TD_Def,Sub_Avg) as either a submission specialist, striker, or grappler: {fighter}. Return one of the following three strings as your answer: 'submission specialist', 'striker', 'grappler'",
        "stream": False
    }

    response = requests.post(url, json=payload)
    data = response.json()
    
    print(data)
    '''