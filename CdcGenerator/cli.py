import click
import re
from CdcGenerator.cdcgenerator import CdCGenerator

@click.command()
@click.option('-d', '--debug', is_flag=True)
@click.option('-S', '--no-stats', is_flag=True)
@click.option('-A', '--no-answers', is_flag=True)
# @click.option('-o', '--output', type=click.Path(), required=True)
@click.argument('input_entry_excel', type=click.Path())
def cli(debug, input_entry_excel, no_stats, no_answers):
    cdcgenerator = CdCGenerator(debug, stats = not no_stats, answers = not no_answers)
    cdcgenerator.generateLatexPdf(input_entry_excel)
