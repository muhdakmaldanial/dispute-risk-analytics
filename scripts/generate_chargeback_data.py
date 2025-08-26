import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

RECORD_COUNT = 12345

REASON_CODES = [
    'R101 Unauthorized Transaction',
    'R102 Services Not Received',
    'R103 Goods Not as Described',
    'R104 Duplicate Charge',
    'R105 Cancelled Subscription',
    'R106 Incorrect Amount',
    'R107 Late Settlement',
    'R108 Credit Not Processed',
    'R109 Fraudulent Activity',
    'R110 Customer Dispute',
    'R111 Technical Error',
    'R112 Billing Issue',
    'R113 Unauthorized Recurring Charge',
    'R114 Failed Delivery',
    'R115 Payment Method Error'
]

STAGES = ['First Chargeback', 'Pre-Arbitration', 'Arbitration']

STATUS_LIST = [
    'Submitted', 'Under Review', 'Additional Info Requested', 'Representment Received',
    'Won', 'Lost', 'Merchant Refunded', 'Withdrawn by Cardholder', 'Timed Out',
    'Manual Review Required', 'Pending Arbitration', 'Pre-Arbitration Submitted',
    'Pre-Arbitration Rejected', 'Arbitration Filed', 'Arbitration Closed'
]

REASON_CODE_FRAUD_TYPE_MAP = {
    'R109 Fraudulent Activity': ['Phishing', 'Account Takeover', 'Stolen Card', 'Friendly Fraud'],
    'R101 Unauthorized Transaction': ['Stolen Card', 'Account Takeover'],
    'R113 Unauthorized Recurring Charge': ['Friendly Fraud']
}

CURRENCIES = ['USD', 'MYR', 'SGD', 'EUR', 'THB', 'AUD', 'GBP', 'JPY', 'KRW', 'HKD',
              'IDR', 'INR', 'CNY', 'CAD', 'NZD', 'CHF', 'PHP', 'AED', 'ZAR', 'BDT']

BANKS = ['Maybank', 'CIMB', 'HSBC', 'RHB', 'Public Bank',
         'UOB', 'OCBC', 'AmBank', 'Bank Islam', 'Standard Chartered']

CHANNELS = ['Issuer Portal', 'In-House Review', 'Merchant Coordination',
            'Automated Dispute System', 'Manual Investigation']
TRANSACTION_TYPES = ['Online', 'POS', 'QR', 'Subscription', 'Wallet']
CARD_TYPES = ['Debit', 'Credit', 'Prepaid']
CUSTOMER_SEGMENTS = ['Regular', 'Premium', 'Business']
FRAUD_TYPES = ['Phishing', 'Account Takeover',
               'Friendly Fraud', 'Stolen Card', 'Synthetic Identity']
# MERCHANTS = ['Shopee', 'Lazada', 'Netflix', 'AirAsia']
MERCHANT_CATEGORY_MAP = {
    # E-commerce
    'Shopee': 'E-commerce',
    'Lazada': 'E-commerce',
    'Zalora': 'E-commerce',
    'Amazon': 'E-commerce',
    'eBay': 'E-commerce',
    'AliExpress': 'E-commerce',
    'Qoo10': 'E-commerce',
    'PG Mall': 'E-commerce',
    'Sephora': 'E-commerce',

    # Travel
    'AirAsia': 'Travel',
    'Malaysia Airlines': 'Travel',
    'Booking.com': 'Travel',
    'Agoda': 'Travel',
    'Expedia': 'Travel',
    'Traveloka': 'Travel',
    'Klook': 'Travel',
    'Trip.com': 'Travel',

    # Entertainment / Subscription
    'Netflix': 'Entertainment',
    'Spotify': 'Subscription',
    'YouTube Premium': 'Subscription',
    'Apple Music': 'Subscription',
    'Disney+': 'Entertainment',
    'Viu': 'Entertainment',
    'Astro': 'Subscription',
    'HBO Go': 'Subscription',

    # Fashion & Retail
    'Uniqlo': 'Fashion',
    'H&M': 'Fashion',
    'Nike': 'Fashion',
    'Adidas': 'Fashion',
    'Charles & Keith': 'Fashion',
    'Padini': 'Fashion',
    'Watsons': 'Retail',
    'Guardian': 'Retail',
    'IKEA': 'Retail',
    'Popular': 'Retail',
    'MR.DIY': 'Retail',

    # Food & Beverage
    'McDonald': 'Food & Beverage',
    'KFC': 'Food & Beverage',
    'Starbucks': 'Food & Beverage',
    'Domino': 'Food & Beverage',
    'Texas Chicken': 'Food & Beverage',
    'GrabFood': 'Food & Beverage',
    'foodpanda': 'Food & Beverage',
    'Secret Recipe': 'Food & Beverage',
    'Tealive': 'Food & Beverage',
    'Boost Juice': 'Food & Beverage',

    # Grocery / Hypermarket
    'Tesco': 'Grocery',
    'Giant': 'Grocery',
    'AEON': 'Grocery',
    'Jaya Grocer': 'Grocery',
    'Mydin': 'Grocery',
    'Econsave': 'Grocery',
    'FamilyMart': 'Grocery',

    # Transport / Mobility
    'Grab': 'Transport',
    'TNG eWallet': 'Transport',
    'Setel': 'Transport',
    'MAXIS': 'Telecom',
    'Digi': 'Telecom',
    'Celcom': 'Telecom'
}
ANALYSTS = ['Akmal Danial', 'Nadiah Saat', 'Shazlin Suhaime']
FAST_TRACK_REASONS = [
    'R101 Unauthorized Transaction',
    'R109 Fraudulent Activity',
    'R113 Unauthorized Recurring Charge'
]

