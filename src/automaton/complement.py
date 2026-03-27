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
    raise NotImplementedError("TODO (Membre 5) : Implémenter complement()")
