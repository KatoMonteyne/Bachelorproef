# Bachelorproef - De impact van klimaatverandering op de mariene biodiversiteit.
Deze repository bevat de code en ondersteunend materiaal ontwikkeld in het kader van de bachelorproef "De impact van klimaatverandering op de mariene biodiversiteit". <br>

Bachelorproef voorgelegd voor het behalen van de graad Bachelor of Science in de Bio‐ingenieurswetenschappen <br>
Academiejaar: 2025 – 2026

## Beschrijving
Het doel van deze bachelorproef is het onderzoeken van de impact van klimaatverandering op de mariene biodiversiteit met behulp van machinelearningmodellen. Deze repository bevat de scripts gebruikt voor het onderzoek.

## Structuur van de repository
- `Data inladen/`  
  Deze map bevat scripts die gebruikt worden om toekomstige data afkomstig van Bio-ORACLE
  op te slaan als CSV-bestanden. Voor elke biodiversiteitsmaat wordt een afzonderlijk script voorzien.

- `Data/`  
  Deze map bevat alle gebruikte datasets.  
  `Diversity_data_with_biooracle_2010.csv` bevat de huidige Bio-ORACLE-data, geannoteerd met de
  biodiversiteitsmaten.  
  `Diversity_data_with_env.csv` bevat de huidige AquaMaps-data, geannoteerd met de
  biodiversiteitsmaten. <br>
  De overige CSV-bestanden zijn gegenereerd met behulp van de scripts in `Data inladen/`.

- `Kaartjes_MarineBiodiversity.py`  
  Dit script bevat de code voor het genereren van kaarten van de huidige biodiversiteitsmaten.

- `Model_FD.ipynb`  
  Deze notebook bevat de code voor het opstellen van modellen voor fylogenetische diversiteit (FD),
  inclusief de volledige methodologie zoals beschreven in de bachelorproef.

- `Model_GD.ipynb`  
  Deze notebook bevat de code voor het opstellen van modellen voor genetische diversiteit (GD),
  volgens de werkwijze beschreven in de bachelorproef.

- `Model_SR.ipynb`  
  Deze notebook bevat de code voor het opstellen van modellen voor soortenrijkdom (SR),
  volgens de werkwijze beschreven in de bachelorproef.
 
## Gebruik
De code werd ontwikkeld in Python. <br>
Benodigde pakketten worden rechtstreeks in de scripts ingeladen. <br>
Het volstaat om de drie notebooks  
`Model_FD.ipynb`, `Model_GD.ipynb` en `Model_SR.ipynb`  
uit te voeren om de resultaten uit deze bachelorproef te reproduceren.
  
## Auteurs
Emma Aluwé <br>
Kato Monteyne <br>
Morgane Baelen <br>
Norah Van de Putte <br>

Promotoren: prof. dr. Bernard De Baets, dr. ir. Maxime Van Haeverbeke <br>
Tutor: dr. ir. Maxime Van Haeverbeke
