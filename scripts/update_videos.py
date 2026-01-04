#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import re
from datetime import datetime

# Canal do YouTube
YOUTUBE_CHANNEL = "UCmQwQ11GwCzs5qlv4klEX-Q"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL}"

# Caminho do arquivo HTML
HTML_FILE = "musicas/index.html"

def fetch_videos():
    """Busca vídeos do canal via RSS feed"""
    print(f"🔍 Buscando vídeos do canal {YOUTUBE_CHANNEL}...")
    feed = feedparser.parse(FEED_URL)
    
    videos = []
    for entry in feed.entries:
        video = {
            'id': entry.yt_videoid,
            'title': entry.title,
            'url': entry.link,
            'published': entry.published
        }
        videos.append(video)
    
    print(f"✅ Encontrados {len(videos)} vídeos")
    return videos

def create_video_card_html(video):
    """Cria HTML de um card de vídeo"""
    title = video['title']
    video_id = video['id']
    
    return f'''<div class="video-card">
<h3 class="video-title">{title}</h3>
<div class="video-wrapper">
<iframe src="https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" frameborder="0" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>
</div>
</div>'''

def update_html(videos):
    """Atualiza o arquivo HTML com os vídeos"""
    print(f"📝 Atualizando {HTML_FILE}...")
    
    # Lê o arquivo HTML existente
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Cria os cards dos vídeos
    video_cards = '\n'.join([create_video_card_html(video) for video in videos])
    
    # Encontra a seção de vídeos e substitui
    pattern = r'(<div class="videos-grid">)(.*?)(</div>\s*</main>)'
    replacement = rf'\1\n{video_cards}\n\3'
    
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Verifica se houve mudança
    if updated_html == html_content:
        print("ℹ️ Nenhuma atualização necessária")
        return False
    
    # Salva o arquivo atualizado
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print("✅ HTML atualizado com sucesso!")
    return True

if __name__ == "__main__":
    try:
        videos = fetch_videos()
        if videos:
            update_html(videos)
        else:
            print("⚠️ Nenhum vídeo encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise
