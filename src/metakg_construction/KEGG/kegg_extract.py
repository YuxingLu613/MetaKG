from .get_cpd_info import get_cpd_info
from .get_enzyme_info import get_enzyme_info
from .get_pathway_info import get_pathway_info
from .get_reaction_info import get_reaction_info
from .get_module_info import get_module_info
from .get_network_info import get_network_info
from .get_disease_info import get_disease_info
import csv
from utils.save_data import save_entities, save_triples
import sys
sys.path.append("src/")

entities=[]
triples=[]

def save_entity(entities,save_path="data/entities.txt"):
    with open(save_path,"w") as f:
        for entity in entities:
            f.write("\t".join(entity))
            f.write("\n")

def save_triple(triples,save_path="data/triples.txt"):
    with open(save_path,"w") as f:
        for triple in triples:
            f.write("\t".join(triple))
            f.write("\n")

def load_triple(load_path="data/triples.txt"):
    triples=[]
    with open(load_path, newline='', encoding='utf-8') as f:
        all_triples = csv.reader(f, delimiter='\t')
        for line in all_triples:
            triples.append(line)
    return triples
            
def load_entity(load_path="data/entities.txt"):
    entities=[]
    with open(load_path, newline='', encoding='utf-8') as f:
        all_entities = csv.reader(f, delimiter='\t')
        for line in all_entities:
            entities.append(line)
    return entities

def extract_kegg_data():
    # TODO: rewrite and extract from local data, save in csv format
    # cpd_entities,cpd_triples=get_cpd_info()
    # save_entity(cpd_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_cpd_entities.txt")
    # save_triple(cpd_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_cpd_triples.txt")
    cpd_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_cpd_entities.txt")
    cpd_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_cpd_triples.txt")
    entities.extend(cpd_entities)
    triples.extend(cpd_triples)

    # enzyme_entities,enzyme_triples=get_enzyme_info()
    # save_entity(enzyme_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_enzyme_entities.txt")
    # save_triple(enzyme_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_enzyme_triples.txt")
    enzyme_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_enzyme_entities.txt")
    enzyme_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_enzyme_triples.txt")
    entities.extend(enzyme_entities)
    triples.extend(enzyme_triples)

    # pathway_entities,pathway_triples=get_pathway_info()
    # save_entity(pathway_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_pathway_entities.txt")
    # save_triple(pathway_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_pathway_triples.txt")
    pathway_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_pathway_entities.txt")
    pathway_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_pathway_triples.txt")
    entities.extend(pathway_entities)
    triples.extend(pathway_triples)

    # reaction_entities,reaction_triples=get_reaction_info()
    # save_entity(reaction_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_reaction_entities.txt")
    # save_triple(reaction_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_reaction_triples.txt")
    reaction_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_reaction_entities.txt")
    reaction_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_reaction_triples.txt")
    entities.extend(reaction_entities)
    triples.extend(reaction_triples)

    # module_entities,module_triples=get_module_info()
    # save_entity(module_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_module_entities.txt")
    # save_triple(module_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_module_triples.txt")
    module_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_module_entities.txt")
    module_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_module_triples.txt")
    entities.extend(module_entities)
    triples.extend(module_triples)

    # network_entities,network_triples=get_network_info()
    # save_entity(network_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_network_entities.txt")
    # save_triple(network_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_network_triples.txt")
    network_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_network_entities.txt")
    network_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_network_triples.txt")
    entities.extend(network_entities)
    triples.extend(network_triples)

    # disease_entities,disease_triples=get_disease_info()
    # save_entity(disease_entities,"data/extract_data/KEGG/kegg_preprocessed/kegg_disease_entities.txt")
    # save_triple(disease_triples,"data/extract_data/KEGG/kegg_preprocessed/kegg_disease_triples.txt")
    disease_entities=load_entity("data/extract_data/KEGG/kegg_preprocessed/kegg_disease_entities.txt")
    disease_triples=load_triple("data/extract_data/KEGG/kegg_preprocessed/kegg_disease_triples.txt")
    entities.extend(disease_entities)
    triples.extend(disease_triples)


    for i in triples:
        if len(i)<3 or "\n" in i[0] or "\n" in i[1] or "\n" in i[2]:
            triples.remove(i)
            continue
        if i[1]=="has_drug":
            triples.remove(i)
    return entities,triples
