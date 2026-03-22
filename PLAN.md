# Plan d'implémentation — PRJ-Automate

> EFREI P2 2025/2026 — Automates Finis et Expressions Rationnelles
> Deadline rendu Moodle : **29 mars 2026**
> Équipe de 5 membres — Python 3.11+

---

## ⚡ Démarrage rapide

> **À lire en premier après avoir clone le projet.**

### Étape 1 — Installer uv (une seule fois par machine)

**uv** est le gestionnaire de paquets Python utilisé dans ce projet. Il remplace `pip` + `venv` et est beaucoup plus rapide.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Puis redémarrer le terminal (ou exécuter la commande affichée après l'installation)
source $HOME/.local/bin/env
```

> Sur Windows, voir : https://docs.astral.sh/uv/getting-started/installation/

### Étape 2 — Cloner le projet et installer les dépendances

```bash
git clone git@github.com:Tezay/PRJ-Automate.git
cd PRJ-Automate

# Créer l'environnement virtuel Python
uv venv

# Activer l'environnement (à refaire à chaque nouveau terminal)
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Installer toutes les dépendances (rich, pytest, ruff)
uv pip install -e ".[dev]"
```

### Étape 3 — Lancer le programme

```bash
python main.py
```

### Vérifier que tout fonctionne

```bash
pytest tests/ -v          # les tests de models.py doivent passer
ruff check .              # aucune erreur de lint
```

---

## Sommaire

1. [Structure du projet](#1-structure-du-projet)
2. [Configuration de l'environnement](#2-configuration-de-lenvironnement)
3. [Format des fichiers automates](#3-format-des-fichiers-automates)
4. [Architecture : classe Automaton](#4-architecture--classe-automaton)
5. [Modules et responsabilités par membre](#5-modules-et-responsabilités-par-membre)
6. [Boucle principale (main.py)](#6-boucle-principale-mainpy)
7. [Script de génération des traces](#7-script-de-génération-des-traces)
8. [Workflow Git pour l'équipe](#8-workflow-git-pour-léquipe)
9. [Outils de qualité de code](#9-outils-de-qualité-de-code)
10. [Ordre d'implémentation](#10-ordre-dimplémentation)
11. [Vérification end-to-end](#11-vérification-end-to-end)

---

## 1. Structure du projet

```
PRJ-Automate/
├── src/
│   └── automaton/
│       ├── __init__.py
│       ├── models.py        # Classe Automaton (base commune)
│       ├── reader.py        # Lecture fichier .txt
│       ├── display.py       # Affichage tables dans le terminal
│       ├── properties.py    # Tests : déterministe / standard / complet
│       ├── standardize.py   # Standardisation
│       ├── determinize.py   # Déterminisation + complétion
│       ├── minimize.py      # Minimisation (algorithme des partitions)
│       ├── recognize.py     # Reconnaissance de mots
│       └── complement.py    # Automate du langage complémentaire
├── tests/
│   ├── test_models.py
│   ├── test_properties.py
│   ├── test_standardize.py
│   ├── test_determinize.py
│   ├── test_minimize.py
│   └── test_recognize.py
├── automata/                # 1.txt, 2.txt, ... (fournis par les enseignants)
├── traces/                  # Traces d'exécution générées automatiquement
├── main.py                  # Point d'entrée + boucle principale
├── run_traces.py            # Génère toutes les traces d'exécution
├── pyproject.toml           # Configuration du projet Python
└── PLAN.md                  # Ce fichier
```

---

## 2. Configuration de l'environnement

Nous utilisons **uv** (gestionnaire de paquets moderne et rapide) et **pyproject.toml**.

### Installation de uv (une seule fois par machine)

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Mise en place du projet

```bash
# Cloner le repo
git clone git@github.com:Tezay/PRJ-Automate.git
cd PRJ-Automate

# Créer l'environnement virtuel
uv venv

# Activer l'environnement (à faire à chaque nouveau terminal)
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\activate          # Windows

# Installer les dépendances (rich + pytest + ruff)
uv pip install -e ".[dev]"
```

### pyproject.toml

```toml
[project]
name = "prj-automate"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["rich"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## 3. Format des fichiers automates

Les fichiers sont dans `automata/X.txt`. L'utilisateur tape `"8"` pour charger `automata/8.txt`.

```
2          ← nombre de symboles dans l'alphabet (ici 2 → alphabet = {a, b})
5          ← nombre d'états (états numérotés de 0 à 4)
1 0        ← nombre d'états initiaux, suivi de leurs numéros
1 4        ← nombre d'états terminaux, suivi de leurs numéros
6          ← nombre de transitions
0 a 0      ← transition : état 0 --a--> état 0
0 b 0      ← transition : état 0 --b--> état 0
0 a 1
1 b 2
2 a 3
3 a 4
```

---

## 4. Architecture : classe Automaton

La classe `Automaton` est définie **une seule fois** dans `models.py`.
Tous les autres modules l'importent. Chaque fonction de transformation prend un
`Automaton` en entrée et retourne un **nouvel** `Automaton` (pas de modification
en place). Cela rend le code plus sûr et facile à tester.

### Représentation des états : toujours des strings

Pour éviter toute complexité de types Python, **les états sont toujours des chaînes
de caractères (`str`)**, même pour les états simples :

| Situation | Exemple d'état |
|---|---|
| Automate d'origine | `"0"`, `"1"`, `"2"` |
| État composé (après déterminisation) | `"0.1"`, `"1.2.3"`, `"12.3"` |
| État puits (après complétion) | `"P"` |
| État initial (après standardisation) | `"i"` |

Le séparateur `.` permet de distinguer `{1,2,3}` → `"1.2.3"` de `{12,3}` → `"12.3"`.

### Définition de la classe

```python
# src/automaton/models.py

class Automaton:
    def __init__(self):
        self.alphabet: list[str]          # ex: ['a', 'b', 'c']
        self.states: list[str]            # ex: ['0', '1', '2', '3', '4']
        self.initial_states: list[str]    # ex: ['0']
        self.terminal_states: list[str]   # ex: ['3', '4']
        # transitions[(état, symbole)] = liste des états destination
        self.transitions: dict[tuple[str, str], list[str]]
        # ex: {('0', 'a'): ['0', '1'], ('1', 'b'): ['2']}
```

### Règle de nommage des états composés

Lors de la déterminisation, un état est un **ensemble d'états d'origine**.
On le représente en triant les numéros et en les joignant avec `.` :

```python
# États {0, 1} → triés → [0, 1] → "0.1"
# États {12, 3} → triés → [3, 12] → "3.12"
# État singleton {2} → "2"
# Ensemble vide → "P" (état puits)

def states_to_label(states: list[str]) -> str:
    if not states:
        return "P"
    sorted_states = sorted(states, key=lambda s: int(s))
    return ".".join(sorted_states)
```

---

## 5. Modules et responsabilités par membre

### Eliot Cup. — `models.py` + `reader.py` + `display.py`

**Priorité maximale : les autres membres en dépendent.**

**`models.py`** — Classe `Automaton`
- Définit la classe avec ses attributs (voir section 4)
- Méthode `__repr__` ou `__str__` utile pour le débogage

**`reader.py`** — Lecture depuis fichier
```python
def read_automaton(number: int) -> Automaton:
    """Lit automata/{number}.txt et retourne un Automaton."""
```
- Lit le fichier ligne par ligne selon le format décrit en section 3
- Convertit les numéros d'états entiers en strings : `"0"`, `"1"`, etc.
- Génère l'alphabet automatiquement : `n` symboles → `['a', 'b', ..., chr(ord('a')+n-1)]`
- Lève une exception claire si le fichier n'existe pas

**`display.py`** — Affichage dans le terminal avec `rich`
```python
def display_automaton(af: Automaton, title: str = "Automate") -> None:
    """Affiche la table de transitions formatée avec rich."""
```
- Colonne "État" : préfixe `->` si initial, `<-` si terminal (les deux si les deux)
- Cellule `--` si aucune transition pour ce (état, symbole)
- Cellule `"0.1"` si plusieurs destinations (états composés séparés par `.`)
- Colonnes bien alignées quelle que soit la longueur du contenu

Exemple d'affichage attendu :
```
┌──────────┬──────┬──────┬──────┐
│ État     │  a   │  b   │  c   │
├──────────┼──────┼──────┼──────┤
│ -> 0     │ 0.1  │ 0.4  │  0   │
│    1     │  --  │  --  │  2   │
│    2     │  --  │  3   │  --  │
│ <- 3     │  3   │  --  │  --  │
│ <- 4     │  --  │  --  │  2   │
└──────────┴──────┴──────┴──────┘
```

---

### Romain — `properties.py` + `standardize.py`

**`properties.py`** — Tests sur l'automate
```python
def is_deterministic(af: Automaton) -> tuple[bool, list[str]]:
    """Retourne (True/False, liste des raisons si non déterministe).
    Non déterministe si : plusieurs états initiaux OU
    une transition (état, symbole) vers plus d'un état."""

def is_standard(af: Automaton) -> bool:
    """Standard si : un seul état initial ET
    aucune transition ne pointe vers cet état initial."""

def is_complete(af: Automaton) -> tuple[bool, list[str]]:
    """Retourne (True/False, liste des (état, symbole) sans transition).
    À n'appeler que sur un automate déterministe."""
```

**`standardize.py`** — Standardisation
```python
def standardize(af: Automaton) -> Automaton:
    """Crée un nouvel état initial 'i', copie les transitions des anciens
    états initiaux vers 'i'. Retourne un nouvel Automaton standardisé."""
```
- Le nouvel état initial est nommé `"i"`
- Si un ancien état initial était terminal, `"i"` est aussi terminal
- Ne pas modifier l'automate original

---

### Membre 3 — `determinize.py`

```python
def complete(af: Automaton) -> Automaton:
    """Ajoute un état puits 'P' et complète toutes les transitions manquantes.
    À appeler uniquement si l'automate est déjà déterministe mais incomplet."""

def determinize_and_complete(af: Automaton) -> Automaton:
    """Déterminisation par la construction des sous-ensembles (subset construction),
    suivie de la complétion. Retourne l'AFDC.

    Algorithme :
    1. État initial de l'AFDC = label des états initiaux de l'AF (ex: "0.1")
    2. Pour chaque état non traité de l'AFDC, pour chaque symbole :
       a. Calculer l'ensemble des états destination dans l'AF
       b. En faire le label du nouvel état (ex: "1.2.3")
       c. Si pas encore dans l'AFDC, l'ajouter à la file
    3. Si un ensemble est vide → état puits "P"
    4. Un état de l'AFDC est terminal si son label contient un état terminal de l'AF
    """
```

Affichage attendu en plus de la table :
```
Correspondance états AFDC → états AF d'origine :
  "0"    ← {0}
  "0.1"  ← {0, 1}
  "2"    ← {2}
  "P"    ← {} (état puits)
```

---

### Membre 4 — `minimize.py`

```python
def minimize(afdc: Automaton) -> Automaton:
    """Minimise l'AFDC par l'algorithme des partitions (Moore/Myhill).
    Affiche chaque partition numérotée et les transitions en termes de parties.
    Retourne l'AFDCM avec une table de correspondance."""
```

**Algorithme des partitions :**
1. **P0** : partition initiale = `{états terminaux}` + `{états non terminaux}`
2. À chaque itération, raffiner chaque groupe : deux états sont dans le même groupe
   si pour chaque symbole ils vont dans le même groupe de la partition courante
3. Arrêter quand la partition ne change plus
4. Chaque groupe devient un état de l'AFDCM (renommé `0`, `1`, `2`...)

Affichage attendu :
```
Partition P0 : {3, 4} | {0, 1, 2}
Partition P1 : {3, 4} | {2} | {0, 1}
Partition P2 : {3, 4} | {2} | {0} | {1}   ← stable, c'est la finale

Table de correspondance AFDCM → AFDC :
  État 0 ← groupe {0}
  État 1 ← groupe {1}
  État 2 ← groupe {2}
  État 3 ← groupe {3, 4}
```

Si l'automate est déjà minimal : afficher `"L'automate est déjà minimal."`.

---

### Membre 5 — `recognize.py` + `complement.py` + `main.py`

**`recognize.py`** — Reconnaissance de mots
```python
def recognize_word(word: str, afdc: Automaton) -> bool:
    """Simule l'AFDC sur le mot. Retourne True si le mot est reconnu.
    Le mot est lu en entier avant vérification (pas caractère par caractère)."""
```
- Partir de l'état initial unique (l'AFDC en a forcément un)
- Suivre les transitions caractère par caractère
- À la fin du mot : accepté si l'état courant est terminal
- Si un caractère n'est pas dans l'alphabet ou pas de transition : refusé

**`complement.py`** — Langage complémentaire
```python
def complement(a: Automaton) -> Automaton:
    """Retourne un nouvel automate reconnaissant le langage complémentaire.
    Échange les états terminaux et non-terminaux.
    Le paramètre a peut être l'AFDC ou l'AFDCM."""
```

**`main.py`** — Boucle principale (voir section 6)

---

## 6. Boucle principale (main.py)

```
RÉPÉTER indéfiniment :

  1. Demander à l'utilisateur le numéro de l'automate (ou "q" pour quitter)
  2. Lire et afficher l'automate (AF)
  3. Afficher : déterministe ? standard ? complet ?

  4. SI non standard :
       Demander à l'utilisateur s'il veut standardiser
       SI oui → standardiser → mettre à jour AF → afficher l'AF standardisé

  5. Déterminisation / complétion :
       SI déterministe ET complet  → AFDC = AF (pas de traitement)
       SI déterministe ET incomplet → AFDC = complétion(AF)
       SI non déterministe          → AFDC = déterminisation_et_complétion(AF)
       Afficher l'AFDC + la correspondance états

  6. Minimisation :
       AFDCM = minimiser(AFDC)
       Afficher les partitions successives + l'AFDCM + la correspondance états

  7. Reconnaissance de mots :
       TANT QUE l'utilisateur ne tape pas "fin" :
         Lire un mot
         Afficher "OUI" ou "NON"

  8. Automate complémentaire :
       AComp = complémentaire(AFDC ou AFDCM — indiquer lequel)
       Afficher AComp

  9. Proposer de traiter un autre automate ou quitter
```

---

## 7. Script de génération des traces

`run_traces.py` doit :
1. Lister tous les fichiers dans `automata/` (1.txt à 44.txt)
2. Pour chaque automate, simuler les entrées utilisateur via `subprocess` ou `io.StringIO`
3. Capturer la sortie et l'écrire dans `traces/trace_X.txt`

Les réponses automatiques simulées :
- Standardisation : `"o"` (oui, si proposé)
- Mots à tester : une liste de mots prédéfinis puis `"fin"`
- Continuer : `"n"` (non, pour passer au suivant)

---

## 8. Workflow Git pour l'équipe

### Branches par membre

```
main                             ← branche principale (toujours stable)
 ├── feat/models-reader-display  ← Eliot Cup.
 ├── feat/properties-standardize ← Romain
 ├── feat/determinize            ← Membre 3
 ├── feat/minimize               ← Membre 4
 └── feat/recognize-complement-main ← Membre 5
```

### Commandes Git essentielles

**Mise en place (une seule fois) :**
```bash
git clone git@github.com:Tezay/PRJ-Automate.git
cd PRJ-Automate
```

**Créer sa branche de travail :**
```bash
git checkout -b feat/minimize    # remplacer "minimize" par votre partie
```

**Cycle de travail quotidien :**
```bash
# Voir l'état de ses fichiers
git status

# Ajouter les fichiers modifiés au prochain commit
git add src/automaton/minimize.py tests/test_minimize.py

# Créer un commit avec un message clair
git commit -m "feat(minimize): implement Moore partition algorithm"

# Envoyer sa branche sur GitHub (première fois)
git push -u origin feat/minimize

# Envoyer les commits suivants
git push
```

**Mettre à jour sa branche avec les dernières modifs de main :**
```bash
git pull origin main
```

**Convention de messages de commit :**
```
feat(module): description courte     ← nouvelle fonctionnalité
fix(module): description courte      ← correction de bug
test(module): description courte     ← ajout de tests
refactor(module): description courte ← refactorisation
```

### Ouvrir une Pull Request (PR)

1. Sur [github.com/Tezay/PRJ-Automate](https://github.com/Tezay/PRJ-Automate)
2. Onglet **"Pull requests"** → **"New pull request"**
3. Choisir sa branche comme source, `main` comme destination
4. Ajouter un titre et description, cliquer **"Create pull request"**
5. Un autre membre de l'équipe relit et approuve avant le merge

---

## 9. Outils de qualité de code

### ruff — linter et formatter

**À quoi ça sert :**
- **Linter** : analyse le code et signale les problèmes (variables inutilisées,
  imports mal ordonnés, code mort, mauvaises pratiques, etc.)
- **Formatter** : formate automatiquement le style du code (indentation, espaces,
  guillemets, longueur de lignes) — comme un "correcteur orthographique" pour le style

**Comment l'utiliser (depuis la racine du projet) :**
```bash
ruff check .            # affiche les problèmes détectés
ruff check --fix .      # corrige automatiquement les problèmes simples
ruff format .           # formate tout le code automatiquement
```

**Règle d'équipe : lancer `ruff format .` et `ruff check .` avant chaque commit.**

### pytest — tests unitaires

```bash
pytest tests/                      # lance tous les tests
pytest tests/test_minimize.py      # lance un fichier de test spécifique
pytest -v tests/                   # mode verbose (détails)
```

Chaque membre écrit les tests de son propre module dans `tests/test_<module>.py`.

---

## 10. Ordre d'implémentation

```
Semaine 1 :
  → Eliot Cup. : models.py + reader.py (URGENT — bloquant pour tout le monde)
              Puis display.py

  → Membres 2, 3, 4, 5 : peuvent commencer dès que models.py est mergé sur main

Semaine 2 :
  → Romain : properties.py + standardize.py
  → Membre 3 : determinize.py
  → Membre 4 : minimize.py
  → Membre 5 : recognize.py + complement.py

Fin de semaine 2 :
  → Membre 5 : main.py (intégration de tous les modules)
  → Tous : run_traces.py + génération des traces d'exécution
  → Tous : relecture croisée du code, corrections finales
```

---

## 11. Vérification end-to-end

```bash
# 1. Installer l'environnement
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# 2. Vérifier la qualité du code
ruff check .
ruff format --check .

# 3. Lancer les tests
pytest tests/ -v

# 4. Lancer le programme manuellement
python main.py
# → taper "1" pour charger automata/1.txt
# → vérifier l'affichage, les propriétés, la déterminisation, etc.

# 5. Générer toutes les traces
python run_traces.py
# → vérifier que traces/ contient trace_1.txt à trace_44.txt
```
