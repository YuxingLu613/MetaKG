from tqdm import tqdm
import traceback
import sys
sys.path.append("src/")
from tqdm import tqdm
from utils.load_data import load_json

def extract_hmdb_data(file_path,selected_metabolites=None):
    
    hmdb_data=load_json(file_path)

    entities=set()
    triples=set()
    
    entities.add(("Compound","Root"))
    
    for hmdb_id,meta_data in tqdm(hmdb_data.items()):
        if selected_metabolites is not None and hmdb_id not in selected_metabolites:
            continue

        hmdb_id="hmdb_id:"+hmdb_id
        entities.add((hmdb_id,"Compound"))
        triples.add((hmdb_id,"is_a","Compound"))

        try:
            if "chemical_formula" in meta_data.keys() and meta_data["chemical_formula"]:
                entities.add(("Chemical_Formula","Root"))
                triples.add(("chemical_formula:"+meta_data["chemical_formula"],"is_a","Chemical_Formula"))
                entities.add(("chemical_formula:"+meta_data["chemical_formula"],"Chemical_Formula"))
                triples.add((hmdb_id,"chemical_formula","chemical_formula:"+meta_data["chemical_formula"]))

            if "average_molecular_weight" in meta_data.keys() and meta_data["average_molecular_weight"]:
                if type(meta_data["average_molecular_weight"])==str:
                    entities.add(("Average_Molecular_Weight","Root"))
                    triples.add(("average_molecular_weight:"+meta_data["average_molecular_weight"],"is_a","Average_Molecular_Weight"))
                    entities.add(("average_molecular_weight:"+meta_data["average_molecular_weight"],"Average_Molecular_Weight"))
                    triples.add((hmdb_id,"average_molecular_weight","average_molecular_weight:"+meta_data["average_molecular_weight"]))

            if "status" in meta_data.keys() and meta_data["status"]:
                entities.add(("Status","Root"))
                triples.add(("status:"+meta_data["status"],"is_a","Status"))
                entities.add(("status:"+meta_data["status"],"Status"))
                triples.add((hmdb_id,"has_status","status:"+meta_data["status"]))
            
            if "name" in meta_data.keys() and meta_data["name"]:
                entities.add(("Name","Root"))
                triples.add(("name:"+meta_data["name"],"is_a","Name"))
                entities.add(("name:"+meta_data["name"],"Name"))
                triples.add((hmdb_id,"has_name","name:"+meta_data["name"]))

            if "smiles" in meta_data.keys() and meta_data["smiles"]:
                entities.add(("Smiles","Root"))
                triples.add(("smiles:"+meta_data["smiles"],"is_a","Smiles"))
                entities.add(("smiles:"+meta_data["smiles"],"Smiles"))
                triples.add((hmdb_id,"has_smiles","smiles:"+meta_data["smiles"]))
                
            if "secondary_accessions" in meta_data.keys() and meta_data["secondary_accessions"]:
                if type(meta_data["secondary_accessions"]["accession"])==list:
                    for secondary_accession in meta_data["secondary_accessions"]["accession"]:
                        entities.add(("Compound","Root"))
                        triples.add(("hmdb_id:"+secondary_accession,"is_a","Compound"))
                        entities.add(("hmdb_id:"+secondary_accession,"Compound"))
                        triples.add((hmdb_id,"same_as","hmdb_id:"+secondary_accession))
                else:
                    secondary_accession=meta_data["secondary_accessions"]["accession"]
                    entities.add(("Compound","Root"))
                    triples.add(("hmdb_id:"+secondary_accession,"is_a","Compound"))
                    entities.add(("hmdb_id:"+secondary_accession,"Compound"))
                    triples.add((hmdb_id,"same_as","hmdb_id:"+secondary_accession))
            
            if "synonyms" in meta_data.keys() and meta_data["synonyms"]:
                if type(meta_data["synonyms"]["synonym"])==list:
                    for synonym in meta_data["synonyms"]["synonym"]:
                        entities.add(("Synonym","Root"))
                        triples.add(("synonym:"+synonym,"is_a","Synonym"))
                        entities.add(("synonym:"+synonym,"Synonym"))
                        triples.add((hmdb_id,"has_synonym","synonym:"+synonym))
                else:
                    synonym=meta_data["synonyms"]["synonym"]
                    entities.add(("Synonym","Root"))
                    triples.add(("synonym:"+synonym,"is_a","Synonym"))
                    entities.add(("synonym:"+synonym,"Synonym"))
                    triples.add((hmdb_id,"has_synonym","synonym:"+synonym))
            
            if "description" in meta_data.keys() and meta_data["description"]:
                entities.add(("Description","Root"))
                while "\n" in meta_data["description"]:
                    meta_data["description"]=meta_data["description"].replace("\n"," ")
                while "\t" in meta_data["description"]:
                    meta_data["description"]=meta_data["description"].replace("\t"," ")
                triples.add(("description:"+meta_data["description"],"is_a","Description"))
                entities.add(("description:"+meta_data["description"],"Description"))
                triples.add((hmdb_id,"has_description","description:"+meta_data["description"]))
                
            if "inchi" in meta_data.keys() and meta_data["inchi"]:
                entities.add(("Inchi","Root"))
                triples.add(("inchi:"+meta_data["inchi"],"is_a","Inchi"))
                entities.add(("inchi:"+meta_data["inchi"],"Inchi"))
                triples.add((hmdb_id,"has_inchi","inchi:"+meta_data["inchi"]))
            
            if "inchikey" in meta_data.keys() and meta_data["inchikey"]:
                entities.add(("Inchikey","Root"))
                triples.add(("inchikey:"+meta_data["inchikey"],"is_a","Inchikey"))
                entities.add(("inchikey:"+meta_data["inchikey"],"Inchikey"))
                triples.add((hmdb_id,"has_inchikey","inchikey:"+meta_data["inchikey"]))
            
        except Exception as e:
            traceback.print_exc()   
    
        try:

            if "state" in meta_data.keys() and meta_data["state"]:
                entities.add(("State","Root"))
                triples.add(("state:"+meta_data["state"],"is_a","State"))
                entities.add(("state:"+meta_data["state"],"State"))
                triples.add((hmdb_id,"has_state","state:"+meta_data["state"]))
        
            if meta_data["taxonomy"]:
                taxonomy_entity,taxonomy_triple=get_taxonomy(hmdb_id,meta_data["taxonomy"])
                entities.update(taxonomy_entity)
                triples.update(taxonomy_triple)
    
            if meta_data["experimental_properties"]:
                property_entity,property_triple=get_property(hmdb_id,meta_data["experimental_properties"],property_type="experimental")
                entities.update(property_entity)
                triples.update(property_triple)
        
            if meta_data["predicted_properties"]:
                property_entity,property_triple=get_property(hmdb_id,meta_data["predicted_properties"],property_type="predicted")
                entities.update(property_entity)
                triples.update(property_triple)
        
            if meta_data["biological_properties"]:
                property_entity,property_triple=get_property(hmdb_id,meta_data["biological_properties"],property_type="biological")
                entities.update(property_entity)
                triples.update(property_triple)

            if meta_data["normal_concentrations"]:
                concentration_entity,concentration_triple=get_concentrations_v2(hmdb_id,meta_data["normal_concentrations"],meta_data["abnormal_concentrations"])
                entities.update(concentration_entity)
                triples.update(concentration_triple)
            
            if meta_data["diseases"]:
                disease_entity,disease_triple=get_disease(hmdb_id,meta_data["diseases"])
                entities.update(disease_entity)
                triples.update(disease_triple)
                
            if meta_data["general_references"]:
                reference_entity,reference_triple=get_reference(hmdb_id,meta_data["general_references"])
                entities.update(reference_entity)
                triples.update(reference_triple)
            
            if meta_data["protein_associations"]:
                protein_entity,protein_triple=get_protein(hmdb_id,meta_data["protein_associations"])
                entities.update(protein_entity)
                triples.update(protein_triple)
            
            if meta_data["ontology"]:
                ontology_entity,ontology_triple=get_ontology(hmdb_id,meta_data["ontology"])
                entities.update(ontology_entity)
                triples.update(ontology_triple)
    
        except Exception as e:
            traceback.print_exc()
        
        try:
            if "pubchem_compound_id" in meta_data.keys() and meta_data["pubchem_compound_id"]:
                entities.add(("Compound","Root"))
                triples.add(("pubchem_id:"+meta_data["pubchem_compound_id"],"is_a","Compound"))
                entities.add(("pubchem_id:"+meta_data["pubchem_compound_id"],"Compound"))
                triples.add((hmdb_id,"has_pubchem_id","pubchem_id:"+meta_data["pubchem_compound_id"]))
            
            if "kegg_id" in meta_data.keys() and meta_data["kegg_id"]:
                entities.add(("Compound","Root"))
                triples.add(("kegg_id:"+meta_data["kegg_id"],"is_a","Compound"))
                entities.add(("kegg_id:"+meta_data["kegg_id"],"Compound"))
                triples.add((hmdb_id,"has_kegg_id","compound_id:"+meta_data["kegg_id"]))

            if "chebi_id" in meta_data.keys() and meta_data["chebi_id"]:
                entities.add(("Compound","Root"))
                triples.add(("chebi_id:"+meta_data["chebi_id"],"is_a","Compound"))
                entities.add(("chebi_id:"+meta_data["chebi_id"],"Compound"))
                triples.add((hmdb_id,"has_chebi_id","chebi_id:"+meta_data["chebi_id"]))
        except Exception as e:
            traceback.print_exc()

    return list(entities),list(triples)




