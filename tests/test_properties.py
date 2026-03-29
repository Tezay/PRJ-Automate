"""
Tests pour properties.py — is_deterministic, is_standard, is_complete

Responsable : Romain
"""


from src.automaton.models import Automaton
from src.automaton.properties import is_complete, is_deterministic, is_standard


def make_simple_dfa() -> Automaton:
    """Crée un AFD simple pour les tests : 0 -a-> 1 (terminal)."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {("0", "a"): ["1"]}
    return af


def make_nfa_multiple_transitions() -> Automaton:
    """AFN : état 0 avec 'a' vers 0 ET 1."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {("0", "a"): ["0", "1"]}
    return af


def make_complete_nfa() -> Automaton:
    """AFN complet (toutes les paires (état, symbole) définies) mais non déterministe."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {
        ("0", "a"): ["0", "1"],  # non-déterministe
        ("1", "a"): ["1"],
    }
    return af


def make_nfa_multiple_initials() -> Automaton:
    """AFN : deux états initiaux."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0", "1"]
    af.terminal_states = ["1"]
    af.transitions = {("0", "a"): ["1"]}
    return af


class TestIsDeterministic:
    def test_dfa_is_deterministic(self):
        af = make_simple_dfa()
        ok, raisons = is_deterministic(af)
        assert ok is True
        assert raisons == []

    def test_nfa_multiple_transitions(self):
        af = make_nfa_multiple_transitions()
        ok, raisons = is_deterministic(af)
        assert ok is False
        assert len(raisons) > 0

    def test_nfa_multiple_initials(self):
        af = make_nfa_multiple_initials()
        ok, raisons = is_deterministic(af)
        assert ok is False
        assert len(raisons) > 0


class TestIsStandard:
    def test_standard_automaton(self):
        af = make_simple_dfa()
        # Aucune transition ne pointe vers l'état initial "0"
        ok, raisons = is_standard(af)
        assert ok is True
        assert raisons == []

    def test_non_standard_transition_to_initial(self):
        af = make_simple_dfa()
        # Ajouter une transition qui pointe vers l'état initial
        af.transitions[("1", "a")] = ["0"]
        ok, raisons = is_standard(af)
        assert ok is False
        assert len(raisons) > 0

    def test_non_standard_multiple_initials(self):
        af = make_nfa_multiple_initials()
        ok, raisons = is_standard(af)
        assert ok is False
        assert len(raisons) > 0


class TestIsComplete:
    def test_complete_dfa(self):
        af = Automaton()
        af.alphabet = ["a"]
        af.states = ["0", "1"]
        af.initial_states = ["0"]
        af.terminal_states = ["1"]
        af.transitions = {("0", "a"): ["1"], ("1", "a"): ["1"]}
        ok, raisons = is_complete(af)
        assert ok is True
        assert raisons == []

    def test_incomplete_dfa(self):
        af = make_simple_dfa()  # état 1 n'a pas de transition sur 'a'
        ok, raisons = is_complete(af)
        assert ok is False
        assert len(raisons) > 0

    def test_complete_nfa(self):
        """Un AFN (automate non déterministe fini) peut être complet (au moins une transition par (état, symbole))."""
        af = Automaton()
        af.alphabet = ["a"]
        af.states = ["0", "1"]
        af.initial_states = ["0"]
        # État 0 a DEUX transitions sur 'a' (Non-déterministe)
        # État 1 a UNE transition sur 'a'
        # Comme chaque état a au moins une transition pour 'a', il est COMPLET.
        af.transitions = {
            ("0", "a"): ["0", "1"],
            ("1", "a"): ["0"]
        }
        ok, raisons = is_complete(af)
        assert ok is True
        assert raisons == []
