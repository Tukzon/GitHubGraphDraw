#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import random
from datetime import datetime, timedelta

# =========================================================================
# LETTER MAP DICTIONARY
# =========================================================================
LETTER_MAP = {
    'A': ["  #   ", " # #  ", "#   # ", "##### ", "#   # ", "#   # ", "#   # "],
    'B': ["####  ", "#   # ", "#   # ", "####  ", "#   # ", "#   # ", "####  "],
    'C': [" ###  ", "#   # ", "#     ", "#     ", "#     ", "#   # ", " ###  "],
    'D': ["####  ", "#   # ", "#   # ", "#   # ", "#   # ", "#   # ", "####  "],
    'E': ["##### ", "#     ", "#     ", "####  ", "#     ", "#     ", "##### "],
    'F': ["##### ", "#     ", "#     ", "####  ", "#     ", "#     ", "#     "],
    'G': [" ###  ", "#   # ", "#     ", "# ### ", "#   # ", "#   # ", " ###  "],
    'H': ["#   # ", "#   # ", "#   # ", "##### ", "#   # ", "#   # ", "#   # "],
    'I': ["##### ", "  #   ", "  #   ", "  #   ", "  #   ", "  #   ", "##### "],
    'J': [" #### ", "   #  ", "   #  ", "   #  ", "   #  ", "#  #  ", " ##   "],
    'K': ["#   # ", "#  #  ", "# #   ", "##    ", "# #   ", "#  #  ", "#   # "],
    'L': ["#     ", "#     ", "#     ", "#     ", "#     ", "#     ", "##### "],
    'M': ["#   # ", "#   # ", "## ## ", "# # # ", "#   # ", "#   # ", "#   # "],
    'N': ["#   # ", "#   # ", "##  # ", "# # # ", "#  ## ", "#   # ", "#   # "],
    'Ñ': [" ## # ", "#  ## ", "# # # ", "# # # ", "# # # ", "#  ## ", " ## # "],
    'O': [" ###  ", "#   # ", "#   # ", "#   # ", "#   # ", "#   # ", " ###  "],
    'P': ["####  ", "#   # ", "#   # ", "####  ", "#     ", "#     ", "#     "],
    'Q': [" ###  ", "#   # ", "#   # ", "#   # ", "# # # ", "#  #  ", " ## # "],
    'R': ["####  ", "#   # ", "#   # ", "####  ", "# #   ", "#  #  ", "#   # "],
    'S': [" ###  ", "#   # ", "#     ", " ###  ", "    # ", "#   # ", " ###  "],
    'T': ["##### ", "  #   ", "  #   ", "  #   ", "  #   ", "  #   ", "  #   "],
    'U': ["#   # ", "#   # ", "#   # ", "#   # ", "#   # ", "#   # ", " ###  "],
    'V': ["#   # ", "#   # ", "#   # ", "#   # ", "#   # ", " # #  ", "  #   "],
    'W': ["#   # ", "#   # ", "#   # ", "# # # ", "## ## ", "#   # ", "#   # "],
    'X': ["#   # ", "#   # ", " # #  ", "  #   ", " # #  ", "#   # ", "#   # "],
    'Y': ["#   # ", "#   # ", " # #  ", "  #   ", "  #   ", "  #   ", "  #   "],
    'Z': ["##### ", "    # ", "   #  ", "  #   ", " #    ", "#     ", "##### "],
    ' ': ["      ", "      ", "      ", "      ", "      ", "      ", "      "],
    '1': ["  #   ", " ##   ", "  #   ", "  #   ", "  #   ", "  #   ", "##### "],
    '2': [" ###  ", "#   # ", "    # ", "   #  ", "  #   ", " #    ", "##### "],
    '3': [" ###  ", "#   # ", "    # ", "   #  ", "    # ", "#   # ", " ###  "],
    '4': ["   #  ", "  ##  ", " # #  ", "#  #  ", "##### ", "   #  ", "   #  "],
    '5': ["##### ", "#     ", "####  ", "    # ", "    # ", "    # ", "####  "],
    '6': [" ###  ", "#   # ", "#     ", "####  ", "#   # ", "#   # ", " ###  "],
    '7': ["##### ", "    # ", "    # ", "    # ", "    # ", "    # ", "    # "],
    '8': [" ###  ", "#   # ", "#   # ", " ###  ", "#   # ", "#   # ", " ###  "],
    '9': [" ###  ", "#   # ", "#   # ", " #### ", "    # ", "    # ", " ###  "],
    '0': [" ###  ", "#   # ", "#   # ", "#   # ", "#   # ", "#   # ", " ###  "],
    '.': ["      ", "      ", "      ", "      ", "      ", "      ", "  ##  "],
    ',': ["      ", "      ", "      ", "      ", "      ", "    # ", "   #  "],
    ':': ["      ", "  ##  ", "  ##  ", "      ", "  ##  ", "  ##  ", "      "],
    ';': ["      ", "   #  ", "      ", "   #  ", "   #  ", "  #   ", "      "],
    '!': ["  #   ", "  #   ", "  #   ", "  #   ", "  #   ", "      ", "  #   "],
    '?': [" ###  ", "#   # ", "    # ", "   #  ", "  #   ", "      ", "  #   "],
    "'": ["  #   ", "  #   ", " #    ", "      ", "      ", "      ", "      "],
    '"': ["# #   ", "# #   ", "      ", "      ", "      ", "      ", "      "],
    '-': ["      ", "      ", "      ", "##### ", "      ", "      ", "      "],
    '+': ["      ", "   #  ", "   #  ", "##### ", "   #  ", "   #  ", "      "],
    '*': ["      ", "#   # ", "  #   ", "##### ", "  #   ", "#   # ", "      "],
    '/': ["    # ", "   #  ", "  #   ", " #    ", "#     ", "      ", "      "],
    '\\': ["#     ", " #    ", "  #   ", "   #  ", "    # ", "      ", "      "],
    '=': ["      ", "##### ", "      ", "##### ", "      ", "      ", "      "],
    '_': ["      ", "      ", "      ", "      ", "      ", "      ", "##### "],
    '<': ["    # ", "   #  ", "  #   ", "#     ", "  #   ", "   #  ", "    # "],
    '>': ["#     ", "  #   ", "   #  ", "    # ", "   #  ", "  #   ", "#     "],
    '[': ["  ##  ", "  #   ", "  #   ", "  #   ", "  #   ", "  #   ", "  ##  "],
    ']': [" ##   ", "   #  ", "   #  ", "   #  ", "   #  ", "   #  ", " ##   "],
    '(': ["   #  ", "  #   ", " #    ", "#     ", " #    ", "  #   ", "   #  "],
    ')': [" #    ", "  #   ", "   #  ", "    # ", "   #  ", "  #   ", " #    "],
    '{': ["   #  ", "  #   ", "  #   ", "#     ", "  #   ", "  #   ", "   #  "],
    '}': ["  #   ", "   #  ", "   #  ", "    # ", "   #  ", "   #  ", "  #   "],
    '#': ["  # # ", " #####", "  # # ", " #####", "  # # ", " #####", "  # # "],
    '$': ["  #   ", " #####", "# #   ", " ###  ", "  # # ", "##### ", "  #   "],
    '%': ["#   # ", "#  #  ", "   #  ", "  #   ", " #    ", "#  #  ", "#   # "],
    '@': [" ###  ", "#   # ", "# ### ", "# # # ", "# ### ", "#     ", " ### #"],
    '^': ["  #   ", " # #  ", "#   # ", "      ", "      ", "      ", "      "],
    '`': ["  #   ", "   #  ", "    # ", "      ", "      ", "      ", "      "],
    '~': [" ##   ", "#  #  ", "      ", "      ", "      ", "      ", "      "],
    '°': ["  ##  ", " #  # ", " #  # ", "  ##  ", "      ", "      ", "      "],
    '£': ["  #   ", " #####", "  #   ", " #####", "  #   ", " #####", "  #   "],
    '¥': ["#   # ", " # #  ", "  #   ", "##### ", "  #   ", "  #   ", "  #   "],
    '€': [" ###  ", "#     ", "##### ", "#     ", "##### ", "#     ", " ###  "],
    '¢': ["  #   ", " #####", "#     ", "#     ", "#     ", " #####", "  #   "]
}

