import sys
import os
import pandas as pd
from src.utils.save_data import save_entities,save_triples
from src.utils.load_data import load_entities,load_triples
from src.metakg_construction.HMDB.hmdb_extract import extract_hmdb_data
from src.metakg_construction.SMPDB.smpdb_metabolite_extract import extract_smpdb_metabolite_data
from src.metakg_construction.SMPDB.smpdb_protein_extract import extract_smpdb_protein_data
from src.metakg_construction.KEGG.kegg_extract import extract_kegg_data
from src.metakg_analysis.statistics import summary
from src.metakg_analysis.search import search
from src.metakg_analysis.visualize import visualize_graph
from src.metakg_machine_learning import data_partition,kge_training_pipeline


# Stage 1 MetaKG Library: Extract data from metabolome KGs, MetaKG Library construction
# TODO (partially done): Access to more databases (ChEBI, PubChem) and parse
# TODO (partially done): Entity alignment and data cleaning


## Parse HMDB
hmdb_entities,hmdb_triples=extract_hmdb_data(file_path="data/resource/HMDB/hmdb_metabolites.json")
if not os.path.exists("data/extract_data/HMDB"):
    os.mkdir("data/extract_data/HMDB")
save_entities(entities=hmdb_entities,save_path="data/extract_data/HMDB/hmdb_entities.csv")
save_triples(triples=hmdb_triples,save_path="data/extract_data/HMDB/hmdb_triples.csv")


# ## Parse SMPDB
metabolite_entities,metabolite_triples=extract_smpdb_metabolite_data(metabolite_files_dir="data/resource/SMPDB/smpdb_metabolites")
protein_entities,protein_triples=extract_smpdb_protein_data(protein_files_dir="data/resource/SMPDB/smpdb_proteins")
smpdb_entities=pd.concat([metabolite_entities,protein_entities],axis=0).drop_duplicates()
smpdb_triples=pd.concat([metabolite_triples,protein_triples],axis=0).drop_duplicates()
if not os.path.exists("data/extract_data/SMPDB"):
    os.mkdir("data/extract_data/SMPDB")
save_entities(smpdb_entities,"data/extract_data/SMPDB/smpdb_entities.csv")
save_triples(smpdb_triples,"data/extract_data/SMPDB/smpdb_triples.csv")


## Parse KEGG
kegg_entities,kegg_triples=extract_kegg_data()
if not os.path.exists("data/extract_data/KEGG"):
    os.mkdir("data/extract_data/KEGG")
save_entities(kegg_entities,"data/extract_data/KEGG/kegg_entities.csv")
save_triples(kegg_triples,"data/extract_data/KEGG/kegg_triples.csv")


## Load Data
hmdb_entities=load_entities("data/extract_data/HMDB/hmdb_entities.csv")
hmdb_triples=load_triples("data/extract_data/HMDB/hmdb_triples.csv")
smpdb_entities=load_entities("data/extract_data/SMPDB/smpdb_entities.csv")
smpdb_triples=load_triples("data/extract_data/SMPDB/smpdb_triples.csv")
kegg_entities=load_entities("data/extract_data/KEGG/kegg_entities.csv")
kegg_triples=load_triples("data/extract_data/KEGG/kegg_triples.csv")


## Merge
metakg_library_entities=pd.concat([smpdb_entities,kegg_entities,hmdb_entities],axis=0).drop_duplicates()
metakg_library_triples=pd.concat([smpdb_triples,kegg_triples,hmdb_triples],axis=0).drop_duplicates()
save_entities(metakg_library_entities,"data/extract_data/metakg_entities.csv")
save_triples(metakg_library_triples,"data/extract_data/metakg_triples.csv")
metakg_library_entities=load_entities("data/extract_data/metakg_entities.csv")
metakg_library_triples=load_triples("data/extract_data/metakg_triples.csv")


# Application: MetaKG analysis
# You can refer to src/metakg_analysis or case_study/ for more examples

summary.summary(metakg_library_triples,show_bar_graph=False,save_result=True,topk=100)
search.search_backward(metakg_library_triples,["disease:Nonalcoholic fatty liver disease"],["has_disease"],save_results=True,show_only=100)


# Stage 2 MetaKG Embedding: MetaKGE
# TODO: Better integrate triple contrastive learning with Pykeen package (currently just train with RotatE)
# TODO: Automatic comparing different KGE models
# TODO: More flexible training strategy


## Data partition
train_path,valid_path,test_path=data_partition.split_data(triples=metakg_library_triples,
                                                          info_path="data/kge_training/info.txt")

## Training (using pipeline)
training_results=kge_training_pipeline.trainging_pipeline(model_name="RotatE",
                                                          loss="marginranking",
                                                          embedding_dim=128,
                                                          lr=1.0e-3,
                                                          num_epochs=1000,
                                                          batch_size=16384)


# Application: MetaKG Inference
# We will continuelly update applications using MetaKG and MetaKGE
# You can refer to src/metakg_inference or case_study/ for more examples