# MetaKG: An In-Depth Guide to Building Metabolic Knowledge Graphs
**Author:** GXR | **Last Updated:** November 4th, 2024

---

## Step 0: Setting Up Your Environment

1. **Clone the MetaKG Repository:**
   ```bash
   git clone https://github.com/YuxingLu613/MetaKG.git
   ```

2. **(Optional) Create a Conda Environment:**
   ```bash
   conda create -n metakg python==3.8
   conda activate metakg
   ```

3. **Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Key Dependencies:
- `pandas`: 2.0.3
- `pykeen`: 1.10.2
- `bioservices`: 1.11.2
- `networkx`: 3.1
- `tqdm`: 4.66.4

---

## Quick Start Guide

### Step 1: Download MetaKG Resources
Replace the existing files with the following from Google Drive:
- **MetaKG Entities:** [Download](https://drive.google.com/file/d/191pXoQ4wl8GHj8sUzrHCHuVaobWUG5YQ/view?usp=drive_link)
- **MetaKG Triples:** [Download](https://drive.google.com/file/d/1Lq1oDkKhYQSumArl3SOQd6TtNOSW9u1e/view?usp=drive_link)

### Step 2: Constructing the Knowledge Graph
Execute the following command to build MetaKG and train MetaKGE (GPU recommended):
```bash
python quick_start.py
```
*Note: Adjust parameters based on your hardware capabilities.*

### Step 3: Inference from Checkpoint
After training, the pre-trained vectors will be in `metakg/checkpoints/`. Use the `predict` function in `quick_start.py` for inference tasks.

#### Bypass Steps 1 and 2:
1. Download pre-trained vectors: [RotatE.zip](https://drive.google.com/file/d/1rJYrTUC5IQzdHGLWzMXpKlus7VYyKCnE/view?usp=drive_link)
2. Extract to `metakg/checkpoints/`.
3. Modify `quick_start.py` to comment out all lines except line 57.
4. Run:
   ```bash
   python quick_start.py
   ```

---

## Full Version Instructions

### Step 1: Download HMDB Resources
- **Download:** [hmdb_metabolites.json.zip](https://drive.google.com/file/d/1mWLCa1LFNIxoNTn9Sr05m7RoY-VPcsdv/view?usp=drive_link) and unzip to `metakg/data/resource/HMDB/hmdb_metabolites.json`.
- Alternatively, download [HMDB.zip](https://drive.google.com/file/d/1_Wb9m6Yn6hFx4Vsd4ui0zTIRWWfpDiid/view?usp=drive_link) and unzip to `metakg/data/extract_data/HMDB`.

### Step 2: Download SMPDB Resources
- Download and unzip the following to `metakg/data/resource/SMPDB/`:
  - [smpdb_metabolites.csv.zip](https://drive.google.com/file/d/1JCnMi_wkBws9RI9b2xVhJDvBL4RQQX2s/view?usp=drive_link)
  - [smpdb_pathways.csv.zip](https://drive.google.com/file/d/1P3iCsnkwMKMvlq-0KRMTzAXkSEqM-cBv/view?usp=drive_link)
  - [smpdb_proteins.csv.zip](https://drive.google.com/file/d/1PGuDwMlpDoE1zWVQ_Ws8Q-DrBLxFQUmI/view?usp=drive_link)

### Step 3: Download KEGG Resources
- Download and unzip [KEGG.zip](https://drive.google.com/file/d/1TCobU-I9nxvCvYBL2achFv9RqhrzRYUo/view?usp=drive_link) to `metakg/data/extract_data/KEGG`.

### Step 4: Constructing the Knowledge Graph
Run the following command to build MetaKG and train MetaKGE:
```bash
python main.py
```
*Note: Adjust parameters based on your hardware capabilities.*

### Step 5: Inference from Checkpoint
After training, the pre-trained vectors will be in `metakg/checkpoints/`. Use the `predict` function in `main.py` for inference tasks.

#### Bypass Steps 1-4:
1. Download pre-trained vectors: [RotatE.zip](https://drive.google.com/file/d/1rJYrTUC5IQzdHGLWzMXpKlus7VYyKCnE/view?usp=drive_link).
2. Extract to `metakg/checkpoints/`.
3. Modify `main.py` to comment out all lines except line 97.
4. Run:
   ```bash
   python main.py
   ```

This will generate inference results based on the pre-trained model.

--- 