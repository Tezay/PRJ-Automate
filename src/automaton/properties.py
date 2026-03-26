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

"""
Pour ces fonctions on corrige les automates suivants : 
    - 5 (pour les transitions multiples)
    - 20 (pour multiples entrées)
    - 22 (à vérifier les conditions à la main)
    - 26 (à vérifier les conditions à la main)
    - 35 (pour les epsilons)
    - 36 (non standard)
    - 41 (standard)
"""

from automaton.models import Automaton


def is_deterministic(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate est déterministe et retourne les raisons si non.

    Example:
        >>> ok, raisons = is_deterministic(af)
        >>> if not ok:
        ...     for r in raisons:
        ...         print(r)
        "L'état 0 avec le symbole 'a' a plusieurs transitions : ['0', '1']"
    """

    #liste message pour contenir les différents problèmes de automate
    message = []
    #bool pour savoir si déterministe
    deterministe = True

    #Arguments de vérification 
    #vérification que automate possède seulement un etat initial sinon on renvoie FALSE
    if len(Automaton.initial_states) != 1 :
        deterministe = False
        message.append(f"Nombre d'état initiaux incorrect, {len(Automaton.initial_states)} au lieu de 1.")
    
    #vérification que pour chaque paire (état, symbole), il existe au plus une transition sinon on renvoie FALSE
    for (etat, symbole), destinations in Automaton.transitions.items() :
        if len(destinations) > 1 :
            message.append(f"Non déterministe, l'état {etat} possède plusieurs transitions : {destinations}, avec le symbole {symbole}.")
            deterministe = False
    
    #vérification que le symbole espilon n'apparaisse pas dans automate sinon on revoie FALSE
    for (etat, symbole) in Automaton.transitions.keys() :
        if symbole == "" :
            deterministe = False
            message.append(f"Non déterministe, présence symbole vide dans automate depuis etat {etat}.")
        if symbole == "*" :
            deterministe = False
            message.append(f"Non déterministe, présence de epsilon dans automate depuis etat {etat}.")

    return deterministe, message
        


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
