"""
main.py — Point d'entrée du programme

Responsable : Eliot Mass

Ce fichier contient la boucle principale du programme.
Il orchestre tous les modules du package automaton.

Pour lancer le programme :
    python main.py
"""

from automaton.complement import complement
from automaton.determinize import complete, determinize_and_complete
from automaton.display import display_automaton
from automaton.minimize import minimize
from automaton.properties import is_complete, is_deterministic, is_standard
from automaton.reader import read_automaton
from automaton.recognize import recognize_word
from automaton.standardize import standardize


def process_automaton(number: int) -> None:
    """Exécute le pipeline complet de traitement pour un automate donné.

    Étapes :
        1. Lecture et affichage de l'automate (AF)
        2. Test des propriétés : déterministe ? standard ? complet ?
        3. Standardisation si demandée
        4. Déterminisation et/ou complétion → AFDC
        5. Minimisation → AFDCM
        6. Reconnaissance de mots (boucle)
        7. Construction et affichage de l'automate complémentaire

    Args:
        number: Numéro de l'automate à traiter.
    """
    # ── Étape 1 : Lecture et affichage ────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Chargement de l'automate n°{number}")
    print(f"{'='*60}")

    af = read_automaton(number)
    display_automaton(af, title=f"Automate n°{number}")

    # ── Étape 2 : Propriétés ──────────────────────────────────────────────────
    print("\n--- Propriétés de l'automate ---")

    determ, raisons_determ = is_deterministic(af)
    if determ:
        print("Déterministe : OUI")
    else:
        print("Déterministe : NON")
        for r in raisons_determ:
            print(f"  → {r}")

    standard = is_standard(af)
    print(f"Standard     : {'OUI' if standard else 'NON'}")

    if determ:
        complet, raisons_complet = is_complete(af)
        if complet:
            print("Complet      : OUI")
        else:
            print("Complet      : NON")
            for r in raisons_complet:
                print(f"  → {r}")

    # ── Étape 3 : Standardisation (optionnelle) ───────────────────────────────
    if not standard:
        reponse = input("\nVoulez-vous standardiser l'automate ? (o/n) : ").strip().lower()
        if reponse == "o":
            af = standardize(af)
            display_automaton(af, title="Automate standardisé")

    # ── Étape 4 : Déterminisation / Complétion → AFDC ─────────────────────────
    print("\n--- Déterminisation et complétion ---")

    # Re-tester les propriétés sur l'automate courant (potentiellement standardisé)
    determ, _ = is_deterministic(af)
    if determ:
        complet, _ = is_complete(af)
        if complet:
            print("L'automate est déjà déterministe et complet.")
            afdc = af
        else:
            print("L'automate est déterministe mais incomplet → complétion.")
            afdc = complete(af)
    else:
        print("L'automate est non déterministe → déterminisation et complétion.")
        afdc, correspondance = determinize_and_complete(af)
        print("\nCorrespondance états AFDC → états AF d'origine :")
        for label, etats in correspondance.items():
            print(f"  \"{label}\" ← {{{', '.join(etats) if etats else 'vide (état puits)'}}}")

    display_automaton(afdc, title="Automate Déterministe Complet (AFDC)")

    # ── Étape 5 : Minimisation → AFDCM ───────────────────────────────────────
    print("\n--- Minimisation ---")
    afdcm, correspondance_min = minimize(afdc)

    print("\nCorrespondance états AFDCM → états AFDC :")
    for etat_min, etats_afdc in correspondance_min.items():
        print(f"  État \"{etat_min}\" ← {{{', '.join(etats_afdc)}}}")

    display_automaton(afdcm, title="Automate Minimal (AFDCM)")

    # ── Étape 6 : Reconnaissance de mots ─────────────────────────────────────
    print("\n--- Reconnaissance de mots ---")
    print("(Tapez 'fin' pour arrêter la saisie de mots)")

    while True:
        mot = input("Mot à tester : ").strip()
        if mot == "fin":
            break
        if recognize_word(mot, afdc):
            print(f"  → OUI, \"{mot}\" est reconnu par l'automate.")
        else:
            print(f"  → NON, \"{mot}\" n'est pas reconnu par l'automate.")

    # ── Étape 7 : Automate complémentaire ────────────────────────────────────
    print("\n--- Automate complémentaire ---")
    # On utilise l'AFDCM (plus petit)
    print("Construction à partir de l'AFDCM.")
    acomp = complement(afdcm)
    display_automaton(acomp, title="Automate Complémentaire")


def main() -> None:
    """Boucle principale : traite plusieurs automates sans relancer le programme."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    Traitement d'Automates Finis — EFREI P2 2025/2026     ║")
    print("╚══════════════════════════════════════════════════════════╝")

    while True:
        print("\n" + "─" * 60)
        choix = input("Numéro de l'automate à charger (ou 'q' pour quitter) : ").strip()

        if choix.lower() == "q":
            print("Au revoir !")
            break

        if not choix.isdigit():
            print("Entrée invalide. Veuillez entrer un numéro ou 'q'.")
            continue

        try:
            process_automaton(int(choix))
        except FileNotFoundError:
            print(f"Erreur : l'automate n°{choix} n'existe pas dans le dossier automata/.")
        except Exception as e:
            print(f"Erreur inattendue : {e}")


if __name__ == "__main__":
    main()
