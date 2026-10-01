# ======================================================
# DAPT (Domain-Adaptive Pre-Training) com MLM
# Salva checkpoint adaptado ao domínio para uso posterior
# ======================================================

import os
import random
import numpy as np
import pandas as pd
import torch
import transformers

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForMaskedLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

print("Transformers:", transformers.__version__)

# ----------------- Configurações -----------------
BASE_DIR = r"C:\Users\Janaina\Desktop\Mestrado"

# Arquivo usado no DAPT: coloque aqui o corpus textual de domínio
DAPT_PATH = os.path.join(
    BASE_DIR,
    "Comentarios_YT",
    "df_comentarios.csv"
)

TEXT_COL = "Comentário"

BASE_MODEL = "neuralmind/bert-base-portuguese-cased"

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "modelos",
    "dapt_capacitismo_bertimbau"
)

MAX_LEN = 128
BATCH_SIZE = 32
LR = 2e-5
NUM_EPOCHS = 2
WEIGHT_DECAY = 0.01
SEED = 42
MLM_PROB = 0.15

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------- Reprodutibilidade -----------------
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(SEED)

if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True

# ----------------- Carregar dados -----------------
df = pd.read_csv(DAPT_PATH)
assert TEXT_COL in df.columns, f"Coluna '{TEXT_COL}' não encontrada."

df = df.dropna(subset=[TEXT_COL]).copy()
df[TEXT_COL] = (
    df[TEXT_COL]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

texts = df[TEXT_COL].tolist()
print(f"Total de textos para DAPT: {len(texts)}")

# ----------------- Tokenizer e modelo -----------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True)
model = AutoModelForMaskedLM.from_pretrained(BASE_MODEL)

# ----------------- Dataset Hugging Face -----------------
raw_ds = Dataset.from_dict({"text": texts})

def tokenize_fn(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=MAX_LEN,
        padding=False,
    )

tokenized_ds = raw_ds.map(
    tokenize_fn,
    batched=True,
    remove_columns=["text"]
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=MLM_PROB
)

# ----------------- TrainingArguments -----------------
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=WEIGHT_DECAY,
    logging_steps=500,
    save_strategy="epoch",
    save_total_limit=1,
    fp16=torch.cuda.is_available(),
    seed=SEED,
    report_to="none",
    dataloader_num_workers=0,
    dataloader_pin_memory=True,
)

# ----------------- Trainer -----------------
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_ds,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# ----------------- Treino -----------------
trainer.train()

# ----------------- Salvar checkpoint final -----------------
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"[OK] Checkpoint DAPT salvo em: {OUTPUT_DIR}")