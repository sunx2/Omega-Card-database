import sqlite3
import json
items = {'type': [{'key': 'monster', 'value': '0x1'}, {'key': 'spell', 'value': '0x2'}, {'key': 'trap', 
'value': '0x4'}, {'key': 'normal', 'value': '0x10'}, {'key': 'effect', 'value': '0x20'}, {'key': 'fusion', 'value': '0x40'}, {'key': 'ritual', 'value': '0x80'}, {'key': 'trapmonster', 'value': '0x100'}, {'key': 'spirit', 'value': '0x200'}, {'key': 'union', 'value': '0x400'}, {'key': 'dual', 'value': '0x800'}, {'key': 'tuner', 'value': '0x1000'}, {'key': 'synchro', 'value': '0x2000'}, {'key': 'token', 'value': '0x4000'}, {'key': 'quickplay', 'value': '0x10000'}, {'key': 'continuous', 'value': '0x20000'}, {'key': 'equip', 'value': '0x40000'}, {'key': 'field', 'value': '0x80000'}, {'key': 'counter', 'value': '0x100000'}, {'key': 'flip', 'value': '0x200000'}, {'key': 
'toon', 'value': '0x400000'}, {'key': 'xyz', 'value': '0x800000'}, {'key': 'pendulum', 'value': 
'0x1000000'}, {'key': 'spsummon', 'value': '0x2000000'}, {'key': 'link', 'value': '0x4000000'}], 'race': [{'key': 'warrior', 'value': '0x1'}, {'key': 'spellcaster', 'value': '0x2'}, {'key': 'fairy', 'value': '0x4'}, {'key': 'fiend', 'value': '0x8'}, {'key': 'zombie', 'value': '0x10'}, {'key': 'machine', 'value': '0x20'}, {'key': 'aqua', 'value': '0x40'}, {'key': 'pyro', 'value': '0x80'}, {'key': 'rock', 'value': '0x100'}, {'key': 'windbeast', 'value': '0x200'}, {'key': 'plant', 'value': '0x400'}, {'key': 'insect', 'value': '0x800'}, {'key': 'thunder', 'value': '0x1000'}, {'key': 'dragon', 'value': '0x2000'}, {'key': 'beast', 'value': '0x4000'}, {'key': 'beastwarrior', 'value': '0x8000'}, {'key': 'dinosaur', 'value': '0x10000'}, {'key': 'fish', 'value': '0x20000'}, {'key': 'seaserpent', 'value': '0x40000'}, {'key': 'reptile', 'value': '0x80000'}, {'key': 'psycho', 'value': '0x100000'}, {'key': 'devine', 'value': '0x200000'}, {'key': 'creatorgod', 
'value': '0x400000'}, {'key': 'wyrm', 'value': '0x800000'}, {'key': 'cyberse', 'value': '0x1000000'}], 'attribute': [{'key': 'earth', 'value': '0x1'}, {'key': 'water', 'value': '0x2'}, {'key': 'fire', 'value': '0x4'}, {'key': 'wind', 'value': '0x8'}, {'key': 'light', 'value': '0x10'}, {'key': 'dark', 'value': '0x20'}, {'key': 'devine', 'value': '0x40'}], 'card': [{'key': 'card', 'value': '0x8'}, {'key': 'card', 'value': '0x40'}, {'key': 'rush', 'value': '0x80'}, {'key': 'errata', 'value': '0x100'}, {'key': 'mode', 'value': '0x200'}, {'key': 'links', 'value': '0x400'}, {'key': 'card', 'value': '0x800'}, {'key': 'zero', 'value': '0x10000'}],"category":[{'key': 'Speed Spell Card', 'value': '0x2'}, {'key': 'Boss Card', 'value': '0x4'}, {'key': 'Beta Card', 'value': '0x8'}, {'key': 'Action Card', 'value': '0x10'}, {'key': 'Command Card', 'value': '0x20'}, {'key': 'Double Script', 'value': '0x40'}, {'key': 'Rush Legendary', 'value': '0x80'}, {'key': 'Pre Errata', 'value': '0x100'}, {'key': 'DuelMode Card', 'value': '0x200'}, {'key': 'Duel Links', 'value': '0x400'}, {'key': 'Rush Card', 'value': '0x800'}, {'key': 'Start Card', 'value': '0x1000'}, {'key': 'One Card', 'value': '0x2000'}, {'key': 'Two Card', 'value': '0x4000'}, {'key': 'Three Card', 'value': '0x8000'}, {'key': 'Level Zero', 'value': '0x10000'}, {'key': 'Treated As', 'value': '0x20000'}]}


