import csv
from prettytable import PrettyTable, FRAME, ALL
from colorama import init, Fore, Style

init(autoreset=True)

TOLERANCE = 5
MAX_TRAINERS = 10
MIN_TRAINERS = 2

global_balance = []
compensations = []
total_given = []
total_received = []
ban_matrix = []
balance_table = None
balance_csv_rows = []
pokemon_balance_table = PrettyTable()
pokemon_balance_table.hrules = ALL

# -------------------- PARSING & VALIDATION --------------------

def parse_numbers_and_bans(raw_values):
    numbers = []
    bans = []
    for val in raw_values:
        val = val.strip()
        if val.endswith("!"):
            val = val[:-1]
            banned = True
        else:
            banned = False
        if not val.isdigit():
            raise ValueError("Invalid value: " + val)
        number = int(val)
        if number < 0:
            raise ValueError("Value cannot be negative: " + str(number))
        numbers.append(number)
        bans.append(banned)
    return numbers, bans

def validate_data(trainers, data):
    if len(trainers) < MIN_TRAINERS or len(trainers) > MAX_TRAINERS:
        raise ValueError(f"Number of trainers must be between {MIN_TRAINERS} and {MAX_TRAINERS}.")
    for line in data:
        if len(line) - 1 != len(trainers):
            raise ValueError(f"Incorrect number of fields in line: {line}")
        for val in line[1:]:
            if val.endswith("!"):
                val = val[:-1]
            if not val.strip().isdigit():
                raise ValueError(f"Invalid number: {val}")

# -------------------- COMPENSATION --------------------

def compensate_with_balance(trainers):
    global compensations, total_given, total_received
    n = len(trainers)
    compensations = [[0 for _ in range(n)] for _ in range(n)]
    total_given = [0] * n
    total_received = [0] * n

    for given, received in global_balance:
        for i in range(n):
            total_given[i] += given[i]
            total_received[i] += received[i]

    balance = [total_received[i] - total_given[i] for i in range(n)]

    while True:
        surplus = [(i, s) for i, s in enumerate(balance) if s > 0]
        deficit = [(i, -s) for i, s in enumerate(balance) if s < 0]
        if not surplus or not deficit:
            break

        for i, amount in surplus:
            if amount <= 0:
                continue
            total_deficit = sum([x[1] for x in deficit])
            for j, need in deficit:
                if amount <= 0:
                    break
                ratio = need / total_deficit
                transfer = min(amount, round(ratio * amount))
                compensations[i][j] += transfer
                balance[i] -= transfer
                balance[j] += transfer
                amount -= transfer

# -------------------- DISTRIBUTION ALGORITHM --------------------

