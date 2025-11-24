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
pip install pynini
```

**Note pour Windows :** L'installation de Pynini peut nécessiter des outils de compilation. Si vous rencontrez des erreurs, consultez la [documentation officielle de Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini).

## 📁 Structure du projet

```
├── create_far.py          # Script de création du fichier FAR
├── normalize.py           # Script de normalisation de texte
├── cardinal_numbers.far   # Fichier FAR compilé (généré)
└── README.md             # Ce fichier
```

## 🛠️ Utilisation

### Étape 1 : Générer le fichier FAR

Avant la première utilisation, vous devez générer le fichier FAR contenant le FST compilé :

```bash
python create_far.py
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
python normalize.py "5 bonbons"
```
**Résultat :** `cinq bonbons`

**Autres exemples :**

```bash
python normalize.py "J'ai 25 ans et 3 chats"
# Résultat : J'ai vingt-cinq ans et trois chats

python normalize.py "Il y a 100 personnes dans la salle"
# Résultat : Il y a cent personnes dans la salle

python normalize.py "Le train part à 17 heures 42"
# Résultat : Le train part à dix-sept heures quarante-deux
```

#### B. Mode interactif

Lancez le script sans arguments pour entrer en mode interactif :

```bash
python normalize.py
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

#### C. Utiliser un fichier FAR personnalisé

Si vous avez créé un fichier FAR avec un nom différent :

```bash
python normalize.py -f mon_fichier.far "42 réponses"
```

### Aide

Pour afficher l'aide :

```bash
python normalize.py --help
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

Pour personnaliser le FST, éditez le fichier `create_far.py` et modifiez les fonctions suivantes :

- `get_digit_fst()` : Chiffres 0-9
- `get_teen_fst()` : Nombres 10-19
- `get_tens_fst()` : Dizaines 20-90
- `get_hundreds_fst()` : Centaines 100-900
- `build_cardinal_fst()` : Logique de combinaison

Après modification, régénérez le fichier FAR :

```bash
python create_far.py
```

### Étendre la plage de nombres

Pour supporter des nombres au-delà de 1000, ajoutez les règles nécessaires dans la fonction `build_cardinal_fst()`.

## 🐛 Dépannage

### Problème : `ModuleNotFoundError: No module named 'pynini'`

**Solution :** Installez Pynini :
```bash
pip install pynini
```

### Problème : `Le fichier FAR 'cardinal_numbers.far' n'existe pas`

**Solution :** Exécutez d'abord le script de création :
```bash
python create_far.py
```

### Problème : Erreurs de compilation sous Windows

**Solution :** Pynini nécessite des outils de compilation C++. Installez :
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- Ou utilisez WSL (Windows Subsystem for Linux)

## 📚 Ressources

- [Documentation Pynini](https://www.openfst.org/twiki/bin/view/GRM/Pynini)
- [OpenFST](https://www.openfst.org/)
- [Finite State Transducers](https://en.wikipedia.org/wiki/Finite-state_transducer)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Forker le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commiter vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Votre Nom - [Votre GitHub](https://github.com/votre-username)

## 🙏 Remerciements

- Merci à l'équipe OpenFST pour la bibliothèque Pynini
- Inspiré par les systèmes de normalisation de texte en NLP

---

**Note :** Ce projet a été développé dans le cadre de [description du contexte si applicable].

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub !