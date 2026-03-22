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
    - Les états destination séparés par "," si plusieurs (ex: "0,1") pour les NFA
"""

from automaton.models import Automaton


def display_automaton(af: Automaton, title: str = "Automate") -> None:
    """Affiche la table de transitions d'un automate avec rich.

    Args:
        af: L'automate à afficher.
        title: Titre affiché au-dessus de la table.
    """
    raise NotImplementedError("TODO (Eliot Cup.) : Implémenter display_automaton()")
