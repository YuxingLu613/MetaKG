import traceback
import json
from tqdm import tqdm
from bioservices import kegg
import re

def get_module_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()

    k.organism="hsa"
    module_list=k.list("module").strip().split("\n")
    module_id_list = [module.split("\t")[0] for module in module_list]
    module_name_list = [module.split("\t")[1] for module in module_list]
    for module_id,module_name in list(zip(module_id_list,module_name_list)):
        entities.add(("Module","Root"))
        entities.add(("module_id:"+module_id,"Module"))
        triples.add(("module_id:"+module_id,"is_a","Module"))
        try:
            module_parse_result=k.parse(k.get(module_id))
            if "ORTHOLOGY" in module_parse_result:
                for orthology_id,orthology_name in module_parse_result["ORTHOLOGY"].items():
                    for orthology in orthology_id.split(","):
                        entities.add(("Orthology","Root"))
                        entities.add(("orthology_id:"+orthology,"Orthology"))
                        triples.add(("orthology_id:"+orthology,"is_a","Orthology"))
                        triples.add(("module_id:"+module_id,"belongs_to_orthology","orthology_id:"+orthology))
            if "REACTION" in module_parse_result:
                for reaction_id,compound_id in module_parse_result["REACTION"].items():
                    for reaction in re.split(",|\+",reaction_id):
                        entities.add(("Reaction","Root"))
                        entities.add(("reaction_id:"+reaction,"Reaction"))
                        triples.add(("reaction_id:"+reaction,"is_a","Reaction"))
                        entities.add(("Compound","Root"))
                        for compound in compound_id.split("->"):
                            compound=compound[compound.index("C"):compound.index("C")+6]
                            entities.add(("compound_id:"+compound,"Compound"))
                            triples.add(("compound_id:"+compound,"is_a","Compound"))
                            triples.add(("reaction_id:"+reaction,"has_compound","compound_id:"+compound))
                            triples.add(("module_id:"+module_id,"has_reaction","reaction_id:"+reaction))
            if "PATHWAY" in module_parse_result:
                for pathway_id,pathway_name in module_parse_result["PATHWAY"].items():
                    entities.add(("Pathway","Root"))
                    entities.add(("pathway_id:"+pathway_id,"Pathway"))
                    triples.add(("pathway_id:"+pathway_id,"is_a","Pathway"))
                    triples.add(("module_id:"+module_id,"has_pathway","pathway_id:"+pathway_id))
            if "COMPOUND" in module_parse_result:
                for compound_id,compound_name in module_parse_result["COMPOUND"].items():
                    entities.add(("Compound","Root"))
                    entities.add(("compound_id:"+compound_id,"Compound"))
                    triples.add(("compound_id:"+compound_id,"is_a","Compound"))
                    triples.add(("compound_id:"+compound_id,"has_module","module_id:"+module_id))
            if "REFERENCE" in module_parse_result:
                for reference in module_parse_result["REFERENCE"]:
                    if "REFERENCE" in reference.keys() and "PMID" in reference["REFERENCE"]:
                        reference=reference["REFERENCE"][reference["REFERENCE"].index("PMID")+5:reference["REFERENCE"].index("]")]
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+reference,"is_a","Reference"))
                        entities.add(("pubmed_id:"+reference,"Reference"))
                        triples.add(("module_id:"+module_id,"has_reference","pubmed_id:"+reference))
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
            