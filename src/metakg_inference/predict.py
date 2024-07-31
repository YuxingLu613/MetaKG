from pykeen.predict import predict_triples,predict_all,predict_target
import torch
from pykeen.predict import predict_target
from pykeen.datasets.base import TriplesFactory
import os


def link_prediction(model,triple_factor_data_train,head=None,relation=None,tail=None,show_num=3):
    if head=="":
        head=None
    if relation=="":
        relation=None
    if tail=="":
        tail=None
    assert (head is None) ^ (relation is None) ^ (tail is None)
    if not head:
        predicted_result= predict_target(
            model=model,
            relation=relation,
            tail=tail,
            triples_factory=triple_factor_data_train,
        )
    if not relation:
        predicted_result= predict_target(
            model=model,
            head=head,
            tail=tail,
            triples_factory=triple_factor_data_train,
        )
    if not tail:
        predicted_result= predict_target(
            model=model,
            relation=relation,
            head=head,
            triples_factory=triple_factor_data_train,
        )
    predicted_result=predicted_result.df.iloc[:,1:]
    predicted_result.columns=["score","target"]
    predicted_result.reset_index(inplace=True)
    return predicted_result[["target","score"]][:show_num]


def predict(model_name, head=None, relation=None, tail=None, show_num=3):

    model=torch.load(f"./checkpoints/{model_name}/trained_model.pkl",map_location=torch.device('cpu'))

    if os.path.exists(f"checkpoints/{model_name}/data/triple/test_triples/base.pth"):
        triple_factor_data_train=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/test_triples")
        triple_factor_data_val=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/val_triples")
        triple_factor_data_test=TriplesFactory.from_path_binary(f"checkpoints/{model_name}/data/triple/test_triples")
    else:
        print("No triples found, please train the model first")
        return None
    
    result=link_prediction(model,triple_factor_data_train,head,relation,tail,show_num)
    print(result)
    return result




