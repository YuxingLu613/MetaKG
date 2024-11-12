import traceback
import json
from tqdm import tqdm
from bioservices import kegg

def get_pathway_info():
    entities=set()
    triples=set()

    k=kegg.KEGG()

    entities=set()
    triples=set()
    k.organism="hsa"
    pathway_list = k.list("pathway", organism="hsa").strip().split("\n")
    pathways_id_list = [pathway.split("\t")[0].replace("hsa","map") for pathway in pathway_list]
    pathways_name_list = [pathway.split("\t")[1] for pathway in pathway_list]
    for pathway,pathway_name in tqdm(list(zip(pathways_id_list,pathways_name_list))):
        entities.add(("Pathway","Root"))
        entities.add(("pathway_id:"+pathway,"Pathway"))
        triples.add(("pathway_id:"+pathway,"is_a","Pathway"))
        try:
            pathway_parse_result=k.parse(k.get(pathway))
            if "MODULE" in pathway_parse_result:
                for module_id,module_name in pathway_parse_result["MODULE"].items():
                    module_id=module_id[4:]
                    entities.add(("Module","Root"))
                    entities.add(("module_id:"+module_id,"Module"))
                    triples.add(("module_id:"+module_id,"is_a","Module"))
                    triples.add(("pathway_id:"+pathway,"has_module","module_id:"+module_id))
            if "DRUG" in pathway_parse_result:
                for drug_id,drug_name in pathway_parse_result["DRUG"].items():
                    entities.add(("Drug","Root"))
                    entities.add(("drug_id:"+drug_id,"Drug"))
                    triples.add(("drug_id:"+drug_id,"is_a","Drug"))
                    triples.add(("pathway_id:"+pathway,"has_drug","drug_id:"+drug_id))
            if "REL_PATHWAY" in pathway_parse_result:
                rel_pathways=pathway_parse_result["REL_PATHWAY"].split("             ")
                for rel_pathway in rel_pathways:
                    rel_pathway_id=rel_pathway[rel_pathway.index("map"):rel_pathway.index("map")+8]
                    rel_pathway_name=rel_pathway[rel_pathway.index("map")+10:]
                    entities.add(("Pathway","Root"))
                    entities.add(("pathway_id:"+rel_pathway_id,"Pathway"))
                    triples.add(("pathway_id:"+rel_pathway_id,"is_a","Pathway"))
                    triples.add(("pathway_id:"+pathway,"related_to_pathway","pathway_id:"+rel_pathway_id))
            if "COMPOUND" in pathway_parse_result:
                for compound_id,compound_name in pathway_parse_result["COMPOUND"].items():
                    entities.add(("Compound","Root"))
                    entities.add(("compound_id:"+compound_id,"Compound"))
                    triples.add(("compound_id:"+compound_id,"is_a","Compound"))
                    triples.add(("compound_id:"+compound_id,"has_pathway","pathway_id:"+pathway))
            if "REFERENCE" in pathway_parse_result:
                for reference in pathway_parse_result["REFERENCE"]:
                    if "REFERENCE" in reference.keys() and "PMID" in reference["REFERENCE"]:
                        reference=reference["REFERENCE"][reference["REFERENCE"].index("PMID")+5:reference["REFERENCE"].index("]")]
                        entities.add(("Reference","Root"))
                        entities.add(("pubmed_id:"+reference,"Reference"))
                        triples.add(("pubmed_id:"+reference,"is_a","Reference"))
                        triples.add(("pathway_id:"+pathway,"has_reference","pubmed_id:"+reference))
            if "NETWORK" in pathway_parse_result:
                for network in pathway_parse_result["NETWORK"]:
                    for network_id,network_name in pathway_parse_result["NETWORK"].items():
                        if network_id=="ELEMENT" or not network_name:
                            continue
                        entities.add(("Network","Root"))
                        entities.add(("network_id:"+network_id,"Network"))
                        triples.add(("network_id:"+network_id,"is_a","Network"))
                        triples.add(("pathway_id:"+pathway,"has_network","network_id:"+network_id))
            if "GENE" in pathway_parse_result:
                for gene_id,gene_name in pathway_parse_result["GENE"].items():
                    hsa_gene=gene_name[:gene_name.index(";")]
                    entities.add(("Gene","Root"))
                    triples.add(("gene_id:"+hsa_gene,"is_a","Gene"))
                    entities.add(("gene_name:"+hsa_gene,"Gene"))
                    triples.add(("pathway_id:"+pathway,"related_to_gene","gene_name:"+hsa_gene))
                    if "KO" in gene_name:
                        KO_id=gene_name[gene_name.index("KO:")+3:gene_name.index("KO:")+9]
                        entities.add(("KO","Root"))
                        entities.add(("ko_id:"+KO_id,"KO"))
                        triples.add(("ko_id:"+KO_id,"is_a","KO"))
                        triples.add(("gene_name:"+hsa_gene,"has_ko","ko_id:"+KO_id))
                    if "EC" in gene_name:
                        EC_id=gene_name[gene_name.index("EC:")+3:gene_name.index("EC:")+9]
                        entities.add(("EC","Root"))
                        entities.add(("ec_id:"+EC_id,"EC"))
                        triples.add(("ec_id:"+EC_id,"is_a","EC"))
                        triples.add(("gene_name:"+hsa_gene,"has_ec","ec_id:"+EC_id))
            if "KO_PATHWAY" in pathway_parse_result:
                KO_id=pathway_parse_result["KO_PATHWAY"]
                entities.add(("Pathway","Root"))
                entities.add(("pathway_id:"+KO_id,"KO"))
                triples.add(("pathway_id:"+KO_id,"is_a","Pathway"))
                triples.add(("pathway_id:"+pathway,"same as","pathway_id:"+KO_id))
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
            