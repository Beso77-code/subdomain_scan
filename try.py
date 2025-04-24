from pathlib import Path
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed

user_domain = input("Enter your site: ")
thread_num = int(input("Enter your thread max 10 (1-10): "))
wordlist = Path.cwd() / "Subdomain.txt"

def load_sublist(sub_file):
    with open(sub_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_sub(sub):
    domain_full = f"{sub}.{user_domain}"
    try:
        result = dns.resolver.resolve(domain_full, 'A')
        for ip in result:
            print(f"found --> {ip.to_text()} {domain_full}")
    except:
        return None

subdomain_list = load_sublist(wordlist)
thread_result = []

with ThreadPoolExecutor(max_workers=thread_num) as ex:
    process = [ex.submit(check_sub, sub) for sub in subdomain_list]
    for r in as_completed(process):
        results = r.result()
        if results:
            print(results)
        thread_result.append(results)

print("done process")
