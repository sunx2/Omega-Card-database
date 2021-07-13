import json

data = json.load(open("database/data.json"))
banlist = json.load(open('database/banlist.json'))
cards = list(data.keys())


massive = {}

for language in ["en","de","fr","es","it","ko","pt","ja"]:
    languagex = {}
    for i in cards:
        try:
            languagex[i] = data[i]
            try:
                languagex[i]['n'] = data[i]['text'][language]['name']
                languagex[i]["d"] = data[i]['text'][language]['desc']
            except:
                    languagex[i]['n'] = data[i]['text']["en"]['name']
                    languagex[i]["d"] = data[i]['text']["en"]['desc']
                    languagex['notrans'] = True
        except Exception as r:
            print(r,data[i]['text'].keys())
            break
    massive[language] = languagex


for language in ["en","de","fr","es","it","ko","pt","ja"]:
    for i in cards:
        try:
            del massive[language][i]['text']
            del massive[language][i]['images']
        except:
            break
    json.dump(massive[language],open(f"database/lang/data-{language}-min.json","w"),separators=(',',':'))


