import json
from nltk import wordpunct_tokenize as tokenizer
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--json', dest='json',
                        default='kvret_train_public.json',
                        help='process json file')
    args = parser.parse_args()

    with open(args.json) as f:
        dialogues = json.load(f)

    with open('kvret_entities.json') as f:
        entities_dict = json.load(f)

    #['distance','traffic_info','location', 'weather_attribute','temperature',"weekly_time", 'event', 'time','date','party','room','agenda']
    global_kb_type = entities_dict.keys().remove("poi")
    global_temp = []
    di = {}
    for e in global_kb_type:
        for p in map(lambda x: str(x).lower(), entities_dict[e]):       
            if "_" in p and p.replace("_"," ")!=p:
                di[p.replace("_"," ")] = p 
            else:
                if p!=p.replace(" ","_"):
                    di[p] = p.replace(" ","_")
    global_temp.append(di)

    for d in dialogues:
        
        if(d['scenario']['task']['intent']=="navigate"):
            print("#navigate#")
            temp = []
            names = {}
            for el in d['scenario']['kb']['items']:
                poi = " ".join(tokenizer(el['poi'].replace("'"," "))).replace(" ", "_").lower()
                slots = ['poi','distance','traffic_info','poi_type','address']
                for slot in slots:
                    el[slot] = " ".join(tokenizer(el[slot].replace("'"," "))).lower()
                names[el['poi']] = poi
                di = {
                    el['distance']: el['distance'].replace(" ", "_"),
                    el['traffic_info']: el['traffic_info'].replace(" ", "_"),
                    el['poi_type']: el['poi_type'].replace(" ", "_"),
                    el['address']: el['address'].replace(" ", "_"),}
                print("0 "+di[el['distance']]+" "+di[el['traffic_info']]+" "+di[el['poi_type']]+" poi "+poi)
                for slot in slots:
                    print("0 {} {} ".format(poi, slot)+di[el[slot]])
                temp.append(di)
            temp += global_temp

            if(len(d['dialogue'])%2 != 0):
                d['dialogue'].pop()
            
            j = 1
            for i in range(0,len(d['dialogue']),2):
                user = " ".join(cleaner(tokenizer(str(d['dialogue'][i]['data']['utterance']).lower())))
                bot = " ".join(cleaner(tokenizer(str(d['dialogue'][i+1]['data']['utterance']).lower())))
                bot, user = entity_replace(temp, bot, user, names) 
                nav_poi = ['address','poi','type']
                gold_entity = []
                for key in bot.split(' '):                    
                    for e in global_kb_type:
                        for p in map(lambda x: str(x).lower(), entities_dict[e]):      
                            if(key == p):
                                gold_entity.append(key)  
                            elif(key == str(p).replace(" ", "_")):
                                gold_entity.append(key)               
                    for e in entities_dict['poi']:
                        for p in nav_poi:
                            if(key == str(e[p]).lower()):
                                gold_entity.append(key)  
                            elif(key == str(e[p]).lower().replace(" ", "_")):
                                gold_entity.append(key)
                gold_entity = list(set(gold_entity))
                if bot!="" and user!="":
                    print(str(j)+" "+user+'\t'+bot+'\t'+str(gold_entity))
                    j+=1
            print("")

        elif (d['scenario']['task']['intent']=="weather"): 
            print("#weather#")
            temp = []
            print("0 today "+d['scenario']['kb']['items'][0]["today"])
            for el in d['scenario']['kb']['items']:
                for el_key in el.keys():
                    el[el_key] = " ".join(tokenizer(el[el_key])).lower()
                loc = el['location'].replace(" ", "_")
                di = {el['location']: loc}
                temp.append(di)
                days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
                for day in days:
                    print("0 "+loc+" "+day+" "+ el[day].split(',')[0].rstrip().replace(" ", "_"))
                    print("0 "+loc+" "+day+" "+ el[day].split(',')[1].split(" ")[1] +" "+el[day].split(',')[1].split(" ")[3])
                    print("0 "+loc+" "+day+" "+ el[day].split(',')[2].split(" ")[1] +" "+el[day].split(',')[2].split(" ")[3])
            temp += global_temp

            if(len(d['dialogue'])%2 != 0):
                d['dialogue'].pop()

            j = 1 
            for i in range(0,len(d['dialogue']),2):
                user = " ".join(cleaner(tokenizer(str(d['dialogue'][i]['data']['utterance']).lower())))
                bot = " ".join(cleaner(tokenizer(str(d['dialogue'][i+1]['data']['utterance']).lower())))
                bot, user = entity_replace(temp, bot, user) 
                gold_entity = []
                for key in bot.split(' '):                    
                    for e in global_kb_type:
                        for p in map(lambda x: str(x).lower(), entities_dict[e]):      
                            if(key == p):
                                gold_entity.append(key)  
                            elif(key == str(p).replace(" ", "_")):
                                gold_entity.append(key) 
                gold_entity = list(set(gold_entity))
                if bot!="" and user!="":
                    print(str(j)+" "+user+'\t'+bot+'\t'+str(gold_entity))
                    j+=1
            print("")

        elif (d['scenario']['task']['intent']=="schedule"): 
            print("#schedule#")
            temp = []
            names = {}
            if(d['scenario']['kb']['items'] != None):
                for el in d['scenario']['kb']['items']:
                    for el_key in el.keys():
                        el[el_key] = " ".join(tokenizer(el[el_key])).lower()
                    
                    ev = el['event'].replace(" ", "_")
                    names[el['event']] = ev
                    
                    slots = ['time','date','party','room','agenda']
                    di = {}
                    for slot in slots:
                        if el[slot]=="-":
                            continue
                        if slot == "time":
                            print("0 "+ev+" "+slot+" "+el[slot].replace(" ", ""))  
                            di[el[slot]] = el[slot].replace(" ", "")
                        else:
                            print("0 "+ev+" "+slot+" "+el[slot].replace(" ", "_"))  
                            di[el[slot]] = el[slot].replace(" ", "_")
                    temp.append(di)

            temp += global_temp

            if(len(d['dialogue'])%2 != 0):
                d['dialogue'].pop()

            j=1
            for i in range(0,len(d['dialogue']),2):
                user = " ".join(cleaner(tokenizer(str(d['dialogue'][i]['data']['utterance']).lower())))
                bot = " ".join(cleaner(tokenizer(str(d['dialogue'][i+1]['data']['utterance']).lower())))         
                bot, user = entity_replace(temp, bot, user, names)  
                gold_entity = []
                for key in bot.split(' '):                    
                    for e in global_kb_type:
                        for p in map(lambda x: str(x).lower(), entities_dict[e]):      
                            if(key == p):
                                gold_entity.append(key)  
                            elif(key == str(p).replace(" ", "_")):
                                gold_entity.append(key) 
                gold_entity = list(set(gold_entity))
                if bot!="" and user!="":
                    print(str(j)+" "+user+'\t'+bot+'\t'+str(gold_entity))
                    j+=1
            print("")


