"""
Module complement.py — Automate du langage complémentaire

Responsable : Eliot Mass

Construction de l'automate complémentaire :
    Un automate reconnaissant le langage complémentaire L' s'obtient simplement
    en échangeant les états terminaux et les états non terminaux d'un AFDC.

    Autrement dit : un état devient terminal dans AComp s'il ne l'était PAS dans A,
    et inversement.

    ATTENTION : Cette opération n'est valide que sur un automate déterministe
    et complet (AFDC ou AFDCM). Elle ne fonctionnerait pas sur un AFN.

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
    comp_ok, _ = is_complete(a)
    det_ok, _ = is_deterministic(a)
    if not comp_ok or not det_ok:
        print("Il faut que l'automate soit complet et déterministe.")
        return a

    acomp = Automaton()

    acomp.alphabet = a.alphabet[:]
    acomp.states = a.states[:]
    acomp.initial_states = a.initial_states[:]
    acomp.transitions = a.transitions.copy()

    # Inversion des états terminaux : terminal dans acomp <-> non-terminal dans a
    acomp.terminal_states = [s for s in a.states if s not in a.terminal_states]

    # L'AFDC conserve l'état "P" et l'AFDCM renomme tous ses états en entiers
    type_source = "AFDC" if "P" in a.states else "AFDCM"
    print(f"Construction de l'automate complémentaire à partir d'un {type_source}.")

    return acomp
