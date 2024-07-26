# Description:                 This Python script generates an insurance policy receipt for customers.
# Author:                      Abdul Rahman
# Date:                        2024-07-19 -- 2024-07-24

import datetime
import time
import sys
import FormatValues as FV  # Importing the FormatValues library as FV

# Initialize default values
default_values = [
    1944,  # Policy Number
    869.00,  # Base Premium
    0.25,  # Discount for additional cars
    130.00,  # Extra Liability Cost
    86.00,  # Glass Coverage Cost
    58.00,  # Loaner Car Cost
    0.15,  # HST Rate
    39.99  # Processing Fee
]

# Load default values from const.dat or initialize if not present
try:
    with open('const.dat', 'r') as file:
        lines = file.readlines()
        values = [float(line.strip()) for line in lines]
        if len(values) != 8:
            raise ValueError("Incorrect number of values in const.dat")
except (FileNotFoundError, ValueError):
    with open('const.dat', 'w') as file:
        for value in default_values:
            file.write(f"{value}\n")
    values = default_values

# Define program constants by loading values from const.dat
policy_number = int(values[0])
BASE_PREMIUM = values[1]
ADDITIONAL_DISCOUNT = values[2]  # Discount for additional cars
EXTRA_LIABILITY_COST = values[3]
GLASS_COVERAGE_COST = values[4]
LOANER_CAR_COST = values[5]
HST_RATE = values[6]
PROCESSING_FEE = values[7]

# Define the progress bar function
def ProgressBar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

