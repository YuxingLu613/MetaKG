import os
import csv
import pandas as pd
import json

def load_entities(file_path="data/entities.csv", as_dataframe=True):
    try:
        if os.path.exists(file_path):
            if as_dataframe:
                return pd.read_csv(file_path,low_memory=False)
            else:
                entities = []
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter='\t')
                    for line in reader:
                        entities.append(line)
                return entities
        else:
            print(f"File '{file_path}' does not exist.")
            return None
    except Exception as e:
        print(f"Error occurred while loading entities: {e}")
        return None


def load_triples(file_path="data/triples.csv", as_dataframe=True):
    try:
        if os.path.exists(file_path):
            if as_dataframe:
                return pd.read_csv(file_path,low_memory=False)
            else:
                triples = []
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter='\t')
                    for line in reader:
                        triples.append(line)
                return triples
        else:
            print(f"File '{file_path}' does not exist.")
            return None
    except Exception as e:
        print(f"Error occurred while loading triples: {e}")
        return None


def load_json(input_path):
    """
    Load and parse a JSON file from a specified input file path.

    Args:
        input_path (str): The file path of the input JSON file.

    Returns:
        dict: A dictionary containing the parsed JSON data.
    """
    with open(input_path, "r") as f:
        content = json.load(f)
    return content
