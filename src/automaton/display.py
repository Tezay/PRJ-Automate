"""
Module display.py — Affichage des automates dans le terminal

Responsable : Eliot Cup.

Utilise la bibliothèque `rich` pour produire des tables bien alignées et lisibles.

Comportement attendu pour la colonne "État" :
    - Préfixe "->" si l'état est initial
    - Préfixe "<-" si l'état est terminal
    - "->/<-" si l'état est à la fois initial et terminal
    - Aucun préfixe sinon (espaces pour l'alignement)

Comportement attendu pour les cellules de transitions :
    - "--" si aucune transition depuis cet état pour ce symbole
    - L'état destination si une seule transition (ex: "2")
    - Les états destination séparés par "," si plusieurs (ex: "0,1") pour les AFN
      Note : on distingue volontairement "0,1" (cellule AFN = non-déterminisme)
      de "0.1" (nom d'un état composé après déterminisation).
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


def display_automaton(af: Automaton, title: str = "Automate") -> None:
    """Affiche la table de transitions d'un automate avec rich.

    Args:
        af: L'automate à afficher.
        title: Titre affiché au-dessus de la table.
    """
    table = Table(title=title, show_lines=False)

    # Colonne "État" : préfixe indicateur d'initial/terminal
    table.add_column("État", justify="left", style="bold", no_wrap=True)

    # Une colonne par symbole de l'alphabet
    for symbol in af.alphabet:
        table.add_column(symbol, justify="center")

    for state in af.states:
        is_init = state in af.initial_states
        is_term = state in af.terminal_states

        if is_init and is_term:
            prefix = "->/<-"
        elif is_init:
            prefix = "->   "
        elif is_term:
            prefix = "<-   "
        else:
            prefix = "     "

        state_label = f"{prefix} {state}"

        cells = []
        for symbol in af.alphabet:
            dests = af.transitions.get((state, symbol), [])
            if not dests:
                cells.append("--")
            elif len(dests) == 1:
                cells.append(dests[0])
            else:
                # AFN : destinations multiples, jointes par ","
                sorted_dests = sorted(dests, key=_state_sort_key)
                cells.append(",".join(sorted_dests))

        table.add_row(state_label, *cells)

    _console.print(table)