def balanced_matrix(trainers, numbers, bans, pokemon_name):
    global balance_table, balance_csv_rows, pokemon_balance_table
    n = len(trainers)
    total = sum(numbers)

    eligible_receivers = [not bans[i] for i in range(n)]
    receivers_count = sum(eligible_receivers)
    demand = [0] * n
    if receivers_count > 0:
        base = total // receivers_count
        extra = total % receivers_count
        for i in range(n):
            if eligible_receivers[i]:
                demand[i] = base + (1 if extra > 0 else 0)
                extra -= 1

    supply = numbers[:]
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    iteration = 0
    max_iterations = 2000

    while sum(supply) > 0 and iteration < max_iterations:
        iteration += 1
        moved = False
        for i in range(n):
            if supply[i] <= 0:
                continue
            needs = []
            total_receivers = sum(1 for j in range(n) if not bans[j] and j != i)
            for j in range(n):
                if i == j or bans[j]:
                    continue
                current = sum(matrix[k][j] for k in range(n))
                if total_receivers == 1:
                    needs.append((j, 99999))  # no limit if only one can receive
                elif current < demand[j]:
                    needs.append((j, demand[j] - current))

            if not needs:
                continue
            needs.sort(key=lambda x: -x[1])
            for j, _ in needs:
                matrix[i][j] += 1
                supply[i] -= 1
                moved = True
                break
        if not moved:
            break

    given = [sum(matrix[i]) for i in range(n)]
    received = [sum(matrix[j][i] for j in range(n)) for i in range(n)]

    global_balance.append((given[:], received[:]))  # ensure copies are stored
    ban_matrix.append(bans)

    if balance_table is None:
        balance_columns = ["Pokemon"]
        for t in trainers:
            balance_columns.append(f"{t} gave")
            balance_columns.append(f"{t} received")
        balance_table = PrettyTable(balance_columns)
        balance_table.hrules = FRAME
        balance_csv_rows.append(balance_columns)
        pokemon_balance_table.field_names = balance_columns

    row_txt = [pokemon_name]
    row_csv = [pokemon_name]
    for i in range(n):
        diff = abs(received[i] - given[i])
        blue = Fore.BLUE if received[i] == 0 and bans[i] else ""
        color = ""
        #if not blue:
            #color = Fore.RED if diff > TOLERANCE else ""
        row_txt.append(f"{color}{given[i]}{Style.RESET_ALL}")
        row_txt.append(f"{blue}{received[i]}{Style.RESET_ALL}")
        row_csv.append(given[i])
        row_csv.append(received[i])

    balance_table.add_row(row_txt)
    pokemon_balance_table.add_row(row_txt)
    balance_csv_rows.append(row_csv)

    return matrix

# -------------------- DISPLAY & EXPORT --------------------

def print_final_summary(trainers):
    n = len(trainers)
    sum_given = [sum(given[i] for given, _ in global_balance) for i in range(n)]
    sum_received = [sum(received[i] for _, received in global_balance) for i in range(n)]

    total_row = ["TOTAL"]
    for i in range(n):
        total_row.append(sum_given[i])
        total_row.append(sum_received[i])

    pokemon_balance_table.add_row(total_row)
    balance_csv_rows.append(["TOTAL"] + sum_given + sum_received)

    with open("pokemon_balance.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(pokemon_balance_table.field_names)
        for row in pokemon_balance_table._rows:
            writer.writerow([str(cell) for cell in row])

def show_all(trainers, trade_table):
    print("\n1. TRADE MATRIX:")
    print(trade_table)
    print("\n2. POKÉMON BALANCE:")
    print(pokemon_balance_table)
    print("Made by ChatGPT and Viteckpl - what a cooperation!")

# -------------------- MAIN --------------------

with open("poczki.txt", "r", encoding="utf-8") as f:
    trainers = f.readline().strip().split(",")
    raw_data = [line.strip().split(",") for line in f if line.strip() != ""]

try:
    validate_data(trainers, raw_data)
except Exception as e:
    print("❌ ERROR IN POCZKI.TXT:", e)
    exit(1)

n = len(trainers)
column_headers = ["Pokemon"]
pairs = []
for i in range(n):
    for j in range(n):
        if i != j:
            column_headers.append(f"{trainers[i]} → {trainers[j]}")
            pairs.append(f"{trainers[i]} → {trainers[j]}")

trade_table = PrettyTable(column_headers)
total_trades = {p: 0 for p in pairs}

for line in raw_data:
    pokemon = line[0]
    numbers, bans = parse_numbers_and_bans(line[1:])
    matrix = balanced_matrix(trainers, numbers, bans, pokemon)
    row = [pokemon]
    for i in range(n):
        for j in range(n):
            if i != j:
                row.append(matrix[i][j])
                pair = f"{trainers[i]} → {trainers[j]}"
                total_trades[pair] += matrix[i][j]
    trade_table.add_row(row, divider=True)

summary_row = ["TOTAL"] + [total_trades[p] for p in pairs]
trade_table.add_row(summary_row)

compensate_with_balance(trainers)
print_final_summary(trainers)
show_all(trainers, trade_table)