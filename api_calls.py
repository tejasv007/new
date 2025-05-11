import requests

# Step 1: Define your details
name = "John Doe"
regNo = "REG12347"
email = "john@example.com"

# Determine which question to solve based on regNo
last_digit = int(regNo[-1])
if last_digit % 2 == 0:
    print("Even digit: Solve Q 2")
else:
    print("Odd digit: Solve Q 1")


init_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
payload = {
    "name": name,
    "regNo": regNo,
    "email": email
}

response = requests.post(init_url, json=payload)
if response.status_code != 200:
    print("Failed to generate webhook. Status code:", response.status_code)
    print("Response:", response.text)
    exit()

data = response.json()
webhook_url = data.get("webhook")
access_token = data.get("accessToken")

if not webhook_url or not access_token:
    print("Invalid response. Missing webhook or accessToken.")
    exit()


final_sql_query = """
SELECT 
    e.FIRST_NAME,
    e.LAST_NAME,
    d.DEPARTMENT_NAME,
    SUM(p.AMOUNT) AS TOTAL_PAYMENT
FROM 
    EMPLOYEE e
JOIN 
    PAYMENTS p ON e.EMP_ID = p.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
GROUP BY 
    e.EMP_ID, e.FIRST_NAME, e.LAST_NAME, d.DEPARTMENT_NAME
ORDER BY 
    TOTAL_PAYMENT DESC
LIMIT 1;
""".strip()

submission_url = webhook_url  
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
submission_payload = {
    "finalQuery": final_sql_query
}

submit_response = requests.post(submission_url, json=submission_payload, headers=headers)
if submit_response.status_code == 200:
    print("Solution submitted successfully.")
else:
    print("Submission failed:", submit_response.status_code)
    print("Details:", submit_response.text)