import csv
from prettytable import PrettyTable
from colorama import init, Fore, Style

init(autoreset=True)

TOLERANCJA = 5
MAX_TRENEROW = 10
MIN_TRENEROW = 2

def parse_liczby_wzbronione(raw_values):
    liczby = []
    zabronione = []
    for val in raw_values:
        val = val.strip()
        if val.endswith("!"):
            val = val[:-1]
            zakaz = True
        else:
            zakaz = False
        if not val.isdigit():
            raise ValueError("Niepoprawna wartość: " + val)
        liczba = int(val)
        if liczba < 0:
            raise ValueError("Liczba nie może być ujemna: " + str(liczba))
        liczby.append(liczba)
        zabronione.append(zakaz)
    return liczby, zabronione

def waliduj_dane(trenerzy, dane):
    if len(trenerzy) < MIN_TRENEROW or len(trenerzy) > MAX_TRENEROW:
        raise ValueError(f"Liczba trenerów musi być między {MIN_TRENEROW} a {MAX_TRENEROW}.")
    for linia in dane:
        if len(linia) - 1 != len(trenerzy):
            raise ValueError(f"Zła liczba pól w linii: {linia}")
        for val in linia[1:]:
            if val.endswith("!"):
                val = val[:-1]
            if not val.strip().isdigit():
                raise ValueError(f"Niepoprawna liczba: {val}")

def zbilansowana_macierz(trenerzy, liczby, zakazy):
    n = len(trenerzy)
    total = sum(liczby)
    target = total / n

    macierz = [[0 for _ in range(n)] for _ in range(n)]
    supply = liczby[:]
    demand = [target] * n

    # Oznacz ile każdy już otrzymał
    received = [0] * n

    while sum(supply) > 0:
        moved = False
        for i in range(n):
            if supply[i] <= 0:
                continue
            # Poszukaj odbiorcy z największym deficytem
            najlepszy_j = None
            max_diff = -1
            for j in range(n):
                if i == j or zakazy[j]:
                    continue
                diff = demand[j] - received[j]
                if diff > max_diff:
                    max_diff = diff
                    najlepszy_j = j
            if najlepszy_j is not None and max_diff > 0:
                macierz[i][najlepszy_j] += 1
                supply[i] -= 1
                received[najlepszy_j] += 1
                moved = True
        if not moved:
            break

    # Wyrównanie niedoborów innymi poczkami (globalna kompensacja)
    remaining = sum(supply)
    i = 0
    while remaining > 0:
        if supply[i] > 0:
            for j in range(n):
                if i != j and not zakazy[j]:
                    macierz[i][j] += 1
                    supply[i] -= 1
                    received[j] += 1
                    remaining -= 1
                    break
        i = (i + 1) % n

    return macierz


def wypisz_wymiany(trenerzy, macierz, pokemon, tabela, suma_wymian):
    n = len(trenerzy)
    row = [pokemon]
    for i in range(n):
        for j in range(n):
            if i != j:
                row.append(macierz[i][j])
                para = f"{trenerzy[i]} → {trenerzy[j]}"
                suma_wymian[para] += macierz[i][j]
    tabela.add_row(row, divider=True)

def wypisz_bilans(trenerzy, macierz, liczby, zakazy, pokemon, bilans_txt, bilans_csv, sumy_globalne=None):
    n = len(trenerzy)
    otrzymane = [sum(macierz[j][i] for j in range(n)) for i in range(n)]
    oddane = [sum(macierz[i][j] for j in range(n)) for i in range(n)]

    row_txt = [pokemon]
    row_csv = [pokemon]

    for i in range(n):
        roznica = abs(otrzymane[i] - oddane[i])
        niebieski = Fore.BLUE if otrzymane[i] == 0 and zakazy[i] else ""
        kolor = ""
        if niebieski == "":
            kolor = Fore.RED if roznica > TOLERANCJA else ""

        row_txt.append(f"{kolor}{oddane[i]:>5}{Style.RESET_ALL}")
        row_txt.append(f"{niebieski}{otrzymane[i]:>5}{Style.RESET_ALL}")
        row_csv.append(oddane[i])
        row_csv.append(otrzymane[i])

        if sumy_globalne is not None:
            sumy_globalne["oddane"][i] += oddane[i]
            sumy_globalne["otrzymane"][i] += otrzymane[i]

    bilans_txt.add_row(row_txt)
    bilans_csv.append(row_csv)

