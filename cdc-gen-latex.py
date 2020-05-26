#!/usr/bin/env python3.8
import pandas as pd
import sys
import math
import datetime
import re

fields_alias = {
"QuestionnairePourPréparerLeCons_Id": None,
"PeuxtuNousDonnerTonNom_First": "Prénom : ",
"PeuxtuNousDonnerTonNom_Last": "Nom : ",
"EstuSatisfaiteDeLambianceDeClasseCeTrimestre": "YES-NO-Est satisfait de l'ambiance de classe ?",
"PeuxtuDécrireCeQuiTeDéplaitDansCetteAmbianceDeClasse": "Ce qui te déplait dans cette ambiance ?",
"RencontrestuDesProblèmesDansCertainesMatières": "YES-NO-Rencontre des problèmes dans certaines matières ?",
"DansQuellesMatières": "CHART-Matières posant le plus de problèmes-Dans quelle matière ?",
"PeuxtuDécrireTontesProblèmesAvecCesMatières": "Problèmes matières : ",
"DansQuellesOptions": "CHART-Options posant le plus de problèmes-Problèmes option : ",
"RencontrestuDesFacilitéesDansCertainesMatières": "YES-NO-As des facilités dans certaines matières ?",
"DansQuellesMatières2": "CHART-Matières dites les plus faciles-Matière facilités : ",
"DansQuellesOptions2": "Options facilités : ",
"PeuxtuDécrireCettecesFacilités": "Facilités",
"AstuUneDemandeÀNousFaireLorsqueTonCasSeraÉtudiéAuConseilDeClasse": "YES-NO-As une demande à faire au CdC ?",
"QuelleEstCetteDemande": "Demande Conseil de classe : ",
"AstuUneIdéeÀNousProposerPourAméliorerLesCoursÀDistance": "YES-NO-As une idée à nous proposer pour améliorer les cours à distance ?",
"PeuxtuNousPrésenterCettecesIdées": "Idées à nous présenter : ",
"SouhaitestuRetournerAuLycée": "YES-NO-Souhaite retourner au lycée ?",
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

YesNoFields_stats = {}
BarChart_stats = {}
EntryCount = 0

PiChart_header = """
\\\\captionsetup[subfigure]{labelformat=empty, font={bf}}
\\\\captionsetup[figure]{labelformat=empty, font={bf}}
\\\\begin{figure}[H]
\\\\begin{center}"""

PiChart_footer = """
\\\\end{center}
\\\\end{figure}
"""

def makePiChart(alias, percentage):
    return """
\\\\begin{subfigure}{.4\\\\textwidth}
\\\\centering
\\\\caption{"""+alias+"""}
\\\\begin{tikzpicture}
\\\\pie[explode=0.1, radius=1]
 {"""+str(int(percentage))+"""/Oui,"""+str(100-int(percentage))+"""/Non}
\\\\end{tikzpicture}
\\\\end{subfigure}"""

def makePiChart2(data, alias):
    total = 0
    text = ""
    for value,count in data.items():
        total += count
    reste = 0.0
    full = 100.0
    text += PiChart_header
    text +="""
\\\\centering
\\\\caption{"""+alias+"""}
\\\\begin{tikzpicture}
\\\\pie[explode=0.3, radius=4]{"""
    for value,count in data.items():
        pc = count/total*100+1/total
        reste += pc-int(pc)
        if reste > 1:
            pc += 1
            reste -= 1
        text +=  str(int(pc))+"""/"""+value+','
    # Removing trailing comma
    text = text[:len(text)-1]
    text += """}
\\\\end{tikzpicture}"""
    text += PiChart_footer

    return text

def makeCharts():
    text = "\\\\section{Quelques statistiques}"
    text += PiChart_header
    for key, (alias, n) in YesNoFields_stats.items():
        percentage = n/EntryCount*100.0
        text += makePiChart(alias, percentage)
    text += PiChart_footer

    for key,values in BarChart_stats.items():
        text += makePiChart2(values, key)
    return text

def extract_values(row):
    data = "\\\\noindent\\\\rule{8cm}{0.4pt}\n\n"
    for field in fields_alias:
        alias = fields_alias[field]
        if not alias:
            continue
        tab = alias.split("YES-NO-")
        if len(tab) == 2:
            alias = tab[1]
            value = row[field]
            if not field in YesNoFields_stats:
                YesNoFields_stats[field] = (alias, 0)
            elif value == "Oui":
                alias,n = YesNoFields_stats[field]
                n+=1
                YesNoFields_stats[field] = (alias,n)
            continue
        tab = alias.split("CHART-")
        if len(tab) == 2:
            value = row[field]
            if isinstance(value,float) and math.isnan(value):
                continue
            key = tab[1].split('-')[0]
            values = value.split(", ")
            if not key in BarChart_stats:
                BarChart_stats[key] = {}
            for v in values:
                if not v in BarChart_stats[key]:
                    BarChart_stats[key][v] = 0
                BarChart_stats[key][v] += 1
            continue
        value = row[field]
        if isinstance(value, float) and math.isnan(value):
            continue
        data += "\\\\"+"textbf{"+alias+"} "+str(value)+" \\\\\\\\"+"\n"
    data += '\n'

    return data

if len(sys.argv)<2:
    print ("Error, needs one argument.")
    exit(1)



data = pd.read_excel(sys.argv[1])

data = data.sort_values(by='PeuxtuNousDonnerTonNom_Last')
EntryCount = len(data)-1
text = ""
for row in data.iterrows():
    text += extract_values(row[1])

# print(BarChart_stats)

text = makeCharts()+"""\\\\section{Les réponses}\n"""+text

with open('template_latex.tex') as template:
    lines = ''.join(template.readlines())

print(re.sub('<data>', text, lines))
