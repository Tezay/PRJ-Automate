"""
Module recognize.py — Reconnaissance de mots

Responsable : Eliot Mass

Ce module permet de tester si un mot appartient au langage reconnu par un automate
déterministe complet (AFDC ou AFDCM).

Règles importantes (sujet) :
    - Le mot est lu EN ENTIER avant vérification.
    - Il ne doit PAS y avoir de lecture caractère par caractère interactive.
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
    if not afdc.initial_states:
        return False
    current_state = afdc.initial_states[0]

    # Parcours du mot EN ENTIER
    for char in word:
        # 1. Vérification de l'alphabet
        if char not in afdc.alphabet:
            return False

        # 2. Récupération de la transition
        # .get() permet de gérer proprement une clé absente (retourne None)
        next_states = afdc.transitions.get((current_state, char))

        # 3. Mise à jour de l'état (on prend le premier élément de la liste car AFD)
        if next_states and len(next_states) > 0:
            current_state = next_states[0]
        else:
            # Si aucune transition n'est définie (ne devrait pas arriver sur un AFDC)
            return False

    # 4. Vérification finale : l'état d'arrivée est-il terminal ?
    return current_state in afdc.terminal_states
