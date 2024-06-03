import os
import pandas as pd

def save_entities(entities, save_path="data/entities.csv"):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if isinstance(entities, list):
            df = pd.DataFrame(entities,columns=["Entity","Entity Type"])
        elif isinstance(entities, pd.DataFrame):
            df = entities
        else:
            raise ValueError("Entities must be either a list or a DataFrame")
        df.to_csv(save_path, index=False)
        print(f"Entities saved to {save_path}")
    except Exception as e:
        print(f"Error occurred while saving entities: {e}")

def save_triples(triples, save_path="data/triples.csv"):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if isinstance(triples, list):
            df = pd.DataFrame(triples,columns=["Head","Relationship","Tail"])
        elif isinstance(triples, pd.DataFrame):
            df = triples
        else:
            raise ValueError("Triples must be either a list or a DataFrame")
        df.to_csv(save_path, index=False)
        print(f"Triples saved to {save_path}")
    except Exception as e:
        print(f"Error occurred while saving triples: {e}")
