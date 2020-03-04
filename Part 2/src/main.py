import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from src.LexicalAnalyzer import LexicalAnalyzer


if __name__ == '__main__':
    table = LexicalAnalyzer('../data/input.txt').create_table()

    for element in table:
        print(element)