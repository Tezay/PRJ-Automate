"""
Module standardize.py — Standardisation d'un automate

Responsable : Romain

Algorithme de standardisation :
    1. Créer un nouvel état initial nommé "i".
    2. Pour chaque ancien état initial, copier toutes ses transitions sortantes
       vers le nouvel état "i" (même symbole, même destination).
    3. Si au moins un ancien état initial était terminal, "i" est aussi terminal.
    4. Retirer les anciens états initiaux de la liste des états initiaux.
    5. Le nouvel état "i" est le seul état initial.

Note :
    - L'automate original n'est PAS modifié. On retourne un nouvel Automaton.
    - On ne doit appeler cette fonction que si l'automate n'est pas standard.
"""

from .models import Automaton
from .properties import is_standard


def standardize(af: Automaton) -> Automaton:
    """Standardise un automate en créant un unique état initial "i".

    Args:
        af: L'automate non standard à standardiser.

    Returns:
        Un nouvel Automaton standardisé (l'original n'est pas modifié).
    """

    #création de la copie de l'automate pour ne pas modifier l'original*
    af_copy = Automaton()
    af_copy.alphabet = af.alphabet.copy()
    af_copy.states = af.states.copy()
    af_copy.initial_states = af.initial_states.copy()
    af_copy.terminal_states = af.terminal_states.copy()
    af_copy.transitions = af.transitions.copy()

    if is_standard(af):
        print("L'automate est déjà standard, aucun changement effectué.")
        return af
    
    else:
        af_copy.states.append("i")

        for etat_initial in af.initial_states:
            for (etat,symbole), destinations in af.transitions.items():
                if etat == etat_initial:
                    key = ("i", symbole)
                    if key not in af_copy.transitions:
                        af_copy.transitions[key] = []
                        
                    af_copy.transitions[key] += destinations

            if etat_initial in af.terminal_states and "i" not in af_copy.terminal_states:
                    af_copy.terminal_states.append("i")

        af_copy.initial_states = ["i"]
        
    return af_copy