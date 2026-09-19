# NESTED LOOP — processing multiple
# categories of data

well_data = {
    "Well_A": [520, 480, 510, 490, 530],
    "Well_B": [310, 295, 320, 285, 300],
    "Well_C": [750, 720, 780, 710, 760]
}

# Outer loop: goes through each well
# Inner loop: goes through each day's data

for well_name, production in well_data.items():
    print(f"\nAnalysing {well_name}:")

    # Inner loop: check each day's production
    for day_number, barrels in enumerate(production, 1):
        if barrels >= 700:
            status = "EXCELLENT"
        elif barrels >= 500:
            status = "GOOD"
        elif barrels >= 300:
            status = "AVERAGE"
        else:
            status = "LOW"

        print(f"  Day {day_number}: {barrels} bbl — {status}")