def entity_replace(temp, bot, user, names={}):   
    # change poi, location, event first
    global_rp = {
        "pf changs": "p_._f_._changs",
        "p f changs": "p_._f_._changs",
        "'": "",
        " re ": " are ",
        "restaurants": "restaurant",
        "activities": "activity",
        "appointments": "appointment",
        "doctors": "doctor",
        "doctor s": "doctor",
        "optometrist s": "optometrist",
        "conferences": "conference",
        "meetings": "meeting",
        "labs": "lab",
        "stores": "store",
        "stops": "stop",
        "centers": "center",
        "garages": "garage",
        "stations": "station",
        "hospitals": "hospital"
    }

    for grp in global_rp.keys():
        bot = bot.replace(grp, global_rp[grp])
        user = user.replace(grp, global_rp[grp])

    for name in names.keys():  
        if name in bot:
            bot = bot.replace(name, names[name])
        if name in user:
            user = user.replace(name, names[name]) 

    for e in temp:
        for wo in e.keys():
            inde = bot.find(wo)
            if(inde!=-1):
                bot = bot.replace(wo, e[wo]).replace('_drive','_dr')
            inde = user.find(wo)
            if(inde!=-1):
                user = user.replace(wo, e[wo]).replace('_drive','_dr')
    return bot, user


def cleaner(token_array):
    new_token_array = []
    for idx, token in enumerate(token_array):
        temp = token
        if token==".." or token=="." or token=="...": continue
        if (token=="am" or token=="pm") and token_array[idx-1].isdigit():
            new_token_array.pop()
            new_token_array.append(token_array[idx-1]+token)
            continue
        if token=="avenue": temp = "ave"
        if token=="heavey" and "traffic" in token_array[idx+1]: temp = "heavy"
        if token=="heave" and "traffic" in token_array[idx+1]: temp = "heavy"
        if token=="'": continue
        if token=="-" and "0" in token_array[idx-1]: 
            new_token_array.pop()
            new_token_array.append(token_array[idx-1]+"f")
            if "f" not in token_array[idx+1]:
                token_array[idx+1] = token_array[idx+1]+"f"
        new_token_array.append(temp)
    return new_token_array
