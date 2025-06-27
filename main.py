"""
Для запуска кода необходимо установить библосы: pip install requests beautifulsoup4

Остальное сами думайте, у вас тут весь код

Да, я люблю перед переменными ставить _, что тут такого???!!

KillerGrass Programms (https://t.me/killergrass_programms), 2025
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_js_code(url):
    try:
        _response = requests.get(url)
        _response.raise_for_status()
        
        _soup = BeautifulSoup(response.text, 'html.parser')
        
        inline_scripts = []
        for script in _soup.find_all('script'):
            if not script.has_attr('src') and script.string:
                inline_scripts.append(script.string.strip())
        
        external_scripts = []
        for script in _soup.find_all('script', src=True):
            script_url = urljoin(url, script['src'])
            try:
                _script_response = requests.get(script_url)
                _script_response.raise_for_status()
                external_scripts.append(_script_response.text.strip())
            except requests.RequestException as e:
                print(f"Не удалось загрузить внешний скрипт {script_url}: {e}")
        
        return {
            'inline_scripts': inline_scripts,
            'external_scripts': external_scripts,
            'url': url
        }
    
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None

if __name__ == "__main__":
    _website_url = input("Введите URL сайта для проверки: ")
    _js_code = extract_js_code(_website_url)
    
    if _js_code:
        print(f"\nНайдено inline-скриптов: {len(_js_code['inline_scripts'])}")
        print(f"Найдено внешних скриптов: {len(_js_code['external_scripts'])}")
        
        with open('js_code_extracted.txt', 'w', encoding='utf-8') as f:
            f.write(f"URL: {_js_code['url']}\n\n")
            f.write("=== Inline скрипты ===\n")
            for i, script in enumerate(_js_code['inline_scripts'], 1):
                f.write(f"\n--- Inline скрипт #{i} ---\n")
                f.write(script)
            
            f.write("\n\n=== Внешние скрипты ===\n")
            for i, script in enumerate(_js_code['external_scripts'], 1):
                f.write(f"\n--- Внешний скрипт #{i} ---\n")
                f.write(script)
        
        print("JavaScript код сохранен в файл 'js_code_extracted.txt'")
    else:
        print("Не удалось извлечь JavaScript код.")
        
    input()