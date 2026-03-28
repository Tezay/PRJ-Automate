"""
Module models.py — Classe Automaton

Ce module définit la structure de données centrale utilisée dans tout le projet.

Responsable : Eliot Cup.

Règle fondamentale :
    Les états sont TOUJOURS représentés sous forme de chaînes de caractères (str).

    | Situation                        | Exemple d'état     |
    |----------------------------------|--------------------|
    | Automate d'origine               | "0", "1", "2"      |
    | État composé (déterminisation)   | "0.1", "1.2.3"     |
    | Cellule NFA (destinations mult.) | affiché "0,1"      |
    | État puits (complétion)          | "P"                |
    | Nouvel état initial (standard.)  | "i"                |
"""


class Automaton:
    """Représente un automate fini (déterministe ou non déterministe).

    Attributes:
        alphabet (list[str]): Les symboles de l'alphabet.
            Ex: ['a', 'b', 'c'] pour un automate à 3 symboles.

        states (list[str]): La liste de tous les états.
            Ex: ['0', '1', '2', '3', '4']

        initial_states (list[str]): Les états initiaux.
            Ex: ['0'] pour un automate déterministe, ['0', '1'] pour non-déter.

        terminal_states (list[str]): Les états terminaux (acceptants).
            Ex: ['3', '4']

        transitions (dict[tuple[str, str], list[str]]): La table de transitions.
            Clé   : (état_départ, symbole)
            Valeur: liste des états destination (1 seul si déterministe)
            Ex: {('0', 'a'): ['0', '1'], ('1', 'b'): ['2']}
    """

    def __init__(self) -> None:
        self.alphabet: list[str] = []
        self.states: list[str] = []
        self.initial_states: list[str] = []
        self.terminal_states: list[str] = []
        self.transitions: dict[tuple[str, str], list[str]] = {}

    def __repr__(self) -> str:
        return (
            f"Automaton("
            f"states={self.states}, "
            f"alphabet={self.alphabet}, "
            f"initial={self.initial_states}, "
            f"terminal={self.terminal_states}, "
            f"transitions={len(self.transitions)} règles)"
        )


def states_to_label(states: list[str]) -> str:
    """Convertit un ensemble d'états en label textuel pour un état composé.

    Trie les états par leur valeur numérique et les joint avec ".".
    Un ensemble vide retourne "P" (état poubelle).

    Args:
        states: Liste d'états (strings) à combiner.

    Returns:
        Le label de l'état composé.

    Examples:
        >>> states_to_label(["1", "2", "3"])
        '1.2.3'
        >>> states_to_label(["12", "3"])
        '3.12'
        >>> states_to_label([])
        'P'
        >>> states_to_label(["0"])
        '0'
    """
    if not states:
        return "P"
    sorted_states = sorted(states, key=lambda s: int(s))
    return ".".join(sorted_states)
