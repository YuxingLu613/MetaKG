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
from src.metakg_inference.predict import predict


# Stage 1 MetaKG Library: Extract data from metabolome KGs, MetaKG Library construction
# TODO (partially done): Access to more databases (ChEBI, PubChem) and parse
# TODO (partially done): Entity alignment and data cleaning

# Load data
metakg_library_entities=load_entities("data/extract_data/metakg_entities.csv")
metakg_library_triples=load_triples("data/extract_data/metakg_triples.csv")


# Application: MetaKG analysis
# You can refer to src/metakg_analysis or case_study/ for more examples

# summary.summary(metakg_library_triples,show_bar_graph=False,save_result=True,topk=20)
# search.search_backward(metakg_library_triples,["disease:Nonalcoholic fatty liver disease"],["has_disease"],save_results=True,show_only=20)



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
                                                          num_epochs=1,
                                                          batch_size=16384)


# Application: MetaKG Inference
# We will continuelly update applications using MetaKG and MetaKGE
# You can refer to src/metakg_inference or case_study/ for more examples

predict(model="RotatE",head="hmdb_id:HMDB0000001",relation="has_disease",tail=None,show_num=3)