# Get user input
def get_user_input():
    first_name = input("Enter first name: ").title()
    last_name = input("Enter last name: ").title()
    address = input("Enter address: ")
    city = input("Enter city: ").title()
    province = input("Enter province (##): ").upper()
    while not FV.validate_province(province):
        print("Invalid province code. Please enter a valid two-letter province code.")
        province = input("Enter province (##): ").upper()
    postal_code = input("Enter postal code (#9# 9#9): ")
    formatted_postal_code = FV.format_and_validate_postal_code(postal_code)
    while formatted_postal_code is None:
        print("Invalid postal code. Please enter a valid postal code.")
        postal_code = input("Enter postal code (#9# 9#9): ")
        formatted_postal_code = FV.format_and_validate_postal_code(postal_code)
    phone_number = input("Enter phone number (999-999-9999): ")
    num_cars = int(input("Enter number of cars: "))
    extra_liability = input("Extra liability coverage (Y/N): ").upper() == 'Y'
    glass_coverage = input("Glass coverage (Y/N): ").upper() == 'Y'
    loaner_car = input("Loaner car coverage (Y/N): ").upper() == 'Y'
    insured_value = input("Insured value up to $1,000,000 (Y/N): ").upper()
    payment_option = input("Pay in full or monthly (F/M): ").upper()
    down_payment = float(input("Enter down payment (if any): ")) if payment_option == 'M' else 0

    # Get claim information
    claim_number = input("Enter claim number: ")
    claim_date = input("Enter claim date (YYYY-MM-DD): ")
    try:
        claim_date = datetime.datetime.strptime(claim_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        claim_date = input("Enter claim date (YYYY-MM-DD): ")
        claim_date = datetime.datetime.strptime(claim_date, "%Y-%m-%d")
    claim_amount = float(input("Enter claim amount: "))

    return (first_name, last_name, address, city, province, formatted_postal_code, phone_number, num_cars,
            extra_liability, glass_coverage, loaner_car, insured_value, payment_option, down_payment,
            claim_number, claim_date, claim_amount)

# Calculate insurance premium
def calculate_premium(user_input):
    (first_name, last_name, address, city, province, postal_code, phone_number, num_cars,
     extra_liability, glass_coverage, loaner_car, insured_value, payment_option, down_payment,
     claim_number, claim_date, claim_amount) = user_input

    # Calculate base premium for the first car
    base_premium_first_car = BASE_PREMIUM

    # Calculate the premium for additional cars with the discount
    base_premium_additional_cars = (num_cars - 1) * BASE_PREMIUM * (1 - ADDITIONAL_DISCOUNT)

    # Calculate total base premium
    total_base_premium = base_premium_first_car + base_premium_additional_cars

    # Calculate extra coverage costs
    extra_costs = 0
    if extra_liability:
        extra_costs += num_cars * EXTRA_LIABILITY_COST
    if glass_coverage:
        extra_costs += num_cars * GLASS_COVERAGE_COST
    if loaner_car:
        extra_costs += num_cars * LOANER_CAR_COST

    # Calculate the subtotal premium
    subtotal_premium = total_base_premium + extra_costs

    # HST calculation
    hst = subtotal_premium * HST_RATE
    total_premium_with_hst = subtotal_premium + hst

    if payment_option == 'M':
        total_owing = total_premium_with_hst - down_payment
        monthly_payment = (total_owing + PROCESSING_FEE) / 8
    else:
        total_owing = total_premium_with_hst
        monthly_payment = 0

    return total_base_premium, extra_costs, subtotal_premium, hst, total_premium_with_hst, total_owing, monthly_payment


#  display receipt
def display_receipt(user_input, premium_details, claims, policy_number):
    (first_name, last_name, address, city, province, postal_code, phone_number, num_cars,
     extra_liability, glass_coverage, loaner_car, insured_value, payment_option, down_payment,
     claim_number, claim_date, claim_amount) = user_input

    total_base_premium, extra_costs, subtotal_premium, hst, total_premium_with_hst, total_owing, monthly_payment = premium_details

    # Formatting for display
    BasePremiumDsp = f"${total_base_premium:,.2f}"
    ExtraCostsDsp = f"${extra_costs:,.2f}"
    SubtotalPremiumDsp = f"${subtotal_premium:,.2f}"
    HstDsp = f"${hst:,.2f}"
    TotalPremiumWithHstDsp = f"${total_premium_with_hst:,.2f}"
    TotalOwingDsp = f"${total_owing:,.2f}"
    MonthlyPaymentDsp = f"${monthly_payment:,.2f}"
    DownPaymentDsp = f"${down_payment:,.2f}"
    ProcessingFeeDsp = f"${PROCESSING_FEE:,.2f}"
    ClaimAmountDsp = f"${claim_amount:,.2f}"
    full_name = first_name + " " + last_name

    print()
    print("     +---------------------------------------------------------------+")
    print("     |                     ONE STOP INSURANCE COMPANY                |")
    print("     +---------------------------------------------------------------+")
    print("                              CUSTOMER DETAILS                    ")
    print()
    print(f"      Policy #:   {int(policy_number)}                                Date: {datetime.date.today()} ")
    print()
    print(f"      {full_name:<20s}                                {phone_number}")
    print(f"      {address}, {postal_code}")
    print(f"      {city}, {province}")
    print()
    print()
    print("                         POLICY COVERAGE DETAILS        ")
    print()
    print("                         Extra             Glass            Loaner Car  ")
    print(f"      Car #           Liability          Coverage            Coverage  ")
    print("      ----------------------------------------------------------------")
    for i in range(1, num_cars + 1):
        print(f"        {i:<5}             {'Y' if extra_liability else 'N'}                 {'Y' if glass_coverage else 'N'}                   {'Y' if loaner_car else 'N'}")
    print("      ----------------------------------------------------------------")
    print("                                 PAYMENT DETAILS              ")
    print()
    print(f"      Premium for {num_cars:<2} vehicle(s):                            {BasePremiumDsp:>10s}")
    print(f"      Extra coverage costs:                                 {ExtraCostsDsp:>10s}")
    print(f"      -------------------------                             ----------")
    print(f"      Subtotal:                                             {SubtotalPremiumDsp:>10s}")
    print(f"      HST:                                                  {HstDsp:>10s}")
    print(f"      -------------------------                             ----------")
    print(f"      Total:                                                {TotalPremiumWithHstDsp:>10s}")
    print(f"      Payment Option:                                          {'Monthly' if payment_option == 'M' else 'Full'} ")
    if payment_option == 'M':
        print(f"      Down Payment:                                        -{DownPaymentDsp:>10s}")
        print(f"      -------------------------                             ----------")
        print(f"      Total Owing:                                          {TotalOwingDsp:>10s}")
        print(f"      Processing Fee:                                       {ProcessingFeeDsp:>10s}")
        print(f"      Monthly Payment:                                      {MonthlyPaymentDsp:>10s}")
        print()
        today = datetime.date.today()
        first_payment_date = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        print(f"      First Payment Due:                                    {first_payment_date}")
    print("      ----------------------------------------------------------------")
    print("                             PREVIOUS CLAIMS               ")
    print()
    print("      Claim #                   Claim Date                      Amount")
    print("      ----------------------------------------------------------------")
    for claim in claims:
        formatted_claim_date = claim[1].strftime("%Y-%m-%d")
        print(f"       {claim[0]:<9}                {formatted_claim_date:<11}                 {ClaimAmountDsp:>10} ")
    print("      ----------------------------------------------------------------")
    print("                   Thank You For Choosing One Stop Insurance!            ")
    print()
    print()


# Show blinking message
def show_blinking_message(message, duration, repetitions):
    for _ in range(repetitions):
        print(message, end='\r')
        time.sleep(duration)
        sys.stdout.write('\033[2K\r')  # Clears the entire line and carriage returns
        time.sleep(duration)
    print(f"\r{message}")

# Save policy data to a new file
def save_policy_data(policy_number, user_input, total_premium_pre_tax):
    try:
        with open('policy.dat', 'a') as file:
            file.write(f"{policy_number}, {user_input[0]}, {user_input[1]}, {user_input[2]}, {user_input[3]}, {user_input[4]}, {user_input[5]}, {user_input[6]}, {user_input[7]}, {user_input[8]}, {user_input[9]}, {user_input[10]}, {user_input[11]}, {user_input[12]}, {user_input[13]}, {user_input[14]}, {user_input[15]}, {total_premium_pre_tax:.2f}\n")
        print("Policy data saved to policy.dat")
    except IOError:
        print("Error: Unable to write policy data to file.")

# Save default values to const.dat
# Save default values to const.dat
def save_default_values(values):
    try:
        with open('const.dat', 'w') as file:
            for value in values:
                file.write(f"{value}\n")
    except IOError:
        print("Error: Unable to write to const.dat file.")


# Main Program starts here.
policy_number = values[0]

while True:
    # Gather User inputs.
    claims = []
    user_input = get_user_input()
    
    # Perform required calculations.
    premium_details = calculate_premium(user_input)
    claims.append((user_input[-3], user_input[-2], user_input[-1]))
    
    # Display results.
    display_receipt(user_input, premium_details, claims, policy_number)

    # Show progress bar
    TotalIterations = 30
    Message = "Saving Policy Data ..."
    for i in range(TotalIterations + 1):
        time.sleep(0.1)
        ProgressBar(i, TotalIterations, prefix=Message, suffix='Complete', length=50)

    print()
    show_blinking_message("Policy data has been saved", 0.5, 6)

    # Save the policy data
    save_policy_data(policy_number, user_input, premium_details[0] / (1 + HST_RATE))

    # Update policy number and save it
    policy_number += 1
    values[0] = policy_number
    save_default_values(values)

    # Ask if user wants to enter another customer
    another = input("Do you want to enter another customer? (Y/N): ").upper()
    if another != 'Y':
        break

# Any housekeeping duties at the end of the program.
