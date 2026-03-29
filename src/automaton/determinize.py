"""
Module determinize.py — Déterminisation et complétion d'un automate

Responsable : Edouard & Eliot Cup.

Ce module fournit deux fonctions publiques :
    - complete()                   : AFD incomplet -> AFD complet (ajout état poubelle)
    - determinize_and_complete()   : AFN (ou epsilon-AFN) -> AFDC (subset construction)

Algorithme de complétion (complete) :
    1. Copier l'automate sans le modifier (pas de mutation).
    2. Ajouter un état poubelle "P" si absent.
    3. Pour chaque (état, symbole) sans transition, ajouter une transition vers "P".

Algorithme de déterminisation (_determinize) :
    Utilise la "construction des sous-ensembles" (subset construction) :
    1. Calculer l'epsilon-fermeture des états initiaux -> état initial de l'AFDC.
    2. Utiliser une file (queue) d'états composés à traiter.
    3. Pour chaque état composé et chaque symbole (hors epsilon) :
       a. Calculer l'union des transitions depuis tous les états du groupe.
       b. Calculer l'epsilon-fermeture de l'union.
       c. Créer le label de l'état résultant avec states_to_label().
       d. Si ce label n'est pas encore un état de l'AFDC, l'ajouter à la file.
    4. Un état de l'AFDC est terminal si son groupe contient au moins un état
       terminal de l'AF original.
    5. Le symbole epsilon ("*") est retiré de l'alphabet de l'AFDC résultant.

Correspondance retournée :
    {label_afdc: [liste des états AF d'origine]}
    Exemple : {"0.1": ["0", "1"], "P": []}
"""

from rich.console import Console
from rich.table import Table

from .models import Automaton, states_to_label
from .properties import is_complete, is_deterministic

_console = Console()


def display_correspondence_afdc(
    afdc_states: list[str],
    correspondence: dict[str, list[str]],
) -> None:
    """Affiche la table de correspondance AFDC -> AF d'origine avec rich.

    Chaque ligne associe un état de l'AFDC aux états AF d'origine qu'il regroupe.

    Args:
        afdc_states: Liste ordonnée des états de l'AFDC (pour l'ordre d'affichage).
        correspondence: Mapping état AFDC -> liste des états AF d'origine.
    """
    table = Table(
        title="Correspondance AFDC -> AF d'origine",
        show_header=True,
        header_style="bold",
    )
    table.add_column("État AFDC", justify="center")
    table.add_column("États AF d'origine", justify="center")

    for state in afdc_states:
        origins = correspondence.get(state, [])
        cell = "{" + ", ".join(origins) + "}" if origins else "∅ (état poubelle)"
        table.add_row(state, cell)

    _console.print(table)


def epsilon_closure(states: set[str], transitions: dict) -> set[str]:
    """Calcule l'epsilon-fermeture d'un ensemble d'états.

    Retourne tous les états atteignables depuis `states` via des transitions
    epsilon ("*"), y compris les états de départ eux-mêmes.

    Args:
        states: Ensemble des états de départ.
        transitions: Dictionnaire de transitions de l'automate original.

    Returns:
        L'epsilon-fermeture sous forme d'ensemble de labels d'états.
    """
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for dest in transitions.get((state, "*"), []):
            if dest not in closure:
                closure.add(dest)
                stack.append(dest)
    return closure


def complete(af: Automaton) -> Automaton:
    """Complète un automate déterministe en ajoutant un état poubelle "P".

    Ne modifie PAS l'automate d'entrée (pas de mutation).

    Args:
        af: Un automate déterministe, possiblement incomplet.

    Returns:
        Un nouvel Automaton avec toutes les transitions (état, symbole) définies.
        L'état poubelle "P" est ajouté si au moins une transition était manquante.
    """
    new_af = Automaton()
    new_af.alphabet = list(af.alphabet)
    new_af.states = list(af.states)
    new_af.initial_states = list(af.initial_states)
    new_af.terminal_states = list(af.terminal_states)
    new_af.transitions = dict(af.transitions)

    # Ajout de l'état poubelle si absent
    if "P" not in new_af.states:
        new_af.states.append("P")

    # Remplissage des transitions manquantes vers l'état poubelle
    for state in new_af.states:
        for symbol in new_af.alphabet:
            if (state, symbol) not in new_af.transitions:
                new_af.transitions[(state, symbol)] = ["P"]

    return new_af


