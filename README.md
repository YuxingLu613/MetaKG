# MetaKG

## Overview

MetaKG is a comprehensive toolkit designed for the construction, analysis, and machine learning tasks associated with knowledge graphs (KGs) in the biomedical domain. This toolkit leverages various resources such as KEGG, HMDB, SMPDB, and others to create an extensive and integrated KG for research purposes.

## Directory Structure

The project structure is organized as follows:

```
.
|____checkpoints
|____README.md
|____case_study
|____main.py
|____data
| |____kge_training
| | |____TestSet.txt
| | |____info.txt
| | |____TrainingSet.txt
| | |____ValidationSet.txt
| |____resource
| | |____KEGG
| | | |____orthology
| | | |____reaction
| | | |____rclass
| | | |____disease
| | | |____brite
| | | |____module
| | | |____network
| | | |____enzyme
| | | |____compound
| | | |____pathway
| | | |____drug
| | | |____genome
| | | |____glycan
| | |____HMDB
| | | |____hmdb_metabolites.xml
| | | |____hmdb_metabolites.json
| | |____SMPDB
| | | |____smpdb_metabolites
| | | |____smpdb_proteins
| |____extract_data
| | |____metakg_triples.csv
| | |____KEGG
| | | |____kegg_triples.csv
| | | |____kegg_entities.csv
| | | |____kegg_preprocessed
| | |____ChEBI
| | |____HMDB
| | | |____hmdb_triples.csv
| | | |____hmdb_entities.csv
| | |____PubChem
| | | |____pubchem_entities.csv
| | | |____pubchem_triples.csv
| | |____metakg_entities.csv
| | |____SMPDB
| | | |____smpdb_entities.csv
| | | |____smpdb_triples.csv
|____outputs
| |____look_backward.json
| |____statistics.json
|____src
| |____metakg_inference
| | |____predict.py
| |______init__.py
| |____utils
| | |____save_data.py
| | |______init__.py
| | |____convert_xml_to_json.py
| | |____load_data.py
| |____metakg_analysis
| | |____statistics
| | | |______init__.py
| | | |____summary.py
| | | |____utils.py
| | |______init__.py
| | |____visualize
| | | |____visualize_graph.py
| | |____search
| | | |______init__.py
| | | |____search.py
| |____metakg_machine_learning
| | |____kge_training_pipeline.py
| | |____kge_validation.py
| | |____data_partition.py
| | |______init__.py
| | |____kge_training.py
| |____metakg_construction
| | |____merge_database.py
| | |______init__.py
| | |____Others
| | |____KEGG
| | | |____get_module_info.py
| | | |____get_enzyme_info.py
| | | |____get_pathway_info.py
| | | |____get_disease_info.py
| | | |______init__.py
| | | |____kegg_extract.py
| | | |____get_network_info.py
| | | |____get_cpd_info.py
| | | |____get_reaction_info.py
| | |____ChEBI
| | | |____get_chebi_resource.py
| | |____HMDB
| | | |______init__.py
| | | |____hmdb_extract.py
| | |____PubChem
| | | |____get_pubchem_resource.py
| | |____SMPDB
| | | |____smpdb_metabolite_extract.py
| | | |____smpdb_protein_extract.py
| | | |____smpdb_merge.py
```

## Components

### Data

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
