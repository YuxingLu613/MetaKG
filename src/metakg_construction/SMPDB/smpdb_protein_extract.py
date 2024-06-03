import os
import sys
sys.path.append("../../")
import pandas as pd
from tqdm import tqdm
from utils.save_data import save_entities,save_triples

def extract_smpdb_protein_data(protein_files_dir, save_entities_path=None, save_triples_path=None):
    protein_file_list=os.listdir(protein_files_dir)
    protein_df = pd.concat([pd.read_csv(os.path.join(protein_files_dir,f)) for f in protein_file_list])

    protein_df.loc[protein_df["Pathway Name"].str.contains("De Novo Triacylglycerol Biosynthesis"), "SMPDB ID"] = "SYN00001"
    protein_df.loc[protein_df["Pathway Name"].str.contains("Cardiolipin Biosynthesis"), "SMPDB ID"] = "SYN00002"
    protein_df.loc[protein_df["Pathway Name"].str.contains("Phosphatidylcholine Biosynthesis"), "SMPDB ID"] = "SYN00003"
    protein_df.loc[protein_df["Pathway Name"].str.contains("Phosphatidylethanolamine Biosynthesis"), "SMPDB ID"] = "SYN00004"

    useful_info=protein_df[["SMPDB ID","Pathway Subject","Uniprot ID","HMDBP ID","Gene Name"]].drop_duplicates()

    entities = set()
    triples = set()
    for index,info in tqdm(useful_info.iterrows(),desc="extracting SMPDB proteins",total=len(protein_file_list)):
        entities.add(("pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:],"Pathway"))
        triples.add(("pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:],"is_a","Pathway"))
        if pd.notna(info["HMDBP ID"]):
            entities.add(("hmdbp_id:"+info["HMDBP ID"],"Compound"))
            triples.add(("hmdbp_id:"+info["HMDBP ID"],"is_a","Protein"))
            triples.add(("hmdbp_id:"+info["HMDBP ID"],"related_to_pathway","pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:]))
        if pd.notna(info["Uniprot ID"]):
            entities.add(("uniport_id:"+info["Uniprot ID"],"Protein"))
            triples.add(("uniport_id:"+info["Uniprot ID"],"is_a","Protein"))
            triples.add(("uniport_id:"+info["Uniprot ID"],"related_to_pathway","pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:]))
            if pd.notna(info["HMDBP ID"]):
                triples.add(("hmdbp_id:"+info["HMDBP ID"],"has_uniprot_id","uniport_id:"+info["Uniprot ID"]))
        if pd.notna(info["Pathway Subject"]):
            entities.add(("taxonomy_class:"+info["Pathway Subject"],"Taxonomy_Class"))
            triples.add(("taxonomy_class:"+info["Pathway Subject"],"is_a","Taxonomy_Class"))
            triples.add(("pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:],"has_pathway_class","taxonomy_class:"+info["Pathway Subject"]))
        if pd.notna(info["Gene Name"]):
            entities.add(("gene_name:"+info["Gene Name"],"Gene"))
            triples.add(("gene_name:"+info["Gene Name"],"is_a","Gene"))
            triples.add(("gene_name:"+info["Gene Name"],"related_to_pathway","pathway_id:"+info["SMPDB ID"][:3]+info["SMPDB ID"][5:]))
            if pd.notna(info["HMDBP ID"]):
                triples.add(("hmdbp_id:"+info["HMDBP ID"],"related_to_gene","gene_name:"+info["Gene Name"]))

    entities=pd.DataFrame(entities,columns=["Entity","Entity Type"])
    triples=pd.DataFrame(triples,columns=["Head","Relationship", "Tail"])

    if save_entities_path:
        save_entities(entities, save_path=save_entities_path)
    if save_triples_path:
        save_triples(triples, save_path=save_triples_path)

    return entities,triples