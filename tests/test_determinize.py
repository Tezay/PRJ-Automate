"""
Tests pour determinize.py — complete() et determinize_and_complete()

Responsable : Edouard
"""

from automaton.determinize import complete, determinize_and_complete
from automaton.models import Automaton
from automaton.recognize import recognize_word


def make_incomplete_dfa() -> Automaton:
    """AFD déterministe mais incomplet : état 1 sans transition sur 'b'."""
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
    """AFN classique : état 0 --a--> 0 et 1, état 1 --b--> 2 (terminal)."""
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
    def test_adds_trash_state(self):
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

    def test_trash_not_terminal(self):
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
        """Vérifier : un seul état initial, toutes transitions vers 1 état"""
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
        """L'état initial de l'AFDC doit être dans la correspondance"""
        initial = afdc.initial_states[0]
        assert initial in correspondance

    def test_nfa_produces_expected_states(self):
        """La subset construction doit produire les états composés attendus."""
        af = make_nfa()

        afdc, _ = determinize_and_complete(af)

        assert len(afdc.states) == 4
        assert "0.1" in afdc.states

    def test_nfa_language_preserved(self):
        """L'AFDC produit doit reconnaître exactement le même langage que le AFN."""
        af = make_nfa()

        afdc, _ = determinize_and_complete(af)

        assert recognize_word("ab", afdc) is True
        assert recognize_word("aab", afdc) is True
        assert recognize_word("aba", afdc) is True
        assert recognize_word("b", afdc) is False
        assert recognize_word("a", afdc) is False
        assert recognize_word("", afdc) is False
