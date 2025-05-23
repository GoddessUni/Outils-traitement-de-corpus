# TP6
## Evaluation
Dans cette étape, je divise le processus en 2 parties:

### Partie 1: Evaluer le modèle avec test.csv
J'ai conçu un script generate_test_set afin de générer un corpus de test de 100 données à partir de mes 100,000 données d'origine.
Pour cette raison, j'ai utilisé d'abord label_class.py pour obtenir l'ordre des étiquettes lors de la construction du modèle.
Et puis j'ai extrait aléatoirement 100 échantillons avec les catégories qui apparaissaient dans le corpus d'entrainement du modèle et j'ai converti leurs catégories en binaire, et j'ai finalement exporté test.csv.

Après cela, j'ai conçu un script evaluate_model.py pour tester mon modèle et j'ai enregistré les résultats sur evaluation.txt.

=== Threshold: 0.30 ===
Hamming Loss: 0.371025641025641
Accuracy (exact match): 0.0
Micro Precision: 0.007890461824089116
Micro Recall: 0.34
Micro F1: 0.015422998412338398

=== Threshold: 0.40 ===
Hamming Loss: 0.04153846153846154
Accuracy (exact match): 0.0
Micro Precision: 0.005128205128205128
Micro Recall: 0.02
Micro F1: 0.00816326530612245

=== Threshold: 0.50 ===
Hamming Loss: 0.008547008547008548
Accuracy (exact match): 0.0
Micro Precision: 0.0
Micro Recall: 0.0
Micro F1: 0.0

Les résultats montrent que dans la tâche de prédiction multi-catégories, la précision du modèle est très faible, et il y a de moins en moins d'étiquettes prédites par le modèle après l'augmentation du seuil.
Cela montre que la distribution de l'ensemble d'entraînement n'est pas équilibrée.
En raison des performances limitées de mon ordinateur, le corpus d'entraînement réellement utilisé par mon modèle est très petit. Je pense que si j'utilise entièrement les 100,000 données pour entraîner le modèle, sa précision peut être grandement améliorée.

### Partie 2: Distribution des catégories du texte sur Internet
Puisque j'ai également trouvé le texte sur Internet, je peux enfin utiliser le modèle pour prédire sa catégorie.
J'ai conçu un script prediction.py pour distribuer les étiquettes de catégories au texte que j'ai trouvé sur Internet et nettoyé.
Maintenant j'ai obtenu la prédiction comme:

échantillon du texte:
 From Wikipedia, the free encyclopedia Galaxy containing the Solar System This article is about the galaxy. For other uses, see Milky Way (disambiguation) . The Milky Way or Milky Way Galaxy [ c ] is t

catégories:
['astro-ph', 'astro-ph.GA', 'cond-mat.quant-gas', 'cond-mat.stat-mech', 'cond-mat.supr-con', 'cs.CC', 'cs.CR', 'cs.CV', 'cs.DB', 'cs.DM', 'cs.DS', 'cs.LG', 'cs.NI', 'cs.RO', 'cs.SE', 'cs.SI', 'econ.GN', 'eess.SP', 'eess.SY', 'gr-qc', 'hep-lat', 'hep-th', 'math.AG', 'math.CA', 'math.CO', 'math.CV', 'math.DG', 'math.DS', 'math.FA', 'math.IT', 'math.MG', 'math.MP', 'math.QA', 'math.SG', 'nlin.PS', 'nlin.SI', 'nucl-ex', 'patt-sol', 'physics.ao-ph', 'physics.atom-ph', 'physics.flu-dyn', 'q-bio.BM', 'q-fin.EC', 'q-fin.ST', 'stat.TH']

Avec les probabilités les plus élevées:
nucl-ex: 0.444
eess.SP: 0.440

Je pense que c'est parce que mon modèle est principalement entraîné par les résumés des articles scientifiques, et il n'est pas fort lorsqu'il traite des pages d'introduction de connaissances qui ne sont pas très liées à les thèses.
