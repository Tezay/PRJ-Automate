"""
Module properties.py — Vérification des propriétés d'un automate

Responsable : Romain

Ce module regroupe les trois tests demandés par le sujet :
    - Déterministe ?
    - Standard ?
    - Complet ?

Chaque fonction affiche le résultat du test et retourne l'information
pour que main.py puisse prendre des décisions basées sur ces résultats.
"""

from automaton.models import Automaton


def is_deterministic(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate est déterministe et retourne les raisons si non.

    Un automate est déterministe si :
        1. Il possède exactement un seul état initial.
        2. Pour chaque paire (état, symbole), il existe au plus une transition.

    Args:
        af: L'automate à tester.

    Returns:
        Un tuple (résultat, raisons) où :
            - résultat (bool) : True si déterministe, False sinon.
            - raisons (list[str]) : liste de messages expliquant pourquoi
              l'automate n'est pas déterministe (vide si déterministe).

    Example:
        >>> ok, raisons = is_deterministic(af)
        >>> if not ok:
        ...     for r in raisons:
        ...         print(r)
        "L'état 0 avec le symbole 'a' a plusieurs transitions : ['0', '1']"
    """
    raise NotImplementedError("TODO (Romain) : Implémenter is_deterministic()")


def is_standard(af: Automaton) -> bool:
    """Vérifie si l'automate est standard.

    Un automate est standard si :
        1. Il possède exactement un seul état initial.
        2. Aucune transition ne pointe vers cet état initial.

    Args:
        af: L'automate à tester.

    Returns:
        True si l'automate est standard, False sinon.
    """
    raise NotImplementedError("TODO (Romain) : Implémenter is_standard()")


def is_complete(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate déterministe est complet.

    Un automate est complet si pour chaque état et chaque symbole de l'alphabet,
    il existe au moins une transition définie.

    ATTENTION : Cette fonction ne doit être appelée que sur un automate
    déterministe. Pour un NFA, le résultat n'aurait pas de sens.

    Args:
        af: L'automate déterministe à tester.

    Returns:
        Un tuple (résultat, raisons) où :
            - résultat (bool) : True si complet, False sinon.
            - raisons (list[str]) : liste des paires (état, symbole) sans transition.

    Example:
        >>> ok, raisons = is_complete(af)
        >>> if not ok:
        ...     for r in raisons:
        ...         print(r)
        "Pas de transition depuis l'état '1' avec le symbole 'b'"
    """
    raise NotImplementedError("TODO (Romain) : Implémenter is_complete()")
