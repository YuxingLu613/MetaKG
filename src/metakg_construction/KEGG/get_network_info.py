import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_network_info():
    entities=set()
    triples=set()
    k=kegg.KEGG()

    k.organism="hsa"
    network_list=k.list("network").strip().split("\n")
    network_id_list = [network.split("\t")[0] for network in network_list]
    network_name_list = [network.split("\t")[1] for network in network_list]
    for network_id,network_name in list(zip(network_id_list,network_name_list)):
        entities.add(("Network","Root"))
        entities.add(("network_id:"+network_id,"Network"))
        triples.add(("network_id:"+network_id,"is a","Network"))
        try:
            network_parse_result=k.parse(k.get(network_id))
            if "PATHWAY" in network_parse_result:
                for pathway_id,pathway_name in network_parse_result["PATHWAY"].items():
                    entities.add(("Pathway","Root"))
                    entities.add(("pathway_id:"+pathway_id,"Pathway"))
                    triples.add(("pathway_id:"+pathway_id,"is a","Pathway"))
                    triples.add(("pathway_id:"+network_id,"belongs_to_network","network_id:"+network_id))
            if "DISEASE" in network_parse_result:
                for disease_id,disease_name in network_parse_result["DISEASE"].items():
                    entities.add(("Disease","Root"))
                    entities.add(("disease_id:"+disease_id,"Disease"))
                    triples.add(("disease_id:"+disease_id,"is a","Disease"))
                    triples.add(("disease_id:"+disease_id,"belongs_to_network","network_id:"+network_id))
            if "GENE" in network_parse_result:
                for gene_id,gene_name in network_parse_result["GENE"].items():
                    gene_name=gene_name.split(";")[0]
                    entities.add(("Gene","Root"))
                    entities.add(("gene_name:"+gene_name,"Gene"))
                    triples.add(("gene_name:"+gene_name,"is a","Gene"))
                    triples.add(("gene_name:"+gene_name,"belongs_to_network","network_id:"+network_id))
            if "REFERENCE" in network_parse_result:
                for reference in network_parse_result["REFERENCE"]:
                    if "REFERENCE" in reference.keys() and "PMID" in reference["REFERENCE"]:
                        reference=reference["REFERENCE"][reference["REFERENCE"].index("PMID")+5:]
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+reference,"is a","Reference"))
                        entities.add(("pubmed_id:"+reference,"Reference"))
                        triples.add(("network_id:"+network_id,"has_reference","pubmed_id:"+reference))
            if  "METABOLITE" in network_parse_result:
                for metabolite_id in network_parse_result["METABOLITE"].split(" "):
                    if "C" in metabolite_id:
                        metabolite_id=metabolite_id[metabolite_id.index("C"):metabolite_id.index("C")+6]
                        entities.add(("Compound","Root"))
                        entities.add(("compound_id:"+metabolite_id,"Compound"))
                        triples.add(("compound_id:"+metabolite_id,"is a","Compound"))
                        triples.add(("compound_id:"+metabolite_id,"belongs_to_network","network_id:"+network_id))
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
            