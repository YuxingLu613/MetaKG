import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_reaction_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()
    k.organism="hsa"

    reaction_list = k.list("reaction").strip().split("\n")
    reactions_id_list = [reaction.split("\t")[0].replace("hsa","map") for reaction in reaction_list]
    reactions_name_list = [reaction.split("\t")[1] for reaction in reaction_list]
    for reaction in tqdm(reactions_id_list):
        entities.add(("Reaction","Root"))
        triples.add(("reaction_id:"+reaction,"is a","Reaction"))
        try:
            reaction_parse_result=k.parse(k.get(reaction))
            if "PATHWAY" in reaction_parse_result:
                for pathway_id,pathway_name in reaction_parse_result["PATHWAY"].items():
                    entities.add(("Pathway","Root"))
                    triples.add(("pathway_id:"+pathway_id,"is a","Pathway"))
                    entities.add(("pathway_id:"+pathway_id,"Pathway"))
                    triples.add(("reaction_id:"+reaction,"has_pathway","pathway_id:"+pathway_id))
            if "ENZYME" in reaction_parse_result:
                for enzyme in reaction_parse_result["ENZYME"]:
                    entities.add(("Enzyme","Root"))
                    triples.add(("enzyme_id:"+enzyme,"is a","Enzyme"))
                    entities.add(("enzyme_id:"+enzyme,"Enzyme"))
                    triples.add(("reaction_id:"+reaction,"has_enzyme","enzyme_id:"+enzyme))
            if "EQUATION" in reaction_parse_result:
                for equation in reaction_parse_result["EQUATION"].split(" "):
                    if "C" not in equation:
                        continue
                    equation=equation[equation.index("C"):(equation.index("C")+6)]
                    entities.add(("Compound","Root"))
                    triples.add(("compound_id:"+equation,"is a","Compound"))
                    entities.add(("compound_id:"+equation,"Compound"))
                    triples.add(("compound_id:"+equation,"has_reaction","reaction_id:"+reaction))
            if "RCLASS" in reaction_parse_result:
                for rclasses in reaction_parse_result["RCLASS"].split(" "):
                    if "R" not in rclasses:
                        continue
                    rclasses=rclasses[rclasses.index("R"):(rclasses.index("R")+6)]
                    entities.add(("Reaction","Root"))
                    triples.add(("reaction_id:"+rclasses,"is a","Reaction"))
                    entities.add(("reaction_id:"+rclasses,"Reaction"))
                    triples.add(("reaction_id:"+reaction,"belongs_to_reaction_class","reaction_id:"+rclasses))
            if "MODULE" in reaction_parse_result:
                for module_id,module_name in reaction_parse_result["MODULE"].items():
                    entities.add(("Module","Root"))
                    triples.add(("module_id:"+module_id,"is a","Module"))
                    entities.add(("module_id:"+module_id,"Module"))
                    triples.add(("reaction_id:"+reaction,"has_module","module_id:"+module_id))
            if "ORTHOLOGY" in reaction_parse_result:
                for orthology_id,orthology_name in reaction_parse_result["ORTHOLOGY"].items():
                    entities.add(("Orthology","Root"))
                    triples.add(("orthology_id:"+orthology_id,"is a","Orthology"))
                    entities.add(("orthology_id:"+orthology_id,"Orthology"))
                    triples.add(("reaction_id:"+reaction,"belongs_to_orthology","orthology_id:"+orthology_id))
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
            