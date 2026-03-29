"""
Module minimize.py — Minimisation d'un automate déterministe complet

Responsable : Eliot Cou.

Algorithme des partitions (Moore) :
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

from rich.console import Console
from rich.table import Table

from automaton.models import Automaton

_console = Console()


def _state_sort_key(state: str) -> tuple[int, int | str]:
    """Clé de tri pour les noms d'états.

    Returns:
        Un tuple (type, valeur) où type=0 pour les états numériques
        et type=1 pour les états non numériques.
    """
    return (0, int(state)) if state.isdigit() else (1, state)


def _sorted_group(group: list[str]) -> list[str]:
    """Trie un groupe d'états (numériques d'abord, puis non-numériques)."""
    return sorted(group, key=_state_sort_key)


def _format_partition(partition: list[list[str]]) -> str:
    """Formate une partition en chaîne de caractères.

    Utilisé pour l'en-tête de chaque étape et pour la détection de stabilité.
    Exemple : [["3","4"], ["0","1","2"]] -> "{3, 4} | {0, 1, 2}"
    """
    return " | ".join("{" + ", ".join(group) + "}" for group in partition)


def _find_group_index(partition: list[list[str]], state: str) -> int:
    """Retourne l'indice du groupe contenant l'état donné.

    Utilisé pour construire les signatures et les transitions de l'AFDCM.

    Raises:
        ValueError: si l'état n'appartient à aucun groupe de la partition.
    """
    for index, group in enumerate(partition):
        if state in group:
            return index
    raise ValueError(f"État introuvable dans la partition : {state}")


def _display_partition_step(
    afdc: Automaton,
    label: str,
    partition: list[list[str]],
    is_stable: bool = False,
) -> None:
    """Affiche une étape de la minimisation : en-tête + table des transitions.

    L'en-tête indique le nom de la partition (P0, P1...) et les groupes courants.
    La table montre, pour chaque état, vers quel groupe (G0, G1...) il transite
    sur chaque symbole de l'alphabet.

    Args:
        afdc: L'automate déterministe complet.
        label: Nom de la partition, ex. "P0" ou "P1".
        partition: La partition à afficher.
        is_stable: Si True, ajoute "<- stable" à l'en-tête.
    """
    stable_suffix = "  <- stable" if is_stable else ""
    _console.print(
        f"[bold]Partition {label}[/bold] : "
        f"{_format_partition(partition)}{stable_suffix}"
    )

    # Table des transitions : une colonne "État", une colonne par symbole
    table = Table(show_header=True, header_style="bold")
    table.add_column("État", justify="center")
    for symbol in afdc.alphabet:
        table.add_column(symbol, justify="center")

    for group in partition:
        for state in group:
            # Pour chaque symbole, on indique l'indice du groupe cible (G0, G1...)
            row = [state]
            for symbol in afdc.alphabet:
                destination = afdc.transitions[(state, symbol)][0]
                group_index = _find_group_index(partition, destination)
                row.append(f"G{group_index}")
            table.add_row(*row)

    _console.print(table)


def _display_correspondence(
    afdcm: Automaton,
    correspondence: dict[str, list[str]],
) -> None:
    """Affiche la table de correspondance AFDCM -> AFDC avec rich.

    Chaque ligne associe un état de l'AFDCM au groupe d'états AFDC qu'il représente.
    """
    table = Table(
        title="Correspondance AFDCM -> AFDC",
        show_header=True,
        header_style="bold",
    )
    table.add_column("État AFDCM", justify="center")
    table.add_column("Groupe AFDC", justify="center")

    for min_state in afdcm.states:
        group = correspondence[min_state]
        table.add_row(min_state, "{" + ", ".join(group) + "}")

    _console.print(table)


def _refine_partition(afdc: Automaton, partition: list[list[str]]) -> list[list[str]]:
    """Raffine une partition en séparant les états dont les comportements diffèrent.

    Principe :
        Deux états p et q d'un même groupe G sont "équivalents" dans cette partition
        si, pour chaque symbole, ils transitent vers le même groupe.
        S'ils ne le font pas, ils sont séparés dans deux sous-groupes distincts.

    Mécanisme — la "signature" :
        La signature d'un état est un tuple d'indices de groupes, un par symbole.
        Exemple sur alphabet {a, b}, partition P = [{3,4}, {0,1,2}] :
            - état 0 : -a-> état 1 (dans G1), -b-> état 0 (dans G1) -> signature = (1, 1)
            - état 2 : -a-> état 3 (dans G0), -b-> état 0 (dans G1) -> signature = (0, 1)
        - états 0 et 2 ont des signatures différentes : ils seront séparés.
        - états 0 et 1, s'ils ont la même signature, resteront dans le même groupe.

    Le dictionnaire `buckets` :
        Clé   = signature (tuple d'entiers)
        Valeur = liste des états partageant cette signature

        Après la boucle, chaque entrée forme un nouveau sous-groupe.
        Si tous les états du groupe ont la même signature -> un seul bucket
        -> pas de séparation.
        Si les signatures diffèrent -> plusieurs buckets -> le groupe est divisé.

    Tri final des sous-groupes :
        Les nouveaux sous-groupes sont triés par leur premier état pour garantir
        un ordre stable. Sans ce tri, deux partitions identiques pourraient être
        jugées différentes selon l'ordre de parcours du dictionnaire, ce qui
        empêcherait la détection de stabilité (Pi+1 == Pi).

    Args:
        afdc: L'automate déterministe complet.
        partition: La partition courante Pi à raffiner.

    Returns:
        La partition raffinée Pi+1.
    """
    refined: list[list[str]] = []

    # On traite chaque groupe de la partition actuelle indépendamment
    for group in partition:

        # buckets regroupe les états par signature :
        # clé    = signature de l'état (tuple des indices de groupe cibles)
        # valeur = liste des états ayant cette signature
        buckets: dict[tuple[int, ...], list[str]] = {}

        for state in group:
            # Signature de cet état : pour chaque symbole, on note l'indice
            # du groupe cible dans la partition courante
            signature = tuple(
                _find_group_index(partition, afdc.transitions[(state, symbol)][0])
                for symbol in afdc.alphabet
            )

            if signature not in buckets:
                buckets[signature] = []
            buckets[signature].append(state)

        # Chaque bucket devient un sous-groupe : on trie les états à l'intérieur
        state_groups = [_sorted_group(states) for states in buckets.values()]

        # Tri des sous-groupes par leur premier état pour ordre déterministe
        state_groups.sort(key=lambda states: _state_sort_key(states[0]))

        refined.extend(state_groups)

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

    # --- Partition initiale P0 : terminaux d'un côté, non-terminaux de l'autre ---
    # Ces deux groupes sont distinguables par définition :
    # l'un reconnaît le mot courant, pas l'autre.
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

    _display_partition_step(afdc, "P0", partition)

    iteration = 0

    # --- Boucle de raffinage : on répète jusqu'à ce que la partition ne change plus ---
    while True:
        next_partition = _refine_partition(afdc, partition)
        iteration += 1

        is_stable = next_partition == partition
        _display_partition_step(afdc, f"P{iteration}", next_partition, is_stable)

        if is_stable:
            final_partition = next_partition
            break

        partition = next_partition

    if len(final_partition) == len(afdc.states):
        _console.print("L'automate est déjà minimal.")

    # --- Construction de l'AFDCM à partir de la partition finale ---

    afdcm = Automaton()
    afdcm.alphabet = afdc.alphabet[:]

    correspondence: dict[str, list[str]] = {}

    # group_to_min_state : correspondance inverse utilisée pendant la construction.
    # Clé    = indice du groupe dans final_partition (entier)
    # Valeur = nom du nouvel état dans l'AFDCM ("0", "1", "2"...)
    # Permet de retrouver le nom AFDCM d'un groupe sans reparcourir la liste.
    group_to_min_state: dict[int, str] = {}

    for index, group in enumerate(final_partition):
        min_state = str(index)
        afdcm.states.append(min_state)
        correspondence[min_state] = group[:]
        group_to_min_state[index] = min_state

    # L'état initial de l'AFDCM est le groupe qui contient l'état initial de l'AFDC
    initial_group_index = _find_group_index(final_partition, afdc.initial_states[0])
    afdcm.initial_states = [group_to_min_state[initial_group_index]]

    # Un groupe est terminal si au moins un de ses états était terminal dans l'AFDC
    for index, group in enumerate(final_partition):
        if any(state in afdc.terminal_states for state in group):
            afdcm.terminal_states.append(group_to_min_state[index])

    # Construction des transitions de l'AFDCM :
    # Tous les états d'un même groupe ont les mêmes transitions (propriété garantie
    # par le raffinage). On prend donc le premier état du groupe comme "représentant"
    # et on lit ses transitions : elles sont valides pour tout le groupe.
    for index, group in enumerate(final_partition):
        representative = group[0]  # représentant : choix arbitraire, tous équivalents
        source_state = group_to_min_state[index]

        for symbol in afdcm.alphabet:
            destination = afdc.transitions[(representative, symbol)][0]
            destination_group_index = _find_group_index(final_partition, destination)
            destination_state = group_to_min_state[destination_group_index]
            afdcm.transitions[(source_state, symbol)] = [destination_state]

    _display_correspondence(afdcm, correspondence)

    return afdcm, correspondence
