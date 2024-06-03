import os
import sys
sys.path.append("../../")
import pandas as pd
from tqdm import tqdm
from utils.save_data import save_entities,save_triples
from smpdb_metabolite_extract import extract_smpdb_metabolite_data
from smpdb_protein_extract import extract_smpdb_protein_data

def extract_smpdb():
    metabolite_entities,metabolite_triples=extract_smpdb_metabolite_data(
        metabolite_files_dir="../../../data/resource/SMPDB/smpdb_metabolites",
        save_entities_path="../../../data/extract_triples/SMPDB/smpdb_metabolite_entities.csv",
        save_triples_path="../../../data/extract_triples/SMPDB/smpdb_metabolite_triples.csv"
        )

    protein_entities,protein_triples=extract_smpdb_protein_data(
        protein_files_dir="../../../data/resource/SMPDB/smpdb_proteins",
        save_entities_path="../../../data/extract_triples/SMPDB/smpdb_protein_entities.csv",
        save_triples_path="../../../data/extract_triples/SMPDB/smpdb_protein_triples.csv"
        )


    smpdb_entities=pd.concat([metabolite_entities,protein_entities],axis=0).drop_duplicates()
    smpdb_triples=pd.concat([metabolite_triples,protein_triples],axis=0).drop_duplicates()

    save_entities(smpdb_entities,"../../../data/extract_triples/SMPDB/smpdb_entities.csv")
    save_triples(smpdb_triples,"../../../data/extract_triples/SMPDB/smpdb_triples.csv")
    
    return smpdb_entities,smpdb_triples

extract_smpdb()