"""
Module reader.py — Lecture d'automates depuis des fichiers .txt

Responsable : Eliot Cup.

Format attendu du fichier automata/X.txt :
    Ligne 1 : nombre de symboles dans l'alphabet
    Ligne 2 : nombre d'états (numérotés de 0 à N-1)
    Ligne 3 : nombre d'états initiaux, suivi de leurs numéros (séparés par des espaces)
    Ligne 4 : nombre d'états terminaux, suivi de leurs numéros (séparés par des espaces)
    Ligne 5 : nombre de transitions
    Lignes suivantes : transitions sous la forme "état_départ symbole état_arrivée"

Exemple (automata/5.txt) :
    1
    2
    1 1
    1 0
    2
    1 a 0
    0 a 0
"""

import os

from automaton.models import Automaton

# Dossier contenant les fichiers automates, relatif à la racine du projet
AUTOMATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "automata")


def read_automaton(number: int) -> Automaton:
    """Lit le fichier automata/{number}.txt et retourne un Automaton.

    Args:
        number: Le numéro de l'automate à charger (ex: 8 pour automata/8.txt).

    Returns:
        Un objet Automaton rempli avec les données du fichier.

    Raises:
        FileNotFoundError: Si le fichier automata/{number}.txt n'existe pas.
        ValueError: Si le format du fichier est invalide.
    """
    raise NotImplementedError("TODO (Eliot Cup.) : Implémenter read_automaton()")
