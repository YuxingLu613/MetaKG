from pubchempy import Compound
from utils import load_json
from tqdm import tqdm
import traceback
import csv
import os

# TODO: Not fully done

def get_PubChem_cpd_info(cid,keys_list=["h_bond_acceptor_count","h_bond_donor_count","heavy_atom_count"]):
    entities=set()
    triples=set()
    parse_result=Compound.from_cid(cid).to_dict()
    keys_list=list(set(keys_list)&set(parse_result.keys()))
    cid="pubchem_id:"+str(cid)
    for key in keys_list:
        if key=="h_bond_acceptor_count":
            _="atom_count:"+str(parse_result["h_bond_acceptor_count"])
            entities.add((_,"h_bond_acceptor_count"))
            triples.add((cid,"h_bond_acceptor_count",_))
        if key=="h_bond_donor_count":
            _="atom_count:"+str(parse_result["h_bond_donor_count"])
            entities.add((_,"h_bond_donor_count"))
            triples.add((cid,"h_bond_donor_count",_))
        if key=="heavy_atom_count":
            _="atom_count:"+str(parse_result["heavy_atom_count"])
            entities.add((_,"heavy_atom_count"))
            triples.add((cid,"heavy_atom_count",_))
    import time
    time.sleep(1)
    return entities,triples


def get_pubchem_resource(file_path,selected_metabolites=None):
    
    hmdb_data=load_json(file_path)

    entities=set()
    triples=set()
    pubchem_ids=[]
    for hmdb_id,meta_data in tqdm(hmdb_data.items()):
        if selected_metabolites is not None and hmdb_id not in selected_metabolites:
            continue

        
        if "pubchem_compound_id" in meta_data.keys() and meta_data["pubchem_compound_id"]:
            entities.add(("pubchem_id:"+meta_data["pubchem_compound_id"],"Pubchem_id"))
            triples.add((hmdb_id,"has_pubchem_id","pubchem_id:"+meta_data["pubchem_compound_id"]))
            pubchem_ids.append(meta_data["pubchem_compound_id"])

    for id in tqdm(pubchem_ids[:20]):
        try:
            pubchem_entity,pubchem_triple=get_PubChem_cpd_info(id)
            entities.update(pubchem_entity)
            triples.update(pubchem_triple)
        except Exception as e:
            traceback.print_exc()

    return list(entities),list(triples)

def save_entity(entities):
    with open("data/entities.txt","w") as f:
        for entity in entities:
            f.write("\t".join(entity))
            f.write("\n")

def save_triple(triples):
    with open("data/triples.txt","w") as f:
        for triple in triples:
            f.write("\t".join(triple))
            f.write("\n")

def load_triple():
    triples=[]
    with open("data/triples.txt", newline='', encoding='utf-8') as f:
        all_triples = csv.reader(f, delimiter='\t')
        for line in all_triples:
            triples.append(line)
    return triples
            
def load_entity():
    entities=[]
    with open("data/entities.txt", newline='', encoding='utf-8') as f:
        all_entities = csv.reader(f, delimiter='\t')
        for line in all_entities:
            entities.append(line)
    return entities