# MetaKG Reproduce Report - LYX - 2024/07/29

---

## Step-0: Create Environment & Install Dependencies

1. Clone MetaKG repository

```bash
git clone https://github.com/YuxingLu613/MetaKG.git
```

2. (Optional) Create and activate a dedicated Conda environment:

```bash
conda create -n metakg python==3.8
conda activate metakg
```

3. Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Key Dependencies:

```python
pandas 2.0.3
pykeen 1.10.2
bioservices 1.11.2
networkx 3.1
tqdm 4.66.4
```

---



## Quick start version (Full version is below)

### Step-1: Download MetaKG resources

Download MetaKG entities and MetaKG triples from Google Drive and replace them with current `metakg/data/extract_data/metakg_entities.csv` and `metakg/data/extract_data/metakg_triples.csv`.

- metakg_entities.csv: https://drive.google.com/file/d/191pXoQ4wl8GHj8sUzrHCHuVaobWUG5YQ/view?usp=drive_link

- metakg_triples.csv: https://drive.google.com/file/d/1Lq1oDkKhYQSumArl3SOQd6TtNOSW9u1e/view?usp=drive_link



### Step-2: KG construction & training

Run `quick_start.py` to construct MetaKG and train MetaKGE. (GPU is highly recommended)
```bash
python quick_start.py
```
MetaKG Library is stored in the format of triples, all the analysis & statistics results will be stored in `metakg/outputs/`.

**Note:** Parameters should be adjusted based on your hardware. For example, using a single Nvidia A100 GPU, setting `batch_size` to 16384 will take approximately 1 minute per epoch, or about 1 day for full training.



### Step-3: Inference from checkpoint

After the MetaKGE training in **Step-2**, the pre-trained MetaKGE vectors are stored in `metakg/checkpoints/` folder. Use the `predict` function in `quick_start.py` for custom inference tasks.



To bypass **Steps 1 and 2** and directly explore MetaKG's inference capabilities:

1. Download the pre-trained MetaKGE vectors from Google Drive. 

- RotatE.zip: https://drive.google.com/file/d/1rJYrTUC5IQzdHGLWzMXpKlus7VYyKCnE/view?usp=drive_link

- Extract this .zip file to `metakg/checkpoints/` folder.

- Modify `quick_start.py`: 
  - Comment out all lines except line 57.
- Run the modified script:

```bash
python quick_start.py
```

This will generate inference results based on the pre-trained model.

---


## Full version

### Step-1: Download HMDB resources

Download `hmdb_metabolites.json.zip` from Google Drive and unzip to `metakg/data/resource/HMDB/hmdb_metabolites.json`.

- hmdb_metabolites.json.zip: https://drive.google.com/file/d/1mWLCa1LFNIxoNTn9Sr05m7RoY-VPcsdv/view?usp=drive_link

or you can download `HMDB.zip` from Google Drive and unzip to `metakg/data/extract_data/HMDB`.

- HMDB.zip: https://drive.google.com/file/d/1_Wb9m6Yn6hFx4Vsd4ui0zTIRWWfpDiid/view?usp=drive_link

### Step-2: Download SMPDB resources

Download `smpdb_metabolites.csv.zip`, `smpdb_pathways.csv.zip`  and `smpdb_proteins.csv.zip`from Google Drive and unzip to `metakg/data/resource/SMPDB/`.

- smpdb_metabolites.csv.zip: https://drive.google.com/file/d/1JCnMi_wkBws9RI9b2xVhJDvBL4RQQX2s/view?usp=drive_link
- smpdb_pathways.csv.zip: https://drive.google.com/file/d/1P3iCsnkwMKMvlq-0KRMTzAXkSEqM-cBv/view?usp=drive_link
- smpdb_proteins.csv.zip: https://drive.google.com/file/d/1PGuDwMlpDoE1zWVQ_Ws8Q-DrBLxFQUmI/view?usp=drive_link

or you can download `SMPDB.zip` from Google Drive and unzip to `metakg/data/extract_data/HMDB`.

- SMPDB.zip: https://drive.google.com/file/d/1PPcb7yIHBgKgz8swbpFhuCKu3b6GTdWE/view?usp=drive_link

### Step-3: Download KEGG resources

Download `KEGG.zip` from Google Drive and unzip to `metakg/data/extract_data/KEGG/kegg_preprocessed`.

- KEGG_preprocessed.zip: https://drive.google.com/file/d/1m-QS3HjGr17-3SuYlvvHreSCTDNkNKy9/view?usp=drive_link

or you can download `KEGG.zip` from Google Drive and unzip to `metakg/data/extract_data/KEGG`.

- KEGG.zip: https://drive.google.com/file/d/1TCobU-I9nxvCvYBL2achFv9RqhrzRYUo/view?usp=drive_link

### Step-4: KG construction & training

Run `main.py` to construct MetaKG and train MetaKGE. (GPU is highly recommended)

```bash
python main.py
```

MetaKG Library is stored in the format of triples, all the analysis & statistics results will be stored in `metakg/outputs/`.

**Note:** Parameters should be adjusted based on your hardware. For example, using a single Nvidia A100 GPU, setting `batch_size` to 16384 will take approximately 1 minute per epoch, or about 1 day for full training.

### Step-5: Inference from checkpoint

After the MetaKGE training in **Step-4**, the pre-trained MetaKGE vectors are stored in `metakg/checkpoints/` folder. Use the `predict` function in `main.py` for custom inference tasks.



To bypass **Steps 1-4** and directly explore MetaKG's inference capabilities:

1. Download the pre-trained MetaKGE vectors from Google Drive. 

- RotatE.zip: https://drive.google.com/file/d/1rJYrTUC5IQzdHGLWzMXpKlus7VYyKCnE/view?usp=drive_link

- Extract this .zip file to `metakg/checkpoints/` folder.

- Modify `main.py`: 
  - Comment out all lines except line 97.
- Run the modified script:

```bash
python main.py
```

This will generate inference results based on the pre-trained model.