def get_taxonomy(hmdb_id,taxonomy_dict,keys_list=["direct_parent","kingdom","super_class","class","sub_class","molecular_framework","alternative_parents","substituents","external_descriptors"]):
    entities=set()
    triples=set()
    keys_list=list(set(keys_list)&set(taxonomy_dict.keys()))
    for key in keys_list:
        if key=="alternative_parents":
            if taxonomy_dict["alternative_parents"]:
                _=taxonomy_dict["alternative_parents"]['alternative_parent']
                if type(_)==list:
                    for i in _:
                        entities.add(("Taxonomy_Class","Root"))
                        triples.add(("taxonomy_class:"+i,"is_a","Taxonomy_Class"))
                        entities.add(("taxonomy_class:"+i,"Taxonomy_Class"))
                        triples.add((hmdb_id,"has_alternative_class","taxonomy_class:"+i))
                else:
                    entities.add(("Taxonomy_Class","Root"))
                    triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                    entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                    triples.add((hmdb_id,"has_alternative_class","taxonomy_class:"+_))
                    
        if key=="direct_parent":
            if taxonomy_dict["direct_parent"]:
                _=taxonomy_dict["direct_parent"]
                entities.add(("Taxonomy_Class","Root"))
                triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                triples.add((hmdb_id,"has_class","taxonomy_class:"+_))
            
        if key=="sub_class":
            if taxonomy_dict["sub_class"]:
                _=taxonomy_dict["sub_class"]
                entities.add(("Taxonomy_Class","Root"))
                triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                triples.add((hmdb_id,"has_class","taxonomy_class:"+_))
                if taxonomy_dict["direct_parent"]:
                    dr=taxonomy_dict["direct_parent"]
                    triples.add(("taxonomy_class:"+dr,"is_a_sub_class_of","taxonomy_class:"+_))

        if key=="class":
            if taxonomy_dict["class"]:
                _=taxonomy_dict["class"]
                entities.add(("Taxonomy_Class","Root"))
                triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                triples.add((hmdb_id,"has_class","taxonomy_class:"+_))
                if taxonomy_dict["sub_class"]:
                    sc=taxonomy_dict["sub_class"]
                    triples.add(("taxonomy_class:"+sc,"is_a_sub_class_of","taxonomy_class:"+_))
                
        if key=="super_class":
            if taxonomy_dict["super_class"]:
                _=taxonomy_dict["super_class"]
                entities.add(("Taxonomy_Class","Root"))
                triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                triples.add((hmdb_id,"has_class","taxonomy_class:"+_))
                if taxonomy_dict["class"]:
                    cl=taxonomy_dict["class"]
                    triples.add(("taxonomy_class:"+cl,"is_a_sub_class_of","taxonomy_class:"+_))
            
        if key=="kingdom":
            if taxonomy_dict["kingdom"]:
                _=taxonomy_dict["kingdom"]
                entities.add(("Taxonomy_Class","Root"))
                triples.add(("taxonomy_class:"+_,"is_a","Taxonomy_Class"))
                entities.add(("taxonomy_class:"+_,"Taxonomy_Class"))
                triples.add((hmdb_id,"has_kingdom","taxonomy_class:"+_))
                if taxonomy_dict["super_class"]:
                    sc=taxonomy_dict["super_class"]
                    triples.add(("taxonomy_class:"+sc,"is_a_sub_class_of","taxonomy_class:"+_))


        if key=="molecular_framework":
            if taxonomy_dict["molecular_framework"]:
                _=taxonomy_dict["molecular_framework"]
                if type(_)==dict:
                    _=_["@name"]
                entities.add(("Taxonomy_Molecular_Framework","Root"))
                triples.add(("taxonomy_molecular_framework:"+_,"is_a","Taxonomy_Molecular_Framework"))
                entities.add(("taxonomy_molecular_framework:"+_,"Taxonomy_Molecular_Framework"))
                triples.add((hmdb_id,"has_molecular_framework","taxonomy_molecular_framework:"+_))
            
        if key=="substituents":
            if taxonomy_dict["substituents"]:
                _=taxonomy_dict["substituents"]['substituent']
                if type(_)==list:
                    for i in _:
                        entities.add(("Taxonomy_Substituent","Root"))
                        triples.add(("taxonomy_substituent:"+i,"is_a","Taxonomy_Substituent"))
                        entities.add(("taxonomy_substituent:"+i,"Taxonomy_Substituent"))
                        triples.add((hmdb_id,"has_substituent","taxonomy_substituent:"+i))
                else:
                    entities.add(("Taxonomy_Substituent","Root"))
                    triples.add(("taxonomy_substituent:"+_,"is_a","Taxonomy_Substituent"))
                    entities.add(("taxonomy_substituent:"+_,"Taxonomy_Substituent"))
                    triples.add((hmdb_id,"has_substituent","taxonomy_substituent:"+_))
            
        if key=="external_descriptors":
            if taxonomy_dict["external_descriptors"]:
                _=taxonomy_dict["external_descriptors"]['external_descriptor']
                if type(_)==list:
                    for i in _:
                        entities.add(("Taxonomy_External_Descriptor","Root"))
                        triples.add(("taxonomy_external_descriptor:"+i,"is_a","Taxonomy_External_Descriptor"))
                        entities.add(("taxonomy_external_descriptor:"+i,"Taxonomy_External_Descriptor"))
                        triples.add((hmdb_id,"has_external_descriptor","taxonomy_external_descriptor:"+i))
                else:
                    entities.add(("Taxonomy_External_Descriptor","Root"))
                    triples.add(("taxonomy_external_descriptor:"+_,"is_a","Taxonomy_External_Descriptor"))
                    entities.add(("taxonomy_external_descriptor:"+_,"Taxonomy_External_Descriptor"))
                    triples.add((hmdb_id,"has_external_descriptor","taxonomy_external_descriptor:"+_))
    
    return entities,triples


