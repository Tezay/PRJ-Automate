"""
Tests pour minimize.py

Responsable : Membre 4 (compléter ces tests)
"""

from automaton.models import Automaton
from automaton.minimize import minimize


def make_already_minimal_dfa() -> Automaton:
    """DFA minimal : 0 -a-> 1 (terminal), 0 -b-> 0, 1 -a-> 1, 1 -b-> 0."""
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
    """DFA non minimal : états 1 et 2 sont équivalents (même comportement)."""
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


class TestMinimize:
    def test_returns_automaton(self):
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert isinstance(afdcm, afdcm.__class__)

    def test_already_minimal_same_size(self):
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert len(afdcm.states) == len(af.states)

    def test_non_minimal_reduced(self):
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        # Les états 1 et 2 doivent être fusionnés → 2 états au total
        assert len(afdcm.states) < len(af.states)

    def test_correspondence_covers_all_afdc_states(self):
        af = make_non_minimal_dfa()
        _, correspondance = minimize(af)
        all_covered = [s for states in correspondance.values() for s in states]
        for state in af.states:
            assert state in all_covered
