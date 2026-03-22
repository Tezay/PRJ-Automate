"""Tests pour models.py — Classe Automaton et states_to_label()"""

from automaton.models import Automaton, states_to_label


class TestStatestoLabel:
    def test_single_state(self):
        assert states_to_label(["0"]) == "0"

    def test_multiple_states_sorted(self):
        assert states_to_label(["2", "0", "1"]) == "0.1.2"

    def test_empty_is_puits(self):
        assert states_to_label([]) == "P"

    def test_multidigit_sorting(self):
        # {3, 12} doit donner "3.12" (tri numérique, pas alphabétique)
        assert states_to_label(["12", "3"]) == "3.12"


class TestAutomaton:
    def test_default_values(self):
        af = Automaton()
        assert af.alphabet == []
        assert af.states == []
        assert af.initial_states == []
        assert af.terminal_states == []
        assert af.transitions == {}

    def test_repr(self):
        af = Automaton()
        af.states = ["0", "1"]
        af.alphabet = ["a"]
        # Vérifie juste que __repr__ ne lève pas d'exception
        assert isinstance(repr(af), str)