def get_types(type,lists):
    if lists not in ['attribute',"race"]:
        lists = "type"
    ret=[]
    for item in items[lists]:
        hexVal=int(item['value'],0)
        if type&hexVal==hexVal:
            ret.append(hex(hexVal))
    return ret



#get_type = lambda x : [ f'0x{int(y)*(10**list(reversed(hex(x).split("x")[1])).index(y))}' for y in hex(x).split("x")[1] if y!="0"]
def get_from_list(x,point):
    return [y["key"] for y in items[point] if y["value"] in get_types(x,point)]


def get_set_codes(setcode):
    ret = []
    while setcode > 0:
        ret.append(setcode & 0xFFFF)
        setcode = setcode >> 16
    return ret
def split_pendu_level(level):
  return [level&0xFFFF, (level>>16)&0xFF]


adr = {'0x8': 'Left', '0x4': 'BottomRight', '0x20': 'Right', '0x1': 'BottomLeft', '0x2': 'Bottom', '0x40': 'TopLeft', '0x80': 'Top', '0x100': 'TopRight'}
def get_link_marker(_def):
    ret=[]
    value = 0x01
    while value<=0x100:
        if value != 0x10:
            if _def&value==value:
                ret.append(value)
        value=value*2
    return [adr[hex(x)] for x in ret]


