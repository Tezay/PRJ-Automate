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

Exemple (automata/7.txt) :
    1
    2
    1 1
    1 0
    2
    1 a 1
    1 a 0
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
    path = os.path.normpath(os.path.join(AUTOMATA_DIR, f"{number}.txt"))

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Le fichier automata/{number}.txt n'existe pas."
        )

    with open(path, encoding="utf-8") as f:
        lines = []
        for line in f:
            cleaned_line = line.strip()
            if cleaned_line != "":
                lines.append(cleaned_line)

    try:
        idx = 0
        af = Automaton()

        # Ligne 1 : nombre de symboles -> génération de l'alphabet
        n_symbols = int(lines[idx])
        idx += 1
        af.alphabet = [chr(ord("a") + i) for i in range(n_symbols)]

        # Ligne 2 : nombre d'états -> numérotés de 0 à n-1
        n_states = int(lines[idx])
        idx += 1
        af.states = [str(i) for i in range(n_states)]

        # Ligne 3 : états initiaux
        parts = lines[idx].split()
        idx += 1
        n_init = int(parts[0])
        af.initial_states = [parts[i] for i in range(1, n_init + 1)]

        # Ligne 4 : états terminaux
        parts = lines[idx].split()
        idx += 1
        n_term = int(parts[0])
        af.terminal_states = [parts[i] for i in range(1, n_term + 1)]

        # Ligne 5 : nombre de transitions
        n_trans = int(lines[idx])
        idx += 1

        # Lignes suivantes : transitions "état_départ symbole état_arrivée"
        for _ in range(n_trans):
            parts = lines[idx].split()
            idx += 1
            from_state, symbol, to_state = parts[0], parts[1], parts[2]
            key = (from_state, symbol)
            if key not in af.transitions:
                af.transitions[key] = []
            af.transitions[key].append(to_state)

    except (IndexError, ValueError) as e:
        raise ValueError(
            f"Format invalide dans automata/{number}.txt : {e}"
        ) from e

    return af
