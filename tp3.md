# Tp3
## Visualiser votre corpus et réaliser des statistiques de texte
J'ai trouvé le dataset des résumés des articles "gfissore/arxiv-abstracts-2021" sur le site Hugging Face et je l'ai utilisé comme le corpus d'entraînement. J'ai construit un script "get_csv.py" pour téléchargé aléatoirement 100,000 échantillons pour analyse et j'ai utilisé des graines de nombres aléatoires 42 pour assurer que l'opération puisse être reproduite.
J'ai conçu un script visualization.py (dans src/plot/visualization.py) pour générer les graphique de la longueur des résumé (nombre de mots) et de la distribution Zipf (les 30 mots les plus fréquents).
J'ai utilisé matplotlib, seaborn, nltk pour construire mon script.
Mais ce corpus est trop volumineus pour mon projet, et je ne peux pas former le modèle avec mon ordinateur. Par conséquent, j'ai réduit la quantité de données et je n'ai gardé que les 300 premiers pour entraîner le modèle.