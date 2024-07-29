# MetaKG

## Overview

![MetaKG Overall Figure](https://github.com/YuxingLu613/MetaKG/blob/08afd663928899262fa06509a4aa50846ab6d83b/MetaKG%20Figure%201.png)

## Directory Structure

The project structure is organized as follows:

```
.
|____main.py
|____src
| |___metakg_construction   # construction core
| | |____merge_database.py
| | |____Others
| | |____KEGG
| | | |____get_module_info.py
| | | |____get_enzyme_info.py
| | | |____get_pathway_info.py
| | | |____get_disease_info.py
| | | |____kegg_extract.py
| | | |____get_network_info.py
| | | |____get_cpd_info.py
| | | |____get_reaction_info.py
| | |____ChEBI
| | | |____get_chebi_resource.py
| | |____HMDB
| | | |____hmdb_extract.py
| | |____PubChem
| | | |____get_pubchem_resource.py
| | |____SMPDB
| | | |____smpdb_metabolite_extract.py
| | | |____smpdb_protein_extract.py
| | | |____smpdb_merge.py
| |____metakg_analysis   # analysis core
| | |____statistics
| | | |____summary.py
| | | |____utils.py
| | |____visualize
| | | |____visualize_graph.py
| | |____search
| | | |____search.py
| |____metakg_machine_learning   # machine learning core
| | |____kge_training_pipeline.py
| | |____kge_validation.py
| | |____data_partition.py
| | |____kge_training.py
| |____metakg_inference   # inference core
| | |____predict.py
| |____utils
| | |____save_data.py
| | |____convert_xml_to_json.py
| | |____load_data.py
|____data
| |____kge_training
| | |____TestSet.txt
| | |____info.txt
| | |____TrainingSet.txt
| | |____ValidationSet.txt
| |____resource
| | |____KEGG   # KEGG resources, you can get the web-crawled data from 
| | |____HMDB   # HMDB resources, you can get from https://hmdb.ca/downloads
| | | |____hmdb_metabolites.xml
| | | |____hmdb_metabolites.json
| | |____SMPDB  # SMPDB resources, you can get from https://www.smpdb.ca/downloads
| | | |____smpdb_metabolites
| | | |____smpdb_proteins
| |____extract_data
| | |____metakg_triples.csv   # triples in MetaKG Library
| | |____metakg_entities.csv  # entities in MetaKG Library
| | |____KEGG
| | | |____kegg_triples.csv
| | | |____kegg_entities.csv
| | | |____kegg_preprocessed
| | |____HMDB
| | | |____hmdb_triples.csv
| | | |____hmdb_entities.csv
| | |____SMPDB
| | | |____smpdb_entities.csv
| | | |____smpdb_triples.csv
|____outputs
| |____look_backward.json
| |____statistics.json
|____checkpoints
|____README.md
|____case_study
```

## Components

### Data

All data can be accessed at https://drive.google.com/drive/folders/1TiUtBCG4e2rJ7WIBf_NZ6En8VLbw2aoY?usp=sharing.

- kge_training: Contains the training, validation, and test sets for knowledge graph embedding (KGE) training.
- resource: Holds various biomedical databases (KEGG, HMDB, SMPDB) with different categories of data (e.g., metabolites, proteins, enzymes).
- extract_data: Contains preprocessed data and entity/triple files for different databases, ready for KG construction.

### Source Code

- src/metakg_inference: Scripts for making predictions using the knowledge graph.
- src/utils: Utility scripts for data conversion, loading, and saving.
- src/metakg_analysis: Tools for analyzing the knowledge graph, including statistics computation and visualization.
- src/metakg_machine_learning: Scripts for training, validating, and partitioning data for machine learning models on the KG.
- src/metakg_construction: Scripts for extracting and merging data from different databases to construct the knowledge graph.

### Miscellaneous

- checkpoints: Directory for storing model checkpoints during training.
- case_study: Contains specific case studies or examples of how the MetaKG can be applied.

- main.py: The main script to run the project.

## Getting Started

1. Install Dependencies: Ensure all necessary Python packages are installed.
2. Prepare Data: Place raw data files in the appropriate directories under data/resource.
3. Run Data Extraction: Use the scripts in src/metakg_construction to extract and preprocess data.
4. Train Models: Utilize the training pipeline in src/metakg_machine_learning to train KGE models.
5. Analyze and Infer: Use the analysis and inference scripts to evaluate the knowledge graph and make predictions.
