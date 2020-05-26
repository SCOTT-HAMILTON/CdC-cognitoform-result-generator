#!/usr/bin/env python3.8
import pandas as pd
# from pandas_ods_reader import read_ods
import sys
import math
import datetime
import re

fields_alias = {

"QuestionnairePourPréparerLeCons_Id": None,
"PeuxtuNousDonnerTonNom_First": "Prénom : ",
"PeuxtuNousDonnerTonNom_Last": "Nom : ",
"EstuSatisfaiteDeLambianceDeClasseCeTrimestre": "",
"PeuxtuDécrireCeQuiTeDéplaitDansCetteAmbianceDeClasse": "Ce qui te déplait dans cette ambiance ?",
"RencontrestuDesProblèmesDansCertainesMatières": "",
"DansQuellesMatières": "Dans quelle matière ?",
"PeuxtuDécrireTontesProblèmesAvecCesMatières": "Problèmes matières : ",
"DansQuellesOptions": "Problèmes option : ",
"RencontrestuDesFacilitéesDansCertainesMatières": "",
"DansQuellesMatières2": "Matière facilités : ",
"DansQuellesOptions2": "Options facilités : ",
"PeuxtuDécrireCettecesFacilités": "Facilités",
"AstuUneDemandeÀNousFaireLorsqueTonCasSeraÉtudiéAuConseilDeClasse": "",
"QuelleEstCetteDemande": "Demande Conseil de classe : ",
"AstuUneIdéeÀNousProposerPourAméliorerLesCoursÀDistance": "",
"PeuxtuNousPrésenterCettecesIdées": "Idées à nous présenter : ",
"SouhaitestuRetournerAuLycée": "",
"PourquoiSouhaitestuRetournerAuLycée": "Pourquoi souhaite-tu retourner au lycée ?",
"PourquoiNeSouhaitestuPasRetournerAuLycée": "Pourquoi ne souhaite-tu pas retourner au lycée ?",
"CommentSestPasséCeConfinementPourToiLesCoursLeTravailQuelsOntÉtéLesProblèmesRencontrés": "Le confinement c'est bien passé ?",
"QuelAÉtéTonRessentiSurTouteLannée": "Ton ressenti sur l'année : ",
"QuellesSontTesCraintesPourLannéeProchaine": "Tes craintes : ",
"Entry_Status": None,
"Entry_DateCreated": None,
"Entry_DateSubmitted": None,
"Entry_DateUpdated": None,
}

def get_text(value):
    if type(value) == float:
        return ""
    return value

def extract_values(row):
    # print ("\nROW : ",row)
    # print("### ",end='')
    print ("---\n")
    for field in fields_alias:
        alias = fields_alias[field]
        if not alias:
            continue
        value = row[field]
        if isinstance(value, float) and math.isnan(value):
            continue
        print ("\\textbf{",alias,"}",str(value),"\\")
    print()
    # return values

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

data = data.sort_values(by='PeuxtuNousDonnerTonNom_First')

for row in data.iterrows():
    values = extract_values(row[1])
    # print ('*'+values["name"]+"*  ")
