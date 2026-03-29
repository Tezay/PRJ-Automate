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

def e_fermeture(states: list[str], af: Automaton) -> list[str]:
    """
    Calcule l'ensemble des états accessibles via des epsilon-transitions.
    On considère que le symbole epsilon est représenté par *.
    """
    closure = set(states)
    stack = list(states)
    
    while stack:
        current = stack.pop()
        cle = (current, "*")
        if cle in af.transitions:
            for next_state in af.transitions[cle]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return sorted(list(closure))

def determinize(af: Automaton) -> Automaton:
    """Déterminise un automate non déterministe en utilisant la construction des sous-ensembles.

    Args:
        af: L'automate non déterministe à déterminiser."""
    
    initial_closure = e_fermeture(af.initial_states, af)
    init_label = states_to_label(initial_closure)
    
    afd_states = [init_label]
    afd_transitions = {}
    queue = [initial_closure]
    visited = {init_label}

    while queue:
        current_group = queue.pop(0)
        current_label = states_to_label(current_group)
        
        #On ne boucle que sur les vrais symboles (pas epsilon)
        alphabet_sans_epsilon = [s for s in af.alphabet if s not in ["", "ε"]]
        
        for symbole in alphabet_sans_epsilon:
            destinations = set()
            for etat in current_group:
                cle = (etat, symbole)
                if cle in af.transitions:
                    for d in af.transitions[cle]:
                        destinations.add(d)
            
            if destinations:
                #On calcule la fermeture des destinations trouvées
                dest_with_epsilon = e_fermeture(list(destinations), af)
                new_label = states_to_label(dest_with_epsilon)
                
                afd_transitions[(current_label, symbole)] = [new_label]
                
                if new_label not in visited:
                    visited.add(new_label)
                    afd_states.append(new_label)
                    queue.append(dest_with_epsilon)

    new_terminals = []
    for label in afd_states:
        components = label.split('.')
        if any(c in af.terminal_states for c in components):
            new_terminals.append(label)

    af.states = afd_states
    af.initial_states = [init_label]
    af.terminal_states = new_terminals
    af.transitions = afd_transitions
    # On nettoie l'alphabet pour enlever epsilon de l'AFD final
    af.alphabet = [s for s in af.alphabet if s != "*"]    
    return af


def determinize_and_complete(af: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    if is_determinize(af):
        if is_complete(af):
            return af,{state: [state] for state in af.states}
        else:
            return complete(af),{state: [state] for state in af.states}
    else:
        return complete(determinize(af)),{state: [state] for state in af.states}