def get_property(hmdb_id,property_dict,property_type="predicted",keys_list=["cellular_locations","biospecimen_locations","tissue_locations","pathways"]):
    entities=set()
    triples=set()
    
    if property_type in ["experimental","predicted"]:
        for property in property_dict["property"]:
            if type(property)==dict:
                if property["value"] in ["Yes","No"]:
                    entities.add(("Property","Root"))
                    triples.add((property_type+"_property:"+property["kind"],"is_a","Property"))
                    entities.add((property_type+"_property:"+property["kind"],"Property"))
                    triples.add((hmdb_id,"has_"+property_type+"_property",property_type+"_property:"+property["kind"]))
        
    elif property_type=="biological":
        keys_list=list(set(keys_list)&set(property_dict.keys()))
        for key in keys_list:
            if key=="cellular_locations":
                if property_dict["cellular_locations"]:
                    if type(property_dict["cellular_locations"]['cellular'])==str:
                        property_dict["cellular_locations"]['cellular']=[property_dict["cellular_locations"]['cellular']]
                    for _ in property_dict["cellular_locations"]['cellular']:
                        entities.add(("Cellular_Location","Root"))
                        triples.add(("cellular_location:"+_,"is_a","Cellular_Location"))
                        entities.add(("cellular_location:"+_,"Cellular_Location"))
                        triples.add((hmdb_id,"has_cellular_location","cellular_location:"+_))
                    
            if key=="biospecimen_locations":
                if property_dict["biospecimen_locations"]:
                    if type(property_dict["biospecimen_locations"]['biospecimen'])==str:
                        property_dict["biospecimen_locations"]['biospecimen']=[property_dict["biospecimen_locations"]['biospecimen']]
                    for _ in property_dict["biospecimen_locations"]['biospecimen']:
                        entities.add(("Biospecimen_Location","Root"))
                        triples.add(("biospecimen_location:"+_,"is_a","Biospecimen_Location"))
                        entities.add(("biospecimen_location:"+_,"Biospecimen_Location"))
                        triples.add((hmdb_id,"has_biospecimen_location","biospecimen_location:"+_))

            if key=="tissue_locations":
                if property_dict["tissue_locations"]:
                    if "tissue" in property_dict["tissue_locations"].keys():
                        if type(property_dict["tissue_locations"]['tissue'])==str:
                            property_dict["tissue_locations"]['tissue']=[property_dict["tissue_locations"]['tissue']]
                        for _ in property_dict["tissue_locations"]['tissue']:
                            entities.add(("Tissue_Location","Root"))
                            triples.add(("tissue_location:"+_,"is_a","Tissue_Location"))
                            entities.add(("tissue_location:"+_,"Tissue_Location"))
                            triples.add((hmdb_id,"has_tissue_location","tissue_location:"+_))

            if key=="pathways":
                if property_dict["pathways"]:
                    for _ in property_dict["pathways"]['pathway']:
                        if type(_)==dict:
                            if _["smpdb_id"]!=None:
                                entities.add(("Pathway","Root"))
                                triples.add(("pathway_id:"+_["smpdb_id"],"is_a","Pathway"))
                                entities.add(("pathway_id:"+_["smpdb_id"],"Pathway"))
                                triples.add((hmdb_id,"has_pathway","pathway_id:"+_["smpdb_id"]))
                            if _["kegg_map_id"]!=None:
                                entities.add(("Pathway","Root"))
                                triples.add(("pathway_id:"+_["kegg_map_id"],"is_a","Pathway"))
                                entities.add(("pathway_id:"+_["kegg_map_id"],"Pathway"))
                                triples.add((hmdb_id,"has_pathway","pathway_id:"+_["kegg_map_id"]))
                    
    return entities,triples


