import pandas as pd

Punkte_limit = input("Wie viele Punkte sind maximal erlaubt? ")
print(Punkte_limit)
int_g_punkte = int(Punkte_limit)

df = pd.read_excel("Uruk619.xlsx", sheet_names ="Nordfront-Armeebogen 2018")
df.columns = ["Anzahl", "Name", "Level", "Ausrüstung", "Fraktion", "Trupp", "Punkte", "Gesamt", "Müll1", "Müll2"]

##########################################################
### Algemeine Abfragen
##########################################################

Punkte_limit_Liste = df["Gesamt"][0]
int_Punkte_limit_liste = int(Punkte_limit_Liste)
Bogen_Check = df["Gesamt"][5]
Trupp_Check = df["Gesamt"][6]

print(Bogen_Check)

if int_g_punkte >= int_Punkte_limit_liste:
    print("OK1")

if Bogen_Check == "Ja":
    print("OK2")

if Trupp_Check == "Ja":
    print("OK3")

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





