"""
Module complement.py — Automate du langage complémentaire

Responsable : Eliot Mass

Construction de l'automate complémentaire :
    Un automate reconnaissant le langage complémentaire L' s'obtient simplement
    en échangeant les états terminaux et les états non terminaux d'un AFDC.

    Autrement dit : un état devient terminal dans AComp s'il ne l'était PAS dans A,
    et inversement.

    ATTENTION : Cette opération n'est valide que sur un automate déterministe
    et complet (AFDC ou AFDCM). Elle ne fonctionnerait pas sur un NFA.

Le programme doit indiquer à partir de quel automate (AFDC ou AFDCM) le
complémentaire a été construit.
"""

from automaton.models import Automaton
from automaton.properties import is_complete, is_deterministic


def complement(a: Automaton) -> Automaton:
    """Construit l'automate reconnaissant le langage complémentaire.

    Échange les états terminaux et non terminaux de l'automate.
    La structure (états, alphabet, transitions, état initial) est conservée.

    Args:
        a: L'automate déterministe et complet (AFDC ou AFDCM).

    Returns:
        Un nouvel Automaton reconnaissant le langage complémentaire.
        L'automate original n'est pas modifié.
    """
    if not is_complete(a) or not is_deterministic(a):
        print("Il faut que l'automate soit complet")
        return
    # 1. Création d'une nouvelle instance (non-mutabilité)
    acomp = Automaton()
    
    # 2. Copie de la structure existante
    acomp.alphabet = a.alphabet[:]
    acomp.states = a.states[:]
    acomp.initial_states = a.initial_states[:]
    acomp.transitions = a.transitions.copy()
    
    # 3. Inversion des états terminaux
    # Un état devient terminal dans AComp s'il ne l'était PAS dans A, et inversement.
    acomp.terminal_states = [s for s in a.states if s not in a.terminal_states]
    
    # 4. Identification et affichage du type d'automate source
    # Si l'état puits "P" est présent, on considère que c'est un AFDCM (Minimal)
    # Sinon, c'est un AFDC (Complet standard)
    type_source = "AFDCM" if "P" in a.states else "AFDC"
    print(f"Construction de l'automate complémentaire à partir d'un {type_source}.")
    
    return acomp