# =========================================================================
# MAIN FUNCTIONS
# =========================================================================

def generate_word_matrix(word):
    """
    Given a string 'word', this function generates a matrix of 7 rows and 
    (5 + 1) * len(word) - 1 columns.
    - Each letter is 5 columns wide, and there is 1 blank column separating letters.
    - For example: If there are n letters, each one contributes 5 columns, plus 1 blank column
      after each letter except for the last one. So total columns = n*5 + (n-1)*1 = n*6 - 1.
    """
    # Convert the input word to uppercase to search in LETTER_MAP
    word = word.upper()

    # Calculate the total number of columns
    total_columns = len(word)*6 - 1
    rows = 7

    # Initialize the final matrix with blank spaces
    final_matrix = [[" " for _ in range(total_columns)] for _ in range(rows)]

    current_col = 0
    for i, letter in enumerate(word):
        # Retrieve the letter definition from LETTER_MAP if it exists
        if letter in LETTER_MAP:
            letter_pixels = LETTER_MAP[letter]
        else:
            # If the letter is not defined, use a 7x5 blank placeholder
            letter_pixels = ["     " for _ in range(rows)]
        
        # Place the letter onto the final matrix at the current column offset
        for r in range(rows):
            for c in range(5):
                final_matrix[r][current_col + c] = letter_pixels[r][c]

        # Add a blank column as separator (except after the last letter)
        if i < len(word) - 1:
            current_col += 6  # 5 columns for the letter + 1 space
        else:
            current_col += 5  # on the last letter, no extra blank space needed

    return final_matrix


