"""
Tests pour standardize.py

Responsable : Romain (compléter ces tests)
"""

from src.automaton.properties import is_standard
from src.automaton.models import Automaton
from src.automaton.standardize import standardize


def make_non_standard() -> Automaton:
    """NFA avec deux états initiaux et une transition vers l'initial."""
    af = Automaton()
    af.alphabet = ["a", "b"]
    af.states = ["0", "1", "2"]
    af.initial_states = ["0", "1"]
    af.terminal_states = ["2"]
    af.transitions = {
        ("0", "a"): ["2"],
        ("1", "b"): ["2"],
        ("2", "a"): ["0"],  # transition vers un état initial
    }
    return af


class TestStandardize:
    def test_new_initial_state_named_i(self):
        af = make_non_standard()
        sfa = standardize(af)
        assert "i" in sfa.initial_states
        assert sfa.initial_states == ["i"]

    def test_original_not_modified(self):
        af = make_non_standard()
        standardize(af)
        assert af.initial_states == ["0", "1"]

    def test_no_transition_to_initial(self):
        af = make_non_standard()
        sfa = standardize(af)
        for (src, sym), dests in sfa.transitions.items():
            assert "i" not in dests, f"Une transition pointe vers 'i' : {src} --{sym}--> {dests}"

    def test_transitions_copied_from_old_initials(self):
        af = make_non_standard()
        sfa = standardize(af)
        # Les transitions de "0" et "1" doivent être accessibles depuis "i"
        assert ("i", "a") in sfa.transitions
        assert ("i", "b") in sfa.transitions

    def test_terminal_initial_makes_i_terminal(self):
        af = Automaton()
        af.alphabet = ["a"]
        af.states = ["0", "1"]
        af.initial_states = ["0"]
        af.terminal_states = ["0"]
        af.transitions = {("0", "a"): ["1"]}
    
        sfa = standardize(af)
    
        # L'automate résultant est-il standard ?
        assert is_standard(sfa)
    
        # L'état initial est-il unique ?
        assert len(sfa.initial_states) == 1
    
        # L'état initial n'est-il pas terminal ?
        assert sfa.initial_states[0] in sfa.terminal_states
    
        # Le langage reconnu est-il préservé ? (si vous avez une fonction pour ça)
        # assert same_language(af, sfa)
