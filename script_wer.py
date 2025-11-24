#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de calcul du WER (Word Error Rate) pour la normalisation de nombres
Usage: python script_wer.py "chemin/vers/dataset.csv"
"""

import sys
import re
import pandas as pd
import pynini
from pathlib import Path
from jiwer import wer
from Text_Normalisation_Cardinaux_0_a_1000 import normalize_cardinals_in_sentence

# ============================================
# CONFIGURATION
# ============================================

FAR_FILE = "cardinal_numbers.far"
FST_NAME = "CARDINAL"

# ============================================
# CHARGEMENT DU FST
# ============================================

def load_fst_from_far(far_path=FAR_FILE, fst_name=FST_NAME):
    """
    Charge le FST depuis le fichier FAR
    """
    if not Path(far_path).exists():
        print(f"❌ ERREUR: Le fichier FAR '{far_path}' n'existe pas.", file=sys.stderr)
        print(f"   Veuillez d'abord générer le fichier FAR avec create_far.py", file=sys.stderr)
        sys.exit(1)
    
    try:
        far_reader = pynini.Far(far_path, mode="r")
        try:
            fst = far_reader[fst_name]
        except KeyError:
            print(f"❌ ERREUR: Le FST '{fst_name}' n'existe pas dans le FAR.", file=sys.stderr)
            far_reader.close()
            sys.exit(1)
        
        far_reader.close()
        return fst
    except Exception as e:
        print(f"❌ ERREUR lors du chargement du FAR: {e}", file=sys.stderr)
        sys.exit(1)

# ============================================
# NORMALISATION : utilisation de la fonction importée normalize_cardinals_in_sentence
# ============================================

# ============================================
# CALCUL DU WER
# ============================================

def calculate_wer_from_csv(csv_path, fst):
    """
    Calcule le WER à partir d'un fichier CSV
    """
    print(f"📂 Chargement du dataset: {csv_path}")
    
    # Vérifier que le fichier existe
    if not Path(csv_path).exists():
        print(f"❌ ERREUR: Le fichier '{csv_path}' n'existe pas.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Charger le CSV
        df = pd.read_csv(csv_path)
        
        # Vérifier les colonnes requises
        required_columns = ['reference', 'input']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ ERREUR: Colonnes manquantes dans le CSV: {missing_columns}", file=sys.stderr)
            print(f"   Colonnes trouvées: {list(df.columns)}", file=sys.stderr)
            sys.exit(1)
        
        print(f"✓ Dataset chargé: {len(df)} lignes")
        
    except Exception as e:
        print(f"❌ ERREUR lors du chargement du CSV: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Préparer les données
    print("\n🔄 Normalisation des phrases...")
    ref = df['reference'].to_list()
    inpt = df['input'].to_list()
    
    hyp = []
    for i, sentence in enumerate(inpt):
        normalized = normalize_cardinals_in_sentence(str(sentence), fst)
        hyp.append(normalized)
        
        # Afficher progression tous les 100 éléments
        if (i + 1) % 100 == 0:
            print(f"  Traité: {i + 1}/{len(inpt)} phrases")
    
    print(f"✓ Normalisation terminée: {len(hyp)} phrases traitées")
    
    # Calculer le WER pour chaque paire
    print("\n📊 Calcul du WER...")
    wers = []
    
    if len(ref) != len(hyp):
        print(f"⚠️ ATTENTION: Nombre de références ({len(ref)}) != nombre d'hypothèses ({len(hyp)})", file=sys.stderr)
        min_len = min(len(ref), len(hyp))
        ref = ref[:min_len]
        hyp = hyp[:min_len]
        print(f"   Utilisation des {min_len} premières lignes seulement")
    
    for i in range(len(ref)):
        try:
            score = wer(ref[i], hyp[i])
            wers.append(score)
        except Exception as e:
            print(f"⚠️ Erreur au calcul du WER pour la ligne {i}: {e}", file=sys.stderr)
            wers.append(1.0)  # WER maximum en cas d'erreur
    
    # Calculer le WER moyen
    average_wer = sum(wers) / len(wers) if wers else 0.0
    
    return average_wer, wers, ref, hyp

# ============================================
# AFFICHAGE DES RÉSULTATS
# ============================================

def display_results(average_wer, wers, ref, hyp, show_examples=True, num_examples=5):
    """
    Affiche les résultats du calcul WER
    """
    print("\n" + "="*60)
    print("RÉSULTATS")
    print("="*60)
    print(f"📈 WER Score Moyen: {average_wer:.4f} ({average_wer*100:.2f}%)")
    print(f"📊 Nombre total de phrases: {len(wers)}")
    print(f"✓ WER minimum: {min(wers):.4f}")
    print(f"✗ WER maximum: {max(wers):.4f}")
    print("="*60)
    

# ============================================
# SAUVEGARDE DES RÉSULTATS
# ============================================

def save_results(csv_path, ref, hyp, wers, output_path=None):
    """
    Sauvegarde les résultats dans un fichier CSV
    """
    if output_path is None:
        # Créer un nom de fichier de sortie basé sur l'entrée
        input_path = Path(csv_path)
        output_path = input_path.parent / f"{input_path.stem}_results.csv"
    
    results_df = pd.DataFrame({
        'reference': ref,
        'hypothesis': hyp,
        'wer': wers
    })
    
    results_df.to_csv(output_path, index=False)
    print(f"\n💾 Résultats sauvegardés dans: {output_path}")

# ============================================
# INTERFACE EN LIGNE DE COMMANDE
# ============================================

def print_usage():
    """Affiche l'aide d'utilisation"""
    print("Usage:")
    print(f"  python {sys.argv[0]} <chemin_dataset.csv>")
    print()
    print("Exemples:")
    print(f'  python {sys.argv[0]} data/test.csv')
    print(f'  python {sys.argv[0]} "C:/Users/data/dataset.csv"')
    print()
    print("Options:")
    print(f"  -h, --help          Affiche cette aide")
    print(f"  -o, --output FILE   Sauvegarde les résultats dans FILE")
    print(f"  -n, --no-examples   N'affiche pas les exemples")
    print()
    print("Le CSV doit contenir les colonnes 'reference' et 'input'")

def main():
    """Point d'entrée principal"""
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("❌ ERREUR: Aucun fichier CSV fourni.", file=sys.stderr)
        print()
        print_usage()
        sys.exit(1)
    
    # Gérer l'aide
    if sys.argv[1] in ["-h", "--help"]:
        print_usage()
        sys.exit(0)
    
    # Parser les arguments
    csv_path = None
    output_path = None
    show_examples = True
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ["-o", "--output"]:
            if i + 1 < len(sys.argv):
                output_path = sys.argv[i + 1]
                i += 2
            else:
                print("❌ ERREUR: Option -o requiert un chemin de fichier", file=sys.stderr)
                sys.exit(1)
        elif arg in ["-n", "--no-examples"]:
            show_examples = False
            i += 1
        elif csv_path is None:
            csv_path = arg
            i += 1
        else:
            print(f"❌ ERREUR: Argument inconnu: {arg}", file=sys.stderr)
            print_usage()
            sys.exit(1)
    
    if csv_path is None:
        print("❌ ERREUR: Aucun fichier CSV fourni.", file=sys.stderr)
        print_usage()
        sys.exit(1)
    
    print("="*60)
    print("CALCUL DU WER - Normalisation de Nombres Cardinaux")
    print("="*60)
    
    # Charger le FST
    print("\n🔧 Chargement du FST...")
    fst = load_fst_from_far()
    print("✓ FST chargé avec succès")
    
    # Calculer le WER
    average_wer, wers, ref, hyp = calculate_wer_from_csv(csv_path, fst)
    
    # Afficher les résultats
    display_results(average_wer, wers, ref, hyp, show_examples)
    
    # Sauvegarder les résultats si demandé
    if output_path:
        save_results(csv_path, ref, hyp, wers, output_path)
    
    print("\n✓ Processus terminé avec succès!")

# ============================================
# EXÉCUTION
# ============================================

if __name__ == "__main__":
    main()