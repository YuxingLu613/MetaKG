
from bioservices import chebi
from utils import load_json
from tqdm import tqdm
import traceback
import csv
import os

# TODO: Not fully done

def get_CHEBI_cpd_info(cid,keys_list=["OntologyParents"]):
    entities=set()
    triples=set()
    c=chebi.ChEBI()
    parse_result=c.getCompleteEntity(cid)
    cid="chebi_id:"+str(cid)
    for key in keys_list:
        if key=="OntologyParents":
            _=parse_result["OntologyParents"]
            for i in _:
                entities.add((str(i["chebiId"]),"Chebi_id"))
                triples.add((cid,str(i["type"]),str(i["chebiId"])))
    return entities,triples

def get_chebi_resource(file_path,selected_metabolites=None):
    
    hmdb_data=load_json(file_path)

    entities=set()
    triples=set()
    chebi_ids=[]
    for hmdb_id,meta_data in tqdm(hmdb_data.items()):
        if selected_metabolites is not None and hmdb_id not in selected_metabolites:
            continue
        
        # hmdb_id="hmdb_id:"+hmdb_id
        # entities.add((hmdb_id,"Hmdb_id"))
        
        if "chebi_id" in meta_data.keys() and meta_data["chebi_id"]:
            entities.add(("chebi_id:"+meta_data["chebi_id"],"Chebi_id"))
            triples.add((hmdb_id,"has_chebi_id","chebi_id:"+meta_data["chebi_id"]))
            chebi_ids.append(meta_data["chebi_id"])

    for id in tqdm(chebi_ids[:30]):
        try:
            chebi_entity,chebi_triple=get_CHEBI_cpd_info(id)
            entities.update(chebi_entity)
            triples.update(chebi_triple)
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
