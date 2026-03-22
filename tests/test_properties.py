"""
Tests pour properties.py — is_deterministic, is_standard, is_complete

Responsable : Membre 2 (écrire les tests de son propre module)

Conseils pour écrire les tests :
    - Créer des automates simples à la main (sans passer par le reader)
    - Tester les cas nominaux ET les cas limites (automate vide, 1 seul état...)
    - Un test = une chose vérifiée
"""

import pytest
from automaton.models import Automaton
from automaton.properties import is_complete, is_deterministic, is_standard


def make_simple_dfa() -> Automaton:
    """Crée un DFA simple pour les tests : 0 -a-> 1 (terminal)."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {("0", "a"): ["1"]}
    return af


def make_nfa_multiple_transitions() -> Automaton:
    """NFA : état 0 avec 'a' vers 0 ET 1."""
    af = Automaton()
    af.alphabet = ["a"]
    af.states = ["0", "1"]
    af.initial_states = ["0"]
    af.terminal_states = ["1"]
    af.transitions = {("0", "a"): ["0", "1"]}
    return af


def make_nfa_multiple_initials() -> Automaton:
    """NFA : deux états initiaux."""
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
        assert is_standard(af) is True

    def test_non_standard_transition_to_initial(self):
        af = make_simple_dfa()
        # Ajouter une transition qui pointe vers l'état initial
        af.transitions[("1", "a")] = ["0"]
        assert is_standard(af) is False

    def test_non_standard_multiple_initials(self):
        af = make_nfa_multiple_initials()
        assert is_standard(af) is False


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
