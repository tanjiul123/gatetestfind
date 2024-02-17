import requests
from bs4 import BeautifulSoup
import re

def get_random_user_agent():
    # This function is simplified to return a static user agent string
    # You can replace this string with any valid user agent
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

def check_gateway(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None
    bsoup = BeautifulSoup(response.text, 'html.parser')
    
    payment_gateways = {
        # Payment gateways patterns simplified for readability
        # Add or adjust patterns as needed
    }

    detected_gateway = None

    for pg, patterns in payment_gateways.items():
        if len(patterns) > 1:
            script_elements = bsoup.find_all('script', {'src': patterns[1]['src']})
        else:
            script_elements = []
        script_elements += bsoup.find_all('script', {'src': patterns[2]['src']}) if len(patterns) > 2 else []
        script_elements += bsoup.find_all('script', {'src': patterns[3]['src']}) if len(patterns) > 3 else []

        if bsoup.find(*patterns) or any(script_element for script_element in script_elements) or bsoup.find(string=re.compile(rf'.*{pg}.*', re.IGNORECASE)):
            detected_gateway = pg
            break

    return url, detected_gateway

def add_https_if_missing(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url

def process_url(url):
    url = url.strip()
    url = add_https_if_missing(url)
    try:
        result = check_gateway(url)
        if result and result[1]:
            url, gateway = result
            print(f"Detected payment gateway for {url}: {gateway}")
        else:
            print(f"No payment gateway detected for {url}.")
    except Exception as e:
        print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    user_input_url = input("Enter the site link without http/https: ")
    process_url(user_input_url)
