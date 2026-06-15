from extractor import (
    extract_company,
    extract_role
)

from notion_service import create_job_entry
from notion_duplicate import job_exists

message = """
MathCo Graduate Hiring Program – 2027 Batch

Position: AI Analyst

Compensation:
₹6 LPA Fixed CTC
"""

company = extract_company(message)
role = extract_role(message)

print(company)
print(role)

if job_exists(company, role):

    print("⚠️ Already Exists")

else:

    create_job_entry(
        company,
        role,
        message
    )