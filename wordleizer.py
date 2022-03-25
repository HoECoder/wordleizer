#!/usr/bin/env python
"""Helper to solve wordle"""
from typing import Sequence
import click

from wordleizer_functions import contains, letters_in_position, letters_not_in_position, not_contains

@click.group(chain=True)
@click.pass_context
@click.option("-f",
              "--file",
              "word_list_file",
              type=click.Path(exists=True, readable=True),
              default="five_letter_words.txt",
              help="Line oriented list of words to use to search")
def cli(ctx: click.Context, word_list_file: str):
    """Wordle solver.

    Chain together any of the commands to filter the list of potential words
    """
    ctx.ensure_object(dict)
    with open(word_list_file, encoding="utf-8") as _f:
        words = [line.strip() for line in _f if line.strip()]
        ctx.obj["words"] = words

@cli.command("contains")
@click.pass_context
@click.argument("search_letters",
                type=str)
def click_contains(ctx: click.Context, search_letters: str):
    """Returns the words containing all the given search letters, in any order"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = contains(remaining_words, search_letters)
    ctx.obj["remaining_words"] = candidates
    return "contains"

@cli.command("not_contains")
@click.pass_context
@click.argument("search_letters",
                type=str)
def click_not_contains(ctx: click.Context, search_letters: str):
    """Returns the words not containing all the given search letters, in any order"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = not_contains(remaining_words, search_letters)
    ctx.obj["remaining_words"] = candidates
    return "not_contains"

@cli.command("letters_in_position")
@click.pass_context
@click.argument("search_word", type=str)
def click_letters_in_position(ctx: click.Context, search_word: str):
    """Finds only words with letters in the given position, use _ for blanks/wildcards"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = letters_in_position(remaining_words, search_word)
    ctx.obj["remaining_words"] = candidates
    return "letters_in_position"

@cli.command("letters_not_in_position")
@click.pass_context
@click.option("-p", "--pattern", "patterns", multiple=True, default=[], help="Pattern of where letters are not")
def click_letters_not_in_position(ctx: click.Context, patterns: Sequence[str]):
    """Finds only words with letters not in the given position, use _ for blanks/wildcards"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = letters_not_in_position(remaining_words, patterns)
    ctx.obj["remaining_words"] = candidates

    return "letters_not_in_position"

def prepare_output_lines(remaining_words: Sequence[str], words_per_line: int) -> str:
    """Nicely formats the remaining words with words_per_line on each line"""
    lines = []
    accum = []
    for idx, word in enumerate(remaining_words):
        if idx > 0 and idx % words_per_line == 0:
            lines.append(" ".join(accum))
            accum = []
        accum.append(word)
    if accum:
        lines.append(" ".join(accum))
    return "\n".join(lines)

@cli.result_callback()
@click.pass_context
def process_results(ctx: click.Context, results, word_list_file: str):
    """Shows the results"""
    click.echo(f"Used: '{word_list_file}'")
    functions = " ".join(results)
    click.echo(f"Ran: {functions}")
    if "remaining_words" in ctx.obj:
        click.echo(f"Found: {len(ctx.obj['remaining_words'])} candidates")
        click.echo(prepare_output_lines(ctx.obj["remaining_words"], 12))

if __name__ == "__main__":
    cli() #pylint: disable=no-value-for-parameter
