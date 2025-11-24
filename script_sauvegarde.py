from Text_Normalisation_Cardinaux_0_a_1000 import *


# ============================================
# Creation du fichier FAR
# ============================================

def create_far_archive(output_path="cardinal_numbers.far"):
    """
    Crée un fichier FAR contenant le FST de normalisation
    """
    
    # print("Construction du FST cardinal...")
    # cardinal_fst = build_cardinal_fst()
    
    print(f"Création du fichier FAR: {output_path}")
    
    # Écrire le fichier FAR avec pynini.Far en mode écriture
    far_writer = pynini.Far(output_path, mode="w")
    
    # Ajouter le FST avec la méthode add()
    far_writer.add("CARDINAL", fst_00_to_1000)
    print(f"  ✓ FST 'CARDINAL' ajouté au FAR")
    
    # Fermer le writer
    far_writer.close()
    
    print(f"✓ Fichier FAR créé avec succès: {output_path}")
    return output_path

#============================================
# 4. FONCTION DE TEST
# ============================================

def test_fst_from_far(far_path="cardinal_numbers.far"):
    """
    Teste le FST depuis le fichier FAR
    """
    print("\n" + "="*50)
    print("TEST DU FST DEPUIS LE FICHIER FAR")
    print("="*50)
    
    # Lire le fichier FAR
    far_reader = pynini.Far(far_path, mode="r")
    
    # Récupérer le FST
    cardinal_fst = far_reader["CARDINAL"]
    
    # Tests
    test_cases = ["0", "7", "15", "42", "99", "100", "256", "1000"]
    
    for number in test_cases:
        try:
            result = apply_fst(number, cardinal_fst)
            print(f"{number:>4} → {result}")
        except Exception as e:
            print(f"{number:>4} → ERREUR: {e}")
    
    # Fermer le reader
    far_reader.close()

# ============================================
# 5. FONCTION PRINCIPALE
# ============================================

def main():
    """Point d'entrée principal"""
    
    # Créer le fichier FAR
    far_path = create_far_archive("cardinal_numbers.far")
    
    # Tester le FST
    test_fst_from_far(far_path)
    
    print("\n✓ Processus terminé avec succès!")
    
    
if __name__ == "__main__":
    main()