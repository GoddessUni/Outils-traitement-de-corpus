# TP5
## Fine Tuning le modèle
Tout d'abord, j'ai préparé l'environnement pour le processus de fine-tuning:
pip install transformers datasets scikit-learn torch

Mon but:
1. Convertir multi-étiquettes en un format vectoriel binaire acceptable pour le modèle (MultiLabelBinarizer).
2. Utiliser des modèles de langage pré-entraînés (tels que BERT) comme modèle de base.
3. Réglage fin avec l'API Transformer's Trainer.
4. Définir les indicateurs d'évaluation adaptés aux tâches multi-étiquettes (micro-F1).

Pour les faire, j'ai créer un script fine_tuning.py.

Après ce processus, j'ai obtenu un modèle entrainé avec les fichiers:
- config.json
- model.safetensor
- special_tokens_map.json
- tokenizer_config.json
- tokenizer.json
- vocab.txt
