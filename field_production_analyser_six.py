# PETROLEUM FIELD PRODUCTION ANALYSER
# ═══════════════════════════════════════
# STAGE 1: EXPANDED DATASET
# ═══════════════════════════════════════

field_data = {
    "Well_Alpha": {
        "production": [520, 480, 510, 490,
                       530, 470, 500, 495,
                       515, 505],
        "location": "Northern Block",
        "type": "Oil"
    },
    "Well_Beta": {
        "production": [310, 295, 320, 285,
                       300, 315, 290, 305,
                       295, 310],
        "location": "Southern Block",
        "type": "Oil"
    },
    "Well_Gamma": {
        "production": [750, 720, 780, 710,
                       760, 740, 725, 755,
                       745, 730],
        "location": "Northern Block",
        "type": "Gas condensate"
    },
    "Well_Delta": {
        "production": [180, 165, 190, 175,
                       185, 170, 195, 160,
                       188, 177],
        "location": "Eastern Block",
        "type": "Oil"
    }
}

print("Dataset loaded successfully.")
print(f"Wells in field: {len(field_data)}")

# ═══════════════════════════════════════
# STAGE 2: ANALYSIS FUNCTIONS
# ═══════════════════════════════════════

def calculate_average(production_list):
    return sum(production_list) / len(production_list)

def calculate_variance(production_list):
    """
    Variance = difference between best and worst day.
    Low variance = consistent well.
    High variance = inconsistent well.
    """
    return max(production_list) - min(production_list)

def classify_well(average_production):
    """
    Classify well performance based on average output.
    """
    if average_production >= 700:
        return "HIGH PERFORMER"
    elif average_production >= 450:
        return "SOLID PERFORMER"
    elif average_production >= 250:
        return "AVERAGE PERFORMER"
    else:
        return "UNDERPERFORMER — review required"

def find_best_day(production_list):
    best = max(production_list)
    day = production_list.index(best) + 1
    return best, day

def find_worst_day(production_list):
    worst = min(production_list)
    day = production_list.index(worst) + 1
    return worst, day

# ═══════════════════════════════════════
# STAGE 3: INDIVIDUAL WELL REPORT
# ═══════════════════════════════════════

def generate_well_report(well_name, well_info):
    production = well_info["production"]
    avg = calculate_average(production)
    variance = calculate_variance(production)
    classification = classify_well(avg)
    best_output, best_day = find_best_day(production)
    worst_output, worst_day = find_worst_day(production)
    total = sum(production)

    print(f"\n{'='*45}")
    print(f"  WELL REPORT: {well_name}")
    print(f"{'='*45}")
    print(f"  Location    : {well_info['location']}")
    print(f"  Type        : {well_info['type']}")
    print(f"  Classification : {classification}")
    print(f"  {'─'*40}")
    print(f"  Average daily  : {avg:.1f} bbl")
    print(f"  Total (10 days): {total} bbl")
    print(f"  Best day       : Day {best_day} — {best_output} bbl")
    print(f"  Worst day      : Day {worst_day} — {worst_output} bbl")
    print(f"  Consistency    : {variance} bbl variance")

    if variance > 100:
        print(f"  ⚠ HIGH VARIANCE — investigate cause")
    else:
        print(f"  ✓ CONSISTENT production pattern")

generate_well_report("Well_Alpha", field_data["Well_Alpha"])

# ═══════════════════════════════════════
# STAGE 4: FIELD SUMMARY REPORT
# ═══════════════════════════════════════

def generate_field_summary():
    print(f"\n{'#'*45}")
    print(f"  FIELD SUMMARY REPORT")
    print(f"{'#'*45}")

    total_field_production = 0
    best_well = ""
    best_well_avg = 0
    most_consistent_well = ""
    lowest_variance = float('inf')

    for well_name, well_info in field_data.items():
        production = well_info["production"]
        avg = calculate_average(production)
        variance = calculate_variance(production)
        total_field_production += sum(production)

        # Find best performing well
        if avg > best_well_avg:
            best_well_avg = avg
            best_well = well_name

        # Find most consistent well
        if variance < lowest_variance:
            lowest_variance = variance
            most_consistent_well = well_name

    print(f"\n  Total field production : {total_field_production} bbl")
    print(f"  Wells analysed         : {len(field_data)}")
    print(f"  Best performer         : {best_well}")
    print(f"  Most consistent        : {most_consistent_well}")
    print(f"  Average per well       : "
          f"{total_field_production/len(field_data):.0f} bbl/10 days")        
    


def run_analyser():
    print("\nPETROLEUM FIELD PRODUCTION ANALYSER")
    print("Built by: [Your Name]")
    print("Purpose: Well performance analysis\n")

    # Generate individual reports
    for well_name, well_info in field_data.items():
        generate_well_report(well_name, well_info)

    # Generate field summary
    generate_field_summary()

    print(f"\n{'='*45}")
    print("  Analysis complete.")
    print(f"{'='*45}\n")


run_analyser()