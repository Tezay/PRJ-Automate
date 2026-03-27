"""
Module recognize.py — Reconnaissance de mots

Responsable : Eliot Mass

Ce module permet de tester si un mot appartient au langage reconnu par un automate
déterministe complet (AFDC ou AFDCM).

Règles importantes (sujet) :
    - Le mot est lu EN ENTIER avant vérification.
    - Il ne doit PAS y avoir de lecture caractère par caractère interactive.
    - L'utilisateur tape "fin" pour terminer la session de reconnaissance.
"""

from automaton.models import Automaton


def recognize_word(word: str, afdc: Automaton) -> bool:
    """Teste si un mot est reconnu par l'automate déterministe complet.

    Simule l'exécution de l'automate sur le mot en suivant les transitions.
    Si à la fin du mot l'état courant est terminal → le mot est accepté.

    Args:
        word: Le mot à tester (chaîne de caractères).
        afdc: L'automate déterministe et complet à utiliser pour la reconnaissance.

    Returns:
        True si le mot est reconnu (appartient au langage), False sinon.

    Note:
        Si un symbole du mot n'appartient pas à l'alphabet de l'automate,
        ou si aucune transition n'est définie (ne devrait pas arriver sur un AFDC),
        le mot est considéré comme non reconnu.
    """
    raise NotImplementedError("TODO (Membre 5) : Implémenter recognize_word()")
