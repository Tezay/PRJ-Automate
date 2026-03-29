"""
Module properties.py — Vérification des propriétés d'un automate

Responsable : Romain

Ce module regroupe les trois tests demandés par le sujet :
    - Déterministe ?
    - Standard ?
    - Complet ?

Chaque fonction retourne l'information pour que main.py puisse
prendre des décisions basées sur ces résultats.
"""

from .models import Automaton


def is_deterministic(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate est déterministe et retourne les raisons si non.

    Example:
        >>> is_deterministic(af)
        >>> False, "L'état 0 avec le symbole 'a' a plusieurs transitions : ['0', '1']"
    """
    message = []
    deterministe = True

    # Un seul état initial autorisé
    if len(af.initial_states) != 1:
        deterministe = False
        message.append(f"Nombre d'état initiaux incorrect, {len(af.initial_states)} au lieu de 1.")

    # Au plus une transition par paire (état, symbole)
    for (etat, symbole), destinations in af.transitions.items():
        if len(destinations) > 1:
            message.append(f"Non déterministe, l'état {etat} possède plusieurs transitions : {destinations}, avec le symbole {symbole}.")
            deterministe = False

    # Pas de transitions epsilon
    for (etat, symbole) in af.transitions.keys():
        if symbole == "":
            deterministe = False
            message.append(f"Non déterministe, présence symbole vide dans automate depuis etat {etat}.")
        if symbole == "*":
            deterministe = False
            message.append(f"Non déterministe, présence de epsilon dans automate depuis etat {etat}.")

    return deterministe, message


def is_standard(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate est standard.

    Un automate est standard si :
        1. Il possède exactement un seul état initial.
        2. Aucune transition ne pointe vers cet état initial.

    Returns:
        Un tuple (résultat, raisons) où :
            - résultat (bool) : True si l'automate est standard, False sinon.
            - raisons (list[str]) : liste des raisons si non standard.
    """
    message = []

    # Un seul état initial requis
    if len(af.initial_states) != 1:
        message.append(f"Nombre d'états initiaux incorrect : {len(af.initial_states)} au lieu de 1.")
        return False, message

    initial_state = af.initial_states[0]

    # Aucune transition ne doit pointer vers l'état initial
    for (etat, symbole), destinations in af.transitions.items():
        if initial_state in destinations:
            message.append(
                f"La transition depuis l'état {etat} avec le symbole '{symbole}' "
                f"pointe vers l'état initial {initial_state}."
            )
            return False, message

    return True, message


def is_complete(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate déterministe est complet.

    Un automate est complet si pour chaque état et chaque symbole de l'alphabet,
    il existe au moins une transition définie.

    Returns:
        Un tuple (résultat, raisons) où :
            - résultat (bool) : True si complet, False sinon.
            - raisons (list[str]) : liste des paires (état, symbole) sans transition.

    Example:
        >>> is_complete(af)
        >>> False, ["Pas de transition depuis l'état '1' avec le symbole 'b'"]
    """
    message = []
    complet = True

    for etat in af.states:
        for symbole in af.alphabet:
            if (etat, symbole) not in af.transitions:
                message.append(f"Pas de transition depuis l'état '{etat}' avec le symbole '{symbole}'.")
                complet = False

    return complet, message