def get_concentrations(hmdb_id,concentration_dict,concentration_type):
    entities=set()
    triples=set()
    
    for _ in concentration_dict["concentration"]:
        if type(_)==dict:
            entities.add(("Biospecimen_Location","Root"))
            triples.add(("biospecimen_location:"+_["biospecimen"],"is_a","Biospecimen_Location"))
            entities.add(("biospecimen_location:"+_["biospecimen"],"Biospecimen_Location"))
            triples.add((hmdb_id,"has_"+concentration_type+"_concentration_in","biospecimen_location:"+_["biospecimen"]))
            if _["references"]:
                if type(_["references"]["reference"])==dict:
                    _["references"]["reference"]=[_["references"]["reference"]]
                for r in _["references"]["reference"]:
                    if "pubmed_id" in r.keys() and r["pubmed_id"]:
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+r["pubmed_id"],"is_a","Reference"))
                        entities.add(("pubmed_id:"+r["pubmed_id"],"Reference"))
                        triples.add(("biospecimen_location:"+_["biospecimen"],"has_reference","pubmed_id:"+r["pubmed_id"]))
    
    return entities,triples


def get_concentrations_v2(hmdb_id,normal_concentration_dict,abnormal_concentration_dict):
    entities=set()
    triples=set()

    import re
    normal_concentration_value_dict={}
    for _ in normal_concentration_dict["concentration"]:
        entities.add(("Biospecimen_Location","Root"))
        if type(_)==dict:
            triples.add(("biospecimen_location:"+_["biospecimen"],"is_a","Biospecimen_Location"))
            entities.add(("biospecimen_location:"+_["biospecimen"],"Biospecimen_Location"))
            if _["concentration_value"]:
                if not _["biospecimen"] in normal_concentration_value_dict.keys():
                    normal_concentration_value_dict[_["biospecimen"]]=[]
                # split by " ", "-", "±", "+/-", "(", ")"
                concentration_value=re.split(" |±|\+\/-|\(|\)|,|e",_["concentration_value"])[0].strip("=<> ")
                if " " in concentration_value:
                    concentration_value=(float(concentration_value.split(" ")[0])+float(concentration_value.split(" ")[-1]))/2
                elif "-" in concentration_value:
                    concentration_value=(float(concentration_value.split("-")[0])+float(concentration_value.split("-")[-1]))/2
                elif "–" in concentration_value:
                    concentration_value=(float(concentration_value.split("–")[0])+float(concentration_value.split("–")[-1]))/2
                if concentration_value:
                    normal_concentration_value_dict[_["biospecimen"]].append(float(concentration_value))
            if _["references"]:
                if type(_["references"]["reference"])==dict:
                    _["references"]["reference"]=[_["references"]["reference"]]
                for r in _["references"]["reference"]:
                    if "pubmed_id" in r.keys() and r["pubmed_id"]:
                        entities.add(("Reference","Root"))
                        triples.add(("pubmed_id:"+r["pubmed_id"],"is_a","Reference"))
                        entities.add(("pubmed_id:"+r["pubmed_id"],"Reference"))
                        triples.add((hmdb_id,"has_reference","pubmed_id:"+r["pubmed_id"]))
            
    for key,value in normal_concentration_value_dict.items():
        if len(value):
            normal_concentration_value_dict[key]=sum(value)/len(value)
            triples.add((hmdb_id,"has_normal_concentration_in","biospecimen_location:"+key))
        else:
            normal_concentration_value_dict[key]=0
    
    if abnormal_concentration_dict and abnormal_concentration_dict["concentration"]:
        for _ in abnormal_concentration_dict["concentration"]:
            entities.add(("Biospecimen_Location","Root"))
            if type(_)==dict:
                triples.add(("biospecimen_location:"+_["biospecimen"],"is_a","Biospecimen_Location"))
                entities.add(("biospecimen_location:"+_["biospecimen"],"Biospecimen_Location"))
                if _["concentration_value"]:
                    # split by " ", "-", "±", "+/-", "(", ")"
                    concentration_value=re.split(" |±|\+\/-|\(|\)|,|e",_["concentration_value"])[0].strip("=<> ")
                    if " " in concentration_value:
                        concentration_value=(float(concentration_value.split(" ")[0])+float(concentration_value.split(" ")[-1]))/2
                    elif "-" in concentration_value:
                        concentration_value=(float(concentration_value.split("-")[0])+float(concentration_value.split("-")[-1]))/2
                    elif "–" in concentration_value:
                        concentration_value=(float(concentration_value.split("–")[0])+float(concentration_value.split("–")[-1]))/2
                    if _["biospecimen"] not in normal_concentration_value_dict.keys():
                        normal_concentration_value_dict[_["biospecimen"]]=0
                    if float(concentration_value)>normal_concentration_value_dict[_["biospecimen"]]:
                        entities.add(("disease:"+_["patient_information"],"Disease"))
                        triples.add((hmdb_id,"has_disease","disease:"+_["patient_information"]))
                        triples.add((hmdb_id,"has_upper_concentration_in","disease:"+_["patient_information"]))
                        triples.add((hmdb_id,"has_abnormal_concentration_in","biospecimen_location:"+_["biospecimen"]))
                    else:
                        entities.add(("disease:"+_["patient_information"],"Disease"))
                        triples.add((hmdb_id,"has_disease","disease:"+_["patient_information"]))
                        triples.add((hmdb_id,"has_lower_concentration_in","disease:"+_["patient_information"]))
                        triples.add((hmdb_id,"has_abnormal_concentration_in","biospecimen_location:"+_["biospecimen"]))
                if _["references"]:
                    if type(_["references"]["reference"])==dict:
                        _["references"]["reference"]=[_["references"]["reference"]]
                    for r in _["references"]["reference"]:
                        if "pubmed_id" in r.keys() and r["pubmed_id"]:
                            entities.add(("Reference","Root"))
                            triples.add(("pubmed_id:"+r["pubmed_id"],"is_a","Reference"))
                            entities.add(("pubmed_id:"+r["pubmed_id"],"Reference"))
                            triples.add((hmdb_id,"has_reference","pubmed_id:"+r["pubmed_id"]))
    
    return entities,triples




