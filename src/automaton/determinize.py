"""
Module determinize.py — Déterminisation et complétion d'un automate

Responsable : Edouard

Ce module fournit deux fonctions :
    - complete()                   : pour un DFA incomplet → DFA complet
    - determinize_and_complete()   : pour un NFA → DFA complet (subset construction)

Algorithme de complétion (complete) :
    1. Ajouter un état puits "P".
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
    5. Si l'union est vide → état puits "P".

Affichage attendu (en plus de la table) :
    Correspondance états AFDC → états AF d'origine :
      "0"    ← {0}
      "0.1"  ← {0, 1}
      "P"    ← {} (état puits)
"""

from automaton.models import Automaton


def complete(af: Automaton) -> Automaton:
    """Complète un automate déterministe en ajoutant un état puits "P".

    À n'appeler que sur un automate déjà déterministe mais incomplet.

    Args:
        af: L'automate déterministe incomplet.

    Returns:
        Un nouvel Automaton déterministe et complet.
    """
    raise NotImplementedError("TODO (Edouard) : Implémenter complete()")


def determinize_and_complete(af: Automaton) -> tuple[Automaton, dict[str, list[str]]]:
    """Déterminise et complète un automate non déterministe.

    Applique la construction des sous-ensembles (subset construction),
    puis complète l'automate résultant si nécessaire.

    Args:
        af: L'automate non déterministe à déterminiser.

    Returns:
        Un tuple (afdc, correspondance) où :
            - afdc (Automaton) : l'automate déterministe et complet résultant.
            - correspondance (dict[str, list[str]]) : mapping label AFDC → états AF.
              Ex: {"0.1": ["0", "1"], "2": ["2"], "P": []}
    """
    raise NotImplementedError(
        "TODO (Edouard) : Implémenter determinize_and_complete()"
    )
