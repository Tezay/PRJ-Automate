"""
Tests pour determinize.py — complete() et determinize_and_complete()

Responsable : Edouard (compléter ces tests)
"""

from automaton.models import Automaton
from automaton.determinize import complete, determinize_and_complete


def make_incomplete_dfa() -> Automaton:
    """DFA déterministe mais incomplet : état 1 sans transition sur 'b'."""
    af = Automaton()
    af.alphabet = ["a", "b"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {
        ("0", "a"): ["1"],
        ("0", "b"): ["0"],
        ("1", "a"): ["1"],
        # ("1", "b") manquant
    }
    return af


def make_nfa() -> Automaton:
    """NFA classique : état 0 --a--> 0 et 1, état 1 --b--> 2 (terminal)."""
    af = Automaton()
    af.alphabet = ["a", "b"]
    af.states = ["0", "1", "2"]
    af.initial_states = ["0"]
    af.terminal_states = ["2"]
    af.transitions = {
        ("0", "a"): ["0", "1"],
        ("1", "b"): ["2"],
        ("2", "a"): ["2"],
    }
    return af


class TestComplete:
    def test_adds_puits_state(self):
        af = make_incomplete_dfa()
        afdc = complete(af)
        assert "P" in afdc.states

    def test_all_transitions_defined(self):
        af = make_incomplete_dfa()
        afdc = complete(af)
        for state in afdc.states:
            for symbol in afdc.alphabet:
                assert (state, symbol) in afdc.transitions, (
                    f"Transition manquante : ({state}, {symbol})"
                )

    def test_puits_not_terminal(self):
        af = make_incomplete_dfa()
        afdc = complete(af)
        assert "P" not in afdc.terminal_states

    def test_original_states_preserved(self):
        af = make_incomplete_dfa()
        afdc = complete(af)
        for state in af.states:
            assert state in afdc.states


class TestDeterminizeAndComplete:
    def test_result_is_deterministic(self):
        af = make_nfa()
        afdc, _ = determinize_and_complete(af)
        # Vérifier : un seul état initial, toutes transitions vers 1 état
        assert len(afdc.initial_states) == 1
        for dests in afdc.transitions.values():
            assert len(dests) == 1

    def test_result_is_complete(self):
        af = make_nfa()
        afdc, _ = determinize_and_complete(af)
        for state in afdc.states:
            for symbol in afdc.alphabet:
                assert (state, symbol) in afdc.transitions

    def test_correspondence_returned(self):
        af = make_nfa()
        afdc, correspondance = determinize_and_complete(af)
        assert isinstance(correspondance, dict)
        # L'état initial de l'AFDC doit être dans la correspondance
        initial = afdc.initial_states[0]
        assert initial in correspondance