# New dictionary mapping stages to appropriate statuses
STATUS_BY_STAGE = {
    'First Chargeback': {
        'statuses': ['Submitted', 'Under Review', 'Additional Info Requested', 'Representment Received',
                     'Won', 'Lost', 'Merchant Refunded', 'Withdrawn by Cardholder', 'Timed Out'],
        'weights':  [0.15, 0.1, 0.08, 0.05, 0.25, 0.15, 0.08, 0.03, 0.11]
    },
    'Pre-Arbitration': {
        'statuses': ['Pre-Arbitration Submitted', 'Pre-Arbitration Rejected', 'Won', 'Lost',
                     'Merchant Refunded', 'Withdrawn by Cardholder', 'Manual Review Required', 'Pending Arbitration'],
        'weights':  [0.2, 0.1, 0.2, 0.2, 0.1, 0.05, 0.1, 0.05]
    },
    'Arbitration': {
        'statuses': ['Arbitration Filed', 'Arbitration Closed', 'Won', 'Lost', 'Timed Out'],
        'weights':  [0.2, 0.2, 0.2, 0.3, 0.1]
    }
}

unique_refs = random.sample(range(100000, 999999), RECORD_COUNT)
MERCHANTS = list(MERCHANT_CATEGORY_MAP.keys())


def generate_record(index):
    reason = random.choice(REASON_CODES)

    transaction_date = fake.date_between_dates(
        date_start=datetime(2023, 1, 1),
        date_end=datetime(2025, 12, 15)
    )

    settlement_delay = random.randint(7, 30)
    settlement_date = transaction_date + timedelta(days=settlement_delay)

    if reason in FAST_TRACK_REASONS:
        filing_delay = random.randint(1, 30)
    else:
        filing_delay = random.randint(7, 90)

    filing_date = settlement_date + timedelta(days=min(filing_delay, 120))

    amount = round(random.uniform(5, 2000), 2)
    stage = random.choice(STAGES)
    status_choices = STATUS_BY_STAGE[stage]
    status = random.choices(
        status_choices['statuses'], weights=status_choices['weights'])[0]
    currency = random.choice(CURRENCIES)
    issuer = random.choice(BANKS)
    merchant = random.choice(MERCHANTS)
    merchant_category = MERCHANT_CATEGORY_MAP[merchant]
    analyst = random.choice(ANALYSTS)
    card_type = random.choice(CARD_TYPES)
    channel = random.choice(CHANNELS)
    tx_type = random.choice(TRANSACTION_TYPES)
    segment = random.choice(CUSTOMER_SEGMENTS)
    risk_score = random.randint(30, 90)
    cardholder_country = random.choices(
        ['Malaysia', 'Thailand', 'Singapore', 'Australia', 'Indonesia', 'Philippines', 'Vietnam', 'India',
         'Hong Kong', 'Japan', 'South Korea', 'United States', 'United Kingdom'],
        weights=[0.35, 0.12, 0.12, 0.08, 0.07, 0.06,
                 0.05, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02]
    )[0]
    sla_met = 'Yes' if filing_delay <= 45 else 'No'

    fraud_types_possible = REASON_CODE_FRAUD_TYPE_MAP.get(reason, None)
    if fraud_types_possible:
        is_fraud = 'Yes'
        fraud_type = random.choice(fraud_types_possible)
    else:
        is_fraud = random.choices(['Yes', 'No'], weights=[0.1, 0.9])[0]
        fraud_type = random.choice(FRAUD_TYPES) if is_fraud == 'Yes' else '-'

    urgency = 'High' if is_fraud == 'Yes' and (amount > 500 or risk_score > 80) else (
              'Medium' if amount > 1000 or risk_score > 60 else 'Low')

    return {
        "Chargeback Reference Number": f"CBR{unique_refs[index]}",
        "Transaction Date": transaction_date,
        "Filing Date": filing_date,
        "Settlement Date": settlement_date,
        "Issuer Bank": issuer,
        "Merchant Name": merchant,
        "Merchant Category": merchant_category,
        "Transaction Amount": amount,
        "Currency": currency,
        "Reason Code": reason,
        "Chargeback Stage": stage,
        "Status": status,
        "Analyst": analyst,
        "SLA Met": sla_met,
        "Days to File": (filing_date - transaction_date).days,
        "Days to Resolve": (filing_date - settlement_date).days,
        "Resolution Channel": channel,
        "Merchant Risk Score": risk_score,
        "Transaction Type": tx_type,
        "Card Type": card_type,
        "Customer Segment": segment,
        "Fraudulent Transaction": is_fraud,
        "Fraud Type": fraud_type,
        "Case Urgency": urgency,
        "Cardholder Country": cardholder_country
    }


def generate_dataset():
    data = [generate_record(i) for i in range(RECORD_COUNT)]
    df = pd.DataFrame(data)
    df.to_csv("chargeback_analytics_dataset.csv", index=False)
    print(
        f"✅ Dataset with {RECORD_COUNT} records saved as 'chargeback_analytics_dataset.csv'")


if __name__ == "__main__":
    generate_dataset()
