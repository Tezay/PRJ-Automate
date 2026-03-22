"""
Module minimize.py — Minimisation d'un automate déterministe complet

Responsable : Membre 4

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
    Partition P2 : {3, 4} | {2} | {0} | {1}  ← stable

    Table de correspondance AFDCM → AFDC :
      État "0" ← groupe {0}
      État "1" ← groupe {1}
      État "2" ← groupe {2}
      État "3" ← groupe {3, 4}

Si l'automate est déjà minimal (P0 == partition finale) :
    Afficher "L'automate est déjà minimal."
"""

from automaton.models import Automaton


def minimize(afdc: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    """Minimise un automate déterministe complet par l'algorithme des partitions.

    Affiche chaque partition numérotée et les transitions exprimées en termes
    de parties au cours du processus. Affiche un message si déjà minimal.

    Args:
        afdc: L'automate déterministe et complet à minimiser.

    Returns:
        Un tuple (afdcm, correspondance) où :
            - afdcm (Automaton) : l'automate minimal résultant.
            - correspondance (dict[str, list[str]]) : mapping état AFDCM → états AFDC.
              Ex: {"0": ["0"], "1": ["1"], "2": ["2"], "3": ["3", "4"]}
    """
    raise NotImplementedError("TODO (Membre 4) : Implémenter minimize()")
