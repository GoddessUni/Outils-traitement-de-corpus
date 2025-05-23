# TP1
## Partie 1
1. CoNLL 2003 propose la tâche concernant la reconnaissance des entités nommées indépendamment de la langue. Dans cette tâche on concentre sur 4 types d'entités nommées : les personnes, les lieux, les organisations et les noms d'entités diverses qui n'appartiennent pas aux trois groupes précédents.
2. Dans CoNLL 2003 il y a les données de 4 colonnes séparées par un seul espace.Le premier élément de chaque ligne est un mot, le deuxième une balise de partie de la parole (POS), le troisième une balise de morceau syntaxique et le quatrième la balise d'entité nommée.
3. CoNLL-2003 répond au besoin d’évaluer et d’améliorer les systèmes de reconnaissance d’entités nommées. Il couvert les besoins de l'évaluation standardisée des modèles des entités nommées, de l'amélioration des modèles des entités nommées en contexte journalistique, du développement de techniques adaptées aux langues multiples, et de l'amélioration des applications utilisant la reconnaissance d'entités nommées.
4. Plusieurs modèles ont été entrainées sur CoNLL 2003 tels que les modèle statistiques: HMM, CRF, SVM. Les modèles de Deep Learning: BiLSTM-CRF avec embeddings. Les modèles de transformers: BERT, RoBERTa, XLM-R.
5. CoNLL 2003 est un corpus multilingue qui contient des textes en anglais et en allemand.

## Partie 2
1. Je voudrais concevoir un programme pour obtenir automatiquement le contenu du texte sur les pages web et produire un résumé court.
2. Maintenant, je traite principalement sur le sujet d'obtenir le corpus depuis wikipédia et générer l'abstraite de ce corpus.
3. Je vais réaliser la tâche de génération abstraite.
4. Je récupère les données sur Internet en page html, et je les nettoie et les transforme en fichier txt.
5. Je vais les récupérer sur les page web tel que Wikipédia.
6. Oui, ces données sont libre d'accès.