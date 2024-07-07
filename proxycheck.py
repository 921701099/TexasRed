import threading
import queue
import requests

q = queue.Queue()
valid = []

with open("Free_Proxy_List.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",proxies={"http": proxy, "https:": proxy})

        except:
            continue
        if res.status_code == 200:
            write_proxies(proxy)
def write_proxies(proxy):
    with open("workin_proxy.txt", "a") as f:
        f.write(proxy + "\n")

def proxycheckstart():
    for _ in range(10):
        threading.Thread(target=check_proxies).start()

proxycheckstart()