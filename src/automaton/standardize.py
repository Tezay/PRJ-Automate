"""
Module standardize.py — Standardisation d'un automate

Responsable : Membre 2

Algorithme de standardisation :
    1. Créer un nouvel état initial nommé "i".
    2. Pour chaque ancien état initial, copier toutes ses transitions sortantes
       vers le nouvel état "i" (même symbole, même destination).
    3. Si au moins un ancien état initial était terminal, "i" est aussi terminal.
    4. Retirer les anciens états initiaux de la liste des états initiaux.
    5. Le nouvel état "i" est le seul état initial.

Note :
    - L'automate original n'est PAS modifié. On retourne un nouvel Automaton.
    - On ne doit appeler cette fonction que si l'automate n'est pas standard.
"""

from automaton.models import Automaton


def standardize(af: Automaton) -> Automaton:
    """Standardise un automate en créant un unique état initial "i".

    Args:
        af: L'automate non standard à standardiser.

    Returns:
        Un nouvel Automaton standardisé (l'original n'est pas modifié).
    """
    raise NotImplementedError("TODO (Membre 2) : Implémenter standardize()")
