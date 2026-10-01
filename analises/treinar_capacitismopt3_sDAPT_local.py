# ======================================================
# Fase 3 - Fine-tuning supervisionado SEM DAPT
# Treina no Capta-PTBR e aplica inferência no BiasTube
# ======================================================

import os
import json
import random
import numpy as np
import pandas as pd
import torch
import transformers

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    average_precision_score,
    classification_report,
)
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

CAPTA_PATH = os.path.join(BASE_DIR, "tuPyE", "tupye_padronizado_capta_estagio2.csv")

BIAS_PATH = os.path.join(BASE_DIR, "Comentarios_YT", "df_comentarios.csv")

TEXT_COL = "text"
LABEL_COL = "capacitismo_majoritario_bin"
BIAS_TEXT_COL = "Comentário"

BASE_MODEL = "neuralmind/bert-base-portuguese-cased"

OUTPUT_DIR = os.path.join(BASE_DIR, "modelos", "ft_capta_sem_dapt")
SPLIT_PATH = os.path.join(BASE_DIR, "modelos", "split_capta_ptbr_seed42.csv")

MAX_LEN = 128
BATCH_SIZE = 32
LR = 2e-5
NUM_EPOCHS = 2
WEIGHT_DECAY = 0.01
SEED = 42

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------- Seed -----------------
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(SEED)

# ----------------- Dados -----------------
df = pd.read_csv(CAPTA_PATH)

df = df.dropna(subset=[TEXT_COL, LABEL_COL]).copy()
df[TEXT_COL] = df[TEXT_COL].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()
df[LABEL_COL] = df[LABEL_COL].astype(int)

df = df.reset_index(drop=True)
df["row_id"] = df.index

# ----------------- Split -----------------
if os.path.exists(SPLIT_PATH):
    split_df = pd.read_csv(SPLIT_PATH)
    train_ids = split_df[split_df["split"] == "train"]["row_id"].tolist()
    test_ids = split_df[split_df["split"] == "test"]["row_id"].tolist()
else:
    train_ids, test_ids = train_test_split(
        df["row_id"], test_size=0.2, random_state=SEED, stratify=df[LABEL_COL]
    )
    split_df = pd.concat([
        pd.DataFrame({"row_id": train_ids, "split": "train"}),
        pd.DataFrame({"row_id": test_ids, "split": "test"})
    ])
    split_df.to_csv(SPLIT_PATH, index=False)

train_df = df[df["row_id"].isin(train_ids)]
test_df = df[df["row_id"].isin(test_ids)]

# ----------------- Tokenizer -----------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

# ----------------- Dataset -----------------
class TextClsDataset(Dataset):
    def __init__(self, df):
        self.labels = df[LABEL_COL].tolist()
        self.enc = tokenizer(df[TEXT_COL].tolist(), truncation=True, max_length=MAX_LEN)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.enc.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

train_ds = TextClsDataset(train_df)
test_ds = TextClsDataset(test_df)

# ----------------- Balanceamento -----------------
num_pos = train_df[LABEL_COL].sum()
num_neg = len(train_df) - num_pos
N = len(train_df)

class_weights = torch.tensor([
    N/(2*num_neg), 
    N/(2*num_pos)
], dtype=torch.float)

sample_weights = np.where(
    train_df[LABEL_COL] == 1,
    class_weights[1],
    class_weights[0]
)

sampler = WeightedRandomSampler(sample_weights, len(sample_weights))

# ----------------- Modelo -----------------
model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL, num_labels=2)

# ----------------- Trainer -----------------
class WeightedTrainer(Trainer):
    def __init__(self, class_weights=None, sampler=None, *args, **kwargs):
        if "processing_class" not in kwargs and "tokenizer" in kwargs:
            kwargs["processing_class"] = kwargs.pop("tokenizer")
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights
        self.custom_sampler = sampler

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        cw = self.class_weights.to(logits.device) if self.class_weights is not None else None
        loss_fct = CrossEntropyLoss(weight=cw) if cw is not None else CrossEntropyLoss()
        loss = loss_fct(
            logits.view(-1, model.config.num_labels),
            labels.view(-1)
        )

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
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=WEIGHT_DECAY,
    fp16=torch.cuda.is_available(),
    report_to="none",
)

trainer = WeightedTrainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    data_collator=DataCollatorWithPadding(tokenizer),
)

# ----------------- Treino -----------------
trainer.train()

# ----------------- Métricas -----------------
pred = trainer.predict(test_ds)

logits = pred.predictions
y_true = pred.label_ids
y_pred = np.argmax(logits, axis=1)
y_prob = torch.softmax(torch.tensor(logits), dim=1).cpu().numpy()[:,1]

metrics = {
    "Accuracy": accuracy_score(y_true, y_pred),
    "Precision+": precision_recall_fscore_support(y_true, y_pred, average="binary")[0],
    "Recall+": precision_recall_fscore_support(y_true, y_pred, average="binary")[1],
    "F1+": precision_recall_fscore_support(y_true, y_pred, average="binary")[2],
    "F1macro": precision_recall_fscore_support(y_true, y_pred, average="macro")[2],
    "AUROC": roc_auc_score(y_true, y_prob) if len(np.unique(y_true))>1 else 0,
    "AUPRC+": average_precision_score(y_true, y_prob),
}

print(metrics)

# ----------------- BiasTube -----------------
bias_df = pd.read_csv(BIAS_PATH)
bias_df = bias_df.dropna(subset=[BIAS_TEXT_COL])

enc = tokenizer(bias_df[BIAS_TEXT_COL].tolist(), truncation=True, max_length=MAX_LEN)

class InferDataset(Dataset):
    def __init__(self, enc):
        self.enc = enc

    def __len__(self):
        return len(self.enc["input_ids"])

    def __getitem__(self, idx):
        return {k: torch.tensor(v[idx]) for k,v in self.enc.items()}

bias_ds = InferDataset(enc)

pred = trainer.predict(bias_ds)
logits = pred.predictions

bias_df["pred"] = np.argmax(logits, axis=1)
bias_df["prob"] = torch.softmax(torch.tensor(logits), dim=1).cpu().numpy()[:,1]

bias_df.to_csv(os.path.join(OUTPUT_DIR, "biastube_predito.csv"), index=False)

top20 = bias_df.sort_values("prob", ascending=False).head(20)
top20.to_csv(os.path.join(OUTPUT_DIR, "top20_capacitistas.csv"), index=False)

print("FINALIZADO")