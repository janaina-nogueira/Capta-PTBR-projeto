import pandas as pd
import numpy as np

# caminho do arquivo gerado
PATH = r"C:\Users\Janaina\Desktop\Mestrado\modelos\ft_capta_sem_dapt\biastube_predito_sem_dapt.csv"

df = pd.read_csv(PATH)

# ----------------- nome da coluna -----------------
COL_PROB = "prob"

# ----------------- estatísticas descritivas -----------------
stats = df[COL_PROB].describe(percentiles=[0.5, 0.9, 0.95, 0.99])

print("\n=== Estatísticas descritivas ===")
print(stats)

# salvar em dict (útil pra LaTeX depois)
stats_dict = {
    "Total": len(df),
    "Media": df[COL_PROB].mean(),
    "Mediana": df[COL_PROB].median(),
    "Std": df[COL_PROB].std(),
    "Min": df[COL_PROB].min(),
    "P90": df[COL_PROB].quantile(0.90),
    "P95": df[COL_PROB].quantile(0.95),
    "P99": df[COL_PROB].quantile(0.99),
    "Max": df[COL_PROB].max(),
}

print("\nResumo formatado:")
for k, v in stats_dict.items():
    print(f"{k}: {v:.6f}")

# ----------------- faixas de probabilidade -----------------
bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]

df["faixa"] = pd.cut(df[COL_PROB], bins=bins, labels=labels, include_lowest=True)

dist = df["faixa"].value_counts().sort_index()
perc = df["faixa"].value_counts(normalize=True).sort_index() * 100

print("\n=== Distribuição por faixa ===")
for faixa in labels:
    print(f"{faixa}: {dist[faixa]} ({perc[faixa]:.3f}%)")

# ----------------- salvar tabela pronta -----------------
faixa_df = pd.DataFrame({
    "faixa": labels,
    "N": [dist[f] for f in labels],
    "%": [perc[f] for f in labels]
})

faixa_df.to_csv("faixas_probabilidade.csv", index=False)

# ----------------- TOP exemplos completos -----------------

TOP_N = 100  # pode aumentar (ex: 200, 500)

top = df.sort_values(COL_PROB, ascending=False).head(TOP_N)

top_export = top[[
    "Comentário",
    "pred",
    "prob"
]].copy()

top_export.to_csv(
    "top_capacitismo_completo.csv",
    index=False,
    encoding="utf-8-sig"  # importante pro Excel
)

print(f"\n[OK] TOP {TOP_N} comentários salvos em top_capacitismo_completo.csv")