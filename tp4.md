# TP4
## Augmentation des données
J'ai conçu dans cette étape un script augmentation.py pour prétraiter et augmenter mes données.
Dans mon fichier CSV de corpus, le champ des catégories est une liste sous forme de chaînes (par exemple : ['astro-ph.SR']), qui doit être convertie en une véritable liste de balises. En même temps, j'ai fait le prétraitement du texte et l'amélioration simple des données pour les champs abstraits.

1. Lire les catégories CSV et analyser dans des listes multi-étiquettes.
2. Faire le prétraitement du texte pour l'abstrait (en minuscules, supprimer les caractères spéciaux, les participes).
3. Amélioration des données : "supprimer les mots" au hasard chaque donnée pour générer un nouvel échantillon synthétique (la taille de la version améliorée des données est le double de celle des données d'origine).
4. Utiliser MultiLabelBinarizer pour transformer les étiquettes en vecteurs binaires multi-étiquettes (pratique pour la formation du modèle).

Pour les faire, j'ai conçu plusieurs fonction:
- Parse_categories : Transformer la chaîne de catégorie en liste.
- Clean_text : Mettre en minuscules, supprimer les caractères non littéraux.
- Tokenize_text : La division des mots.
- Random_deletion : Amélioration des données, suppression aléatoire de certains mots.
- Preprocess_and_augment : Retourner les vecteurs d'étiquette et le texte amélioré.

Et maintenant j'ai le fichier augmented_data.csv prêt pour l'entrainement.