class DataBase(object):
    def __init__(self):
        self.db = sqlite3.connect("databases/OmegaDb.cdb")
        self.cursor = self.db.cursor()
        self.template = {
            "text": {
                "en": {
                    "name": None,
                    "desc":None,
                },
                "de":{
                    "name": None,
                    "desc":None,
                },
                "fr":{
                    "name": None,
                    "desc":None,
                },
                
                "es":{
                    "name": None,
                    "desc":None,
                },
                "it":{
                    "name": None,
                    "desc":None,
                },
                "ko":{
                    "name": None,
                    "desc":None,
                },
                "pt":{
                    "name": None,
                    "desc":None,
                },
                "ja":{
                    "name": None,
                    "desc":None,
                }
            },
            "ot":None,
            "alias":None,
            "archetype":[],
            "type":None,
            "atk":None,
            "def":None,
            "level":None,
            "race":None,
            "attribute":None,
            "category":None,
            "setid":'',
            "images":{
                "art":None,
                "small":None,
                "pic":None
            }
        }
        self.bigjson = {}
    def create_image_urls(self,id):
        return {
            "art":f"https://storage.googleapis.com/ygoprodeck.com/pics_artgame/{id}.jpg",
            "small":f"https://storage.googleapis.com/ygoprodeck.com/pics_small/{id}.jpg",
            "pic":f"https://storage.googleapis.com/ygoprodeck.com/pics/{id}.jpg"
        }
    def get_Text(self,id,lang):
        sql = f'''
        select desc from texts where id={id}
        ''' if lang=="en" else f'''
            select desc from {lang}_texts where id={id}
        '''
        pd = self.cursor.execute(sql)
        fg =  pd.fetchone()[0]
        return fg
    def get_all_archetype(self):
        sql = '''
        select betacode, name from setcodes
        '''
        d = self.cursor.execute(sql)
        archetype = {x[0]:x[1] for x in d.fetchall()}
        sql = '''
        select officialcode, name from setcodes
        '''
        d = self.cursor.execute(sql)
        for x in d.fetchall():
            archetype[x[0]] = x[1]
        return archetype
    def get_all_texts(self):
        sql = '''
        select
            id,
            texts.name as en_text,
            texts.desc as en_desc,
            fr_texts.name as fr_name,
            fr_texts.desc as fr_desc,
            de_texts.name as de_name,
            de_texts.desc as de_desc,
            es_texts.name as es_name,
            es_texts.desc as es_desc,
            it_texts.name as it_name,
            it_texts.desc as it_desc,
            pt_texts.name as pt_name,
            pt_texts.desc as pt_desc,
            ko_texts.name as ko_name,
            ko_texts.desc as ko_desc,
            ja_texts.name as ja_name,
            ja_texts.desc as ja_desc
            from texts left join fr_texts USING(id) left join de_texts USING(id)  left join es_texts USING(id) 
            left join it_texts USING(id)  left join pt_texts USING(id)   left join ko_texts USING(id)  left join ja_texts USING(id) ;
        '''
        d = self.cursor.execute(sql).fetchall()
        
        json.dump({x[0]:list(x)[1:] for x in d},open("datasets/texts.json",'w'))
        return {x[0]:list(x)[1:] for x in d}
        
    def get_all(self):
        arche = self.get_all_archetype()
        texts = self.get_all_texts()
        sql = "select id,ot,alias,setcode,type,atk,def,level,race,attribute,category,setid from datas"
        a = self.cursor.execute(sql).fetchall()
        for i in a:
            if int(i[0])<9000:
                continue
            try:
                d= {
            "text": {
                "en": {
                    "name": None,
                    "desc":None,
                },
                "de":{
                    "name": None,
                    "desc":None,
                },
                "fr":{
                    "name": None,
                    "desc":None,
                },
                "es":{
                    "name": None,
                    "desc":None,
                },
                "it":{
                    "name": None,
                    "desc":None,
                },
                "ko":{
                    "name": None,
                    "desc":None,
                },
                "pt":{
                    "name": None,
                    "desc":None,
                },
                "ja":{
                    "name": None,
                    "desc":None,
                }
            },
            
        }
                d["id"],d["ot"],d["alias"],d["archetype"],d["type"],d["attack"],d['defense'],d['level'],d['race'],d['attribute'],d['category'],d['setid'] = i
                for j in ["type","attribute","race","category"]:
                    d[j] = get_from_list(d[j],j)
                d["setid"] = d["setid"].split(",")
                if d["level"] > 20:
                    p = split_pendu_level(d['level'])
                    d['level'] = p[0]
                    d['pendulum-scale'] = p[1]
                if 'link' in d['type']:
                    d['link'] = d['level']
                elif 'xyz' in d['type']:
                    d['rank'] = d['level']
                if d['archetype'] == 0:
                    d['archetype'] = "Neutral"
                else:
                    try:
                        d['archetype'] = arche[d['archetype']]
                    except:
                        d['archetype'] = ','.join( [arche[x] for x in get_set_codes(d['archetype']) if x in arche.keys()])
                d['images'] = self.create_image_urls(d['id'])
                if "link" in d['type']:
                    d['linkarrows'] = get_link_marker(d['defense'])
                    d['defense'] = -2
                langs = ['en','fr', 'de', 'es', 'it', 'pt', 'ko', 'ja']
                for k in ['race','category','type','attribute']:
                    d[k] = ','.join(d[k])
                    if d[k] == "":
                        del d[k]
                if "monster" not in d['type']:
                    del d['attack']
                    del d['defense']
                    del d['level']
                for k in langs:
                    name = texts[d['id']][langs.index(k)*2]
                    descp = texts[d['id']][langs.index(k)*2+1]
                    if name != None:
                        d["text"][k]["name"] = name
                        d["text"][k]["desc"] = descp
                    else:
                        del d['text'][k]
                #for p in ['text',"images"]:
                    #d[p] = json.dumps(d[p])
                self.bigjson[d['id']] = d

            except Exception as e:
                print(f"error {e}")
                return

                
        return self.bigjson
    
    def get_banlist(self):
        banjson={}
        lists = {1:"TCG",2:"OCG",9:"DL",3:"WCS"}
        sql = "select * from bandatas"
        d = self.cursor.execute(sql).fetchall()
        for item in d:
            item = list(item)
            v = {
            "TCG": 3,
            "OCG":3,
            "DL": 3,
            "WCS":3
            }
            try:
                v[lists[item[1]]] = item[2]
                banjson[str(item[0])] =v
            except:
                pass
        return banjson








blobs = DataBase()
json.dump(blobs.get_all(),open("database/data.json",'w'),separators=(',',':'))
json.dump(blobs.get_banlist(),open("database/banlist.json","w"),separators=(',',':'))
