"""
This module provides methods to read in the raw data.
"""
import glob
import os

import pandas as pd


def get_files(filepath):
    """
    Gets all files in nested filepath.
    """
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for file in files:
            all_files.append(os.path.abspath(file))

    return all_files


def read_file(filepath):
    """
    Reads .json file.
    """
    return pd.read_json(filepath, lines=True)
