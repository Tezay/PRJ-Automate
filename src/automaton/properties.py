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

from .models import Automaton


def is_deterministic(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate est déterministe et retourne les raisons si non.

    Example:
        >>> is_deterministic(af)
        >>> False, "L'état 0 avec le symbole 'a' a plusieurs transitions : ['0', '1']"
    """

    #liste message pour contenir les différents problèmes de automate
    message = []
    #bool pour savoir si déterministe
    deterministe = True

    #Arguments de vérification 
    #vérification que automate possède seulement un etat initial sinon on renvoie FALSE
    if len(af.initial_states) != 1 :
        deterministe = False
        message.append(f"Nombre d'état initiaux incorrect, {len(af.initial_states)} au lieu de 1.")
    
    #vérification que pour chaque paire (état, symbole), il existe au plus une transition sinon on renvoie FALSE
    for (etat, symbole), destinations in af.transitions.items() :
        if len(destinations) > 1 :
            message.append(f"Non déterministe, l'état {etat} possède plusieurs transitions : {destinations}, avec le symbole {symbole}.")
            deterministe = False
    
    #vérification que le symbole espilon n'apparaisse pas dans automate sinon on revoie FALSE
    for (etat, symbole) in af.transitions.keys() :
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
    Returns:
        True si l'automate est standard, False sinon.
    """
    #Véfication que automate possède seulement un etat initial sinon on renvoie FALSE
    if len(af.initial_states) != 1:
        return False
    
    #Vérification que aucune transition ne pointe vers l'état initial

    #On récupère l'état initial
    initial_state = af.initial_states[0]

    #On vérifie que aucune transition ne pointe vers l'état initial
    for (etat, symbole), destinations in af.transitions.items():
        if initial_state in destinations:
            print(f"Non standard, la transition depuis l'état {etat} avec le symbole {symbole} pointe vers l'état initial {initial_state}.")
            return False
    
    #Si les deux conditions sont satisfaites, l'automate est standard
    return True
    

def is_complete(af: Automaton) -> tuple[bool, list[str]]:
    """Vérifie si l'automate déterministe est complet.

    Un automate est complet si pour chaque état et chaque symbole de l'alphabet,
    il existe au moins une transition définie.

    ATTENTION : Cette fonction renvoie FALSE si l'automate n'est pas déterministe,
    car un automate non déterministe ne peut pas être complet.

    Returns:
        Un tuple (résultat, raisons) où :
            - résultat (bool) : True si complet, False sinon.
            - raisons (list[str]) : liste des paires (état, symbole) sans transition.

    Example:
        >>> is_complete(af)
        >>> False, ["Pas de transition depuis l'état '1' avec le symbole 'b'"]
    """

    #Vérification que l'automate est déterministe
    if not is_deterministic(af):
        return False, ["L'automate n'est pas déterministe, par conséquent on ne peut pas le compléter;"]
    
    #Création de la liste "message" pour stocker les raisons pour lesquelles l'automate n'est pas complet.
    message = []
    #Création d'un bool "complet", initialisé à True, pour savoir si l'automate est complet ou non.
    complet = True

    #Vérification que pour chaque état et chaque symbole de l'alphabet, il existe au moins une transition définie
    #On parcourt tous les états présent dans l'automate
    for etat in af.states:
        #On parcourt tous les symboles de l'alphabet
        for symbole in af.alphabet:
            #On vérifie si la paire (état, symbole) existe dans les transitions de l'automate
            if (etat, symbole) not in af.transitions:
                message.append(f"Pas de transition depuis l'état '{etat}' avec le symbole '{symbole}'.")
                complet = False
    
    return complet, message