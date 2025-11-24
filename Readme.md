# Normalisation de Nombres Cardinaux en Français

Un système de normalisation de texte basé sur les FST (Finite State Transducers) qui convertit les nombres de 0 à 1000 en leur forme écrite en français.

## 📋 Description

Ce projet utilise la bibliothèque **Pynini** pour créer un transducteur à états finis (FST) capable de normaliser les nombres cardinaux dans un texte. Par exemple, "5 bonbons" devient "cinq bonbons".

### Fonctionnalités

- ✅ Normalisation des nombres de **0 à 1000**
- ✅ Support des règles grammaticales françaises (traits d'union, accords)
- ✅ Traitement de textes complets avec plusieurs nombres
- ✅ Mode ligne de commande et mode interactif
- ✅ FST compilé dans un fichier FAR pour une utilisation rapide

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

**Note pour Windows :** L'installation de Pynini peut nécessiter des outils de compilation. Si vous rencontrez des erreurs, consultez la [documentation officielle de Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini).

## 📁 Structure du projet

```
├──data/                                        # Dossier comportant une dataset pour l'evaluation de notre FSt
├       ├──/dataset_normalisation_0_1000.csv    # dataset en question.
├── script_sauvegarde.py                        # Script de création du fichier FAR
├── script.py                                   # Script de normalisation de texte
├── cardinal_numbers.far                        # Fichier FAR compilé (généré)
├── script_wer.py                               # Script pour reproduire le score WER obtenu 
├── Text_Normalisation_Cardinaux_0_a_1000.py    # Script de creation du FST  
├── Text_Normalisation_Cardinaux_0_a_1000.ypnb  # Script de creation du FST notebook
├── rapport.pdf                                 # Mon rapport 
└── README.md                                   # Ce fichier
```

## 🛠️ Utilisation

### Étape 1 : si Fichier Far absent : Générer le fichier FAR

Si le fichier Far absent, vous devez générer le fichier FAR contenant le FST compilé :

```bash
python script_sauvegarde.py
```

**Sortie attendue :**
```
Construction du FST cardinal...
Création du fichier FAR: cardinal_numbers.far
  ✓ FST 'CARDINAL' ajouté au FAR
✓ Fichier FAR créé avec succès: cardinal_numbers.far

==================================================
TEST DU FST DEPUIS LE FICHIER FAR
==================================================
   0 → zéro
   7 → sept
  15 → quinze
  42 → quarante-deux
  99 → quatre-vingt-dix-neuf
 100 → cent
 256 → deux cent cinquante-six
1000 → mille

✓ Processus terminé avec succès!
```

### Étape 2 : Normaliser du texte

Une fois le fichier FAR créé, vous pouvez normaliser du texte de plusieurs façons :

#### A. Mode ligne de commande

```bash
python script.py "800 francs"
```
**Résultat :** `huit-cents francs`

**Autres exemples :**

```bash
python script.py "J'ai 25 ans et 3 chats"
# Résultat : J'ai vingt-cinq ans et trois chats

```

#### B. Mode interactif

Lancez le script sans arguments pour entrer en mode interactif :

```bash
python script.py
```

**Exemple de session interactive :**
```
============================================================
MODE INTERACTIF - Normalisation de nombres
============================================================
Fichier FAR: cardinal_numbers.far
Tapez votre texte (ou 'quit' pour quitter)
============================================================

Texte> 5 bonbons
  → cinq bonbons

Texte> J'ai 25 ans
  → J'ai vingt-cinq ans

Texte> quit

👋 Au revoir!
```
### Comment repoduire l'obtention de mon score WER
```bash
python script_wer.py "data/dataset_normalisation_0_1000.csv"
```
**Résultat :**
```
============================================================
CALCUL DU WER - Normalisation de Nombres Cardinaux
============================================================

🔧 Chargement du FST...
✓ FST chargé avec succès
📂 Chargement du dataset: data/dataset_normalisation_0_1000.csv
✓ Dataset chargé: 133 lignes

🔄 Normalisation des phrases...
  Traité: 100/133 phrases
✓ Normalisation terminée: 133 phrases traitées

📊 Calcul du WER...

============================================================
RÉSULTATS
============================================================
📈 WER Score Moyen: 0.0071 (0.71%)
📊 Nombre total de phrases: 133
✓ WER minimum: 0.0000
✗ WER maximum: 0.2500
============================================================

✓ Processus terminé avec succès!
```

### Aide

Pour afficher l'aide :

```bash
python script.py --help
```

## 📝 Exemples de normalisation

| Entrée | Sortie |
|--------|--------|
| `0` | `zéro` |
| `7` | `sept` |
| `15` | `quinze` |
| `25` | `vingt-cinq` |
| `42` | `quarante-deux` |
| `99` | `quatre-vingt-dix-neuf` |
| `100` | `cent` |
| `256` | `deux cent cinquante-six` |
| `1000` | `mille` |

## 🔧 Personnalisation

### Modifier les règles de normalisation

Pour personnaliser le FST, éditez le fichier `Text_Normalisation_Cardinaux_0_a_1000.py` et modifiez les dictionnaires que vous sauhaiter ou certains fst que vous souhaitez modifier. 

Après modification, régénérez le fichier FAR :

```bash
python script_sauvegarde.py
```


## 🐛 Dépannage

### Problème : `ModuleNotFoundError: No module named 'pynini'`

**Solution :** Installez Pynini :
```bash
pip install pynini
```

### Problème : `Le fichier FAR 'cardinal_numbers.far' n'existe pas`

**Solution :** Exécutez d'abord le script de création :
```bash
python script_sauvegarde.py
```

### Problème : Erreurs de compilation sous Windows

**Solution :** Pynini nécessite des outils de compilation C++. Installez :
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Ou utilisez WSL (Windows Subsystem for Linux)
- Ou encore installer [via conda-forge](https://pypi.org/project/pynini/#:~:text=While%20Pynini%20is%20neit)

## 📚 Ressources

- [Documentation Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini)
- [OpenFST](https://www.openfst.org/)
- [Finite State Transducers](https://fr.wikipedia.org/wiki/Transducteur_fini)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Forker le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commiter vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request


## 👨‍💻 Auteur

FOKA MAGHEN YANN BRONDON- [Votre GitHub](https://github.com/yann214)

## 🙏 Remerciements

- Merci à l'équipe OpenFST pour la bibliothèque Pynini
- Inspiré par les systèmes de normalisation de texte en NLP

---

**Note :** Ce projet a été développé dans le cadre de la phase de test pour le stage de 3 mois sur la Normalisation de Text offert pas IndabaX.

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub !