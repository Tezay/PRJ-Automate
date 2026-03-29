"""
Module minimize.py — Minimisation d'un automate déterministe complet

Responsable : Eliot Cou.

Algorithme des partitions (Moore / table-filling) :
    1. Partition initiale P0 :
           P0 = { états terminaux } + { états non terminaux }
       (deux groupes, sauf si l'un est vide)

    2. Raffinage : à chaque itération, pour chaque groupe G de la partition Pi,
       deux états p, q ∈ G sont séparés si pour un symbole a :
           transition(p, a) et transition(q, a) n'appartiennent pas au même groupe.
       Si deux états sont séparés, on divise G en sous-groupes.

    3. Répéter jusqu'à stabilité (Pi+1 == Pi).

    4. Construire l'AFDCM :
           - Chaque groupe de la partition finale = un état (renommé 0, 1, 2...).
           - L'état contenant l'état initial de l'AFDC est l'état initial de l'AFDCM.
           - Un état est terminal si son groupe contient au moins un état terminal.
           - Les transitions sont déduites en suivant les transitions d'un représentant.

Affichage attendu :
    Partition P0 : {3, 4} | {0, 1, 2}
    Partition P1 : {3, 4} | {2} | {0, 1}
    Partition P2 : {3, 4} | {2} | {0} | {1}  <- stable

    Table de correspondance AFDCM -> AFDC :
      État "0" <- groupe {0}
      État "1" <- groupe {1}
      État "2" <- groupe {2}
      État "3" <- groupe {3, 4}

Si l'automate est déjà minimal (P0 == partition finale) :
    Afficher "L'automate est déjà minimal."
"""

from automaton.models import Automaton


def _state_sort_key(state: str) -> tuple[int, int | str]:
    """Clé de tri pour les noms d'états.

    Returns:
        Un tuple (type, valeur) où type=0 pour les états numériques
        et type=1 pour les états non numériques.
    """
    return (0, int(state)) if state.isdigit() else (1, state)


def _sorted_group(group: list[str]) -> list[str]:
    """Trie un groupe d'états selon la convention du projet."""
    return sorted(group, key=_state_sort_key)


def _format_partition(partition: list[list[str]]) -> str:
    """Formate une partition pour l'affichage demandé."""
    return " | ".join("{" + ", ".join(group) + "}" for group in partition)


def _find_group_index(partition: list[list[str]], state: str) -> int:
    """Retourne l'indice du groupe contenant l'état donné."""
    for index, group in enumerate(partition):
        if state in group:
            return index
    raise ValueError(f"État introuvable dans la partition : {state}")


def _print_group_transitions(afdc: Automaton, partition: list[list[str]]) -> None:
    """Affiche les transitions de chaque état vers les groupes de la partition."""
    print("Transitions en termes de parties :")
    for group in partition:
        for state in group:
            transitions = []
            for symbol in afdc.alphabet:
                destination = afdc.transitions[(state, symbol)][0]
                group_index = _find_group_index(partition, destination)
                transitions.append(f"{symbol}->G{group_index}")
            print(f"  {state} : " + ", ".join(transitions))


def _refine_partition(afdc: Automaton, partition: list[list[str]]) -> list[list[str]]:
    """Raffine une partition à partir des signatures de transitions."""
    refined: list[list[str]] = []

    for group in partition:
        buckets: dict[tuple[int, ...], list[str]] = {}

        for state in group:
            signature = tuple(
                _find_group_index(partition, afdc.transitions[(state, symbol)][0])
                for symbol in afdc.alphabet
            )
            buckets.setdefault(signature, []).append(state)

        split_groups = [_sorted_group(states) for states in buckets.values()]
        split_groups.sort(key=lambda states: (_state_sort_key(states[0]), len(states)))
        refined.extend(split_groups)

    return refined


def minimize(afdc: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    """Minimise un automate déterministe complet par l'algorithme des partitions.

    Affiche chaque partition numérotée et les transitions exprimées en termes
    de parties au cours du processus. Affiche un message si déjà minimal.

    Args:
        afdc: L'automate déterministe et complet à minimiser.

    Returns:
        Un tuple (afdcm, correspondance) où :
            - afdcm (Automaton) : l'automate minimal résultant.
            - correspondance (dict[str, list[str]]) : mapping état AFDCM -> états AFDC.
              Ex: {"0": ["0"], "1": ["1"], "2": ["2"], "3": ["3", "4"]}
    """
    if len(afdc.initial_states) != 1:
        raise ValueError(
            "La minimisation attend un automate déterministe complet "
            "avec un seul état initial."
        )

    terminal_states = _sorted_group(
        [state for state in afdc.states if state in afdc.terminal_states]
    )
    non_terminal_states = _sorted_group(
        [state for state in afdc.states if state not in afdc.terminal_states]
    )

    partition: list[list[str]] = []
    if terminal_states:
        partition.append(terminal_states)
    if non_terminal_states:
        partition.append(non_terminal_states)

    print(f"Partition P0 : {_format_partition(partition)}")
    _print_group_transitions(afdc, partition)

    iteration = 0

    while True:
        next_partition = _refine_partition(afdc, partition)
        iteration += 1
        is_stable = next_partition == partition
        stable_suffix = "  <- stable" if is_stable else ""
        formatted = _format_partition(next_partition)
        print(f"Partition P{iteration} : {formatted}{stable_suffix}")
        _print_group_transitions(afdc, next_partition)

        if is_stable:
            final_partition = next_partition
            break

        partition = next_partition

    if len(final_partition) == len(afdc.states):
        print("L'automate est déjà minimal.")

    afdcm = Automaton()
    afdcm.alphabet = afdc.alphabet[:]

    correspondence: dict[str, list[str]] = {}
    group_to_min_state: dict[int, str] = {}

    for index, group in enumerate(final_partition):
        min_state = str(index)
        afdcm.states.append(min_state)
        correspondence[min_state] = group[:]
        group_to_min_state[index] = min_state

    initial_group_index = _find_group_index(final_partition, afdc.initial_states[0])
    afdcm.initial_states = [group_to_min_state[initial_group_index]]

    for index, group in enumerate(final_partition):
        if any(state in afdc.terminal_states for state in group):
            afdcm.terminal_states.append(group_to_min_state[index])

    for index, group in enumerate(final_partition):
        representative = group[0]
        source_state = group_to_min_state[index]

        for symbol in afdcm.alphabet:
            destination = afdc.transitions[(representative, symbol)][0]
            destination_group_index = _find_group_index(final_partition, destination)
            destination_state = group_to_min_state[destination_group_index]
            afdcm.transitions[(source_state, symbol)] = [destination_state]

    print("Table de correspondance AFDCM -> AFDC :")
    for min_state in afdcm.states:
        group = correspondence[min_state]
        print(f'  État "{min_state}" <- groupe {{{", ".join(group)}}}')

    return afdcm, correspondence
