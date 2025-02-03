#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import argparse
import random
import logging
from datetime import datetime, timedelta
from typing import List

# -----------------------------------------------------------------------------
# Global configuration
# -----------------------------------------------------------------------------
COMMIT_HOUR: str = "12:00:00"  # Fixed commit hour (can be parameterized)

# =============================================================================
# LETTER MAP DICTIONARY
# =============================================================================
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

# =============================================================================
# Helper Functions
# =============================================================================

def run_git_command(cmd: List[str], dry_run: bool = False) -> None:
    """
    Executes a git command using subprocess.run.
    If dry_run is True, only logs the command without executing it.
    """
    if dry_run:
        logging.info(f"[Dry-run] Command: {' '.join(cmd)}")
    else:
        logging.debug(f"Executing command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

def check_git_repo(dry_run: bool = False) -> None:
    """
    Checks if the current directory is a git repository.
    Exits the script with an error if not.
    """
    if dry_run:
        logging.info("[Dry-run] Git repository check skipped.")
        return
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        logging.error("Current directory is not a git repository. Run 'git init' to initialize it.")
        sys.exit(1)

# =============================================================================
# Main Matrix Generators
# =============================================================================

def generate_word_matrix(word: str) -> List[List[str]]:
    """
    Given a word, generates a 2D matrix representing the word using
    pixel-like characters. Each letter occupies 5 columns and is separated by
    1 blank column.
    """
    word = word.upper()
    total_columns = len(word) * 6 - 1
    rows = 7
    final_matrix = [[" " for _ in range(total_columns)] for _ in range(rows)]
    current_col = 0

    for i, letter in enumerate(word):
        # Get the letter representation; if not available, use a blank placeholder.
        letter_pixels = LETTER_MAP.get(letter, ["     "] * rows)
        for r in range(rows):
            for c in range(5):
                final_matrix[r][current_col + c] = letter_pixels[r][c]
        current_col += 6 if i < len(word) - 1 else 5

    return final_matrix

# =============================================================================
# Git Commit Functions
# =============================================================================

def make_commit_for_day(date_str: str, commits: int = 1, dry_run: bool = False, filename: str = "progress.txt") -> None:
    """
    Makes a specified number of commits on the given date.
    For each commit, appends a line to the file (filename) and performs a git commit with a forced date.
    """
    for i in range(commits):
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"Commit {i+1} on {date_str}\n")
        except Exception as e:
            logging.error(f"Error writing to {filename}: {e}")
            sys.exit(1)

        # Stage the file and make the commit
        run_git_command(["git", "add", filename], dry_run=dry_run)
        commit_message = f"Automatic commit on {date_str} ({i+1} of {commits})"
        commit_date_str = f"{date_str}T{COMMIT_HOUR}"
        run_git_command(
            ["git", "commit", "--date", commit_date_str, "-m", commit_message],
            dry_run=dry_run
        )

# =============================================================================
# Drawing Functions
# =============================================================================

def draw_on_github(word: str, start_date: datetime, mode: str = "max", dry_run: bool = False, filename: str = "progress.txt") -> None:
    """
    Generates the commits needed to 'draw' the specified word on the GitHub contributions graph.
    Each column of the matrix corresponds to a week (column * 7 + row days offset).
    """
    matrix = generate_word_matrix(word)
    rows = len(matrix)
    cols = len(matrix[0])

    for col in range(cols):
        for row in range(rows):
            if matrix[row][col] == '#':
                # In max mode, 10 commits per day; in random mode, random between 1 and 10.
                num_commits = 10 if mode == "max" else random.randint(1, 10)
                offset_days = col * 7 + row
                commit_date = start_date + timedelta(days=offset_days)
                date_str = commit_date.strftime("%Y-%m-%d")
                logging.info(f"Date: {date_str} - Commits: {num_commits}")
                make_commit_for_day(date_str, commits=num_commits, dry_run=dry_run, filename=filename)

def draw_full_on_github(start_date: datetime, mode: str = "max", dry_run: bool = False, filename: str = "progress.txt", weeks: int = 52) -> None:
    """
    In full mode, generates commits for every day in the contributions graph grid.
    By default, it fills 52 weeks (7 days each) starting from start_date.
    The commit intensity (max or random) is applied accordingly.
    """
    rows = 7
    cols = weeks  # Each column represents one week.
    for col in range(cols):
        for row in range(rows):
            num_commits = 10 if mode == "max" else random.randint(1, 10)
            offset_days = col * 7 + row
            commit_date = start_date + timedelta(days=offset_days)
            date_str = commit_date.strftime("%Y-%m-%d")
            logging.info(f"Date: {date_str} - Commits: {num_commits}")
            make_commit_for_day(date_str, commits=num_commits, dry_run=dry_run, filename=filename)

# =============================================================================
# Main Function
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Draw a word on your GitHub contributions graph, or fill the entire grid in full mode."
    )
    parser.add_argument("word", nargs="?", help="Word or phrase to draw (ignored in full mode).")
    parser.add_argument(
        "--mode",
        choices=["max", "random"],
        default="max",
        help="Commit mode: 'max' creates 10 commits per day, 'random' creates 1-10 commits per day."
    )
    parser.add_argument(
        "--start-date",
        default=None,
        help="Start date in YYYY-MM-DD format. Defaults to 52 weeks ago if not specified."
    )
    parser.add_argument(
        "--file",
        default="progress.txt",
        help="File to modify for creating commits."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without making actual changes to git."
    )
    parser.add_argument(
        "--commit-hour",
        default=COMMIT_HOUR,
        help="Commit hour in HH:MM:SS format (default: 12:00:00)."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Display detailed logging information."
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Enable full mode: perform commits on every day in the contributions graph grid starting from start_date."
    )
    # Optional parameter to adjust the number of weeks in full mode (default: 52 weeks)
    parser.add_argument(
        "--weeks",
        type=int,
        default=52,
        help="Number of weeks (columns) to fill in full mode. Default is 52."
    )
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Update global commit hour if provided
    global COMMIT_HOUR
    COMMIT_HOUR = args.commit_hour

    # Check if current directory is a git repository
    check_git_repo(dry_run=args.dry_run)

    # Create the progress file if it doesn't exist
    if not os.path.exists(args.file):
        try:
            with open(args.file, "w", encoding="utf-8") as f:
                f.write("Progress file for drawing on the GitHub contributions graph.\n")
        except Exception as e:
            logging.error(f"Error creating file {args.file}: {e}")
            sys.exit(1)

    # Process the start date
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            logging.error("ERROR: Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        start_date = datetime.now() - timedelta(days=364)

    logging.info("Starting the drawing process...")
    if args.full:
        # Full mode: commit for every day in the grid (default 52 weeks x 7 days).
        draw_full_on_github(start_date, mode=args.mode, dry_run=args.dry_run, filename=args.file, weeks=args.weeks)
    else:
        # Word mode: require a word to draw.
        if not args.word:
            logging.error("ERROR: No word provided. Please specify a word or use --full mode.")
            sys.exit(1)
        draw_on_github(args.word, start_date, mode=args.mode, dry_run=args.dry_run, filename=args.file)
    logging.info("Process completed. Now you can run 'git push' to push the commits to your remote repository.")

if __name__ == "__main__":
    main()
