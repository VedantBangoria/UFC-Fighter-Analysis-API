import requests

url = "http://localhost:11434/api/generate"
prompt = "Classify the ufc fighter that is given by the following stats that follow the format (SLpM,Str_Acc,SApM,Str_Def,TD_Avg,TD_Acc,TD_Def,Sub_Avg) as either a submission specialist, striker, or grappler: {fighter}. Return one of the following three strings as your answer: 'submission specialist', 'striker', 'grappler'"

#dont use the name stick to above prompt since llm is limited on ufc info
fighter = ("2.80","55%","3.15","48%","3.47","57%","50%","1.3")
payload = {
    "model": "gemma3:4b",
    "prompt": "is Goran Reljic the ufc fighter a striker, grappler, or submission specialist. Return one of the following three strings as your answer: 'submission specialist', 'striker', 'grappler'",
    "stream": False
}

response = requests.post(url, json=payload)
data = response.json()

print(data)