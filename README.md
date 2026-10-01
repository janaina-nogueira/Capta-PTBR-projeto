# CAPTA-PTBR v1.0

Portal Streamlit para organização e divulgação do Corpus CAPTA-PTBR, modelos,
análises e resultados da dissertação.

## Executar
```powershell
py -m pip install -r requirements.txt
py -m streamlit run streamlit_app.py
```

## Antes de publicar
1. Adicione os CSVs nas pastas `corpus/estagio_1` e `corpus/estagio_2`.
2. Adicione os artefatos dos modelos em `models/`.
3. Adicione códigos/notebooks em `analises/`.
4. Revise quais dados podem ser disponibilizados publicamente.
5. Faça commit e push no GitHub.
6. Conecte o repositório ao Streamlit Community Cloud.

## Identidade visual
A paleta foi inspirada no slide da dissertação fornecido pela autora.
As imagens de UFMS/FACOM em `assets/` foram extraídas do slide fornecido para esta versão do protótipo.
Para publicação institucional definitiva, substitua-as pelos arquivos oficiais aprovados pela UFMS/FACOM.
