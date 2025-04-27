import feedparser
import requests
from datetime import datetime
from typing import List, Dict
import time
import re
import json

def read_sites_file() -> List[Dict[str, str]]:
    sites = []
    with open('sites.txt', 'r', encoding='utf-8') as file:
        # Skip header line
        next(file)
        for line in file:
            if line.strip():
                # Extract site name and URL using regex
                match = re.search(r'(.+?)\s*\((https?://[^)]+)\)', line)
                if match:
                    site_name = match.group(1).strip()
                    url = match.group(2).strip()
                    sites.append({
                        'name': site_name,
                        'url': url,
                        'description': line.split('|')[1].strip() if '|' in line else ''
                    })
    return sites

def get_portuguese_feed_url(original_url: str) -> str:
    # Mapeamento de URLs em inglês para português
    portuguese_feeds = {
        'ign.com': 'https://br.ign.com/feed.xml',
        'gamespot.com': 'https://www.gamespot.com/feeds/mashup/',
        'kotaku.com': 'https://kotaku.com/rss',
        'eurogamer.net': 'https://www.eurogamer.pt/?format=rss',
        'pcgamer.com': 'https://www.pcgamer.com/rss/',
        'theverge.com': 'https://www.theverge.com/gaming/rss/index.xml',
        'nintendolife.com': 'https://www.nintendolife.com/feeds/news',
        'pushsquare.com': 'https://www.pushsquare.com/feeds/news',
        'purexbox.com': 'https://www.purexbox.com/feeds/news',
        'rockpapershotgun.com': 'https://www.rockpapershotgun.com/feed'
    }
    
    # Tenta encontrar um feed em português correspondente
    for domain, pt_url in portuguese_feeds.items():
        if domain in original_url:
            return pt_url
    
    return original_url  # Se não encontrar, retorna a URL original

def clean_html(text: str) -> str:
    # Remove tags HTML básicas
    text = re.sub(r'<[^>]+>', '', text)
    # Remove espaços extras
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_news(sites: List[Dict[str, str]]) -> List[Dict]:
    all_news = []
    total_sites = len(sites)
    
    for index, site in enumerate(sites, 1):
        try:
            print(f"\nProcessando site {index}/{total_sites}: {site['name']}")
            
            # Tenta primeiro o feed em português
            pt_url = get_portuguese_feed_url(site['url'])
            feed = feedparser.parse(pt_url)
            
            # Se não encontrar entradas, tenta o feed original
            if not feed.entries:
                print(f"  - Feed em português não encontrado, usando versão em inglês...")
                feed = feedparser.parse(site['url'])
            
            # Get the last two entries
            last_two_entries = feed.entries[:2]
            
            for entry in last_two_entries:
                title = entry.get('title', '')
                if title:
                    print(f"  - Notícia: {title}")
                    
                    # Obtém o resumo/descrição da notícia
                    summary = entry.get('summary', '') or entry.get('description', '')
                    if summary:
                        summary = clean_html(summary)
                    
                    # Obtém o subtítulo se disponível
                    subtitle = entry.get('subtitle', '') or entry.get('subtitle_detail', {}).get('value', '')
                    if subtitle:
                        subtitle = clean_html(subtitle)
                    
                    # Estrutura padronizada em JSON
                    news_item = {
                        "source": {
                            "name": site['name'],
                            "url": site['url'],
                            "pt_url": pt_url,
                            "description": site['description']
                        },
                        "article": {
                            "title": title,
                            "subtitle": subtitle,
                            "summary": summary,
                            "link": entry.get('link', ''),
                            "published": entry.get('published', ''),
                            "author": entry.get('author', ''),
                            "categories": entry.get('tags', []) or entry.get('category', [])
                        },
                        "metadata": {
                            "fetch_date": datetime.now().isoformat(),
                            "language": "pt" if pt_url != site['url'] else "en"
                        }
                    }
                    all_news.append(news_item)
            
            # Be nice to the servers
            time.sleep(1)
            
        except Exception as e:
            print(f"Erro ao buscar notícias de {site['name']}: {str(e)}")
    
    return all_news

def save_to_json(news_items: List[Dict], filename: str = 'news.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    print(f"\nDados salvos em {filename}")

def main():
    print("Iniciando busca de notícias...")
    sites = read_sites_file()
    news_items = fetch_news(sites)
    save_to_json(news_items)
    print(f"Processo concluído! {len(news_items)} notícias coletadas.")

if __name__ == "__main__":
    main()