def get_disease(hmdb_id,disease_dict):
    entities=set()
    triples=set()
    
    for _ in disease_dict["disease"]:
        if type(_)==dict:
            entities.add(("disease:"+_["name"],"Disease"))
            triples.add((hmdb_id,"has_disease","disease:"+_["name"]))
            # if _["omim_id"]:
            #     entities.add(("omim_id:"+_["omim_id"],"Omim_id"))
            #     triples.add(("disease:"+_["name"],"has_omim_id","omim_id:"+_["omim_id"]))
            if type(_["references"]["reference"])==dict:
                _["references"]["reference"]=[_["references"]["reference"]]
            for r in _["references"]["reference"]:
                if "pubmed_id" in r.keys() and r["pubmed_id"]:
                    entities.add(("Reference","Root"))
                    triples.add(("pubmed_id:"+r["pubmed_id"],"is_a","Reference"))
                    entities.add(("pubmed_id:"+r["pubmed_id"],"Reference"))
                    triples.add(("disease:"+_["name"],"has_reference","pubmed_id:"+r["pubmed_id"]))
    
    return entities,triples


def get_reference(hmdb_id,reference_dict):
    entities=set()
    triples=set()
    
    for r in reference_dict["reference"]:
        if type(r)==dict:
            if "pubmed_id" in r.keys() and r["pubmed_id"]:
                entities.add(("Reference","Root"))
                triples.add(("pubmed_id:"+r["pubmed_id"],"is_a","pubmed_id_id"))
                entities.add(("pubmed_id:"+r["pubmed_id"],"Reference"))
                triples.add((hmdb_id,"has_reference","pubmed_id:"+r["pubmed_id"]))
                
    return entities,triples