def wypisz_sume_globalna(trenerzy, bilans_txt, bilans_csv, sumy_globalne):
    row_txt = ["TOTAL"]
    row_csv = ["TOTAL"]
    for i in range(len(trenerzy)):
        row_txt.append(f"{sumy_globalne['oddane'][i]:>5}")
        row_txt.append(f"{sumy_globalne['otrzymane'][i]:>5}")
        row_csv.append(sumy_globalne['oddane'][i])
        row_csv.append(sumy_globalne['otrzymane'][i])
    bilans_txt.add_row(row_txt)
    bilans_csv.append(row_csv)

def wypisz_saldo(trenerzy, sumy_globalne):
    saldo = [sumy_globalne["otrzymane"][i] - sumy_globalne["oddane"][i] for i in range(len(trenerzy))]
    with open("saldo_debug.txt", "w", encoding="utf-8") as f:
        print("\n🔍 SALDO KOŃCOWE:")
        f.write("Saldo końcowe (otrzymane - oddane):\n")
        for i, t in enumerate(trenerzy):
            info = f"{t}: {saldo[i]}"
            print(info)
            f.write(info + "\n")

log_nieudanych = []

with open("poczki.txt", "r", encoding="utf-8") as f:
    trenerzy = f.readline().strip().split(",")
    dane = [line.strip().split(",") for line in f if line.strip() != ""]

try:
    waliduj_dane(trenerzy, dane)
except Exception as e:
    print("BŁĄD W PLIKU POCZKI.TXT:", e)
    exit(1)

n = len(trenerzy)
kolumny_wymian = ["Pokemon"]
pary = []
for i in range(n):
    for j in range(n):
        if i != j:
            kolumny_wymian.append(f"{trenerzy[i]} → {trenerzy[j]}")
            pary.append(f"{trenerzy[i]} → {trenerzy[j]}")

tabela_wymian = PrettyTable(kolumny_wymian)
suma_wymian = {p: 0 for p in pary}

kolumny_bilans = ["Pokemon"]
for t in trenerzy:
    kolumny_bilans.append(f"{t} oddał")
    kolumny_bilans.append(f"{t} dostał")

tabela_bilans = PrettyTable(kolumny_bilans)
bilans_csv_rows = [kolumny_bilans]
sumy_globalne = {"oddane": [0] * n, "otrzymane": [0] * n}

for line in dane:
    pokemon = line[0]
    liczby, zakazy = parse_liczby_wzbronione(line[1:])
    macierz = zbilansowana_macierz(trenerzy, liczby, zakazy)
    wypisz_wymiany(trenerzy, macierz, pokemon, tabela_wymian, suma_wymian)
    wypisz_bilans(trenerzy, macierz, liczby, zakazy, pokemon, tabela_bilans, bilans_csv_rows, sumy_globalne=sumy_globalne)

suma_row = ["RAZEM"] + [suma_wymian[p] for p in pary]
tabela_wymian.add_row(suma_row)
wypisz_sume_globalna(trenerzy, tabela_bilans, bilans_csv_rows, sumy_globalne)
wypisz_saldo(trenerzy, sumy_globalne)

print(tabela_wymian)
print(tabela_bilans)

with open("wynik.txt", "w", encoding="utf-8") as f:
    f.write(str(tabela_wymian))

with open("bilans.txt", "w", encoding="utf-8") as f:
    f.write(str(tabela_bilans))

with open("wynik.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(kolumny_wymian)
    for row in tabela_wymian._rows:
        writer.writerow(row)

with open("bilans.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(bilans_csv_rows)

if log_nieudanych:
    print("\n🛑 Problemy z rozdzieleniem niektórych poczków:")
    for log in log_nieudanych:
        print(log)
    with open("problemy.txt", "w", encoding="utf-8") as f:
        for log in log_nieudanych:
            f.write(log + "\n")
else:
    print("\n✅ Wszystkie poczki udało się przydzielić i zbilansować.")
