import pynini
from pynini.lib import pynutil
import re

# ==========================================
# 1. Fonctions Helper
# ==========================================

def apply_fst(text, fst):
    """Applique un FST à une chaîne d'entrée."""
    try:
        return(pynini.shortestpath(pynini.accep(text, token_type='utf8') @ fst).string("utf8"))
    except Exception as e:
        return(f"Error: {e}, for input:'{text}'")

def I_O_FST(input_str: str, output_str: str) -> pynini.Fst:
    """Creates an FST mapping input_str to output_str."""
    input_str = str(input_str)
    output_str = str(output_str)
    input_accep = pynini.accep(input_str, token_type="utf8")
    output_accep = pynini.accep(output_str, token_type="utf8")
    fst = pynini.cross(input_accep, output_accep)
    return fst.optimize()

# ==========================================
# 2. Définition des FSTs de base (0-69)
# ==========================================

# Unités (0-9)
digit_map = {
    "0": "zéro", "1": "un", "2": "deux", "3": "trois", "4": "quatre",
    "5": "cinq", "6": "six", "7": "sept", "8": "huit", "9": "neuf",
}
fst_units_list = [I_O_FST(k, v) for k, v in digit_map.items()]
fst_units_base = pynini.union(*fst_units_list).optimize()

# Gestion des zéros non significatifs (ex: 09 -> neuf)
delete_zero = pynutil.delete("0")
fst_zero_prefix = delete_zero.star
fst_units_with_leading_zeros = (fst_zero_prefix + fst_units_base).optimize()

# Teens (10-19)
teens_map = {
    "10": "dix", "11": "onze", "12": "douze", "13": "treize", "14": "quatorze",
    "15": "quinze", "16": "seize", "17": "dix-sept", "18": "dix-huit", "19": "dix-neuf",
}
fst_teens = pynini.union(*[I_O_FST(k, v) for k, v in teens_map.items()]).optimize()

# Dizaines (20, 30, 40, 50, 60)
tens_digit_map = {
    "2": "vingt", "3": "trente", "4": "quarante", "5": "cinquante", "6": "soixante",
}
fst_tens_digit_list = [I_O_FST(digit, text) for digit, text in tens_digit_map.items()]
fst_tens_digits = pynini.union(*fst_tens_digit_list).optimize()
fst_eat_zero = I_O_FST("0", "") # "0" -> <eps>
fst_exact_tens = (fst_tens_digits + fst_eat_zero).optimize()

# Dizaines composées (21-29, 31-39... 61-69)
compound_units_map = {k: v for k, v in digit_map.items() if (k != "0" and k != "1")}
fst_compound_units_digits = pynini.union(*[I_O_FST(num, text) for num, text in compound_units_map.items()]).optimize()

fst_insert_space = I_O_FST("", "-") # Insertion de tiret
fst_compound_tens_standard = (fst_tens_digits + fst_insert_space + fst_compound_units_digits).optimize()

# Gestion du "et un" (21, 31, 41, 51, 61)
fst_one_unit = I_O_FST("1", "un").optimize()
fst_insert_et_space = I_O_FST("", "-et-")
fst_compound_et_un = (fst_tens_digits + fst_insert_et_space + fst_one_unit).optimize()

fst_compound_tens = pynini.union(fst_compound_tens_standard, fst_compound_et_un).optimize()

# ==========================================
# 3. Définition des FSTs complexes (70-99)
# ==========================================

# Réutilisation de 10-19
fst_tens_10_to_19 = fst_teens # Alias

# 70-79
# A. Soixante-dix (70)
fst_70 = I_O_FST("7", "soixante-").optimize() + I_O_FST("0", "dix").optimize()
# B. Soixante-et-onze (71)
fst_71 = I_O_FST("7", "soixante").optimize() + fst_insert_et_space + I_O_FST("1", "onze").optimize()
# C. Soixante-douze à 79
fst_tens_12_to_19 = pynini.union(*[I_O_FST(k[1], v) for k, v in teens_map.items() if k not in ["10", "11"]]).optimize()
fst_72_to_79 = I_O_FST("7", "soixante-").optimize() + fst_tens_12_to_19.optimize()
fst_70_to_79 = pynini.union(fst_70, fst_71, fst_72_to_79).optimize()

# 80-89
# Unités 2 à 9 avec tiret
fst_units_2_to_9 = pynini.union(*[I_O_FST(k, "-" + v) for k, v in digit_map.items() if k not in ["0", "1"]]).optimize()

# A. Quatre-vingts (80) - cas particulier du 's'
fst_80 = I_O_FST("8", "quatre-vingt").optimize() + I_O_FST("0", "s").optimize()
# B. Quatre-vingt-un (81)
fst_81 = I_O_FST("8", "quatre-vingt").optimize() + fst_insert_space + I_O_FST("1", "un").optimize()
# C. 82-89
fst_82_to_89 = I_O_FST("8", "quatre-vingt").optimize() + fst_units_2_to_9.optimize()
fst_80_to_89 = pynini.union(fst_80, fst_81, fst_82_to_89).optimize()

