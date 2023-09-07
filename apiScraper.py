import requests
from bs4 import BeautifulSoup
import re
import os
import random

def scrape_for_sk_phrases_and_links(url, base_url, limit):
    print(f'Scraping URL: {url}')
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Invalid URL: {url}')
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find phrases starting with "sk-" and are exactly 46 characters long
    text = soup.get_text()
    sk_phrases = re.findall(r'sk-\w{44}', text)
    sk_phrases = list(set(sk_phrases))  # Remove duplicates
    print(f'Found {len(sk_phrases)} API keys')
    
    # Find links to other pages on the same site
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(base_url)]
    print(f'Found {len(links)} links')
    
    # Recursively scrape the found links (with a limit to prevent infinite recursion)
    for link in links[:limit]:
        sk_phrases += scrape_for_sk_phrases_and_links(link, base_url, limit)
    
    return sk_phrases

if __name__ == '__main__':
    # Print startup message
    print("""███████╗███████╗███╗   ██╗███████╗     █████╗ ██████╗ ██╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
╚══███╔╝██╔════╝████╗  ██║██╔════╝    ██╔══██╗██╔══██╗██║    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
  ███╔╝ █████╗  ██╔██╗ ██║███████╗    ███████║██████╔╝██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
 ███╔╝  ██╔══╝  ██║╚██╗██║╚════██║    ██╔══██║██╔═══╝ ██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
███████╗███████╗██║ ╚████║███████║    ██║  ██║██║     ██║    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                                                                     

""")
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "Why do programmers prefer iOS development? Because on iOS, there are no Windows or Gates.",
        "Why did the programmer go broke? Because he used up all his cache.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express his feelings.",
        "Why did the developer go broke? Because he used up all his cache."
    ]
    print(random.choice(jokes))
    print()
    
    # Check if scrapeList.txt exists, if not, create it
    if not os.path.exists('scrapeList.txt'):
        with open('scrapeList.txt', 'w') as file:
            file.write("# https://example.com")
            file.write("# http://www.example2.com")
            file.write("# https://store.example.net/catalog")
            file.write("# https://archive.example3.com")
            file.write("# http://example4.net")
            file.write("# https://www.example5.com/catalog")
            file.write("# http://store.example6.net")
            file.write("# https://example7.com")
    
    print('Do you want to use proxychains? (yes/no, default is no)')
    use_proxychains = input() or 'no'
    if use_proxychains.lower() == 'yes':
        if os.system('which proxychains') == 0:
            print('Proxychains is installed.')
        else:
            print('Proxychains is not installed. Do you want to install it? (yes/no)')
            install_proxychains = input()
            if install_proxychains.lower() == 'yes':
                if os.system('sudo apt-get install proxychains') != 0:
                    print('There was an error installing proxychains. The program will run without it.')
    
    print('Do you want to read URLs from the scrapeList.txt file? (yes/no, default is no)')
    read_from_file = input() or 'no'
    if read_from_file.lower() == 'yes':
        with open('scrapeList.txt', 'r') as file:
            urls = file.readlines()
        print('Enter the scrape limit (default is 10, if you want to set a higher limit, it is recommended to use proxychains due to rate limiting):')
        limit = int(input() or '10')
        for url in urls:
            if not url.startswith('#'):
                api_keys = scrape_for_sk_phrases_and_links(url.strip(), 'https://', limit)
                print('API Keys found:')
                for key in api_keys:
                    print(key)
    else:
        print('Enter a URL to start scraping from (e.g., https://pastebin.com/0u43j7kH). This is the URL where the scraper will start looking for phrases and links.')
        url = input() or 'https://pastebin.com/0u43j7kH'
        print('Enter the base URL to determine which links to follow (e.g., https://www.example.com). The scraper will only follow links that start with this base URL.')
        base_url = input() or 'https://www.example.com'
        print('Enter the scrape limit (default is 10, if you want to set a higher limit, it is recommended to use proxychains due to rate limiting):')
        limit = int(input() or '10')
        api_keys = scrape_for_sk_phrases_and_links(url, base_url, limit)
        print('API Keys found:')
        for key in api_keys:
            print(key)
