# Traitement d'Automates Finis

Projet académique EFREI P2 - 2025/2026
Implémentation en Python d'une pipeline complète de traitement d'automates finis : lecture, affichage, standardisation, déterminisation, minimisation, reconnaissance de mots et automate complémentaire.

---

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Format des fichiers automates](#format-des-fichiers-automates)
- [Génération des traces](#génération-des-traces)
- [Tests](#tests)
- [Répartition du travail](#répartition-du-travail)
- [Conventions de code](#conventions-de-code)

---

## Fonctionnalités

Le programme applique les étapes suivantes sur chaque automate chargé :

1. Lecture d'un automate depuis un fichier `.txt`
2. Affichage sous forme de table alignée (`->` = état initial, `<-` = état terminal, `--` = pas de transition)
3. Test des propriétés : déterministe, standard, complet - avec affichage des raisons si non
4. Standardisation (optionnelle, sur demande)
5. Déterminisation et complétion (construction des sous-ensembles, support des epsilon-transitions) - affichage de la table de correspondance états AFDC <-> états AF d'origine
6. Minimisation (algorithme de Moore) — affichage des partitions successives numérotées et des transitions par parties
7. Reconnaissance de mots en boucle interactive (saisir `fin` pour terminer)
8. Construction et affichage de l'automate complémentaire (construit à partir de l'AFDCM)

---

## Structure du projet

```
PRJ-Automate/
├── src/
│   └── automaton/
│       ├── __init__.py
│       ├── models.py        # Classe Automaton et utilitaire states_to_label()
│       ├── reader.py        # Lecture des fichiers automata/*.txt
│       ├── display.py       # Affichage en table (rich)
│       ├── properties.py    # is_deterministic(), is_standard(), is_complete()
│       ├── standardize.py   # standardize()
│       ├── determinize.py   # complete(), determinize_and_complete(), epsilon_closure()
│       ├── minimize.py      # minimize()
│       ├── recognize.py     # recognize_word()
│       └── complement.py    # complement()
├── tests/
│   ├── test_models.py
│   ├── test_properties.py
│   ├── test_standardize.py
│   ├── test_determinize.py
│   ├── test_minimize.py
│   ├── test_reader.py
│   ├── test_display.py
│   └── test_recognize.py
├── automata/                # 44 fichiers automates (1.txt à 44.txt)
├── traces/                  # Traces d'exécution générées par run_traces.py
├── main.py                  # Point d'entrée interactif
├── run_traces.py            # Génération automatique des traces
└── pyproject.toml
```

---

## Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) comme gestionnaire de paquets et d'environnement virtuel.

**Pourquoi `uv` ?**
`uv` remplace `pip` + `venv` en une seule commande. Il résout les dépendances beaucoup plus rapidement et garantit la reproductibilité de l'environnement à partir du fichier `pyproject.toml`.

### Installer uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Créer l'environnement et installer les dépendances

```bash
uv venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

uv pip install -e ".[dev]"
```

L'option `-e` installe le package en mode éditable : les modifications dans `src/` sont immédiatement prises en compte sans réinstallation.

**Dépendances :**

| Package  | Rôle                             | Environnement |
|----------|----------------------------------|---------------|
| `rich`   | Affichage des tables en terminal | Production    |
| `pytest` | Exécution des tests unitaires    | Développement |
| `ruff`   | Linter et formateur de code      | Développement |

---

## Utilisation

```bash
python main.py
```

Le programme demande le numéro de l'automate à charger (de 1 à 44), exécute le pipeline complet, puis propose une boucle de reconnaissance de mots.

- Entrer `fin` pour terminer la saisie de mots
- Entrer `q` pour quitter le programme

**Exemple de session :**

```
Numéro de l'automate à charger (ou 'q' pour quitter) : 8

Automate n°8
┌──────────┬─────┬─────┐
│ État     │  a  │  b  │
├──────────┼─────┼─────┤
│ ->    0  │  1  │ --  │
│ <-    1  │  0  │ --  │
└──────────┴─────┴─────┘

Déterministe : OUI
Standard     : OUI
Complet      : NON

--- Déterminisation et complétion ---
...

Mot à tester : a
  → OUI, "a" est reconnu par l'automate.
Mot à tester : fin
```

---

## Format des fichiers automates

Les fichiers sont situés dans `automata/` et suivent le format suivant :

```
4          ← nombre de symboles (génère l'alphabet : a, b, c, d)
5          ← nombre d'états (génère les états : 0, 1, 2, 3, 4)
1 0        ← nombre d'états initiaux, puis leurs numéros
1 4        ← nombre d'états terminaux, puis leurs numéros
6          ← nombre de transitions
0 a 1      ← transition : état source  symbole  état destination
0 b 0
1 b 2
2 a 3
3 a 4
3 b 0
```

- L'alphabet est généré automatiquement : `n` symboles → `a, b, c, …`
- Les états sont numérotés de `0` à `n-1`
- Un automate non déterministe peut avoir plusieurs transitions pour la même paire (état, symbole)
- Les epsilon-transitions sont notées avec le symbole `*`

---

## Génération des traces

Le script `run_traces.py` exécute automatiquement le programme sur les 44 automates et sauvegarde chaque sortie dans `traces/trace_X.txt`.

```bash
python run_traces.py
```

Les entrées utilisateur sont simulées :
- Réponse `o` à la proposition de standardisation
- Série de mots prédéfinis : `a`, `b`, `c`, `d`, `aa`, `ab`, `ac`, `ba`, `bb`, `bc`, `cd`, `aaa`, `abc`, `abcd`, mot vide
- `fin` pour clore la reconnaissance, `q` pour quitter

Les fichiers de traces permettent de vérifier le comportement du programme sur l'ensemble du corpus sans interaction manuelle.

---

## Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Lancer un module spécifique
pytest tests/test_determinize.py -v

# Lancer le linter
ruff check .

# Corriger automatiquement les erreurs de style
ruff check --fix .
ruff format .
```

**Couverture des tests :**

| Fichier de test       | Module testé    | Cas couverts                                          |
|-----------------------|-----------------|-------------------------------------------------------|
| `test_models.py`      | `models.py`     | `states_to_label()`, valeurs par défaut               |
| `test_reader.py`      | `reader.py`     | Alphabet, états, transitions, AFN, erreurs fichier    |
| `test_display.py`     | `display.py`    | Affichage sans exception, contenu des cellules        |
| `test_properties.py`  | `properties.py` | AFD/AFN déterministe, standard, complet               |
| `test_standardize.py` | `standardize.py`| Préservation du langage, état initial `i`             |
| `test_determinize.py` | `determinize.py`| Complétion, subset construction, epsilon-AFN          |
| `test_minimize.py`    | `minimize.py`   | Réduction d'états, partitions, état poubelle          |
| `test_recognize.py`   | `recognize.py`  | Mots acceptés/rejetés, cas limites                    |

---

## Répartition du travail

| Membre              | Modules                                     |
|---------------------|---------------------------------------------|
| Eliot Cup.          | `models.py`, `reader.py`, `display.py`, `determinize.py` (co-auteur) |
| Romain              | `properties.py`, `standardize.py`          |
| Edouard             | `determinize.py` (co-auteur)               |
| Eliot Cou.          | `minimize.py`.                             |
| Eliot Mass          | `recognize.py`, `complement.py`, `main.py` |

---

## Conventions de code

- **Python 3.11+** requis
- **Noms de variables et fonctions** en anglais
- **Docstrings et commentaires** en français
- **Style** géré par `ruff` (longueur de ligne max. 88 caractères, imports triés)
- Chaque fonction de transformation retourne un **nouvel `Automaton`** sans modifier l'entrée
- Les transitions sont stockées sous la forme `dict[tuple[str, str], list[str]]` : `{(état, symbole): [destinations]}`
- Les états composés issus de la déterminisation sont nommés avec le séparateur `.` : `"0.1"`, `"0.1.2"`, etc.
- L'état poubelle est toujours nommé `"P"`
