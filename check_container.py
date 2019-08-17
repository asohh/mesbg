import pandas as pd
import couchdb

import glob


import glob, os
files = []
os.chdir("./lists")
for file in glob.glob("*.xlsx"):
    files.append(file)

Punkte_limit = 619
#print(Punkte_limit)
int_g_punkte = int(Punkte_limit)
x = 0
print(files)
for file in files:
    print("+++++++++++++++++++++++++++++++++"+file+"+++++++++++++++++++++++++++++++++")
    df = pd.read_excel(file, sheet_names ="Nordfront-Armeebogen 2018")
    df.columns = ["Anzahl", "Name", "Level", "Ausrüstung", "Fraktion", "Trupp", "Punkte", "Gesamt", "Müll1", "Müll2"]
    df = df.fillna("")

    ##########################################################
    ### Algemeine Abfragen
    ##########################################################

    Punkte_limit_Liste = df["Gesamt"][0]
    int_Punkte_limit_liste = int(Punkte_limit_Liste)
    Bogen_Check = df["Gesamt"][5]
    Trupp_Check = df["Gesamt"][6]



    #if int_g_punkte < int_Punkte_limit_liste:
    #    print("Check total points")

    if Bogen_Check == "Nein":
        print("Check number of bows")

    #if Trupp_Check == "Ja":
    #   print("OK3")

    ##########################################################
    ### Truppen Abfragen
    ##########################################################

    Anzahl = df["Anzahl"][9:35]
    Name = df["Name"][9:35]
    Level = df["Level"][9:35]
    Ausrüstung = df["Ausrüstung"][9:35]
    Fraktion = df["Fraktion"][9:35]
    Trupp = df["Trupp"][9:35]
    Punkte = df["Punkte"][9:35]
    Gesamt = df["Gesamt"][9:35]

    ##########################################################
    ### Init der Datenbank
    ##########################################################

    user = "admin"
    password = "mesbg"
    couchserver = couchdb.Server("http://%s:%s@localhost:5984/" % (user, password))
    db = couchserver["lotr"]

    total_points = 0
    max_units = [0,0,0,0,0,0,0]
    hero = ["Sauron (24)","Ruhmreich (15)","Mächtig (12)","Legendär (18)","Gering (6)","Unabhängig (0)"]
    warrior = ["Krieger (0)"]
    index = db["1abe5681e131a7edb4e520badc000add"]
    translations = db["1abe5681e131a7edb4e520badc00d499"]
    ##########################################################
    ### Schleife über alle Zeilen der Tabelle
    ##########################################################
    i = 9
    while i < 35:
        _id = -1
        level = "none"
        ##########################################################
        ### Testen, ob Name in Fraktion
        ##########################################################
        if Fraktion[i] != "":
            doc = db[index[Fraktion[i]]]
            if Level[i] in hero:
                for test in doc["heroes"]:
                    if Name[i] in doc["heroes"][test]["names"]:
                        _id = test
                level = "heroes"
            elif Level[i] in warrior:
                for test in doc["warriors"]:
                    if Name[i] in doc["warriors"][test]["names"]:
                        _id = test
                level = "warriors"
            if _id == -1:
                print("Warrior "+Name[i]+" not in army of "+Fraktion[i])
        ##########################################################
        ### Überprüfen anderer Merkmale
        ##########################################################
            else:
                points = doc[level][_id]["points"]
                options = Ausrüstung[i].split(",")
                for option in options:
                    if option != "":
                        option = option.strip()
                        points += doc[level][_id]["options"][translations[option]]
                if int(Punkte[i]) != points:
                    print("points "+doc[level][_id]["names"][0]+" is "+str(Punkte[i])+" but expected "+str(points))
                total_points += points*int(Anzahl[i])
                
                if total_points > int_g_punkte:
                    print("Check total Points")
                if (level=="heroes"):
                    if (translations[Level[i]] != doc[level][_id]["type"]):
                        print("level")
                    if Level[i] == "Sauron (24)":
                        max_units[int(Trupp[i])] = 24
                    elif Level[i] =="Ruhmreich (15)":
                        max_units[int(Trupp[i])] = 15
                    elif Level[i] =="Mächtig (12)":
                        max_units[int(Trupp[i])] = 12
                    elif Level[i] =="Legendär (18)":
                        max_units[int(Trupp[i])] = 18
                    elif Level[i] =="Gering (6)":
                        max_units[int(Trupp[i])] = 6
                    elif Level[i] =="Unabhängig (0)":
                        max_units[int(Trupp[i])] = 0
                else:
                    max_units[int(Trupp[i])] -= int(Anzahl[i])
                    if(max_units[int(Trupp[i])] < 0):
                        print("Check number of warriors in warband "+str(Trupp[i]))
        i += 1


