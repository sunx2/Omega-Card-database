import json

data = json.load(open("database/data.json"))
banlist = json.load(open('database/banlist.json'))
cards = list(data.keys())




for language in ["en","de","fr","es","it","ko","pt","ja"]:
    languagex = {}
    for i in cards:
        languagex[i] = data[i]
        languagex[i]['n'] = data[i]['text'][language]['name']
        languagex[i]["d"] = data[i]['text'][language]['name']
        del languagex[i]['text']
        del languagex[i]['images']
    json.dump(languagex,open(f"database/lang/data-{language}-min.json","w"),separators=(',',':'))


