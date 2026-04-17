"""Generate 200+ synthetic Indian legal cases for the SQLite database."""
import random
import sqlite3
from datetime import datetime, timedelta
from app.sql.database import init_db, get_db_path

random.seed(42)

COURTS = [
    "Supreme Court of India", "Delhi High Court", "Bombay High Court",
    "Madras High Court", "Calcutta High Court", "Karnataka High Court",
    "Allahabad High Court", "Gujarat High Court", "Rajasthan High Court",
    "Kerala High Court", "Punjab & Haryana High Court", "Telangana High Court",
    "Patna High Court", "Gauhati High Court",
]

JUDGES = [
    "Justice D.Y. Chandrachud", "Justice Sanjiv Khanna", "Justice B.R. Gavai",
    "Justice Surya Kant", "Justice Hima Kohli", "Justice Abhay S. Oka",
    "Justice Vikram Nath", "Justice J.K. Maheshwari", "Justice M.M. Sundresh",
    "Justice Bela M. Trivedi", "Justice P.S. Narasimha", "Justice Manoj Misra",
    "Justice Rajesh Bindal", "Justice Aravind Kumar", "Justice Pamidighantam Sri Narasimha",
]

CASE_TYPES = ["Civil", "Criminal", "Constitutional", "Corporate", "Family", "Tax", "Labor", "Property", "Environmental", "IP"]

LEGAL_AREAS = [
    "Fundamental Rights", "Criminal Law", "Contract Law", "Property Law",
    "Family Law", "Tax Law", "Corporate Law", "Environmental Law", "Labor Law", "IP Law",
]

ARTICLES = {
    "Fundamental Rights": ["14", "19", "21", "25", "32"],
    "Criminal Law": ["20", "21", "22"],
    "Contract Law": [],
    "Property Law": ["19(1)(f)", "300A"],
    "Family Law": ["14", "15", "25"],
    "Tax Law": ["265", "266", "269"],
    "Corporate Law": ["19(1)(g)", "301"],
    "Environmental Law": ["21", "48A", "51A(g)"],
    "Labor Law": ["14", "16", "19", "23", "24"],
    "IP Law": ["19(1)(a)", "19(1)(g)"],
}

STATUSES = ["pending", "won", "lost", "settled", "appealed"]
PRIORITIES = ["low", "medium", "high", "critical"]

CLIENT_NAMES = [
    "Tata Motors Ltd.", "Reliance Industries", "Infosys Ltd.", "Wipro Technologies",
    "Adani Enterprises", "Mahindra Group", "Bajaj Auto", "Larsen & Toubro",
    "Dr. Ramesh Sharma", "Smt. Priya Patel", "Shri Vikram Singh", "Ms. Ananya Desai",
    "Kumar & Associates", "Delhi Municipal Corp.", "State of Maharashtra",
    "Union of India", "Central Board of Direct Taxes", "SEBI",
    "M/s Sunrise Exports", "M/s GreenTech Solutions", "ABC Pharmaceuticals Pvt. Ltd.",
    "National Highway Authority", "Food Corporation of India",
    "Smt. Lakshmi Devi", "Shri Rajendra Prasad", "Ms. Fatima Khan",
]

OPPOSING = [
    "Adv. Harish Salve", "Adv. Mukul Rohatgi", "Adv. Kapil Sibal",
    "Adv. Abhishek Manu Singhvi", "Adv. Fali S. Nariman", "Adv. K.K. Venugopal",
    "Adv. Gopal Subramanium", "AG of India", "State Prosecutor",
    "Adv. Indira Jaising", "Adv. Prashant Bhushan", "Adv. Soli Sorabjee",
]

CASE_TITLE_TEMPLATES = [
    "{client} v. State of {state}",
    "{client} v. Union of India",
    "{client} v. {opposing_party}",
    "State of {state} v. {client}",
    "{client} & Ors. v. {opposing_party} & Anr.",
    "In Re: {client}",
]

STATES = [
    "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat",
    "West Bengal", "Rajasthan", "Uttar Pradesh", "Kerala", "Telangana",
]


def random_date(start_year=2015, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d")


def generate_case(i: int) -> dict:
    legal_area = random.choice(LEGAL_AREAS)
    case_type = random.choice(CASE_TYPES)
    client = random.choice(CLIENT_NAMES)
    state = random.choice(STATES)
    status = random.choice(STATUSES)
    filing = random_date(2015, 2023)

    articles = ARTICLES.get(legal_area, [])
    invoked = ",".join(random.sample(articles, min(len(articles), random.randint(1, 3)))) if articles else ""

    title_template = random.choice(CASE_TITLE_TEMPLATES)
    title = title_template.format(
        client=client,
        state=state,
        opposing_party=random.choice(CLIENT_NAMES),
    )

    decision_date = None
    outcome_summary = None
    damages_awarded = None
    if status in ("won", "lost", "settled"):
        decision_date = random_date(int(filing[:4]) + 1, 2025)
        if status == "won":
            outcome_summary = f"Court ruled in favor of {client}. Key arguments on {legal_area} upheld."
            damages_awarded = random.choice([0, 50000, 100000, 500000, 1000000, 5000000, 10000000])
        elif status == "lost":
            outcome_summary = f"Court ruled against {client}. {legal_area} arguments rejected."
            damages_awarded = 0
        else:
            outcome_summary = f"Parties reached settlement. {legal_area} matter resolved out of court."
            damages_awarded = random.choice([25000, 100000, 250000, 500000])

    return {
        "case_number": f"CASE/{random.choice(['CIV','CRM','CON','COR'])}/{2015 + i % 10}/{1000 + i}",
        "case_title": title,
        "court": random.choice(COURTS),
        "judge": random.choice(JUDGES),
        "filing_date": filing,
        "decision_date": decision_date,
        "status": status,
        "case_type": case_type,
        "legal_area": legal_area,
        "articles_invoked": invoked,
        "opposing_counsel": random.choice(OPPOSING),
        "client_name": client,
        "summary": f"Case concerning {legal_area.lower()} involving {client}. Filed as {case_type.lower()} matter in {random.choice(COURTS)}.",
        "outcome_summary": outcome_summary,
        "damages_claimed": random.choice([0, 100000, 500000, 1000000, 5000000, 10000000, 50000000]),
        "damages_awarded": damages_awarded,
        "priority": random.choice(PRIORITIES),
    }


def seed():
    init_db()
    conn = sqlite3.connect(get_db_path())
    cases = [generate_case(i) for i in range(220)]
    for c in cases:
        try:
            conn.execute(
                """INSERT OR IGNORE INTO cases
                (case_number, case_title, court, judge, filing_date, decision_date,
                 status, case_type, legal_area, articles_invoked, opposing_counsel,
                 client_name, summary, outcome_summary, damages_claimed, damages_awarded, priority)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    c["case_number"], c["case_title"], c["court"], c["judge"],
                    c["filing_date"], c["decision_date"], c["status"], c["case_type"],
                    c["legal_area"], c["articles_invoked"], c["opposing_counsel"],
                    c["client_name"], c["summary"], c["outcome_summary"],
                    c["damages_claimed"], c["damages_awarded"], c["priority"],
                ),
            )
        except Exception:
            pass
    conn.commit()
    print(f"Seeded {conn.execute('SELECT COUNT(*) FROM cases').fetchone()[0]} cases.")
    conn.close()


if __name__ == "__main__":
    seed()
