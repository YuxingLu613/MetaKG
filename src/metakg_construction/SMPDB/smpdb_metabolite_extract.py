import os
import sys
sys.path.append("../../")
import pandas as pd
from tqdm import tqdm
from utils.save_data import save_entities,save_triples

def extract_smpdb_metabolite_data(metabolite_files_dir, save_entities_path=None, save_triples_path=None):
    metabolite_file_list = os.listdir(metabolite_files_dir)
    metabolite_df = pd.concat([pd.read_csv(os.path.join(metabolite_files_dir, f)) for f in metabolite_file_list])

    metabolite_df.loc[metabolite_df["Pathway Name"].str.contains("De Novo Triacylglycerol Biosynthesis"), "SMPDB ID"] = "SYN00001"
    metabolite_df.loc[metabolite_df["Pathway Name"].str.contains("Cardiolipin Biosynthesis"), "SMPDB ID"] = "SYN00002"
    metabolite_df.loc[metabolite_df["Pathway Name"].str.contains("Phosphatidylcholine Biosynthesis"), "SMPDB ID"] = "SYN00003"
    metabolite_df.loc[metabolite_df["Pathway Name"].str.contains("Phosphatidylethanolamine Biosynthesis"), "SMPDB ID"] = "SYN00004"

    useful_info = metabolite_df[["SMPDB ID", "Pathway Subject", "HMDB ID", "KEGG ID"]].drop_duplicates()

    entities = set()
    triples = set()
    for index, info in tqdm(useful_info.iterrows(), desc="extracting SMPDB metabolites",total=len(metabolite_file_list)):
        pathway_id = "pathway_id:" + info["SMPDB ID"][:3] + info["SMPDB ID"][5:]
        entities.add((pathway_id, "Pathway"))
        triples.add((pathway_id, "is_a", "Pathway"))

        if pd.notna(info["HMDB ID"]):
            hmdb_id = "hmdb_id:" + info["HMDB ID"]
            entities.add((hmdb_id, "Compound"))
            triples.add((hmdb_id, "is_a", "Compound"))
            triples.add((hmdb_id, "has_pathway", pathway_id))

        if pd.notna(info["KEGG ID"]):
            compound_id = "compound_id:" + info["KEGG ID"]
            entities.add((compound_id, "Compound"))
            triples.add((compound_id, "is_a", "Compound"))
            triples.add((compound_id, "has_pathway", pathway_id))

        if pd.notna(info["Pathway Subject"]):
            taxonomy_class_id = "taxonomy_class:" + info["Pathway Subject"]
            entities.add((taxonomy_class_id, "Taxonomy_Class"))
            triples.add((taxonomy_class_id, "is_a", "Taxonomy_Class"))
            triples.add((pathway_id, "has_pathway_class", taxonomy_class_id))

    entities=pd.DataFrame(entities,columns=["Entity","Entity Type"])
    triples=pd.DataFrame(triples,columns=["Head","Relationship", "Tail"])

    if save_entities_path:
        save_entities(entities, save_path=save_entities_path)
    if save_triples_path:
        save_triples(triples, save_path=save_triples_path)

    return entities,triples