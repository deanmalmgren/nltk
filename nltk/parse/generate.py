# -*- coding: utf-8 -*-
# Natural Language Toolkit: Generating from a CFG
#
# Copyright (C) 2001-2013 NLTK Project
# Author: Steven Bird <stevenbird1@gmail.com>
#         Peter Ljunglöf <peter.ljunglof@heatherleaf.se>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#
from __future__ import print_function

import itertools
import sys
from nltk.grammar import Nonterminal, parse_cfg

def generate(grammar, start=None, depth=None, n=None):
    """
    Generates a list of sentences from a CFG.

    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generate sentences.
    :param depth: The maximal depth of the generated tree.
    :param n: The maximum number of sentences to return.
    :return: A list of lists of terminal tokens.
    """
    sentences = generate_iter(grammar, start, depth)
    return list(itertools.islice(sentences, n))

def generate_iter(grammar, start=None, depth=None):
    """
    Generates an iterator of all sentences from a CFG.

    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generate sentences.
    :param depth: The maximal depth of the generated tree.
    :return: An iterator of lists of terminal tokens.
    """
    if not start:
        start = grammar.start()
    if depth is None:
        depth = sys.maxsize
    return _generate_all(grammar, [start], depth)

def _generate_all(grammar, items, depth):
    if items:
        for frag1 in _generate_one(grammar, items[0], depth):
            for frag2 in _generate_all(grammar, items[1:], depth):
                yield frag1 + frag2
    else:
        yield []

def _generate_one(grammar, item, depth):
    if depth > 0:
        if isinstance(item, Nonterminal):
            for prod in grammar.productions(lhs=item):
                for frag in _generate_all(grammar, prod.rhs(), depth-1):
                    yield frag
        else:
            yield [item]

demo_grammar = """
  S -> NP VP 
  NP -> Det N
  VP -> V NP 
  Det -> 'the'
  Det -> 'a'
  N -> 'man' | 'park' | 'dog' | 'telescope'
  V -> 'saw' | 'walked'
  P -> 'in' | 'with'
"""

def demo():
    N = 42
    print('Generating the first %d sentences for demo grammar:' % (N,))
    print(demo_grammar)
    grammar = parse_cfg(demo_grammar)
    for n, sent in enumerate(generate(grammar, n=N), 1):
        print('%3d. %s' % (n, ' '.join(sent)))

if __name__ == '__main__':
    demo()
