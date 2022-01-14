"""solve https://www.powerlanguage.co.uk/wordle/ puzzle with a pangram"""

import re
import subprocess


def cln(s): return re.sub("[^a-z]", "", s).lower()
def cln2(s): return s.replace("Solutions:\n", "").split("\n")


def main():
    """Will ask you about yellow and green letteres"""

    # query yellow letters and their positions
    yel = {}
    for i in range(1, 6):
        if input(f"Yellow letter(s) on position {i}? y/n ").lower() == "y":
            yel[i] = cln(input(f"Which letter(s)? "))

    # query green letters and their positions
    gre = {}
    if input("Any green letters? y/n ").lower() == "y":
        for i in range(1, 6):
            if input(f"Green letter on position {i}? y/n ").lower() == "y":
                gre[i] = input("Which letter? ").lower()

    # create input set for anagram solver
    inp = set()
    for i in yel:
        for j in yel[i]:
            inp.add(j)
    for i in gre:
        for j in gre[i]:
            inp.add(j)

    # run anagram solver
    out = cln2(subprocess.run(f"anagram_solver {''.join(inp)}",
                              capture_output=True, text=True).stdout)

    # filter solutions according to word length
    out = [i for i in out if len(i) == 5]

    # filter out words with banned yellow letter
    for i in yel:
        out = [wrd for wrd in out if wrd[i - 1] not in yel[i]]

    # keep only words with correct green letter
    if gre:
        for i in gre:
            out = [wrd for wrd in out if wrd[i - 1] == gre[i]]

    return out


if __name__ == "__main__":
    print(main())
