import os
import time
import random
import requests
import json
from bs4 import BeautifulSoup

# Configuration
VISITS_TARGET = 30
MIN_VISIT_TIME = 40
MAX_VISIT_TIME = 65
DELAY_BETWEEN_VISITS = 15
ADSTERRA_URL = "https://www.profitableratecpm.com/icb56k0m?key=34b261d534e4a259e9e2af3861057e03"
RENDER_API_URL = "https://render-tron.appspot.com/render"

def get_fresh_proxies():
    """Récupère les proxies avec des sources fiables"""
    all_proxies = []
    
    # Sources fiables et vérifiées
    sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    ]
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            proxies = [p.strip() for p in response.text.splitlines() if p.strip() and ':' in p]
            
            # Filtrage des doublons
            new_proxies = [p for p in proxies if p not in all_proxies]
            all_proxies.extend(new_proxies)
            
            print(f"✓ {len(new_proxies)} proxies de {url.split('/')[-1]}")
            
        except Exception as e:
            print(f"⚠️ Erreur avec {url}: {str(e)[:50]}...")
    
    # Ajout de proxies de secours si la liste est vide
    if not all_proxies:
        all_proxies = [
            "45.8.211.195:80", "104.18.70.24:80", "104.19.43.6:80",
            "185.176.26.94:80", "185.193.29.160:80", "104.16.63.102:80"
        ]
        print("⚠️ Utilisation des proxies de secours")
    
    print(f"✅ Total: {len(all_proxies)} proxies chargés")
    return all_proxies

def simulate_human_interaction():
    """Simule le temps d'interaction humaine"""
    # Temps de visite
    visit_duration = random.randint(MIN_VISIT_TIME, MAX_VISIT_TIME)
    print(f"⏱ Simulation d'une visite de {visit_duration}s")
    time.sleep(visit_duration)
    return True

def visit_adsterra_via_api(proxy):
    """Effectue une visite via une API de rendu"""
    try:
        print(f"🌐 Début de la visite via API avec proxy: {proxy}")
        
        # Configuration du proxy
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        # 1. Accès indirect via Google
        search_query = random.choice(["news", "weather", "sports", "technology", "music"])
        google_url = f"https://www.google.com/search?q={search_query}+{random.randint(1000,9999)}"
        
        # Rendu de la page Google
        params = {
            "url": google_url,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(RENDER_API_URL, params=params, timeout=30, proxies=proxies)
        response.raise_for_status()
        print("✓ Accès Google simulé")
        time.sleep(random.uniform(2, 4))
        
        # 2. Accès à Adsterra via l'API de rendu
        params = {
            "url": ADSTERRA_URL,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "waitFor": 5000  # Attend 5 secondes que la page se charge
        }
        response = requests.get(RENDER_API_URL, params=params, timeout=60, proxies=proxies)
        response.raise_for_status()
        print("✓ Page Adsterra rendue avec succès")
        
        # 3. Simulation d'interaction
        success = simulate_human_interaction()
        
        if success:
            print("✅ Visite réussie via API!")
            return True
    
    except Exception as e:
        print(f"❌ Erreur pendant la visite API: {str(e)}")
    
    return False

def visit_adsterra_direct(proxy):
    """Tente une visite directe avec requests"""
    try:
        print(f"🌐 Début de la visite directe avec proxy: {proxy}")
        
        # Configuration du proxy
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        
        # 1. Accès indirect via Google
        search_query = random.choice(["news", "weather", "sports", "technology", "music"])
        google_url = f"https://www.google.com/search?q={search_query}+{random.randint(1000,9999)}"
        
        response = requests.get(google_url, headers=headers, timeout=15, proxies=proxies)
        response.raise_for_status()
        print("✓ Accès Google réussi")
        time.sleep(random.uniform(2, 4))
        
        # 2. Accès à Adsterra
        response = requests.get(ADSTERRA_URL, headers=headers, timeout=30, proxies=proxies)
        response.raise_for_status()
        print("✓ Page Adsterra chargée")
        
        # 3. Simulation d'interaction
        success = simulate_human_interaction()
        
        if success:
            print("✅ Visite directe réussie!")
            return True
    
    except Exception as e:
        print(f"❌ Erreur pendant la visite directe: {str(e)}")
    
    return False

def visit_adsterra():
    """Effectue une visite complète optimisée"""
    proxies = get_fresh_proxies()
    proxy = random.choice(proxies) if proxies else None
    
    # Essayer d'abord via l'API de rendu
    if proxy and visit_adsterra_via_api(proxy):
        return True
    
    # Si l'API échoue, essayer en direct
    if proxy and visit_adsterra_direct(proxy):
        return True
    
    # Si tout échoue, essayer sans proxy
    print("⚠️ Tentative sans proxy...")
    if visit_adsterra_direct(None):
        return True
    
    return False

def main():
    print("""
    █████╗ ██████╗ ███████╗████████╗███████╗██████╗ ██████╗  █████╗ 
   ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
   ███████║██║  ██║███████╗   ██║   █████╗  ██████╔╝██████╔╝███████║
   ██╔══██║██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║
   ██║  ██║██████╔╝███████║   ██║   ███████╗██║  ██║██║  ██║██║  ██║
   ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
   Solution Fiable pour Génération de Trafic Adsterra (API Approach)
    """)
    
    visits_count = 0
    
    while visits_count < VISITS_TARGET:
        success = visit_adsterra()
        
        if success:
            visits_count += 1
            print(f"✅ Visites complétées: {visits_count}/{VISITS_TARGET}")
        
        # Délai aléatoire avant la prochaine visite
        delay = DELAY_BETWEEN_VISITS + random.randint(-5, 10)
        print(f"😴 Pause de {delay}s avant la prochaine visite")
        time.sleep(max(10, delay))  # Minimum 10 secondes
    
    print("🎉 Génération de trafic terminée avec succès!")

if __name__ == "__main__":
    # Installation initiale des dépendances
    os.system('pip install requests beautifulsoup4 > /dev/null 2>&1')
    main()