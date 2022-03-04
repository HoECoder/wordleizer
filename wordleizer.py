#!/usr/bin/env python
"""Helper to solve wordle"""
from typing import Sequence
import click

@click.group(chain=True)
@click.pass_context
def cli(ctx: click.Context):
    """Wordle solver.

    Chain together any of the commands to filter the list of potential words
    """
    ctx.ensure_object(dict)

@cli.command("load")
@click.pass_context
@click.option("-f",
              "--file",
              "word_list_file",
              type=click.Path(exists=True, readable=True),
              default="five_letter_words.txt")
def load(ctx: click.Context, word_list_file: str):
    "Loads the list of five letter words"
    with open(word_list_file, encoding="utf-8") as _f:
        words = [line.strip() for line in _f if line.strip()]
        ctx.obj["words"] = words
    return "load"

@cli.command("contains")
@click.pass_context
@click.argument("search_letters",
                type=str)
def contains(ctx: click.Context, search_letters: str):
    """Returns the words containing all the given search letters, in any order"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = []
    for word in remaining_words:
        if all(c in word for c in search_letters):
            candidates.append(word)
    ctx.obj["remaining_words"] = candidates
    return "contains"

@cli.command("not_contains")
@click.pass_context
@click.argument("search_letters",
                type=str)
def not_contains(ctx: click.Context, search_letters: str):
    """Returns the words not containing all the given search letters, in any order"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = []
    for word in remaining_words:
        if any(c in word for c in search_letters):
            continue
        candidates.append(word)
    ctx.obj["remaining_words"] = candidates
    return "not_contains"

@cli.command("letters_in_position")
@click.pass_context
@click.argument("search_word", type=str)
def letters_in_position(ctx: click.Context, search_word: str):
    """Finds only words with letters in the given position, use _ for blanks/wildcards"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = []
    for word in remaining_words:
        has_words = []
        for idx, letter in enumerate(search_word):
            if letter == "_":
                has_words.append(True)
                continue
            if word[idx] == letter:
                has_words.append(True)
            else:
                has_words.append(False)
        if all(has_words):
            candidates.append(word)
    ctx.obj["remaining_words"] = candidates
    return "letters_in_position"

@cli.command("letters_not_in_position")
@click.pass_context
@click.option("-p", "--pattern", "patterns", multiple=True, default=[], help="Pattern of where letters are not")
def letters_not_in_position(ctx: click.Context, patterns: Sequence[str]):
    """Finds only words with letters not in the given position, use _ for blanks/wildcards"""
    if not ctx.obj["words"]:
        return
    remaining_words = ctx.obj.get("remaining_words", ctx.obj["words"])
    candidates = []
    for word in remaining_words:
        pattern_matches = []
        for pattern in patterns:
            missed_letters = []
            for idx, letter in enumerate(pattern):
                if letter == "_":
                    missed_letters.append(True)
                if letter != word[idx]:
                    missed_letters.append(True)
                else:
                    missed_letters.append(False)
            if all(missed_letters):
                pattern_matches.append(True)
            else:
                pattern_matches.append(False)
        if all(pattern_matches):
            candidates.append(word)
    ctx.obj["remaining_words"] = candidates

    return "letters_not_in_position"

@cli.result_callback()
@click.pass_context
def process_results(ctx: click.Context, results):
    """Shows the results"""
    functions = " ".join(results)
    click.echo(f"Ran: {functions}")
    if "remaining_words" in ctx.obj:
        remainders = ctx.obj["remaining_words"]
        lines = []
        accum = []
        click.echo(f"Found {len(remainders)} candidates")
        for idx, word in enumerate(remainders):
            if idx > 0 and idx % 13 == 0:
                lines.append(" ".join(accum))
                accum = []
            accum.append(word)
        if accum:
            lines.append(" ".join(accum))
        click.echo("\n".join(lines))

if __name__ == "__main__":
    cli() #pylint: disable=no-value-for-parameter
