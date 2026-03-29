"""Tests pour reader.py — read_automaton()

Responsable : Eliot Cup.

Utilise les vrais fichiers automata/ fournis sur Moodle.
Chaque test cible un comportement précis du parser.
"""

import pytest

from automaton.reader import read_automaton


class TestAlphabet:
    def test_one_symbol_generates_a(self):
        # 1.txt : 1 symbole -> alphabet = ['a']
        af = read_automaton(1)
        assert af.alphabet == ["a"]

    def test_two_symbols_generates_ab(self):
        # 44.txt : 2 symboles -> alphabet = ['a', 'b']
        af = read_automaton(44)
        assert af.alphabet == ["a", "b"]


class TestStates:
    def test_states_count_and_order(self):
        # 3.txt : 2 états -> ['0', '1']
        af = read_automaton(3)
        assert af.states == ["0", "1"]

    def test_four_states(self):
        # 44.txt : 4 états -> ['0', '1', '2', '3']
        af = read_automaton(44)
        assert af.states == ["0", "1", "2", "3"]


class TestInitialAndTerminal:
    def test_initial_state(self):
        # 8.txt : état initial = 1
        af = read_automaton(8)
        assert af.initial_states == ["1"]

    def test_terminal_state(self):
        # 8.txt : état terminal = 0
        af = read_automaton(8)
        assert af.terminal_states == ["0"]

    def test_multiple_terminal_states(self):
        # 44.txt : 2 états terminaux : 2 et 3
        af = read_automaton(44)
        assert af.terminal_states == ["2", "3"]

    def test_same_state_initial_and_terminal(self):
        # 1.txt : état 0 est à la fois initial et terminal
        af = read_automaton(1)
        assert "0" in af.initial_states
        assert "0" in af.terminal_states


class TestTransitions:
    def test_zero_transitions(self):
        # 1.txt : 0 transitions
        af = read_automaton(1)
        assert af.transitions == {}

    def test_single_transition(self):
        # 3.txt : une seule transition 0 a 1
        af = read_automaton(3)
        assert af.transitions == {("0", "a"): ["1"]}

    def test_nfa_multiple_destinations_accumulated(self):
        # 44.txt : état 3 sur 'a' -> destinations ["3", "2"] (ou ["2","3"])
        af = read_automaton(44)
        dests = af.transitions.get(("3", "a"), [])
        assert len(dests) == 2
        assert set(dests) == {"2", "3"}

    def test_loop_transition(self):
        # 2.txt : 0 a 0 (boucle sur lui-même)
        af = read_automaton(2)
        assert af.transitions[("0", "a")] == ["0"]


class TestErrors:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            read_automaton(999)

    def test_file_not_found_message(self):
        with pytest.raises(FileNotFoundError, match="999"):
            read_automaton(999)
