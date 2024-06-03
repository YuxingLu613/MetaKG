import pickle
import pykeen
from pykeen.datasets.base import PathDataset,CoreTriplesFactory,TriplesFactory
import torch
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop,LCWATrainingLoop
from pykeen.evaluation import RankBasedEvaluator
from pykeen.sampling import BasicNegativeSampler
from pykeen.stoppers import EarlyStopper
from pykeen.losses import MarginRankingLoss
from pykeen.pipeline import pipeline
import os
import numpy as np
from pykeen.models import *
import json
from pykeen.utils import set_random_seed
import pickle

set_random_seed(42)

def save_id_mapping(model_name, dir_path="data"):
    """Save id mapping of the constructed triples in JSON format to the specified directory.

    Args:
        dir_path (str, optional): Directory to save the files. Defaults to "data".

    Returns:
        None
    """
    
    if os.path.exists(f"data/{model_name}/triple/train_triples/base.pth"):
        triple_factor_data_train=TriplesFactory.from_path_binary(f"data/{model_name}/triple/train_triples")
    else:
        triple_factor_data_train, triple_factor_data_val, triple_factor_data_test, triple_factor_data = construct_triples(model_name=model_name)

    if not os.path.exists(os.path.join(dir_path, model_name)):
        os.mkdir(os.path.join(dir_path, model_name))

    with open(os.path.join(dir_path, model_name, "entity_to_id.json"), "w") as f:
        json.dump(triple_factor_data_train.entity_to_id, f)
    with open(os.path.join(dir_path, model_name, "id_to_entity.json"), "w") as f:
        json.dump({i: j for j, i in triple_factor_data_train.entity_to_id.items()}, f)

    with open(os.path.join(dir_path, model_name, "relation_to_id.json"), "w") as f:
        json.dump(triple_factor_data_train.relation_to_id, f)
    with open(os.path.join(dir_path, model_name, "id_to_relation.json"), "w") as f:
        json.dump({i: j for j, i in triple_factor_data_train.relation_to_id.items()}, f)


def construct_triples(model_name,
                    train_path="data/kge_training/TrainingSet.txt",
                    valid_path="data/kge_training/ValidationSet.txt",
                    test_path="data/kge_training/TestSet.txt", 
                    create_inverse_triples=True):
    """Construct triples from the provided training, testing and validation sets.

    Args:
        train_path (str, optional): Path to training set file. Defaults to "data/TrainingSet.txt".
        valid_path (str, optional): Path to validation set file. Defaults to "data/ValidationSet.txt".
        test_path (str, optional): Path to testing set file. Defaults to "data/TestSet.txt".
        create_inverse_triples (bool, optional): Whether or not to create inverse triples. Defaults to True.

    Returns:
        tuple: Tuple containing training, validation and testing data.
    """
    triple_factor_data = PathDataset(training_path=train_path,
                                        testing_path=test_path,
                                        validation_path=valid_path,
                                        create_inverse_triples=create_inverse_triples)
    triple_factor_data_train = triple_factor_data.training
    triple_factor_data_test = triple_factor_data.testing
    triple_factor_data_val = triple_factor_data.validation
    
    if not os.path.exists(f"data/{model_name}/"):
        os.mkdir(f"data/{model_name}/")
    if not os.path.exists(f"data/{model_name}/triple"):
        os.mkdir(f"data/{model_name}/triple")
    triple_factor_data_train.to_path_binary(f"data/kge_training/{model_name}/triple/train_triples")
    triple_factor_data_val.to_path_binary(f"data/kge_training/{model_name}/triple/val_triples")
    triple_factor_data_test.to_path_binary(f"data/kge_training/{model_name}/triple/test_triples")
    
    print(triple_factor_data.summarize())

    return triple_factor_data_train, triple_factor_data_val, triple_factor_data_test, triple_factor_data


