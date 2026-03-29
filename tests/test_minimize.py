"""
Tests pour minimize.py

Responsable : Eliot Cou. & Eliot Cup.
"""

import pytest

from automaton.minimize import minimize
from automaton.models import Automaton


def make_already_minimal_dfa() -> Automaton:
    """AFD minimal à 2 états : reconnaît les mots sur {a,b} se terminant par 'a'.

    Partition finale : [["1"], ["0"]]
    AFDCM : état "0" <- ["1"] (terminal), état "1" <- ["0"] (initial)
    """
    af = Automaton()
    af.alphabet = ["a", "b"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {
        ("0", "a"): ["1"],
        ("0", "b"): ["0"],
        ("1", "a"): ["1"],
        ("1", "b"): ["0"],
    }
    return af


def make_non_minimal_dfa() -> Automaton:
    """AFD non minimal sur {a} : états 1 et 2 équivalents, doivent être fusionnés.

    Partition finale : [["1", "2"], ["0"]]
    AFDCM : état "0" <- ["1", "2"] (terminal), état "1" <- ["0"] (initial)
    """
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1", "2"]
    af.initial_states = ["0"]
    af.terminal_states = ["1", "2"]
    af.transitions = {
        ("0", "a"): ["1"],
        ("1", "a"): ["2"],
        ("2", "a"): ["2"],
    }
    return af


def make_dfa_with_trash_state() -> Automaton:
    """AFDC minimal avec état poubelle 'P' : 0 -a-> 1 (terminal), tout le reste vers P.

    Partition finale : [["1"], ["0"], ["P"]]
    AFDCM : état "0" <- ["1"] (terminal), état "1" <- ["0"] (initial), état "2" <- ["P"]
    """
    af = Automaton()
    af.alphabet = ["a", "b"]
    af.states = ["0", "1", "P"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {
        ("0", "a"): ["1"],
        ("0", "b"): ["P"],
        ("1", "a"): ["P"],
        ("1", "b"): ["P"],
        ("P", "a"): ["P"],
        ("P", "b"): ["P"],
    }
    return af


def make_invalid_dfa_with_two_initial_states() -> Automaton:
    """Automate invalide pour minimize() : deux états initiaux."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0", "1"]
    af.terminal_states = ["1"]
    af.transitions = {
        ("0", "a"): ["1"],
        ("1", "a"): ["1"],
    }
    return af


class TestMinimize:
    def test_returns_automaton(self):
        """minimize() retourne un objet Automaton."""
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert isinstance(afdcm, Automaton)

    def test_already_minimal_preserves_state_count(self):
        """Un AFDC déjà minimal conserve le même nombre d'états."""
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert len(afdcm.states) == 2

    def test_non_minimal_reduces_state_count(self):
        """Un AFDC non minimal produit un AFDCM avec moins d'états."""
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        assert len(afdcm.states) == 2

    def test_non_minimal_correspondence(self):
        """La correspondance groupe exactement les états équivalents."""
        af = make_non_minimal_dfa()
        _, correspondance = minimize(af)
        assert correspondance == {"0": ["1", "2"], "1": ["0"]}

    def test_non_minimal_initial_state(self):
        """L'état initial de l'AFDCM est l'image de l'état initial de l'AFDC."""
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        assert afdcm.initial_states == ["1"]

    def test_non_minimal_terminal_states(self):
        """Tout groupe avec un terminal produit un état terminal dans l'AFDCM."""
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        assert afdcm.terminal_states == ["0"]

    def test_non_minimal_transitions(self):
        """Les transitions de l'AFDCM reflètent la fusion des états équivalents."""
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        assert afdcm.transitions[("1", "a")] == ["0"]  # initial -> terminal
        assert afdcm.transitions[("0", "a")] == ["0"]  # terminal boucle

    def test_with_trash_state_does_not_crash(self):
        """La présence de 'P' avec des états numériques ne lève pas TypeError.
        """
        af = make_dfa_with_trash_state()
        afdcm, _ = minimize(af)
        assert isinstance(afdcm, Automaton)

    def test_with_trash_state_preserves_state_count(self):
        """Un AFDC déjà minimal avec état poubelle conserve son nombre d'états."""
        af = make_dfa_with_trash_state()
        afdcm, _ = minimize(af)
        assert len(afdcm.states) == 3

    def test_raises_on_multiple_initial_states(self):
        """minimize() lève ValueError si l'automate a plusieurs états initiaux."""
        af = make_invalid_dfa_with_two_initial_states()
        with pytest.raises(ValueError):
            minimize(af)
