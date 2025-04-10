# Changelog – PoGo Trade Counter

## v1.0 – Initial Version
- Designed for **3 trainers only**.
- Based on **fixed calculations for 3-way trades**:
  - Trainer 1 <-> Trainer 2
  - Trainer 2 <-> Trainer 3
  - Trainer 3 <-> Trainer 1
- No flexibility or configurability.
- No CSV output.
- No handling of preference restrictions (`!`).
- No balancing or compensation.
- Results shown in one static PrettyTable.

## v2.0 – Multi-Trainer Rewrite & Core Redesign
- Full rewrite to support **2 to 10 trainers**.
- Introduced **dynamic matrix-based distribution algorithm**.
- Implemented preference bans (`!`) to avoid receiving unwanted Pokémon.
- Introduced compensation phase to rebalance total send/receive mismatches.
- Added final balance validation.
- Created output tables:
  - Trade matrix
  - Balance matrix
  - Pokémon-level summary

## v2.5 – Visual Improvements & Exporting
- Standardized table appearance using PrettyTable borders.
- Exported results to:
  - `pokemon_balance.csv`
- Colored red values for trainers exceeding tolerance.
- Colored blue for zero received when banned.
- Added total summary rows.

## v2.6 – English Refactor
- Translated all variables, functions, comments, and labels to English.
- Improved naming clarity (`trainers`, `bans`, `matrix`, etc.).
- Renamed all files and output variables.

## v2.7 – Algorithm Improvements
- Allowed trade limits to be ignored when only one trainer could receive.
- Increased iteration cap to ensure more accurate rebalancing.
- Prevented over-restrictive blocking in distribution phase.
- Ensured all remaining Pokémon were assigned if possible.

## v2.8 – Final Stability Enhancements
- Validated final receive/give totals by cross-referencing tables.
- Added handling for unexpected input errors.
- Removed obsolete balance summary table (replaced by summary row in Pokémon balance).
- Confirmed zero-difference final balances on extensive test sets.

---
**Created by ChatGPT and Viteckpl. What a cooperation!**

