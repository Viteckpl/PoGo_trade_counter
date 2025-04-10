# PoGo Trade Counter

## 🇬🇧 Description (English)

**PoGo Trade Counter** is a tool for fair Pokemon distribution among 2 to 10 trainers. The script analyzes a `poczki.txt` file containing each trainer's available Pokemon and preferences, then produces balanced trade plans and readable tables.

### Features:
- Supports 2 to 10 trainers
- Respects bans on receiving specific Pokemon (indicated by `!` after number)
- Aims for each trainer to give and receive similar numbers of Pokemon
- Compensates trade imbalances with other Pokemon
- Exports result tables to CSV files

### `poczki.txt` file structure
```
Viteck,Kielbas,Nomad
Poczek_A,145,331,456
Poczek_B,282!,497,65
Poczek_C,170,492!,140
Poczek_D,205!,269,253!
```
- The first line lists trainer names.
- Each subsequent line shows how many of each Pokemon a trainer owns. `!` means they do not want to receive that Pokemon.

### Running the script:
```bash
python main.py
```

Results will be shown and saved to:
- `pokemon_balance.csv`
---
**Made by ChatGPT and Viteckpl – what a cooperation!**

---

## 🇵🇱 Opis (Polski)

**PoGo Trade Counter** to narzędzie do sprawiedliwego rozdzielania wymian Pokemonów pomiędzy 2 do 10 trenerami. Program analizuje plik `poczki.txt` zawierający dane o posiadanych Pokemonach i preferencjach trenerów. Na podstawie tych danych dokonuje zbilansowanego przydziału wymian i generuje czytelne tabele.

### Cechy:
- Obsługuje od 2 do 10 trenerów
- Uwzględnia zakazy przyjmowania wybranych Pokemonów (`!` po liczbie)
- Stara się zapewnić, by każdy oddał i otrzymał zbliżoną liczbę Pokemonów
- Kompensuje nierównowagi za pomocą innych Pokemonów
- Eksportuje tabele do plików CSV

### Struktura pliku `poczki.txt`
```
Viteck,Kielbas,Nomad
Poczek_A,145,331,456
Poczek_B,282!,497,65
Poczek_C,170,492!,140
Poczek_D,205!,269,253!
```
- Pierwsza linia zawiera nazwiska trenerów.
- Kolejne linie opisują ile każdy z nich ma danego Pokemona. `!` oznacza, że nie chce go otrzymać.

### Uruchomienie:
```bash
python main.py
```

Wyniki zostaną wyświetlone oraz zapisane w plikach:
- `pokemon_balance.csv`