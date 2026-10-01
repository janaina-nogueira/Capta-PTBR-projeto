# ======================================================
# Fase 3 - COM DAPT
# 1) carrega checkpoint DAPT treinado no BiasTube
# 2) faz treino supervisionado no Capta-PTBR
# 3) aplica o modelo final no BiasTube
# 4) salva CSV com classe predita e probabilidade
# SEM emitir métricas
# ======================================================

import os
import random
import numpy as np
import pandas as pd
import torch
import transformers

from sklearn.model_selection import train_test_split
from torch.nn import CrossEntropyLoss
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)

print("Transformers:", transformers.__version__)

# ----------------- Configurações -----------------
BASE_DIR = r"C:\Users\Janaina\Desktop\Mestrado"

# Dataset supervisionado (Capta)
CAPTA_PATH = os.path.join(
    BASE_DIR,
    "tuPyE",
    "tupye_padronizado_capta_estagio2.csv"
)

# Dataset para inferência final (BiasTube)
BIASTUBE_PATH = os.path.join(
    BASE_DIR,
    "Comentarios_YT",
    "df_comentarios.csv"
)

# Colunas
CAPTA_TEXT_COL = "text"
CAPTA_LABEL_COL = "capacitismo_majoritario_bin"
BIASTUBE_TEXT_COL = "Comentário"

# Checkpoint vindo do DAPT no BiasTube
DAPT_MODEL = os.path.join(
    BASE_DIR,
    "modelos",
    "dapt_capacitismo_bertimbau"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "modelos",
    "ft_capta_com_dapt_majoritario_sem_metricas"
)

SPLIT_PATH = os.path.join(
    BASE_DIR,
    "modelos",
    "split_capta_majoritario_seed42.csv"
)

BIASTUBE_PRED_PATH = os.path.join(
    OUTPUT_DIR,
    "biastube_predito_com_dapt.csv"
)

MAX_LEN = 128
BATCH_SIZE = 32
LR = 2e-5
NUM_EPOCHS = 2
WEIGHT_DECAY = 0.01
SEED = 42

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
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("Rodando em CPU")

# ----------------- Carregar CAPTA -----------------
capta_df = pd.read_csv(CAPTA_PATH)
print("Colunas CAPTA:", capta_df.columns.tolist())

assert CAPTA_TEXT_COL in capta_df.columns, f"Coluna '{CAPTA_TEXT_COL}' não encontrada."
assert CAPTA_LABEL_COL in capta_df.columns, f"Coluna '{CAPTA_LABEL_COL}' não encontrada."

