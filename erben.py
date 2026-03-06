import re
from collections import Counter

soubor = r"C:\Users\HynekMayrhofer\Downloads\sps.txt"

with open(soubor, "r", encoding="utf-8") as f:
    obsah = f.read().lower()

# rozdělení na slova
slova = re.findall(r"\b[a-zá-ž]+\b", obsah)

# 1. počet slov seřazený podle četnosti
print("Slova seřazená podle četnosti:")
pocet_slov = Counter(slova)

for slovo, pocet in pocet_slov.most_common():
    print(slovo, ":", pocet)

# 2. počet písmen seřazený podle četnosti
print("\nPísmena seřazená podle četnosti:")
pismena = Counter(obsah)

for znak, pocet in pismena.most_common():
    if znak.isalpha():
        print(znak, ":", pocet)

# 3. počet 8-písmenných slov
osm_pismena = [slovo for slovo in slova if len(slovo) == 8]

print("\nPočet 8-písmenných slov:", len(osm_pismena))