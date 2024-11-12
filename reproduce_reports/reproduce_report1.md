# MetaKG Reproduce Report - LYX - 2024/07/29

## Overview
MetaKG is a knowledge graph framework integrating metabolomics data from multiple databases (HMDB, SMPDB, KEGG). This guide covers setup, implementation, and usage of both basic and advanced features.

## Prerequisites

### Hardware Requirements
- CUDA-compatible GPU (recommended)
- RAM: 16GB minimum, 32GB recommended 
- Storage: 50GB free space

### Software Requirements
```bash
# Core dependencies
python==3.8
pandas==2.0.3
pykeen==1.10.2
bioservices==1.11.2
networkx==3.1
torch==1.9.0
```

## Implementation Guide

### 1. Data Processing Pipeline

#### Data Extraction
```python
# Extract HMDB data
hmdb_entities, hmdb_triples = extract_hmdb_data(
    file_path="data/resource/HMDB/hmdb_metabolites.json"
)

# Extract SMPDB data
metabolite_entities, metabolite_triples = extract_smpdb_metabolite_data()
protein_entities, protein_triples = extract_smpdb_protein_data()

# Extract KEGG data
kegg_entities, kegg_triples = extract_kegg_data()
```


### 2. Knowledge Graph Embedding

#### Available Models
**Model Categories:**
- Translational: TransE, TransD, TransH, TransR
- Complex: RotatE, ComplEx
- Convolutional: ConvE, ConvKB
- Multiplicative: DistMult, SimplE
- Graph Neural Network: R-GCN, NodePiece
- Other: And more...

#### Training Pipeline
```python
def training_pipeline(model_name, **kwargs):
    # Initialize model and data
    triple_factor_data = construct_triples(model_name)
    
    # Training setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Execute pipeline
    results = pipeline(
        training=triple_factor_data_train,
        validation=triple_factor_data_val,
        testing=triple_factor_data_test,
        model=model_name,
        device=device,
        **kwargs
    )
    
    # Save results
    save_model_artifacts(results, model_name)
    
    return results
```

### 3. Inference and Analysis

#### Link Prediction
```python
def predict(model_name, head=None, relation=None, tail=None, show_num=3):
    """
    Predict missing entities in a triple.
    
    Args:
        model_name: Name of the trained model
        head: Head entity (optional)
        relation: Relation type (optional)
        tail: Tail entity (optional)
        show_num: Number of predictions to show
    
    Returns:
        DataFrame with predictions and scores
    """
```

#### Statistical Analysis
```python
# Generate KG statistics
summary(metakg_library_triples, 
        show_bar_graph=False, 
        save_result=True, 
        topk=20)

# Search related entities
search.search_backward(
    triples=triples,
    nodes=["disease:Nonalcoholic fatty liver disease"],
    relations=["has_disease"],
    show_only=100
)
```

## Directory Structure
```
metakg/
├── data/
│   ├── resource/
│   │   ├── HMDB/
│   │   ├── SMPDB/
│   │   └── KEGG/
│   └── extract_data/
├── checkpoints/
├── results/
└── src/
    ├── metakg_construction/
    ├── metakg_analysis/
    ├── metakg_machine_learning/
    └── metakg_inference/
```

## Model Training Details

### Training Process
1. Data Preparation
   - Split into train/validation/test sets
   - Create inverse triples (optional)
   - Generate ID mappings

2. Model Training
   - Uses SLCWATrainingLoop (Self-Adversarial Learning)
   - Supports early stopping
   - Optional SMILES embedding integration

3. Model Evaluation
   - Uses RankBasedEvaluator
   - Filters existing triples
   - Generates comprehensive metrics

### Saving Artifacts
- Model checkpoints
- Entity embeddings
- Relation embeddings
- ID mappings
- Evaluation results

## Performance Optimization

### Memory Management
- Batch processing for large graphs
- GPU memory optimization
- Gradient checkpointing support

### Training Speed
- Negative sampling strategies
- Early stopping implementation
- Multi-GPU support (where available)

## Troubleshooting

### Common Issues
1. **CUDA Out of Memory**
   - Reduce batch size
   - Enable gradient checkpointing
   - Use CPU offloading

2. **Slow Training**
   - Check GPU utilization
   - Optimize data loading
   - Enable mixed precision training

3. **Poor Convergence**
   - Adjust learning rate
   - Modify negative sampling
   - Try different model architectures

## References
1. [MetaKG GitHub Repository](https://github.com/YuxingLu613/MetaKG)
2. [HMDB Database](https://hmdb.ca/)
3. [SMPDB Database](https://smpdb.ca/)
4. [KEGG Database](https://www.genome.jp/kegg/)
5. [PyKEEN Documentation](https://pykeen.readthedocs.io/)