# 90-99
fst_quatre_vingt_prefix = I_O_FST("9", "quatre-vingt").optimize()
# A. 90
fst_90 = fst_quatre_vingt_prefix + I_O_FST("0", "-dix").optimize()
# B. 91-99 (réutilisation teens)
fst_91_to_99_suffix = pynini.union(*[I_O_FST(k[1], "-" + v) for k, v in teens_map.items() if k != "10"]).optimize()
fst_91_to_99 = fst_quatre_vingt_prefix + fst_91_to_99_suffix
fst_90_to_99 = pynini.union(fst_90, fst_91_to_99).optimize()

# Union 70-99
fst_70_to_99 = pynini.union(fst_70_to_79, fst_80_to_89, fst_90_to_99).optimize()

# ==========================================
# 4. Construction Intermédiaire (0-99)
# ==========================================

# Nécessaire pour les centaines composées (ex: cent-vingt-cinq)
# On a besoin d'un FST qui gère "01", "05", "10", "99" sur 2 chiffres
fst_01_to_09 = (pynutil.delete("0").optimize() + fst_units_base).optimize()

fst_double_digit_00_to_99 = pynini.union(
    I_O_FST("00", ""),           # 00 -> <epsilon>
    fst_01_to_09,                # 01-09
    fst_teens,                   # 10-19
    fst_exact_tens,              # 20, 30...
    fst_compound_tens,           # 21-69
    fst_70_to_99                 # 70-99
).optimize()

# ==========================================
# 5. Les Centaines (100-999) et 1000
# ==========================================

# Unités centaines (2-9)
units_hundreds_map = {k: v for k, v in digit_map.items() if k not in ["0", "1"]}
fst_units_2_to_9_digit = pynini.union(*[I_O_FST(k, v) for k, v in units_hundreds_map.items()]).optimize()

# 100-199
fst_100_exact = I_O_FST("1", "cent").optimize() + I_O_FST("00", "").optimize()
fst_101_to_199 = I_O_FST("1", "cent").optimize() + fst_insert_space + fst_double_digit_00_to_99.optimize()
fst_100_to_199 = pynini.union(fst_100_exact, fst_101_to_199).optimize()

# 200-999
# Exact (200, 300... -> cents avec s)
fst_exact_hundreds = (fst_units_2_to_9_digit + fst_insert_space + I_O_FST("", "cents")).optimize() + I_O_FST("00", "").optimize()
# Composé (201, 999... -> cent sans s)
fst_composed_hundreds = (fst_units_2_to_9_digit + fst_insert_space + I_O_FST("", "cent")).optimize() + fst_insert_space + fst_double_digit_00_to_99.optimize()
fst_200_to_999 = pynini.union(fst_exact_hundreds, fst_composed_hundreds).optimize()

# 1000
fst_1000 = I_O_FST("1000", "mille").optimize()

# ==========================================
# 6. UNION FINALE (0-1000)
# ==========================================

fst_00_to_1000 = pynini.union(
    fst_units_with_leading_zeros, # 0-9
    fst_teens,                    # 10-19
    fst_exact_tens,               # 20,30...
    fst_compound_tens,            # 21-69
    fst_70_to_99,                 # 70-99
    fst_100_to_199,               # 100-199
    fst_200_to_999,               # 200-999
    fst_1000                      # 1000
).optimize()

# ==========================================
# 7. Fonction de Normalisation de phrase
# ==========================================

def normalize_cardinals_in_sentence(sentence: str, cardinal_fst: pynini.Fst) -> str:
    """
    Parcourt une phrase, identifie les séquences de chiffres consécutifs
    et les remplace par leur équivalent textuel en utilisant un FST.
    """
    number_pattern = r'\b\d{1,4}\b' # Max 4 chiffres (pour 1000)

    def replace_match(match: re.Match) -> str:
        number_str = match.group(0)
        # Sécurité : le FST s'arrête à 1000
        if len(number_str) > 4:
            return number_str
        try:
            return apply_fst(number_str, cardinal_fst)
        except:
            return number_str

    result_sentence = re.sub(number_pattern, replace_match, sentence)
    return result_sentence

# ==========================================
# 8. Sauvegarde du FST sur disque
# ==========================================


# ==========================================
# 9. Main execution block
# ==========================================

if __name__ == "__main__":
    print("=== Test unitaire (0-20) ===")
    for i in range(21):
        res = apply_fst(str(i), fst_00_to_1000)
        print(f"{i} -> {res}")
    
    print("\n=== Test cas complexes ===")
    complex_cases = ["71", "80", "81", "200", "201", "1000"]
    for val in complex_cases:
        print(f"{val} -> {apply_fst(val, fst_00_to_1000)}")

    print("\n=== Test de phrase ===")
    phrase_test = "J'ai 3 chiens. Le prix est de 200 euros. Il en restait 71."
    phrase_normalisee = normalize_cardinals_in_sentence(phrase_test, fst_00_to_1000)
    print(f"Originale : {phrase_test}")
    print(f"Normalisée: {phrase_normalisee}")