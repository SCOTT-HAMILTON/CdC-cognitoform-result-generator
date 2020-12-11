import pandas as pd
import sys
import math
import datetime
import re
import pkg_resources
from CdcGenerator.fields import fields

class CdCGenerator():
    def __init__(self, debug, stats=False, answers=True):
        self.debug = debug
        self.stats = stats
        self.answers = answers

        self.fields_alias = fields["2020-2021-1"]
        self.PiChart_header = """
\\\\captionsetup[subfigure]{labelformat=empty, font={bf}}
\\\\captionsetup[figure]{labelformat=empty, font={bf}}
\\\\begin{figure}[H]
\\\\begin{center}"""

        self.PiChart_footer = """
\\\\end{center}
\\\\end{figure}
"""

    def makePiChart(self, alias, percentage, echantillon):
        return """
\\\\begin{subfigure}{.4\\\\textwidth}
\\\\centering
\\\\caption{"""+alias+""" ("""+str(echantillon)+""")}
\\\\begin{tikzpicture}
\\\\pie[explode=0.1, radius=2]
 {"""+str(int(percentage))+"""/Oui,"""+str(100-int(percentage))+"""/Non}
\\\\end{tikzpicture}
\\\\end{subfigure}"""

    def makePiChart2(self, data, alias):
        total = 0
        text = ""
        for value,count in data.items():
            total += count
        reste = 0.0
        full = 100.0
        text += self.PiChart_header
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
        text += self.PiChart_footer

        return text

    def makeCharts(self, YesNoFields_stats, BarChart_stats, EntryCount):
        text = "\\\\section{Quelques statistiques}"
        text += self.PiChart_header
        print(YesNoFields_stats.items())
        for key, (alias, n) in YesNoFields_stats.items():
            percentage = n/EntryCount*100.0
            text += self.makePiChart(alias, percentage, n)
        text += self.PiChart_footer
        text += "\n\\\\pagebreak\n"
        for key,values in BarChart_stats.items():
            text += self.makePiChart2(values, key)
        return text

    def extract_values(self, row, YesNoFields_stats, BarChart_stats):
        data = """\\\\rule{8cm}{0.4pt}
\\\\setlength{\\\\parindent}{0cm}\n\n"""
        for field in self.fields_alias:
            alias = self.fields_alias[field]
            if not alias:
                continue
            tab = alias.split("YES-NO-")
            if len(tab) == 2:
                alias = tab[1]
                value = row[field]
                if not field in YesNoFields_stats:
                    YesNoFields_stats[field] = (alias, 1)
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

        return (data, YesNoFields_stats, BarChart_stats)

    def clean_names_case(self, data):
        columns = ['PeuxtuNousDonnerTonNom_First', 'PeuxtuNousDonnerTonNom_Last']
        data[columns] = data[columns].apply(
                lambda n:
                    n.apply(
                        lambda t: t[0].upper()+t[1:].lower())
                   , axis='columns')
        return data

    def generateLatexPdf(self, input_entry_excel):

        YesNoFields_stats = {}
        BarChart_stats = {}
        EntryCount = 0

        data = pd.read_excel(input_entry_excel)
        data = self.clean_names_case(data)
        data = data.sort_values(by='PeuxtuNousDonnerTonNom_Last')
        EntryCount = len(data)
        text = ""
        final_text = ""
        for row in data.iterrows():
            extracted_text,YesNoFields_stats,BarChart_stats = self.extract_values(row[1], YesNoFields_stats, BarChart_stats)
            text += extracted_text

        if self.stats:
            final_text = self.makeCharts(YesNoFields_stats, BarChart_stats, EntryCount)+"""

\\\\pagebreak

"""
        if self.answers:
            final_text += """\\\\section{Les réponses ("""+str(EntryCount)+""")}\n"""+text

        TEMPLATE_PATH = pkg_resources.resource_filename('CdcGenerator', 'data/template_latex.tex')
        if self.debug:
            print(f"TEMPLATE_PATH : `{TEMPLATE_PATH}`")

        with open(TEMPLATE_PATH) as template:
            lines = ''.join(template.readlines())

        print(re.sub('<data>', final_text, lines))