def _determinize(af: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    """Convertit un AFN (ou epsilon-AFN) en AFD par construction des sous-ensembles.

    Fonction interne - utiliser determinize_and_complete() en point d'entrée.

    Args:
        af: L'automate non déterministe à déterminiser.

    Returns:
        Un tuple (afd, correspondance) où :
        - afd est l'automate déterministe résultant (peut encore être incomplet).
        - correspondance associe chaque label du AFD à ses états d'origine dans l'AF.
    """
    # Sauvegarde des transitions originales
    old_transitions = dict(af.transitions)
    original_terminals = set(af.terminal_states)

    # État initial de l'AFDC = epsilon-fermeture des états initiaux de l'AF
    init_set = epsilon_closure(set(af.initial_states), old_transitions)
    init_label = states_to_label(sorted(init_set))

    queue: list[list[str]] = [sorted(init_set)]
    new_states: list[str] = [init_label]
    new_transitions: dict[tuple[str, str], list[str]] = {}
    correspondence: dict[str, list[str]] = {init_label: sorted(init_set)}

    while queue:
        group = queue.pop(0)
        group_label = states_to_label(group)

        for symbol in af.alphabet:
            # Ignore le symbole epsilon : déjà traité avec epsilon-fermeture
            if symbol == "*":
                continue

            # Union des destinations depuis tous les états du groupe
            destinations: set[str] = set()
            for state in group:
                for dest in old_transitions.get((state, symbol), []):
                    destinations.add(dest)

            # Epsilon-fermeture de l'union
            destinations = epsilon_closure(destinations, old_transitions)

            if destinations:
                dest_list = sorted(destinations)
                dest_label = states_to_label(dest_list)

                # Nouvel état composé découvert : l'ajouter à la file
                if dest_label not in new_states:
                    new_states.append(dest_label)
                    queue.append(dest_list)
                    correspondence[dest_label] = dest_list

                new_transitions[(group_label, symbol)] = [dest_label]

    # Un état de l'AFDC est terminal si au moins un de ses composants l'était dans l'AF
    new_terminals = []
    for label, components in correspondence.items():
        if any(s in original_terminals for s in components):
            new_terminals.append(label)

    result = Automaton()
    result.alphabet = [s for s in af.alphabet if s != "*"]  # on retire l'epsilon
    result.states = new_states
    result.initial_states = [init_label]
    result.terminal_states = new_terminals
    result.transitions = new_transitions
    return result, correspondence


def determinize_and_complete(af: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    """Retourne l'AFDC équivalent à af, ainsi que la table de correspondance des états.

    Gère trois cas :
    - Déjà déterministe et complet : retourné tel quel.
    - Déterministe mais incomplet : complétion seule.
    - Non déterministe (AFN ou epsilon-AFN) : déterminisation puis complétion.

    Args:
        af: N'importe quel automate fini.

    Returns:
        Un tuple (afdc, correspondance) où :
        - afdc est l'automate complet et déterministe équivalent.
        - correspondance associe chaque état de l'afdc à ses états d'origine dans af.
          Exemple : {"0.1": ["0", "1"], "P": []}
    """
    det_ok, _ = is_deterministic(af)
    comp_ok, _ = is_complete(af)

    if det_ok and comp_ok:
        return af, {state: [state] for state in af.states}

    if det_ok:
        # Automate déterministe incomplet : complétion seule
        completed = complete(af)
        correspondence = {s: [s] for s in af.states}
        correspondence["P"] = []
        return completed, correspondence

    # Automate non déterministe : déterminisation puis complétion
    afdc, correspondence = _determinize(af)
    completed = complete(afdc)
    if "P" in completed.states and "P" not in correspondence:
        correspondence["P"] = []
    return completed, correspondence
