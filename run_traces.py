"""
run_traces.py — Génération automatique des traces d'exécution

Exécute le programme sur tous les automates disponibles dans automata/
et sauvegarde la sortie dans traces/trace_X.txt.

Utilisation :
    python run_traces.py

Les entrées utilisateur sont simulées automatiquement :
    - Standardisation    : "o" (oui, si proposé)
    - Mots à tester      : une liste de mots prédéfinis, puis "fin"
    - Quitter            : "q"
"""

import os
import subprocess
import sys

# Dossier des automates
AUTOMATA_DIR = "automata"
TRACES_DIR = "traces"

# Mots testés automatiquement pour chaque automate (adapter si besoin)
TEST_WORDS = ["a", "b", "aa", "ab", "ba", "bb", "aaa", ""]


def get_automaton_numbers() -> list[int]:
    """Retourne la liste des numéros d'automates disponibles dans automata/."""
    numbers = []
    for filename in os.listdir(AUTOMATA_DIR):
        if filename.endswith(".txt") and filename[:-4].isdigit():
            numbers.append(int(filename[:-4]))
    return sorted(numbers)


def build_stdin(number: int) -> str:
    """Construit la chaîne d'entrées simulées pour un automate donné.

    Format : une entrée par ligne, simulant les réponses de l'utilisateur.
    """
    lines = []
    lines.append(str(number))  # numéro de l'automate
    lines.append("o")          # standardiser si proposé
    for word in TEST_WORDS:
        lines.append(word)
    lines.append("fin")        # fin de la reconnaissance de mots
    lines.append("q")          # quitter le programme
    return "\n".join(lines) + "\n"


def run_trace(number: int) -> None:
    """Exécute le programme sur l'automate number et sauvegarde la trace."""
    stdin_data = build_stdin(number)
    output_file = os.path.join(TRACES_DIR, f"trace_{number}.txt")

    result = subprocess.run(
        [sys.executable, "main.py"],
        input=stdin_data,
        capture_output=True,
        text=True,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== Trace d'exécution — Automate n°{number} ===\n\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\n--- ERREURS ---\n")
            f.write(result.stderr)

    if result.returncode == 0:
        print(f"  [OK] traces/trace_{number}.txt")
    else:
        print(f"  [ERREUR] Automate n°{number} — voir traces/trace_{number}.txt")


def main() -> None:
    os.makedirs(TRACES_DIR, exist_ok=True)
    numbers = get_automaton_numbers()

    print(f"Génération des traces pour {len(numbers)} automates...\n")

    for number in numbers:
        run_trace(number)

    print(f"\nTerminé. Traces sauvegardées dans {TRACES_DIR}/")


if __name__ == "__main__":
    main()
