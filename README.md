<img width="396" alt="image" src="https://github.com/YuxingLu613/MetaKG/assets/43573050/f4666a44-1c96-4cf1-b63b-79948ebb2d82"># MetaKG


## Structure
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
| | | |____.DS_Store
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
| | | |____.get_enzyme_info.py.swp
| | | |____get_pathway_info.py
| | | |____get_disease_info.py
| | | |____get_enzyme_info.py
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
