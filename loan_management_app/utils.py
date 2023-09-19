import math
from datetime import datetime, timedelta

def calculate_emi_schedule(principal, annual_interest_rate, tenure, disbursement_date):
    monthly_interest_rate = annual_interest_rate / 12 / 100

    emi = principal * monthly_interest_rate * math.pow(1 + monthly_interest_rate, tenure) / (math.pow(1 + monthly_interest_rate, tenure) - 1)

    emi_schedule = []
    remaining_principal = principal
    for month in range(1, tenure + 1):
        interest_payment = remaining_principal * monthly_interest_rate
        principal_payment = emi - interest_payment
        remaining_principal -= principal_payment

        due_date = disbursement_date + timedelta(days=30 * month)

        emi_schedule.append({
            "Date": due_date.strftime("%Y-%m-%d"),
            "Amount_due": round(emi, 2)
        })

    return emi_schedule