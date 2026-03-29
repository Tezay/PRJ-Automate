"""
Tests pour recognize.py

Responsable : Eliot Mass
"""

from automaton.models import Automaton
from automaton.recognize import recognize_word


def make_dfa_ends_with_a() -> Automaton:
    """DFA qui reconnaît les mots sur {a,b} se terminant par 'a'.
    États : 0 (initial), 1 (terminal)
    Transitions : 0-a->1, 0-b->0, 1-a->1, 1-b->0
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


class TestRecognizeWord:
    def test_word_accepted(self):
        af = make_dfa_ends_with_a()
        assert recognize_word("a", af) is True
        assert recognize_word("ba", af) is True
        assert recognize_word("aba", af) is True

    def test_word_rejected(self):
        af = make_dfa_ends_with_a()
        assert recognize_word("b", af) is False
        assert recognize_word("ab", af) is False
        assert recognize_word("", af) is False  # mot vide, état initial non terminal

    def test_empty_word_accepted_if_initial_terminal(self):
        af = Automaton()
        af.alphabet = ["a"]
        af.states = ["0"]
        af.initial_states = ["0"]
        af.terminal_states = ["0"]  # état initial est terminal
        af.transitions = {("0", "a"): ["0"]}
        assert recognize_word("", af) is True

    def test_unknown_symbol_rejected(self):
        af = make_dfa_ends_with_a()
        assert recognize_word("c", af) is False

    def test_missing_transition_rejected(self):
        """Vérifie le comportement si une transition est manquante (cas non AFDC)."""
        af = Automaton()
        af.alphabet = ["a", "b"]
        af.states = ["0", "1"]
        af.initial_states = ["0"]
        af.terminal_states = ["1"]
        af.transitions = {("0", "a"): ["1"]} # Pas de transition pour 'b'
        assert recognize_word("b", af) is False
        assert recognize_word("ab", af) is False

    def test_long_word(self):
        """Vérifie la stabilité sur un mot plus long."""
        af = make_dfa_ends_with_a()
        long_word = "b" * 100 + "a"
        assert recognize_word(long_word, af) is True
        long_word_fail = "a" + "b" * 100
        assert recognize_word(long_word_fail, af) is False

    def test_no_initial_state(self):
        """Vérifie qu'un automate sans état initial ne reconnaît rien."""
        af = Automaton()
        af.alphabet = ["a"]
        af.states = ["0"]
        af.terminal_states = ["0"]
        assert recognize_word("a", af) is False
        assert recognize_word("", af) is False
