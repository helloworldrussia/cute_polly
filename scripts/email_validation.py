import time

import psycopg2
import requests


def connection():
    conn = psycopg2.connect(
        database="cp",
        user="postgres",
        password="78756",
        host="194.58.107.50",
        port="5432")
    return conn


def get_data():
    conn = connection()
    cursor = conn.cursor()
    sql_string = "SELECT email FROM mailer_address"
    cursor.execute(sql_string)
    data = cursor.fetchall()
    return data


def change_status(email):
    status = 'invalid-email'
    conn = connection()
    cursor = conn.cursor()
    sql_string = f"UPDATE mailer_address SET status = '{status}' WHERE email = '{email}'"
    cursor.execute(sql_string)
    conn.commit()


def validate(email: str):
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email})

    status = response.json()['status']
    if status == "invalid":
        return False
    return True


def dispatcher():
    data = get_data()
    for email in data:
        time.sleep(3)
        email = email[0]
        if validate(email):
            print(f'success {email}')
        else:
            print(f'FAIL {email}')
            change_status(email)


if __name__ == "__main__":
    dispatcher()