def make_commit_for_day(date_str, commits=1):
    """
    Performs a given number of commits 'commits' on the specified date_str (YYYY-MM-DD).
    It appends lines to 'progress.txt' and commits with a forced date (via --date).
    """
    for i in range(commits):
        # Append a line to 'progress.txt' to ensure there's a change to commit
        with open("progress.txt", "a", encoding="utf-8") as f:
            f.write(f"Commit {i+1} on {date_str}\n")

        # Stage the changes in 'progress.txt'
        subprocess.run([
            "git", "add", "progress.txt"
        ])

        # Prepare the commit message
        commit_message = f"Automatic commit on {date_str} ({i+1} of {commits})"
        # Perform the commit, forcing the date
        subprocess.run([
            "git", "commit",
            "--date", date_str + "T12:00:00",  # Fixed hour to avoid ambiguity
            "-m", commit_message
        ], check=True)


def draw_on_github(word, start_date, mode="max"):
    """
    Generates the necessary commits to 'draw' the specified word on the GitHub contributions graph,
    starting from 'start_date' (a datetime object). The 'mode' can be 'max' or 'random'.
    
    - start_date is treated as column 0, row 0 (Sunday).
    - For each column (week) and each row (day), if there's a '#' in the matrix,
      the script will create 5 commits ('max') or a random number (1-5) of commits ('random').
    """
    # Generate the 2D matrix for the word
    matrix = generate_word_matrix(word)

    rows = len(matrix)         # Typically 7
    cols = len(matrix[0])      # Depends on the length of the word

    # Iterate over columns (which represent weeks)
    for col in range(cols):
        # Iterate over rows (which represent days, Sunday to Saturday)
        for row in range(rows):
            if matrix[row][col] == '#':
                if mode == "max":
                    # Use 5 commits for a strong green color
                    num_commits = 5
                else:
                    # Use a random number between 1 and 5
                    num_commits = random.randint(1, 5)

                # Calculate the date based on start_date plus the offset
                # offset_days = number of days from start_date = col*7 + row
                offset_days = col * 7 + row
                commit_date = start_date + timedelta(days=offset_days)

                # Format the date as YYYY-MM-DD
                date_str = commit_date.strftime("%Y-%m-%d")
                make_commit_for_day(date_str, commits=num_commits)



def main():
    parser = argparse.ArgumentParser(description="Draw a word on the GitHub contributions graph.")
    parser.add_argument("word", help="Word or phrase to draw (no quotes needed).")
    parser.add_argument("--mode", choices=["max", "random"], default="max",
                        help="Mode for commits: 'max' = 5 commits per day, 'random' = random number (1-5).")
    parser.add_argument("--start-date", default=None,
                        help="Start date in YYYY-MM-DD format. If not specified, it defaults to 52 weeks ago.")
    args = parser.parse_args()

    # If progress.txt does not exist, create it
    if not os.path.exists("progress.txt"):
        with open("progress.txt", "w", encoding="utf-8") as f:
            f.write("Progress file to draw on the GitHub graph.\n")

    # If no start-date is provided, use 52 weeks (364 days) ago from today
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print("ERROR: Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        start_date = datetime.now() - timedelta(days=364)

    # Call the main drawing function
    draw_on_github(args.word, start_date, mode=args.mode)

    print("Process completed. Now you can run 'git push' to push the commits to your remote repository.")


if __name__ == "__main__":
    main()