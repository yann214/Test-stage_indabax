#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de normalisation de texte avec FST
Usage: python normalize.py "5 bonbons"
"""

import sys
import re
import pynini
from pathlib import Path

# ============================================
# CONFIGURATION
# ============================================

FAR_FILE = "cardinal_numbers.far"
FST_NAME = "CARDINAL"



def apply_fst(text, fst):
    try:
        return(pynini.shortestpath(pynini.accep(text,token_type='utf8') @ fst).string("utf8"))

    except Exception as e:
        return(f"Error: {e}, for input:'{text}'")

# ============================================
# CHARGEMENT DU FST
# ============================================

def load_fst_from_far(far_path=FAR_FILE, fst_name=FST_NAME):
    """
    Charge le FST depuis le fichier FAR
    """
    if not Path(far_path).exists():
        print(f"❌ ERREUR: Le fichier FAR '{far_path}' n'existe pas.", file=sys.stderr)
        print(f"   Veuillez d'abord générer le fichier FAR en exécutant le script de création.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Ouvrir le FAR en mode lecture
        far_reader = pynini.Far(far_path, mode="r")
        
        # Essayer de récupérer le FST
        try:
            fst = far_reader[fst_name]
        except KeyError:
            print(f"❌ ERREUR: Le FST '{fst_name}' n'existe pas dans le FAR.", file=sys.stderr)
            print(f"   Vérifiez que le fichier FAR a été créé correctement.", file=sys.stderr)
            far_reader.close()
            sys.exit(1)
        
        # Fermer le reader
        far_reader.close()
        
        return fst
    except Exception as e:
        print(f"❌ ERREUR lors du chargement du FAR: {e}", file=sys.stderr)
        sys.exit(1)

# ============================================
# NORMALISATION
# ============================================

def normalize_number(number_str, fst):
    """
    Normalise un nombre avec le FST
    """
    try:
        result = apply_fst(number_str, fst)
        return result
    except Exception:
        # Si le FST ne peut pas traiter ce nombre, on le retourne tel quel
        return number_str

def normalize_text(text, fst):
    """
    Normalise tous les nombres dans un texte
    """
    # Pattern pour détecter les nombres (0-1000)
    number_pattern = r'\b\d+\b'
    
    def replace_number(match):
        number = match.group(0)
        # Vérifier que le nombre est dans la plage 0-1000
        try:
            num_value = int(number)
            if 0 <= num_value <= 1000:
                return normalize_number(number, fst)
        except ValueError:
            pass
        return number
    
    # Remplacer tous les nombres dans le texte
    normalized = re.sub(number_pattern, replace_number, text)
    return normalized

# ============================================
# INTERFACE EN LIGNE DE COMMANDE
# ============================================

def print_usage():
    """Affiche l'aide d'utilisation"""
    print("Usage:")
    print(f"  python {sys.argv[0]} <texte>")
    print()
    print("Exemples:")
    print(f'  python {sys.argv[0]} "5 bonbons"')
    print(f'  python {sys.argv[0]} "J\'ai 25 ans et 3 chats"')
    print(f'  python {sys.argv[0]} "Il y a 100 personnes"')
    print()
    print("Options:")
    print(f"  -h, --help     Affiche cette aide")
    print(f"  -f, --file     Spécifie un fichier FAR différent")
    print()
    print(f"Fichier FAR utilisé: {FAR_FILE}")

def main():
    """Point d'entrée principal"""
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("❌ ERREUR: Aucun texte fourni.", file=sys.stderr)
        print()
        print_usage()
        sys.exit(1)
    
    # Gérer l'aide
    if sys.argv[1] in ["-h", "--help"]:
        print_usage()
        sys.exit(0)
    
    # Gérer le fichier FAR personnalisé
    far_file = FAR_FILE
    text_arg_index = 1
    
    if sys.argv[1] in ["-f", "--file"]:
        if len(sys.argv) < 4:
            print("❌ ERREUR: Fichier FAR et texte requis.", file=sys.stderr)
            print_usage()
            sys.exit(1)
        far_file = sys.argv[2]
        text_arg_index = 3
    
    # Récupérer le texte à normaliser
    input_text = sys.argv[text_arg_index]
    
    # Charger le FST
    fst = load_fst_from_far(far_file)
    
    # Normaliser le texte
    normalized_text = normalize_text(input_text, fst)
    
    # Afficher le résultat
    print(normalized_text)

# ============================================
# MODE INTERACTIF (BONUS)
# ============================================

def interactive_mode():
    """Mode interactif pour tester plusieurs phrases"""
    print("="*60)
    print("MODE INTERACTIF - Normalisation de nombres")
    print("="*60)
    print(f"Fichier FAR: {FAR_FILE}")
    print("Tapez votre texte (ou 'quit' pour quitter)")
    print("="*60)
    print()
    
    # Charger le FST une seule fois
    fst = load_fst_from_far()
    
    while True:
        try:
            # Lire l'entrée utilisateur
            user_input = input("Texte> ").strip()
            
            # Vérifier la commande de sortie
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Au revoir!")
                break
            
            # Ignorer les lignes vides
            if not user_input:
                continue
            
            # Normaliser et afficher
            result = normalize_text(user_input, fst)
            print(f"  → {result}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}", file=sys.stderr)

# ============================================
# EXÉCUTION
# ============================================

if __name__ == "__main__":
    # Si aucun argument, lancer le mode interactif
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()