def get_protein(hmdb_id,protein_dict):
    entities=set()
    triples=set()
    
    for p in protein_dict["protein"]:
        if type(p)==dict:
            if "protein_accession" in p.keys():
                if p["protein_accession"]:
                    entities.add(("Protein","Root"))
                    triples.add(("hmdbp_id:"+p["protein_accession"],"is_a","Protein"))
                    entities.add(("hmdbp_id:"+p["protein_accession"],"Protein"))
                    triples.add((hmdb_id,"related_to_protein","hmdbp_id:"+p["protein_accession"]))
                    if "uniprot_id" in p.keys():
                        if p["uniprot_id"]:
                            entities.add(("uniprot_id:"+p["uniprot_id"],"Protein"))
                            triples.add(("uniprot_id:"+p["uniprot_id"],"is_a","Protein"))
                            triples.add(("hmdbp_id:"+p["protein_accession"],"has_uniprot_id","uniprot_id:"+p["uniprot_id"]))
                            triples.add((hmdb_id,"related_to_protein","uniprot_id:"+p["uniprot_id"]))
                    if "gene_name" in p.keys():
                        if p["gene_name"]:
                            entities.add(("gene_name:"+p["gene_name"],"Gene"))
                            triples.add(("gene_name:"+p["gene_name"],"is_a","Gene"))
                            triples.add(("hmdbp_id:"+p["protein_accession"],"related_to_gene","gene_name:"+p["gene_name"]))
                            triples.add((hmdb_id,"related_to_gene","gene_name:"+p["gene_name"]))
    
    return entities,triples


