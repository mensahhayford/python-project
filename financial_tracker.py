name = input("What's your name? ")
print("Welcome to your Apex Tracker,", name, "!")
print("Let's check where you actually stand.")

goal = input("What is your 6-month goal in a few words? ")

target_score = float(input("What score are you aiming for as a number, e.g. 75? "))
current_score = float(input("What is your most recent real score? "))

income = float(input("What's your weekly income/allowance (GHS)? "))
expenses = float(input("What are your total weekly expenses (GHS)? "))
savings = income - expenses

gap = target_score - current_score

print("\n--- GOAL STATUS ---")
print("Your goal:", goal)

if current_score >= target_score:
    print("You are AT or ABOVE your target.")
    print("Score:", current_score, "| Target:", target_score)
    print("Time to raise the target — staying here is playing it safe.")
elif gap <= 5:
    print("You are close. Only", gap, "points away from", target_score)
    print("This is winnable in weeks, not months, if you stay consistent.")
else:
    print("You are", gap, "points away from", target_score)
    print("This needs a real weekly system, not a single push at the end.")

print()
print("--- MONEY STATUS ---")
print("Weekly income:", income)
print("Weekly expenses:", expenses)
print("Weekly savings:", savings)

if savings < 0:
    print("You are spending more than you earn. This needs fixing before anything else.")
elif savings == 0:
    print("You are breaking even. No room for goals that cost money yet.")
else:
    yearly_projection = savings * 52
    print("At this rate, you'd save GHS", yearly_projection, "in a year.")

print()
print("Good luck!")
weekly_log = []
weekly_log.append(current_score)
weekly_log.append(savings)
print("--- THIS WEEK'S LOGGED NUMBERS ---")
for entry in weekly_log:
    print("Logged value:", entry)

    print()