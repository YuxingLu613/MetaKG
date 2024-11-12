import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_enzyme_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()
    enzyme_list = k.list("enzyme").strip().split("\n")
    enzymes_id_list = [enzyme.split("\t")[0].replace("hsa","map") for enzyme in enzyme_list]
    enzymes_name_list = [enzyme.split("\t")[1] for enzyme in enzyme_list]
    for enzyme in tqdm(enzymes_id_list):
        entities.add(("Enzyme","Root"))
        entities.add(("enzyme_id:"+enzyme,"Enzyme"))
        triples.add(("enzyme_id:"+enzyme,"is_a","Enzyme"))
        try:
            enzyme_parse_result=k.parse(k.get(enzyme))
            if "ALL_REAC" in enzyme_parse_result:
                for reaction in enzyme_parse_result["ALL_REAC"]:
                    if reaction[0]=="<":
                        continue
                    entities.add(("Reaction","Root"))
                    triples.add(("reaction_id:"+reaction,"is_a","Reaction"))
                    entities.add(("reaction_id:"+reaction,"Reaction"))
                    triples.add(("reaction_id:"+reaction,"has_enzyme","enzyme_id:"+enzyme))
            if "SUBSTRATE" in enzyme_parse_result:
                for substrate in enzyme_parse_result["SUBSTRATE"]:
                    if ":" not in substrate:
                        continue
                    entities.add(("Compound","Root"))
                    cpd_id=substrate.split(" ")[-1]
                    cpd_id=cpd_id[cpd_id.index(":")+1:cpd_id.index(":")+7]
                    triples.add(("compound_id:"+cpd_id,"is_a","Compound"))
                    entities.add(("compound_id:"+cpd_id,"Compound"))
                    triples.add(("enzyme_id:"+enzyme,"has_substrate","compound_id:"+substrate))
            if "PRODUCT" in enzyme_parse_result:
                for product in enzyme_parse_result["PRODUCT"]:
                    if ":" not in product:
                        continue
                    entities.add(("Compound","Root"))
                    cpd_id=product.split(" ")[-1]
                    cpd_id=cpd_id[cpd_id.index(":")+1:cpd_id.index(":")+7]
                    triples.add(("compound_id:"+cpd_id,"is_a","Compound"))
                    entities.add(("compound_id:"+cpd_id,"Compound"))
                    triples.add(("enzyme_id:"+enzyme,"has_product","compound_id:"+cpd_id))
            if "PATHWAY" in enzyme_parse_result:
                for pathway_id,pathway_name in enzyme_parse_result["PATHWAY"].items():
                    pathway_id=pathway_id.replace("ec","map")
                    entities.add(("Pathway","Root"))
                    entities.add(("pathway_id:"+pathway_id,"Pathway"))
                    triples.add(("pathway_id:"+pathway_id,"is_a","Pathway"))
                    triples.add(("enzyme_id:"+enzyme,"has_pathway","pathway_id:"+pathway_id))
            if "MODULE" in enzyme_parse_result:
                for module_id,module_name in enzyme_parse_result["MODULE"].items():
                    entities.add(("Module","Root"))
                    triples.add(("module_id:"+module_id,"is_a","Module"))
                    entities.add(("module_id:"+module_id,"Module"))
                    triples.add(("enzyme_id:"+enzyme,"has_module","module_id:"+module_id))
            if "ORTHOLOGY" in enzyme_parse_result:
                for orthology_id,orthology_name in enzyme_parse_result["ORTHOLOGY"].items():
                    entities.add(("Orthology","Root"))
                    triples.add(("orthology_id:"+orthology_id,"is_a","Orthology"))
                    entities.add(("orthology_id:"+orthology_id,"Orthology"))
                    triples.add(("enzyme_id:"+enzyme,"belongs_to_orthology","orthology_id:"+orthology_id))
            if "GENES" in enzyme_parse_result:
                if "HSA" in enzyme_parse_result["GENES"]:
                    hsa_genes=enzyme_parse_result["GENES"]["HSA"].split(" ")
                    for hsa_gene in hsa_genes:
                        hsa_gene=hsa_gene[hsa_gene.index("(")+1:hsa_gene.index(")")]
                        entities.add(("Gene","Root"))
                        triples.add(("gene_name:"+hsa_gene,"is_a","Gene"))
                        entities.add(("gene_name:"+hsa_gene,"Gene"))
                        triples.add(("enzyme_id:"+enzyme,"related_to_gene","gene_name:"+hsa_gene))
            if "REFERENCE" in enzyme_parse_result:
                for reference in enzyme_parse_result["REFERENCE"]:
                    if "REFERENCE" in reference.keys() and "PMID" in reference["REFERENCE"]:
                        reference=reference["REFERENCE"][reference["REFERENCE"].index("PMID")+5:reference["REFERENCE"].index("]")]
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+reference,"is_a","Reference"))
                        entities.add(("pubmed_id:"+reference,"Reference"))
                        triples.add(("enzyme_id:"+enzyme,"has_reference","pubmed_id:"+reference))
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
            