#!/usr/bin/env python3
import os
import re
import sys
from dotenv import load_dotenv

# Load .env file from current directory
load_dotenv()

MOVIES_DIR = os.getenv("MOVIES_DIR")
IMDB_ID_PATTERN = r"\[imdbid-tt\d+\]"

def error_checks():
    if not MOVIES_DIR:
        print("ERROR: Unset variable: MOVIES_DIR")
        return False
    if not os.path.isdir(MOVIES_DIR):
        print(f"ERROR: Missing dir: {MOVIES_DIR}")
        return False
    return True

def process_movie(path):
    name = os.path.basename(path)

    if "  " in name:
        print(f"ERROR: Doublespace found in file name: {path}")
        return False

    name_parts = name.split(" ")

    if len(name_parts) < 2:
        print(f"ERROR: Incomplete structure: {path}")
        return False

    movie = name_parts[0]
    year = name_parts[1]

    imdbid_match = re.search(IMDB_ID_PATTERN, name)
    has_imdbid = imdbid_match is not None

    if not re.match(r"^\(\d{4}\)$", year):
        print(f"ERROR: Invalid year: {path}")
        return False

    if has_imdbid:
        print(f"OK: {name}")
    else:
        print(f"MISSING IMDb ID: {name}")

    return True

def main():
    if not error_checks():
        sys.exit(1)

    for item in sorted(os.listdir(MOVIES_DIR)):
        full_path = os.path.join(MOVIES_DIR, item)
        if os.path.isdir(full_path):
            process_movie(full_path)

if __name__ == "__main__":
    main()
