import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_cpd_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()
    k.organism="hsa"
    
    compound_list = k.list("compound").strip().split("\n")
    compounds_id_list = [compound.split("\t")[0].replace("hsa","map") for compound in compound_list]
    compounds_name_list = [compound.split("\t")[1] for compound in compound_list]

    for compound in tqdm(compounds_id_list):
        entities.add(("Compound","Root"))
        entities.add(("compound_id:"+compound,"Compound"))
        triples.add(("compound_id:"+compound,"is_a","Compound"))
        try:
            compound_parse_result=k.parse(k.get(compound))
            if "REACTION" in compound_parse_result:
                if not isinstance(compound_parse_result["REACTION"],list):
                    compound_parse_result["REACTION"]=[compound_parse_result["REACTION"]]
                for reaction in compound_parse_result["REACTION"]:
                    entities.add(("Reaction","Root"))
                    triples.add(("reaction_id:"+reaction,"is_a","Reaction"))
                    entities.add(("reaction:"+reaction,"Reaction")) 
                    triples.add(("compound_id:"+compound,"has_reaction","reaction_id:"+reaction))
            if "REMARK" in compound_parse_result:
                for remark in compound_parse_result["REMARK"]:
                    if "D" not in remark:
                        continue
                    remark=remark[remark.index("D"):remark.index("D")+6]
                    entities.add(("Drug","Root"))
                    triples.add(("drug_id:"+remark,"is_a","Drug"))
                    entities.add(("drug_id:"+remark,"Drug"))
                    triples.add(("compound_id:"+compound,"same_as","drug_id:"+remark))
            if "PATHWAY" in compound_parse_result:
                for pathway_id,pathway_name in compound_parse_result["PATHWAY"].items():
                    entities.add(("Pathway","Root"))
                    triples.add(("pathway_id:"+pathway_id,"is_a","Pathway"))
                    entities.add(("pathway_id:"+pathway_id,"Pathway"))
                    triples.add(("compound_id:"+compound,"has_pathway","pathway_id:"+pathway_id))
            if "MODULE" in compound_parse_result:
                for module_id,module_name in compound_parse_result["MODULE"].items():
                    entities.add(("Module","Root"))
                    triples.add(("module_id:"+module_id,"is_a","Module"))
                    entities.add(("module_id:"+module_id,"Module"))
                    triples.add(("compound_id:"+compound,"has_module","module_id:"+module_id))
            if "NETWORK" in compound_parse_result:
                for network_id,network_name in compound_parse_result["NETWORK"].items():
                    if network_id=="ELEMENT" or not network_name:
                        continue
                    entities.add(("Network","Root"))
                    triples.add(("network_id:"+network_id,"is_a","Network"))
                    entities.add(("network_id:"+network_id,"Network"))
                    triples.add(("compound_id:"+compound,"has_network","network_id:"+network_id))
            if "ENZYME" in compound_parse_result:
                for enzyme in compound_parse_result["ENZYME"]:
                    entities.add(("Enzyme","Root"))
                    triples.add(("enzyme_id:"+enzyme,"is_a","Enzyme"))
                    entities.add(("enzyme_id:"+enzyme,"Enzyme"))
                    triples.add(("compound_id:"+compound,"has_enzyme","enzyme_id:"+enzyme))
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