def get_ontology(hmdb_id,ontology_dict):
    entities=set()
    triples=set()
    
    for i in ontology_dict["root"]:
        if type(i)==str:continue
        if i["term"]=="Physiological effect":
            if "descendants" not in i.keys():continue
            phy_descendants=i["descendants"]["descendant"]
            if type(phy_descendants)==dict:
                phy_descendants=[phy_descendants]
            for phy_descendants2 in phy_descendants:
                entities.add(("Disease","Root"))
                triples.add(("disease:"+phy_descendants2["term"],"is_a","Disease"))
                entities.add(("disease:"+phy_descendants2["term"],"Disease"))
                triples.add((hmdb_id,"has_disease","disease:"+phy_descendants2["term"]))
                if "descendants" not in phy_descendants2.keys():continue
                phy_descendants3=phy_descendants2["descendants"]["descendant"]
                get_synonym(entities,triples,phy_descendants2,entity_type="disease",class_type="Disease")
                if type(phy_descendants3)==dict:
                    phy_descendants=[phy_descendants3]
                else:
                    phy_descendants=phy_descendants3
                for phy_descendants3 in phy_descendants:
                    entities.add(("Disease","Root"))
                    triples.add(("disease:"+phy_descendants3["term"],"is_a","Disease"))
                    entities.add(("disease:"+phy_descendants3["term"],"Disease"))
                    triples.add((hmdb_id,"has_disease","disease:"+phy_descendants3["term"]))
                    triples.add(("disease:"+phy_descendants3["term"],"is_a_sub_class_of","disease:"+phy_descendants2["term"]))
                    get_synonym(entities,triples,phy_descendants3,entity_type="disease",class_type="Disease")
                    if "descendants" not in phy_descendants3.keys():continue
                    phy_descendants4=phy_descendants3["descendants"]["descendant"]
                    if type(phy_descendants4)==dict:
                        phy_descendants=[phy_descendants4]
                    else:
                        phy_descendants=phy_descendants4
                    for phy_descendants4 in phy_descendants:
                        entities.add(("Disease","Root"))
                        triples.add(("disease:"+phy_descendants4["term"],"is_a","Disease"))
                        entities.add(("disease:"+phy_descendants4["term"],"Disease"))
                        triples.add((hmdb_id,"has_disease","disease:"+phy_descendants4["term"]))
                        triples.add(("disease:"+phy_descendants4["term"],"is_a_sub_class_of","disease:"+phy_descendants3["term"]))
                        get_synonym(entities,triples,phy_descendants4,entity_type="disease",class_type="Disease")
                        if "descendants" not in phy_descendants4.keys():continue
                        phy_descendants5=phy_descendants4["descendants"]["descendant"]
                        if type(phy_descendants5)==dict:
                            phy_descendants=[phy_descendants5]
                        else:
                            phy_descendants=phy_descendants5
                        for phy_descendants5 in phy_descendants:
                            entities.add(("Disease","Root"))
                            triples.add(("disease:"+phy_descendants5["term"],"is_a","Disease"))
                            entities.add(("disease:"+phy_descendants5["term"],"Disease"))
                            triples.add((hmdb_id,"has_disease","disease:"+phy_descendants5["term"]))
                            triples.add(("disease:"+phy_descendants5["term"],"is_a_sub_class_of","disease:"+phy_descendants4["term"]))
                            get_synonym(entities,triples,phy_descendants5,entity_type="disease",class_type="Disease")
    
        if i["term"]=="Disposition":
                if "descendants" not in i.keys():continue
                disposition=i["descendants"]["descendant"]
                if type(disposition)==dict:
                    disposition=[disposition]
                for disposition2 in disposition:
                    entities.add(("Disposition","Root"))
                    triples.add(("disposition:"+disposition2["term"],"is_a","Disposition"))
                    entities.add(("disposition:"+disposition2["term"],"Disposition"))
                    triples.add((hmdb_id,"has_disposition","disposition:"+disposition2["term"]))
                    if "descendants" not in disposition2.keys():continue
                    disposition3=disposition2["descendants"]["descendant"]
                    get_synonym(entities,triples,disposition2,entity_type="disposition",class_type="Disposition")
                    if type(disposition3)==dict:
                        disposition=[disposition3]
                    else:
                        disposition=disposition3
                    for disposition3 in disposition:
                        entities.add(("Disposition","Root"))
                        triples.add(("disposition:"+disposition3["term"],"is_a","Disposition"))
                        entities.add(("disposition:"+disposition3["term"],"Disposition"))
                        triples.add((hmdb_id,"has_disposition","disposition:"+disposition3["term"]))
                        triples.add(("disposition:"+disposition3["term"],"is_a_sub_class_of","disposition:"+disposition2["term"]))
                        get_synonym(entities,triples,disposition3,entity_type="disposition",class_type="Disposition")
                        if "descendants" not in disposition3.keys():continue
                        disposition4=disposition3["descendants"]["descendant"]
                        if type(disposition4)==dict:
                            disposition=[disposition4]
                        else:
                            disposition=disposition4
                        for disposition4 in disposition:
                            entities.add(("Disposition","Root"))
                            triples.add(("disposition:"+disposition4["term"],"is_a","Disposition"))
                            entities.add(("disposition:"+disposition4["term"],"Disposition"))
                            triples.add((hmdb_id,"has_disposition","disposition:"+disposition4["term"]))
                            triples.add(("disposition:"+disposition4["term"],"is_a_sub_class_of","disposition:"+disposition3["term"]))
                            get_synonym(entities,triples,disposition4,entity_type="disposition",class_type="Disposition")
                            if "descendants" not in disposition4.keys():continue
                            disposition5=disposition4["descendants"]["descendant"]
                            if type(disposition5)==dict:
                                disposition=[disposition5]
                            else:
                                disposition=disposition5
                            for disposition5 in disposition:
                                entities.add(("Disposition","Root"))
                                triples.add(("disposition:"+disposition5["term"],"is_a","Disposition"))
                                entities.add(("disposition:"+disposition5["term"],"Disposition"))
                                triples.add((hmdb_id,"has_disposition","disposition:"+disposition5["term"]))
                                triples.add(("disposition:"+disposition5["term"],"is_a_sub_class_of","disposition:"+disposition4["term"]))
                                get_synonym(entities,triples,disposition5,entity_type="disposition",class_type="Disposition")
    
    
        if i["term"]=="Process":
                if "descendants" not in i.keys():continue
                process=i["descendants"]["descendant"]
                if type(process)==dict:
                    process=[process]
                for process2 in process:
                    entities.add(("Process","Root"))
                    triples.add(("process:"+process2["term"],"is_a","Process"))
                    entities.add(("process:"+process2["term"],"Process"))
                    triples.add((hmdb_id,"has_process","process:"+process2["term"]))
                    if "descendants" not in process2.keys():continue
                    process3=process2["descendants"]["descendant"]
                    get_synonym(entities,triples,process2,entity_type="process",class_type="Process")
                    if type(process3)==dict:
                        process=[process3]
                    else:
                        process=process3
                    for process3 in process:
                        entities.add(("Process","Root"))
                        triples.add(("process:"+process3["term"],"is_a","Process"))
                        entities.add(("process:"+process3["term"],"Process"))
                        triples.add((hmdb_id,"has_process","process:"+process3["term"]))
                        triples.add(("process:"+process3["term"],"is_a_sub_class_of","process:"+process2["term"]))
                        get_synonym(entities,triples,process3,entity_type="process",class_type="Process")
                        if "descendants" not in process3.keys():continue
                        process4=process3["descendants"]["descendant"]
                        if type(process4)==dict:
                            process=[process4]
                        else:
                            process=process4
                        for process4 in process:
                            entities.add(("Process","Root"))
                            triples.add(("process:"+process4["term"],"is_a","Process"))
                            entities.add(("process:"+process4["term"],"Process"))
                            triples.add((hmdb_id,"has_process","process:"+process4["term"]))
                            triples.add(("process:"+process4["term"],"is_a_sub_class_of","process:"+process3["term"]))
                            get_synonym(entities,triples,process4,entity_type="process",class_type="Process")
                            if "descendants" not in process4.keys():continue
                            process5=process4["descendants"]["descendant"]
                            if type(process5)==dict:
                                process=[process5]
                            else:
                                process=process5
                            for process5 in process:
                                entities.add(("Process","Root"))
                                triples.add(("process:"+process5["term"],"is_a","Process"))
                                entities.add(("process:"+process5["term"],"Process"))
                                triples.add((hmdb_id,"has_process","process:"+process5["term"]))
                                triples.add(("process:"+process5["term"],"is_a_sub_class_of","process:"+process4["term"]))
                                get_synonym(entities,triples,process5,entity_type="process",class_type="Process")
    
    
    
        if i["term"]=="Role":
                if "descendants" not in i.keys():continue
                role=i["descendants"]["descendant"]
                if type(role)==dict:
                    role=[role]
                for role2 in role:
                    entities.add(("Role","Root"))
                    triples.add(("role:"+role2["term"],"is_a","Role"))
                    entities.add(("role:"+role2["term"],"Role"))
                    triples.add((hmdb_id,"has_role","role:"+role2["term"]))
                    if "descendants" not in role2.keys():continue
                    role3=role2["descendants"]["descendant"]
                    get_synonym(entities,triples,role2,entity_type="role",class_type="Role")
                    if type(role3)==dict:
                        role=[role3]
                    else:
                        role=role3
                    for role3 in role:
                        entities.add(("Role","Root"))
                        triples.add(("role:"+role3["term"],"is_a","Role"))
                        entities.add(("role:"+role3["term"],"Role"))
                        triples.add((hmdb_id,"has_role","role:"+role3["term"]))
                        triples.add(("role:"+role3["term"],"is_a_sub_class_of","role:"+role2["term"]))
                        get_synonym(entities,triples,role3,entity_type="role",class_type="Role")
                        if "descendants" not in role3.keys():continue
                        role4=role3["descendants"]["descendant"]
                        if type(role4)==dict:
                            role=[role4]
                        else:
                            role=role4
                        for role4 in role:
                            entities.add(("Role","Root"))
                            triples.add(("role:"+role4["term"],"is_a","Role"))
                            entities.add(("role:"+role4["term"],"Role"))
                            triples.add((hmdb_id,"has_role","role:"+role4["term"]))
                            triples.add(("role:"+role4["term"],"is_a_sub_class_of","role:"+role3["term"]))
                            get_synonym(entities,triples,role4,entity_type="role",class_type="Role")
                            if "descendants" not in role4.keys():continue
                            role5=role4["descendants"]["descendant"]
                            if type(role5)==dict:
                                role=[role5]
                            else:
                                role=role5
                            for role5 in role:
                                entities.add(("Role","Root"))
                                triples.add(("role:"+role5["term"],"is_a","Role"))
                                entities.add(("role:"+role5["term"],"Role"))
                                triples.add((hmdb_id,"has_role","role:"+role5["term"]))
                                triples.add(("role:"+role5["term"],"is_a_sub_class_of","role:"+role4["term"]))
                                get_synonym(entities,triples,role5,entity_type="role",class_type="Role")
    
    return entities,triples

def get_synonym(entities, triples, dict_content,entity_type,class_type):
    if "synonyms" in dict_content.keys():
        if dict_content["synonyms"]:
            if type(dict_content["synonyms"]["synonym"])==list:
                for _ in dict_content["synonyms"]["synonym"]:
                    entities.add((class_type,"Root"))
                    triples.add((entity_type+":"+_,"is_a",class_type))
                    entities.add((entity_type+":"+_,class_type))
                    triples.add((entity_type+":"+_,"is_a",entity_type+":"+dict_content["term"]))
            else:
                entities.add((class_type,"Root"))
                triples.add((entity_type+":"+dict_content["synonyms"]["synonym"],"is_a",class_type))
                entities.add((entity_type+":"+dict_content["synonyms"]["synonym"],class_type))
                triples.add((entity_type+":"+dict_content["synonyms"]["synonym"],"is_a",entity_type+":"+dict_content["term"]))