capta_df = capta_df.dropna(subset=[CAPTA_TEXT_COL, CAPTA_LABEL_COL]).copy()
capta_df[CAPTA_TEXT_COL] = (
    capta_df[CAPTA_TEXT_COL]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

capta_df[CAPTA_LABEL_COL] = pd.to_numeric(capta_df[CAPTA_LABEL_COL], errors="coerce")
capta_df = capta_df.dropna(subset=[CAPTA_LABEL_COL]).copy()
capta_df[CAPTA_LABEL_COL] = capta_df[CAPTA_LABEL_COL].astype(int)
capta_df = capta_df[capta_df[CAPTA_LABEL_COL].isin([0, 1])].copy()

capta_df = capta_df.reset_index(drop=True)
capta_df["row_id"] = capta_df.index

print("\nDistribuição geral CAPTA:")
print(capta_df[CAPTA_LABEL_COL].value_counts(dropna=False))
print(capta_df[CAPTA_LABEL_COL].value_counts(normalize=True, dropna=False))

# ----------------- Split reprodutível -----------------
if os.path.exists(SPLIT_PATH):
    split_df = pd.read_csv(SPLIT_PATH)
    train_ids = split_df.loc[split_df["split"] == "train", "row_id"].tolist()
    test_ids = split_df.loc[split_df["split"] == "test", "row_id"].tolist()
else:
    train_ids, test_ids = train_test_split(
        capta_df["row_id"].tolist(),
        test_size=0.2,
        random_state=SEED,
        stratify=capta_df[CAPTA_LABEL_COL]
    )
    split_df = pd.concat([
        pd.DataFrame({"row_id": train_ids, "split": "train"}),
        pd.DataFrame({"row_id": test_ids, "split": "test"})
    ], ignore_index=True)
    split_df.to_csv(SPLIT_PATH, index=False)

train_df = capta_df[capta_df["row_id"].isin(train_ids)].copy()
test_df = capta_df[capta_df["row_id"].isin(test_ids)].copy()

print("\nDistribuição (train):")
print(train_df[CAPTA_LABEL_COL].value_counts(normalize=True))
print("\nDistribuição (test):")
print(test_df[CAPTA_LABEL_COL].value_counts(normalize=True))

# ----------------- Tokenizer -----------------
tokenizer = AutoTokenizer.from_pretrained(DAPT_MODEL, use_fast=True)

# ----------------- Datasets -----------------
class LabeledTextDataset(Dataset):
    def __init__(self, dataframe, tokenizer, text_col, label_col, max_len=128):
        self.labels = dataframe[label_col].astype(int).tolist()
        texts = dataframe[text_col].tolist()
        self.enc = tokenizer(
            texts,
            truncation=True,
            max_length=max_len,
            padding=False,
        )

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.enc.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

class UnlabeledTextDataset(Dataset):
    def __init__(self, dataframe, tokenizer, text_col, max_len=128):
        texts = dataframe[text_col].tolist()
        self.enc = tokenizer(
            texts,
            truncation=True,
            max_length=max_len,
            padding=False,
        )

    def __len__(self):
        return len(self.enc["input_ids"])

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.enc.items()}
        return item

train_ds = LabeledTextDataset(train_df, tokenizer, CAPTA_TEXT_COL, CAPTA_LABEL_COL, MAX_LEN)
test_ds = LabeledTextDataset(test_df, tokenizer, CAPTA_TEXT_COL, CAPTA_LABEL_COL, MAX_LEN)

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer,
    pad_to_multiple_of=8
)

# ----------------- Balanceamento -----------------
num_pos = int(train_df[CAPTA_LABEL_COL].sum())
num_neg = int(len(train_df) - num_pos)
N = len(train_df)

class_weights = torch.tensor(
    [N / (2 * max(num_neg, 1)), N / (2 * max(num_pos, 1))],
    dtype=torch.float
)

sample_weights = np.where(
    train_df[CAPTA_LABEL_COL].values == 1,
    class_weights[1].item(),
    class_weights[0].item()
)

sampler = WeightedRandomSampler(
    weights=torch.DoubleTensor(sample_weights),
    num_samples=len(sample_weights),
    replacement=True
)

print("\nClass weights [neg, pos]:", class_weights.tolist())

# ----------------- Modelo -----------------
model = AutoModelForSequenceClassification.from_pretrained(
    DAPT_MODEL,
    num_labels=2
)

# ----------------- Trainer customizado -----------------
class WeightedTrainer(Trainer):
    def __init__(self, class_weights=None, sampler=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights
        self.custom_sampler = sampler

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        cw = self.class_weights.to(logits.device) if self.class_weights is not None else None
        loss_fct = CrossEntropyLoss(weight=cw)
        loss = loss_fct(logits.view(-1, model.config.num_labels), labels.view(-1))

        return (loss, outputs) if return_outputs else loss

    def get_train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.args.train_batch_size,
            sampler=self.custom_sampler,
            collate_fn=self.data_collator,
            num_workers=0,
            pin_memory=torch.cuda.is_available()
        )

args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=WEIGHT_DECAY,
    logging_steps=500,
    save_strategy="no",
    fp16=torch.cuda.is_available(),
    seed=SEED,
    report_to="none",
    dataloader_num_workers=0,
    dataloader_pin_memory=True,
    save_total_limit=1,
)

