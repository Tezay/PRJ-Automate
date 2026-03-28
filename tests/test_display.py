"""Tests pour display.py — display_automaton()

On teste principalement que la fonction ne lève pas d'exception (smoke tests)
et que la cellule de transition produit le bon contenu via la logique interne.
Tester la sortie visuelle rich n'est pas pratique en test unitaire.
"""

from io import StringIO

from rich.console import Console

from automaton.display import display_automaton
from automaton.models import Automaton


def _make_automaton(
    alphabet: list[str],
    states: list[str],
    initial: list[str],
    terminal: list[str],
    transitions: dict,
) -> Automaton:
    """Construit un Automaton de test à la main."""
    af = Automaton()
    af.alphabet = alphabet
    af.states = states
    af.initial_states = initial
    af.terminal_states = terminal
    af.transitions = transitions
    return af


class TestDisplayNoException:
    def test_simple_automaton(self):
        """Automate minimal : 1 état, 1 symbole, 1 transition."""
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=["0"],
            terminal=["0"],
            transitions={("0", "a"): ["0"]},
        )
        display_automaton(af, title="Simple") # ne doit pas lever d'exception

    def test_no_transitions(self):
        """Automate sans aucune transition -> toutes les cellules doivent être '--'."""
        af = _make_automaton(
            alphabet=["a", "b"],
            states=["0", "1"],
            initial=["0"],
            terminal=["1"],
            transitions={},
        )
        display_automaton(af, title="Sans transitions")

    def test_initial_and_terminal_same_state(self):
        """Un état est à la fois initial et terminal."""
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=["0"],
            terminal=["0"],
            transitions={},
        )
        display_automaton(af, title="Init+Term")

    def test_nfa_multiple_destinations(self):
        """NFA avec 2 destinations pour une même (état, symbole)."""
        af = _make_automaton(
            alphabet=["a"],
            states=["0", "1", "2"],
            initial=["0"],
            terminal=["2"],
            transitions={("0", "a"): ["1", "2"]},
        )
        display_automaton(af, title="NFA")

    def test_afdc_composite_state_names(self):
        """États nommés avec '.' (après déterminisation) — ne doit pas crasher."""
        af = _make_automaton(
            alphabet=["a"],
            states=["0.1", "2", "P"],
            initial=["0.1"],
            terminal=["2"],
            transitions={
                ("0.1", "a"): ["2"],
                ("2", "a"): ["P"],
                ("P", "a"): ["P"],
            },
        )
        display_automaton(af, title="AFDC")

    def test_empty_automaton(self):
        """Automate vide (aucun état) — ne doit pas crasher."""
        af = _make_automaton(
            alphabet=["a"],
            states=[],
            initial=[],
            terminal=[],
            transitions={},
        )
        display_automaton(af, title="Vide")


class TestCellContent:
    """Vérifie le contenu des cellules via une console capturée (monkey-patching)."""

    def _render(self, af: Automaton) -> str:
        buf = StringIO()
        console = Console(file=buf, highlight=False, no_color=True, width=120)
        # monkey-patch _console dans le module display pour capturer la sortie
        import automaton.display as disp
        original = disp._console
        disp._console = console
        try:
            display_automaton(af)
        finally:
            disp._console = original
        return buf.getvalue()

    def test_missing_transition_shows_dashes(self):
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=["0"],
            terminal=[],
            transitions={}, # pas de transition
        )
        output = self._render(af)
        assert "--" in output

    def test_single_destination_shown(self):
        af = _make_automaton(
            alphabet=["a"],
            states=["0", "1"],
            initial=["0"],
            terminal=["1"],
            transitions={("0", "a"): ["1"]},
        )
        output = self._render(af)
        assert "1" in output

    def test_nfa_multiple_destinations_joined_with_comma(self):
        # Les destinations multiples d'un NFA sont séparées par ","
        # (distinct des états composés après déterminisation, notés avec ".")
        af = _make_automaton(
            alphabet=["a"],
            states=["0", "1", "2"],
            initial=["0"],
            terminal=["2"],
            transitions={("0", "a"): ["2", "1"]},  # ordre inverse -> doit être trié
        )
        output = self._render(af)
        assert "1,2" in output

    def test_initial_prefix_present(self):
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=["0"],
            terminal=[],
            transitions={},
        )
        output = self._render(af)
        assert "->" in output

    def test_terminal_prefix_present(self):
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=[],
            terminal=["0"],
            transitions={},
        )
        output = self._render(af)
        assert "<-" in output

    def test_initial_and_terminal_prefix_present(self):
        af = _make_automaton(
            alphabet=["a"],
            states=["0"],
            initial=["0"],
            terminal=["0"],
            transitions={},
        )
        output = self._render(af)
        assert "->/<-" in output
