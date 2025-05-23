# Outils de traitement de corpus
## Classification des articles multi-catégories
### Workflow
1. python crawling.py https://en.wikipedia.org/wiki/Milky_Way
2. python scraping.py
3. python get_csv.py
4. python visualization.py
5. python save300data.py
6. python augmentation.py
7. python fine_tuning.py
8. python label_class.py
9. python generate_test_set.py
10. python evaluate_model.py
11. python prediction.py

### Lack of several huge files
Parce que les données utilisée pour générer le corpus d'entraînement et le modèle lui-même sont trop volumieux, je ne les ai pas mis dans le dossier "data". Mais ils peuvent tous être obtenus grâce aux processus ci-dessus.
3. python get_csv.py -> arxiv_abstracts_sampled100000.csv
7. python fine_tuning.py -> ./fine_tuned_model/model.safetensors
