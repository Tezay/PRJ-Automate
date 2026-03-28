"""
Tests pour minimize.py

Responsable : Eliot Cou. (compléter ces tests)
"""

import pytest

from automaton.models import Automaton
from automaton.minimize import minimize


def make_already_minimal_dfa() -> Automaton:
    #DFA minimal : 0 -a-> 1 (terminal), 0 -b-> 0, 1 -a-> 1, 1 -b-> 0.
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
    #DFA non minimal : états 1 et 2 sont équivalents (même comportement).
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


def make_invalid_dfa_with_two_initial_states() -> Automaton:
    #Automate invalide pour minimize() : deux états initiaux.
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
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert isinstance(afdcm, Automaton)

    def test_already_minimal_same_size(self):
        af = make_already_minimal_dfa()
        afdcm, _ = minimize(af)
        assert len(afdcm.states) == len(af.states)

    def test_non_minimal_reduced(self):
        af = make_non_minimal_dfa()
        afdcm, _ = minimize(af)
        # Les états 1 et 2 doivent être fusionnés -> 2 états au total
        assert len(afdcm.states) < len(af.states)

    def test_correspondence_covers_all_afdc_states(self):
        af = make_non_minimal_dfa()
        _, correspondance = minimize(af)
        all_covered = [s for states in correspondance.values() for s in states]
        for state in af.states:
            assert state in all_covered

    def test_correspondence_is_a_partition(self):
        af = make_non_minimal_dfa()
        _, correspondance = minimize(af)
        all_covered = [s for states in correspondance.values() for s in states]
        assert sorted(all_covered) == sorted(af.states)
        assert len(all_covered) == len(set(all_covered))

    def test_non_minimal_correspondence_has_merged_group(self):
        af = make_non_minimal_dfa()
        _, correspondance = minimize(af)
        groups = [sorted(group) for group in correspondance.values()]
        assert ["0"] in groups
        assert ["1", "2"] in groups

    def test_initial_state_of_minimal_is_correct(self):
        af = make_non_minimal_dfa()
        afdcm, correspondance = minimize(af)
        initial_min_state = afdcm.initial_states[0]
        assert "0" in correspondance[initial_min_state]

    def test_terminal_states_of_minimal_are_correct(self):
        af = make_non_minimal_dfa()
        afdcm, correspondance = minimize(af)

        for min_state in afdcm.terminal_states:
            assert any(state in af.terminal_states for state in correspondance[min_state])

        for min_state, group in correspondance.items():
            if any(state in af.terminal_states for state in group):
                assert min_state in afdcm.terminal_states

    def test_minimal_transitions_are_correct(self):
        af = make_non_minimal_dfa()
        afdcm, correspondance = minimize(af)

        state_for_0 = next(
            min_state for min_state, group in correspondance.items() if group == ["0"]
        )
        state_for_12 = next(
            min_state
            for min_state, group in correspondance.items()
            if sorted(group) == ["1", "2"]
        )

        assert afdcm.transitions[(state_for_0, "a")] == [state_for_12]
        assert afdcm.transitions[(state_for_12, "a")] == [state_for_12]

    def test_raises_if_not_exactly_one_initial_state(self):
        af = make_invalid_dfa_with_two_initial_states()
        with pytest.raises(ValueError):
            minimize(af)