trainer = WeightedTrainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    tokenizer=tokenizer,
    data_collator=data_collator,
    class_weights=class_weights,
    sampler=sampler,
)

# ----------------- Treino supervisionado no CAPTA -----------------
trainer.train()

# ======================================================
# AVALIAÇÃO NO TESTE (CAPTA) - MÉTRICAS
# ======================================================
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    average_precision_score,
    classification_report,
)

print("\n[INFO] Calculando métricas no conjunto de teste (CAPTA)...\n")

pred_output = trainer.predict(test_ds)

logits = pred_output.predictions
y_true = pred_output.label_ids
y_pred = np.argmax(logits, axis=1)
y_prob = torch.softmax(torch.tensor(logits), dim=1).numpy()[:, 1]

# Accuracy
acc = accuracy_score(y_true, y_pred)

# Precision, Recall, F1 (classe positiva)
precision_pos, recall_pos, f1_pos, _ = precision_recall_fscore_support(
    y_true, y_pred, average="binary", pos_label=1, zero_division=0
)

# F1 macro
_, _, f1_macro, _ = precision_recall_fscore_support(
    y_true, y_pred, average="macro", zero_division=0
)

# AUROC
try:
    auroc = roc_auc_score(y_true, y_prob)
except ValueError:
    auroc = float("nan")

# AUPRC
auprc = average_precision_score(y_true, y_prob)

# Dicionário final
metrics = {
    "Accuracy": float(acc),
    "Precision+": float(precision_pos),
    "Recall+": float(recall_pos),
    "F1+": float(f1_pos),
    "F1macro": float(f1_macro),
    "AUROC": float(auroc),
    "AUPRC+": float(auprc),
}

print("\n=== MÉTRICAS TESTE | COM DAPT ===")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

print("\n=== Classification Report ===")
print(classification_report(y_true, y_pred, digits=4))

# ----------------- Predict no BIAS TUBE -----------------
biastube_df = pd.read_csv(BIASTUBE_PATH)
print("\nColunas BiasTube:", biastube_df.columns.tolist())

assert BIASTUBE_TEXT_COL in biastube_df.columns, f"Coluna '{BIASTUBE_TEXT_COL}' não encontrada."

biastube_df = biastube_df.copy()
biastube_df[BIASTUBE_TEXT_COL] = (
    biastube_df[BIASTUBE_TEXT_COL]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# mantém índice original e remove só os vazios para inferência
biastube_pred_df = biastube_df[biastube_df[BIASTUBE_TEXT_COL] != ""].copy()

biastube_ds = UnlabeledTextDataset(
    biastube_pred_df,
    tokenizer,
    BIASTUBE_TEXT_COL,
    MAX_LEN
)

pred_output = trainer.predict(biastube_ds)
logits = pred_output.predictions

biastube_pred_df["classe_predita"] = np.argmax(logits, axis=1)
biastube_pred_df["probabilidade_positiva"] = (
    torch.softmax(torch.tensor(logits), dim=1).numpy()[:, 1]
)

# recoloca no dataframe completo
biastube_df["classe_predita"] = np.nan
biastube_df["probabilidade_positiva"] = np.nan

biastube_df.loc[biastube_pred_df.index, "classe_predita"] = biastube_pred_df["classe_predita"]
biastube_df.loc[biastube_pred_df.index, "probabilidade_positiva"] = biastube_pred_df["probabilidade_positiva"]

# opcional: converter classe para inteiro onde houver valor
mask_pred = biastube_df["classe_predita"].notna()
biastube_df.loc[mask_pred, "classe_predita"] = biastube_df.loc[mask_pred, "classe_predita"].astype(int)

# ----------------- Salvar saídas -----------------
biastube_df.to_csv(BIASTUBE_PRED_PATH, index=False, encoding="utf-8-sig")
print(f"\n[OK] Predições do BiasTube salvas em: {BIASTUBE_PRED_PATH}")

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"[OK] Modelo final salvo em: {OUTPUT_DIR}")