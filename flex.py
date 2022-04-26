import json
import requests
import re
from PIL import Image
import os

API_KEY = "AIzaSyDyVK_IncLhBoY_H__8JvtHuS_P1R1nqWE"
SEARCH_ENGINE_ID = "e7fb5b3ccda84567f"

def search(query):
  titles = []
  imgs = []
  thumbs = []
  url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&siteSearch=facebook.com&siteSearchFilter=e&c2coff=1"
  data = requests.get(url).json()
  search_items = data.get("items")
  for item in search_items:
      if item['link'][-3:]=='gif':
        continue
      
      if len(item['link'])>300:
        continue
    
      if item['link'][:5]=='http:':
        item['link'] = 'https:'+item['link'][5:]
      
      titles.append(re.split('-|\||; |, |\*|\n',item['title'])[0])
      imgs.append(item['link'])
      thumbs.append(item['image']['thumbnailLink'])
  return titles, imgs, thumbs
  # print(imgs)

def flex(msg):
  titles, imgs, thumbs = search(msg)

  carousel = {"type": "carousel","contents":[]}
  for i in range(len(imgs)):
    with open('template.json') as f:
      bubble = json.load(f)
    bubble['hero']['url'] = imgs[i]
    bubble['body']['contents'][0]['text'] = titles[i]
    bubble['footer']['contents'][0]['action']['data'] = imgs[i]
    carousel['contents'].append(bubble.copy())
  
  print("search results: ")
  print(titles)
  result = json.dumps(carousel)
  return result