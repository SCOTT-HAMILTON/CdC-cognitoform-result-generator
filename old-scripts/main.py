import pandas as pd
import sys
import math
import datetime

def get_text(value):
	if type(value) == float:
		return ""
	return value

def extract_values(row):
	values = {}
	values["name"] 				= row["PeuxtuNousDonnerTonNom_First"]+' '+row["PeuxtuNousDonnerTonNom_Last"]
	values["good_ambiance?"] 	= True if row["EstuSatisfaiteDeLambianceDeClasseCeTrimestre"] == "Oui" else False
	values["pb_ambiance"] 		= get_text(row["PeuxtuDécrireCeQuiTeDéplaitDansCetteAmbianceDeClasse"])
	values["pb_matiere?"] 		= True if row["RencontrestuDesProblèmesDansCertainesMatières"] == "Oui" else False
	values["matiere_avec_pb"] 	= get_text(row["DansQuellesMatières"])
	values["options_avec_pb"] 	= get_text(row["DansQuellesOptions"])
	values["pk_pb_matiere"] 	= get_text(row["PeuxtuDécrireTontesProblèmesAvecCesMatières"])
	values["ease_matiere?"] 	= True if row["RencontrestuDesFacilitéesDansCertainesMatières"] == "Oui" else False
	values["matiere_avec_ease"] = get_text(row["DansQuellesMatières2"])
	values["options_avec_ease"] = get_text(row["DansQuellesOptions2"])
	values["pk_ease_matiere"]	= get_text(row["PeuxtuDécrireCettecesFacilités"])
	values["demande?"]			= True if row["AstuUneDemandeÀNousFaireLorsqueTonCasSeraÉtudiéAuConseilDeClasse"] == "Oui" else False
	values["demande"]			= get_text(row["QuelleEstCetteDemande"])
	values["idee?"]				= True if row["AstuUneIdéeÀNousProposerPourAméliorerLaVieDeClasse"] == "Oui" else False
	values["idee"]				= get_text(row["PeuxtuNousPrésenterCettecesIdées"])

	return values

if len(sys.argv)<2:
	print ("Error, needs one argument.")
	exit(1)


now = datetime.datetime.now()
print ("  ") 

print("""---
title: "Résultats du formulaire pour préparer le CdC"
author: [Scott Hamilton]
date: """+now.strftime("%d")+'-'+now.strftime("%m")+'-'+str(now.year)+"""
subject: "Conseil de Classe"
keywords: [CdC, Formulaire]
lang: "fr"
table-use-row-colors: false
...

**Données du formulaire pour le conseil de classe : **\n  """)


data = pd.read_excel(sys.argv[1])

data = data.sort_values(by='PeuxtuNousDonnerTonNom_Last')

for row in data.iterrows():
	values = extract_values(row[1]);
	print ('*'+values["name"]+"*  ")
	
	if not values["good_ambiance?"]:
		print ("**Mauvaise ambiance** → "+values["pb_ambiance"]+"  ")
	

	if values["pb_matiere?"]:
		print ("**Problème matière**", sep='')
		print (", en "+values["matiere_avec_pb"], end='')
		if values["options_avec_pb"] != "":
			print (", et avec les options "+values["options_avec_pb"])
		if values["pk_pb_matiere"] != "":
			print (" **→ parce que : **"+values["pk_pb_matiere"]);
	
	print("  ")
	if values["ease_matiere?"]:
		print ("**Facilitées matière**",sep='')
		print (", en "+values["matiere_avec_ease"], end='')
		if values["options_avec_ease"] != "":
			print (", et avec les options "+values["options_avec_ease"])
		if values["pk_ease_matiere"] != "":
			print (" **→** parce que : "+values["pk_ease_matiere"]);
		print("  ")

	if values["demande?"]:
		print ("**demande : **\""+values["demande"]+"\"  ");

	if values["idee?"]:
		print ("**idée(s) : **\""+values["idee"]+"\"  ");

	print ()