import click
import re
from CdcGenerator.cdcgenerator import CdCGenerator

@click.command()
@click.option('-d', '--debug', is_flag=True)
# @click.option('-o', '--output', type=click.Path(), required=True)
@click.argument('input_entry_excel', type=click.Path())
def cli(debug, input_entry_excel):
    cdcgenerator = CdCGenerator(debug)
    cdcgenerator.generateLatexPdf(input_entry_excel)
