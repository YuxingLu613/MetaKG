import os
from pykeen.datasets.base import PathDataset,CoreTriplesFactory,TriplesFactory
import torch
from torch.optim import Adam
from pykeen.pipeline import pipeline
from pykeen.utils import set_random_seed
import pickle
import json
import numpy as np
from .kge_training import save_id_mapping,construct_triples


def trainging_pipeline(model_name, loss="marginranking",embedding_dim=128,lr=1.0e-3,num_epochs=1000,batch_size=16384):
    set_random_seed(42)
    if os.path.exists(f"checkpoints/{model_name}/data/triple/train_triples/base.pth"):
        triple_factor_data_train=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/train_triples")
        triple_factor_data_vld=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/val_triples")
        triple_factor_data_tst=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/test_triples")
    else:
        triple_factor_data_train,triple_factor_data_vld,triple_factor_data_tst,triple_factor_data=construct_triples(model_name=model_name)
        save_id_mapping(model_name=model_name)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using: {device}')

    results = pipeline(
        training=triple_factor_data_train,
        validation=triple_factor_data_vld,
        testing=triple_factor_data_tst,
        model=model_name,
        loss=loss,
        model_kwargs=dict(embedding_dim=embedding_dim),
        optimizer=torch.optim.AdamW,
        optimizer_kwargs=dict(lr=lr),
        training_kwargs=dict(num_epochs=num_epochs,
                             use_tqdm_batch=True,
                             batch_size=batch_size),
        evaluation_kwargs=dict(use_tqdm=True,batch_size=batch_size),
        random_seed=42,
        device=device,
    )

    print(results)

    if not os.path.exists(f"checkpoints/{model_name}"):
        os.mkdir(f"checkpoints/{model_name}")

    results.save_to_directory(f"checkpoints/{model_name}",save_metadata=True,save_replicates=True,save_training=True)
    print(f"model saved to checkpoints/{model_name}")
    np.save(f"checkpoints/{model_name}/Entity_Embedding.npy",results.model.entity_representations[0]._embeddings.weight.data.cpu().numpy())
    print(f"entity embedding saved to checkpoints/{model_name}/Entity_Embedding.npy")
    np.save(f"checkpoints/{model_name}/Relation_Embedding.npy",results.model.relation_representations[0]._embeddings.weight.data.cpu().numpy())
    print(f"relation embedding saved to checkpoints/{model_name}/Relation_Embedding.npy")

    with open(f"checkpoints/{model_name}/data/entity_to_id.json","r") as f:
        entity_to_id=json.load(f)
    with open(f"checkpoints/{model_name}/data/id_to_entity.json","r") as f:
        id_to_entity=json.load(f)
    
    HMDBs=[i for i in entity_to_id.keys() if "HMDB" in i]
    HMDB_ids=[entity_to_id[i] for i in HMDBs]

    entity_embeddings=np.load(f"checkpoints/{model_name}/Entity_Embedding.npy")
    HMDB_embedding_dict={}
    for i in HMDB_ids:
        HMDB_embedding_dict[id_to_entity[str(i)]]=entity_embeddings[i]
    
    with open(f"checkpoints/{model_name}/Metabolite_Embedding.pkl","wb") as f:
        pickle.dump(HMDB_embedding_dict,f)
    print(f"Metabolite embedding saved to checkpoints/{model_name}/Metabolite_Embedding.pkl")
    
    return results