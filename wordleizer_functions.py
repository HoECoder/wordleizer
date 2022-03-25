"""Functions used by wordleizer"""

from typing import Sequence


def contains(remaining_words: Sequence[str], search_letters: str) -> Sequence[str]:
    """Returns the words containing all the given search letters, in any order"""
    candidates = []
    for word in remaining_words:
        if all(c in word for c in search_letters):
            candidates.append(word)
    return candidates

def not_contains(remaining_words: Sequence[str], search_letters: str) -> Sequence[str]:
    """Returns the words not containing all the given search letters, in any order"""
    candidates = []
    for word in remaining_words:
        if any(c in word for c in search_letters):
            continue
        candidates.append(word)
    return candidates

def letters_in_position(remaining_words: Sequence[str], search_str: str) -> Sequence[str]:
    """Finds only words with letters in the given position, use _ for blanks/wildcards"""
    candidates = []
    for word in remaining_words:
        has_words = []
        for idx, letter in enumerate(search_str):
            if letter == "_":
                has_words.append(True)
                continue
            if word[idx] == letter:
                has_words.append(True)
            else:
                has_words.append(False)
        if all(has_words):
            candidates.append(word)
    return candidates

def letters_not_in_position(remaining_words: Sequence[str], patterns: Sequence[str]) -> Sequence[str]:
    """Finds only words with letters not in the given position, use _ for blanks/wildcards"""
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
    return candidates
