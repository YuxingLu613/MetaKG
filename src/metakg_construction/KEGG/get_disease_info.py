import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_disease_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()
    k.organism="hsa"
    disease_list=k.list("disease").strip().split("\n")
    disease_id_list = [disease.split("\t")[0] for disease in disease_list]
    disease_name_list = [disease.split("\t")[1] for disease in disease_list]
    for disease_id,disease_name in list(zip(disease_id_list,disease_name_list)):
        entities.add(("Disease","Root"))
        entities.add(("disease_id:"+disease_id,"Disease"))
        triples.add(("disease_id:"+disease_id,"is a","Disease"))
        try:
            disease_parse_result=k.parse(k.get(disease_id))
            if "REFERENCE" in disease_parse_result:
                for reference in disease_parse_result["REFERENCE"]:
                    if "REFERENCE" in reference.keys() and "PMID" in reference["REFERENCE"]:
                        reference=reference["REFERENCE"][reference["REFERENCE"].index("PMID")+5:]
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+reference,"is a","Reference"))
                        entities.add(("pubmed_id:"+reference,"Reference"))
                        triples.add(("disease_id:"+disease_id,"has_reference","pubmed_id:"+reference))
            if "DRUG" in disease_parse_result:
                for drug_id,drug_name in disease_parse_result["DRUG"].items():
                    drug_id=drug_id.split(":")[-1][:-1]
                    entities.add(("Drug","Root"))
                    entities.add(("drug_id:"+drug_id,"Drug"))
                    triples.add(("drug_id:"+drug_id,"is a","Drug"))
                    triples.add(("disease_id:"+disease_id,"has_drug","disease_id:"+drug_id))
        except Exception as e:
            traceback.print_exc()
            
        return entities,triples


def save_entity(entities,path="data/entities.txt"):
    with open(path,"w") as f:
        for entity in entities:
            f.write("\t".join(entity))
            f.write("\n")

def save_triple(triples,path="data/triples.txt"):
    with open(path,"w") as f:
        for triple in triples:
            f.write("\t".join(triple))
            f.write("\n")
            