class KGEmbedding():
    
    def __init__(self,model_name) -> None:
        self.model_name=model_name
    
    def construct_triples(self,
                          train_path="data/TrainingSet.txt",
                          valid_path="data/EvaluationSet.txt",
                          test_path="data/TestSet.txt", 
                          create_inverse_triples=True):
        """Construct triples from the provided training, testing and validation sets.

        Args:
            train_path (str, optional): Path to training set file. Defaults to "data/TrainingSet.txt".
            valid_path (str, optional): Path to validation set file. Defaults to "data/EvaluationSet.txt".
            test_path (str, optional): Path to testing set file. Defaults to "data/TestSet.txt".
            create_inverse_triples (bool, optional): Whether or not to create inverse triples. Defaults to True.

        Returns:
            tuple: Tuple containing training, validation and testing data.
        """
        triple_factor_data = PathDataset(training_path=train_path,
                                         testing_path=test_path,
                                         validation_path=valid_path,
                                         create_inverse_triples=create_inverse_triples)
        triple_factor_data_train = triple_factor_data.training
        triple_factor_data_test = triple_factor_data.testing
        triple_factor_data_val = triple_factor_data.validation
        
        if not os.path.exists(f"data/{self.model_name}/"):
            os.mkdir(f"data/{self.model_name}/")
        if not os.path.exists(f"data/{self.model_name}/triple"):
            os.mkdir(f"data/{self.model_name}/triple")
        triple_factor_data_train.to_path_binary(f"data/{self.model_name}/triple/train_triples")
        triple_factor_data_val.to_path_binary(f"data/{self.model_name}/triple/val_triples")
        triple_factor_data_test.to_path_binary(f"data/{self.model_name}/triple/test_triples")
        
        print(triple_factor_data.summarize())

        self.save_id_mapping()

        return triple_factor_data_train, triple_factor_data_val, triple_factor_data_test, triple_factor_data
    
    
    # 保存xx_to_id,id_to_xx文件
    def save_id_mapping(self, dir_path="data"):
        """Save id mapping of the constructed triples in JSON format to the specified directory.

        Args:
            dir_path (str, optional): Directory to save the files. Defaults to "data".

        Returns:
            None
        """
        
        if os.path.exists(f"data/{self.model_name}/triple/train_triples/base.pth"):
            triple_factor_data_train=TriplesFactory.from_path_binary(f"data/{self.model_name}/triple/train_triples")
        else:
            triple_factor_data_train, triple_factor_data_val, triple_factor_data_test, triple_factor_data = self.construct_triples()

        if not os.path.exists(os.path.join(dir_path, self.model_name)):
            os.mkdir(os.path.join(dir_path, self.model_name))

        with open(os.path.join(dir_path, self.model_name, "entity_to_id.json"), "w") as f:
            json.dump(triple_factor_data_train.entity_to_id, f)
        with open(os.path.join(dir_path, self.model_name, "id_to_entity.json"), "w") as f:
            json.dump({i: j for j, i in triple_factor_data_train.entity_to_id.items()}, f)

        with open(os.path.join(dir_path, self.model_name, "relation_to_id.json"), "w") as f:
            json.dump(triple_factor_data_train.relation_to_id, f)
        with open(os.path.join(dir_path, self.model_name, "id_to_relation.json"), "w") as f:
            json.dump({i: j for j, i in triple_factor_data_train.relation_to_id.items()}, f)
        
    
    # KGE训练
    def Train_KGE(self,save_model=True,add_smiles=False):
        
        # triple_factor_data_train,triple_factor_data_vld,triple_factor_data_tst,triple_factor_data=self.construct_triples()
        
        # results=pipeline(
        #         training=triple_factor_data_train,
        #         testing=triple_factor_data_tst,
        #         stopper="early",
        #         model='TransE',
        #         loss='marginranking',
        #         model_kwargs=dict(embedding_dim=2),
        #         optimizer_kwargs=dict(lr=1.0e-1),
        #         training_kwargs=dict(num_epochs=128, use_tqdm_batch=True),
        #         evaluation_kwargs=dict(use_tqdm=True),
        #         random_seed=1,
        #         device='cuda',
        #     )
        
        # self.model=results.model
        
        if self.model_name=="ConvE":
            KGE_model=ConvE
        if self.model_name=="TransE":
            KGE_model=TransE
        if self.model_name=="TransD":
            KGE_model=TransD
        if self.model_name=="TransH":
            KGE_model=TransH
        if self.model_name=="TransR":
            KGE_model=TransR
        if self.model_name=="KG2E":
            KGE_model=KG2E
        if self.model_name=="RotatE":
            KGE_model=RotatE
        if self.model_name=="ComplEx":
            KGE_model=ComplEx
        if self.model_name=="ConvKB":
            KGE_model=ConvKB
        if self.model_name=="ER-MLP":
            KGE_model=ERMLP
        if self.model_name=="ProjE":
            KGE_model=ProjE
        if self.model_name=="R-GCN":
            KGE_model=RGCN
        if self.model_name=="SimplE":
            KGE_model=SimplE
        if self.model_name=="PairRE":
            KGE_model=PairRE
        if self.model_name=="QuatE":
            KGE_model=QuatE
        if self.model_name=="NodePiece":
            KGE_model=NodePiece
        if self.model_name=="TransF":
            KGE_model=TransF
        if self.model_name=="DistMult":
            KGE_model=DistMult


        if os.path.exists(f"data/{self.model_name}/triple/train_triples/base.pth"):
            triple_factor_data_train=TriplesFactory.from_path_binary(f"data/{self.model_name}/triple/train_triples")
        else:
            triple_factor_data_train,triple_factor_data_vld,triple_factor_data_tst,triple_factor_data=self.construct_triples()


        # negative_sampler=BasicNegativeSampler(
        #     mapped_triples=triple_factor_data_train.mapped_triples,
        #     filtered=True,
        #     # num_negs_per_pos=1
        # )
        
        self.model = KGE_model(
            triples_factory=triple_factor_data_train,
            embedding_dim=128,
            random_seed=42
        ).cuda()
        
        optimizer = Adam(lr=1e-3,params=self.model.get_grad_params())
        criterion = MarginRankingLoss(margin=1)
        
        # early_stopper=EarlyStopper(
        #     model=self.model,
        #     evaluator=RankBasedEvaluator(),
        #     training_triples_factory=triple_factor_data_train,
        #     evaluation_triples_factory=triple_factor_data_vld,
        #     patience=10,
        # )
        
        training_loop = SLCWATrainingLoop(
            model=self.model,
            triples_factory=triple_factor_data_train,
            optimizer=optimizer,
            # negative_sampler=negative_sampler
        )
        
        # Train
        training_loop.train(triples_factory=triple_factor_data_train,
                            num_epochs=100,
                            # stopper=early_stopper,
        )
        
        if add_smiles:
            with open(os.path.join("data", self.model_name, "entity_to_id.json"), "r") as f:
                entity_to_id=json.load(f)
            with open("/home/luyx/HMKG/HMKG-Progress/HMKG/hmkg/hmdb_smiles_embedding.pkl","rb") as f:
                smiles_embedding=pickle.load(f)

            for id in list(smiles_embedding.keys()):
                # print(self.model.entity_representations[0]._embeddings.weight.data[int(entity_to_id["hmdb_id:"+id])])
                # print(self.model.entity_representations[0]._embeddings.weight.data[int(entity_to_id["hmdb_id:"+id])].shape)
                # print(torch.tensor(smiles_embedding[id],device="cuda").shape)
                if "hmdb_id:"+id in entity_to_id.keys():
                    self.model.entity_representations[0]._embeddings.weight.data[int(entity_to_id["hmdb_id:"+id])]=(self.model.entity_representations[0]._embeddings.weight.data[int(entity_to_id["hmdb_id:"+id])]+torch.tensor(smiles_embedding[id],device="cuda"))/2

            training_loop = SLCWATrainingLoop(
                model=self.model,
                triples_factory=triple_factor_data_train,
                optimizer=optimizer,
                negative_sampler=negative_sampler
            )
            
            training_loop.train(triples_factory=triple_factor_data_train,
                        num_epochs=50,
            )
        # print(self.model.entity_representations[0]._embeddings.weight.data[0])
        # self.model.entity_representations[0]._embeddings.weight.data[0]=torch.tensor([0.]*50)
        # print(self.model.entity_representations[0]._embeddings.weight.data[0])
        
        # _ = training_loop.train(
        #     triples_factory=triple_factor_data_train,
        #     num_epochs=100,
        #     batch_size=256,
        # )
        
        print(self.model.entity_representations[0]._embeddings.weight.data[0])
        
        
        if save_model:
            if not os.path.exists("checkpoints/"):
                os.mkdir("checkpoints")
            if add_smiles:
                torch.save(self.model,f"checkpoints/{self.model_name}_add_smiles.pkl")
            else:
                torch.save(self.model,f"checkpoints/{self.model_name}.pkl")
                
        return self.model


    # KGE测试
    def Evaluate_KGE(self,save_results=True,add_smiles=False):
        
        if self.model_name=="ConvE":
            KGE_model=ConvE
        if self.model_name=="TransE":
            KGE_model=TransE
        if self.model_name=="TransD":
            KGE_model=TransD
        if self.model_name=="TransH":
            KGE_model=TransH
        if self.model_name=="TransR":
            KGE_model=TransR
        if self.model_name=="KG2E":
            KGE_model=KG2E
        if self.model_name=="RotatE":
            KGE_model=RotatE
        if self.model_name=="ComplEx":
            KGE_model=ComplEx
        if self.model_name=="ConvKB":
            KGE_model=ConvKB
        if self.model_name=="ER-MLP":
            KGE_model=ERMLP
        if self.model_name=="ProjE":
            KGE_model=ProjE
        if self.model_name=="R-GCN":
            KGE_model=RGCN
        if self.model_name=="SimplE":
            KGE_model=SimplE
        if self.model_name=="PairRE":
            KGE_model=PairRE
        if self.model_name=="QuatE":
            KGE_model=QuatE
        if self.model_name=="NodePiece":
            KGE_model=NodePiece
        if self.model_name=="TransF":
            KGE_model=TransF
        if self.model_name=="DistMult":
            KGE_model=DistMult
            
        if os.path.exists(f"data/{self.model_name}/triple/train_triples/base.pth"):
            triple_factor_data_train=TriplesFactory.from_path_binary(f"data/{self.model_name}/triple/train_triples")
            triple_factor_data_val=TriplesFactory.from_path_binary(f"data/{self.model_name}/triple/val_triples")
            triple_factor_data_test=TriplesFactory.from_path_binary(f"data/{self.model_name}/triple/test_triples")
        else:
            triple_factor_data_train,triple_factor_data_val,triple_factor_data_test,triple_factor_data=self.construct_triples()
        
        self.model = KGE_model(
            triples_factory=triple_factor_data_train,
            embedding_dim=128,
            random_seed=42
        ).cuda()
        
        if add_smiles:
            self.model=torch.load(f"checkpoints/{self.model_name}_add_smiles.pkl")
        else:
            self.model=torch.load(f"checkpoints/{self.model_name}.pkl")
        
        evaluator = RankBasedEvaluator()

        # Get triples to test
        mapped_triples = triple_factor_data_test.mapped_triples
        
        # Evaluate
        results = evaluator.evaluate(
            model=self.model,
            mapped_triples=mapped_triples,
            additional_filter_triples=[
                triple_factor_data_train.mapped_triples,
                triple_factor_data_val.mapped_triples,
            ],
        )

        print(results.data)
        
        if save_results:
            result_data_json = json.dumps({str(k): results.data[k] for k in results.data.keys() if ("realistic" in str(k) and "both" in str(k))}, indent=4, ensure_ascii=False)

            if not os.path.exists("results/"):
                os.mkdir("results")
            
            if add_smiles:
                write_res_pth = f"results/{self.model_name}_add_smiles_results.json"
            else:
                write_res_pth = f"results/{self.model_name}_results.json"
            with open(write_res_pth, "w") as f:
                f.write(result_data_json)
            f.close()

        return results

        
    # 保存所有embedding
    def save_all_embeddings(self,add_smiles=False):
        if not os.path.exists("embeddings/"):
            os.mkdir("embeddings")
        
        if add_smiles:
            np.save(f"embeddings/{self.model_name}_Entity_Embedding_add_smiles.npy",self.model.entity_representations[0]._embeddings.weight.data.cpu().numpy())
            np.save(f"embeddings/{self.model_name}_Relation_Embedding_add_smiles.npy",self.model.relation_representations[0]._embeddings.weight.data.cpu().numpy())
        else:
            np.save(f"embeddings/{self.model_name}_Entity_Embedding.npy",self.model.entity_representations[0]._embeddings.weight.data.cpu().numpy())
            np.save(f"embeddings/{self.model_name}_Relation_Embedding.npy",self.model.relation_representations[0]._embeddings.weight.data.cpu().numpy())
    
    
    # 保存所有HMDB化合物的embedding
    def save_hmdb_embeddings(self):
        with open(f"data/{self.model_name}/entity_to_id.json","r") as f:
            entity_to_id=json.load(f)
        with open(f"data/{self.model_name}/id_to_entity.json","r") as f:
            id_to_entity=json.load(f)
        
        HMDBs=[i for i in entity_to_id.keys() if "HMDB" in i]
        HMDB_ids=[entity_to_id[i] for i in HMDBs]
    
        entity_embeddings=np.load(f"embeddings/{self.model_name}_Entity_Embedding.npy")
        HMDB_embedding_dict={}
        for i in HMDB_ids:
            HMDB_embedding_dict[id_to_entity[str(i)]]=entity_embeddings[i]
        
        
        if not os.path.exists("results/"):
            os.mkdir("results")
        with open(f"results/{self.model_name}_HMDB_Embedding.pkl","wb") as f:
            pickle.dump(HMDB_embedding_dict,f)

    
    # 根据输入的类别保存embedding
    def save_multiple_categories_embedding(self,categories):
        with open(f"data/{self.model_name}/entity_to_id.json","r") as f:
            entity_to_id=json.load(f)
        with open(f"data/{self.model_name}/id_to_entity.json","r") as f:
            id_to_entity=json.load(f)
        with open(self.entity_path, newline='', encoding='utf-8') as f:
            entity_list = f.readlines()
            entity_list = [i.strip("\r\n").split("\t") for i in entity_list]
        
        entities={}
        for entity in entity_list:
            if entity[1] in categories and entity[0] in entity_to_id.keys():
                if entity[1] not in entities.keys():
                    entities[entity[1]] = [entity_to_id[entity[0]]]
                else:
                    entities[entity[1]].append(entity_to_id[entity[0]])
        
        entity_embeddings=np.load(f"embeddings/{self.model_name}_Entity_Embedding.npy")
        
        entity_embeddings_dict={}
        for category in entities.keys():
            category_embedding={}
            for entity_id in entities[category]:
                    category_embedding[id_to_entity[str(entity_id)]]=entity_embeddings[entity_id]
            entity_embeddings_dict[category]=category_embedding
        
        with open(f"results/{self.model_name}_{'_'.join(categories)}_Embedding.pkl","wb") as f:
            pickle.dump(entity_embeddings_dict,f)


    # KGE pipeline
    def KGE_model_pipeline(self,eval_model=True,save_model=True,save_results=True,add_smiles=False,save_embeddings=True,save_HMDB_embedding=True,save_multiple_categories_embedding=None,save_id_mapping=True):
        
        if save_id_mapping:
            self.save_id_mapping(dir_path="data")
        
        self.Train_KGE(save_model=save_model,add_smiles=add_smiles)
        
        if save_embeddings:
            self.save_all_embeddings(add_smiles=add_smiles)
            
        if save_HMDB_embedding:
            self.save_hmdb_embeddings()
        
        if save_multiple_categories_embedding:
            self.save_multiple_categories_embedding(categories=save_multiple_categories_embedding)
            
        if eval_model:
            self.Evaluate_KGE(save_results=save_results,add_smiles=add_smiles)