"""
Module determinize.py — Déterminisation et complétion d'un automate

Responsable : Edouard

Ce module fournit deux fonctions :
    - complete()                   : pour un DFA incomplet → DFA complet
    - determinize_and_complete()   : pour un NFA → DFA complet (subset construction)

Algorithme de complétion (complete) :
    1. Ajouter un état poubelle "P".
    2. Pour chaque (état, symbole) sans transition, ajouter une transition vers "P".
    3. Pour l'état "P" lui-même, ajouter une transition vers "P" pour chaque symbole.

Algorithme de déterminisation (determinize_and_complete) :
    Utilise la "construction des sous-ensembles" (subset construction) :
    1. L'état initial de l'AFDC est le label des états initiaux de l'AF
       (ex: si initiaux = ['0', '1'] → état initial = "0.1").
    2. Utiliser une file (queue) d'états à traiter.
    3. Pour chaque état non traité et chaque symbole :
       a. Calculer l'union des transitions depuis tous les états du groupe.
       b. Créer le label de l'état résultant avec states_to_label().
       c. Si ce label n'est pas encore un état de l'AFDC, l'ajouter à la file.
    4. Un état de l'AFDC est terminal si son groupe contient au moins un état
       terminal de l'AF original.
    5. Si l'union est vide → état poubelle "P".

Affichage attendu (en plus de la table) :
    Correspondance états AFDC → états AF d'origine :
      "0"    ← {0}
      "0.1"  ← {0, 1}
      "P"    ← {} (état poubelle)
"""

from automaton.models import Automaton, states_to_label

def is_determinize(af: Automaton) -> bool:
    """Vérifie si un automate est déjà déterministe.

    Un automate est déterministe si pour chaque état et chaque symbole,
    il existe au plus une transition sortante.

    Args:
        af: L'automate à vérifier.

    Returns:
        True si l'automate est déterministe, False sinon.
    """
    if len(af.initial_states) > 1 or len(af.initial_states) == 0:
        print("L'automate n'est pas déterministe : plusieurs états initiaux")
        return False
    for transition in af.transitions:
        nb_transitions = len(af.transitions[transition])
        if nb_transitions > 1:
            print(f"L'automate n'est pas déterministe : plusieurs transitions pour {transition}")
            return False
    return True    

def is_complete(af: Automaton) -> bool:
    """Vérifie si un automate est complet.

    Un automate est complet si pour chaque état et chaque symbole,
    il existe au moins une transition sortante.

    Args:
        af: L'automate à vérifier.

    Returns:
        True si l'automate est complet, False sinon.
    """
    for state in af.states:
        for symbol in af.alphabet:
            if (state, symbol) not in af.transitions:
                print(f"L'automate n'est pas complet : pas de transition pour ({state}, {symbol})")
                return False
    return True

def complete(af: Automaton) -> Automaton:
    """Complète un automate déterministe en ajoutant un état poubelle "P".

    À n'appeler que sur un automate déjà déterministe mais incomplet.

    Args:
        af: L'automate déterministe incomplet.

    Returns:
        Un nouvel Automaton déterministe et complet.
    """
    af.states.append("P")
    for state in af.states:
        for symbol in af.alphabet:
            if (state, symbol) not in af.transitions:
                af.transitions[(state, symbol)] = ["P"]
    
    for state in af.states:
        if state != "P":
            for symbol in af.alphabet:
                if (state, symbol) not in af.transitions:
                    af.transitions[(state, symbol)] = ["P"]
    return af

def determinize(af: Automaton) -> Automaton:
    """Déterminise un automate non déterministe en utilisant la construction des sous-ensembles.

    Args:
        af: L'automate non déterministe à déterminiser."""
    
    init_list = sorted(list(set(af.initial_states))) 
    init_label = states_to_label(init_list) 
    queue = [init_list] 
    af.states = [init_label]
    af.initial_states = [init_label]
    old_transitions = af.transitions.copy()
    af.transitions = {}

    while queue:
        groupe_courant_list = queue.pop(0)
        groupe_courant_label = states_to_label(groupe_courant_list)
        for symbole in af.alphabet:
            destinations_possibles = set()
            for etat in groupe_courant_list:
                cle = (etat, symbole)
                if cle in af.transitions:
                    for dest in af.transitions[cle]:
                        destinations_possibles.add(dest)            
            if len(destinations_possibles) != 0:
                dest_list = sorted(list(destinations_possibles))
                new_state_label = states_to_label(dest_list)
                
                if new_state_label not in af.states:
                    af.states.append(new_state_label)
                    queue.append(dest_list)
                
                af.transitions[(groupe_courant_label, symbole)] = [new_state_label]
    return af


def determinize_and_complete(af: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    if is_determinize(af):
        if is_complete(af):
            return af,{state: [state] for state in af.states}
        else:
            return complete(af),{state: [state] for state in af.states}
    else:
        return complete(determinize(af)),{state: [state] for state in af.states}
