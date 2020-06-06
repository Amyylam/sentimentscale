# -*- coding: utf-8 -*-
"""
Created on Sun May 31 11:08:35 2020

@author: gen80

#scrap emotion reactions to news articles on Hong Kong-based Chinese media HK01.com as distant supervision for sentiment analysis model training
#identify the dominant reaction as the main sentiment if emotion count >5
#secondary/ a mix of reaction also valuable for identifying what keywords led to relevant reaction (e.g. clustering analysis?)

"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import csv

'''
article_url = r"https://www.hk01.com/18%E5%8D%80%E6%96%B0%E8%81%9E/469177/%E8%B3%9E%E8%8A%B1%E4%B8%AD%E6%AF%92-%E9%A6%AE%E7%9B%88%E7%9B%88%E8%88%87%E8%8A%B1%E5%90%88%E7%85%A7%E9%A0%AD%E6%9A%88-%E5%9C%98%E9%AB%94-%E5%A4%BE%E7%AB%B9%E6%A1%83%E5%B8%B8%E8%A6%8B%E6%96%BC%E5%85%AC%E8%B7%AF%E5%8F%8A%E6%96%9C%E5%9D%A1"
# article title:
# urllib.parse.quote_plus('賞花中毒') -> '%E8%B3%9E%E8%8A%B1%E4%B8%AD%E6%AF%92'
# urllib.parse.unquote_plus('%E8%B3%9E%E8%8A%B1%E4%B8%AD%E6%AF%92') -> '賞花中毒'

response = requests.get(article_url)
article_content = response.text
soup = BeautifulSoup(article_content,'lxml')
#print(soup.img)
article_tag = soup.article

# socialReactions hidden in script

full_article_info =soup.find("script",{'id':"__NEXT_DATA__"}).text
article_dict = json.loads(full_article_info)
#  dict_keys(['dataManager', 'props', 'page', 'query', 'buildId', 'runtimeConfig'])
article_infos = article_dict['props']['pageProps']['initialState']
# dict_keys(['article', 'ui', 'member', 'zone', 'mosaic', 'navigation', 'home', 'core', 'toast', 'category', 'hotArticle', 'issue', 'login', 'careerPage', 'tag', 'bookmark', 'newsletter', 'recommend', 'weather', 'hotTag', 'entrances', 'pua'])

article_only_infos =  article_dict['props']['pageProps']['initialState']['article']['entities']
# dict_keys(['images', 'briefArticles', 'videos', 'articles'])
emotion_reactions = article_dict['props']['pageProps']['initialState']['article']['entities']['articles']['469177']['article']['socialReactions']
'''

# =============================================================================
# 
# article_dict['props']['pageProps']['initialState']['article']['entities']['articles']['469177']['article'].keys()
# Out[56]: dict_keys(['articleId', 'canonicalUrl', 'publishUrl', 'redirectUrl', 'title', 'authors', 'mainCategoryId',\
#    'mainCategory', 'categories', 'isFeatured', 'isSponsored', 'contentType', 'detailPageTopDisplay', 'displayMode', \
#    'description', 'imageCount', 'mainImage', 'originalImage', 'thumbnails', 'blockReaction', 'blockComment', \
#    'socialReactions', 'commentCount', 'publishTime', 'lastModifyTime', 'tags', 'teaser', 'blocks', 'blockAd', \
#    'comment', 'relatedArticles', 'ad'])
# =============================================================================


# =============================================================================
### emotion_reactions = article_dict['props']['pageProps']['initialState']['article']['entities']['articles']['469177']['article']['socialReactions']
# Out[57]: 
# [{'reactionId': 'heart', 'totalCount': 2},
#  {'reactionId': 'like', 'totalCount': 3},
#  {'reactionId': 'angry', 'totalCount': 4},
#  {'reactionId': 'sad', 'totalCount': 5},
#  {'reactionId': 'laugh', 'totalCount': 5}]
# 
# =============================================================================

## now try scrapping toppage of each zone

zone1_url = r'https://www.hk01.com/zone/1/%E6%B8%AF%E8%81%9E' #local affairs
zone2_url = r'https://www.hk01.com/zone/2/%E5%A8%9B%E6%A8%82' #Entertainment
zone3_url =r'https://www.hk01.com/zone/3/%E9%AB%94%E8%82%B2' #Sports
zone4_url = r'https://www.hk01.com/zone/4/%E5%9C%8B%E9%9A%9B' #International
zone5_url = r'https://www.hk01.com/zone/5/%E4%B8%AD%E5%9C%8B' # China
zone6_url = r'https://www.hk01.com/zone/6/%E5%A5%B3%E7%94%9F' #Girls
zone7_url = r'https://www.hk01.com/zone/7/%E7%86%B1%E8%A9%B1' #Hot topic
zone8_url = r'https://www.hk01.com/zone/8/%E7%94%9F%E6%B4%BB' #Lifestyle
zone9_url = r'https://www.hk01.com/zone/9/%E8%97%9D%E6%96%87%E6%A0%BC%E7%89%A9' #Arts
zone10_url = r'https://www.hk01.com/zone/10/%E7%A4%BE%E5%8D%80' #Community
zone11_url = r'https://www.hk01.com/zone/11/%E7%A7%91%E6%8A%80%E7%8E%A9%E7%89%A9' #Tech/Gadgets
zone12_url = r'https://www.hk01.com/zone/12/%E8%A7%80%E9%BB%9E' #Opinions
zone13_url = r'https://www.hk01.com/zone/13/%E5%BD%B1%E5%83%8F' #Photography
zone14_url = r'https://www.hk01.com/zone/14/%E7%B6%93%E6%BF%9F' #Economy


zone_url = r'https://www.hk01.com/zone/8/%E7%94%9F%E6%B4%BB'

for i in range(1,15):
    response = requests.get(eval(f'zone{i}_url'))
    article_content = response.text
    soup = BeautifulSoup(article_content,'lxml')
    full_article_info =soup.find("script",{'id':"__NEXT_DATA__"}).text
    article_dict = json.loads(full_article_info)
    # toppage contains brief articles inside "zone" key, not "article" key
    brief_article_infos =  article_dict['props']['pageProps']['initialState']['zone']['entities']['briefArticles']
    reacted_article_dicts = []
    
    for item in brief_article_infos.keys():
        #print(brief_article_infos[item]['data']['socialReactions'])
        
        if brief_article_infos[item]['data']['socialReactions']:
            print(brief_article_infos[item]['data']['title'])
            print(brief_article_infos[item]['data']['description'])
            print(brief_article_infos[item]['data']['publishTime'])
            # turn posix timestamp to normal datetime object
            ## datetime.fromtimestamp(brief_article_infos[item]['data']['publishTime']).strftime("%Y-%m-%d %H:%M:%S")
            item_info_dict = {k:v for k,v in brief_article_infos[item]['data'].items() if k in ["title","description","articleId","canonicalUrl","mainCategory",'originalImage','commentCount']}
            item_info_dict['publishTime'] = datetime.fromtimestamp(brief_article_infos[item]['data']['publishTime']).strftime("%Y-%m-%d %H:%M:%S")
            item_info_dict['zone'] = 'zone'+str(i)
            
            
            print(brief_article_infos[item]['data']['socialReactions'])
            #turn this reactionId-totalCount format into key-value pair
            emo_dict = {}
            for item in brief_article_infos[item]['data']['socialReactions']:
                emo_dict[item['reactionId']]=item['totalCount']
            ## emo_dict -- {'like': 6, 'heart': 2}
            item_info_dict.update(emo_dict)
            ### {'title': '【學是學非】馮盈盈着黑絲扮女僕\u3000抹茶粉打「400次咖啡」有秘技','description': '忠實粉絲...', 'like': 6,'heart': 2}
        reacted_article_dicts.append(item_info_dict)
    
    #end extracting this i-th zone. save to disk
    ## export to json or csv dictWriter     
    output_folder = r'E:\emo_count_corpus'
    with open(os.path.join(output_folder,'emo_articles.csv'), 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['zone','publishTime',"articleId",'title','description','like','heart','angry','sad','laugh',"canonicalUrl","mainCategory",'originalImage','commentCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        
        articles_stored = set()
        for item in reacted_article_dicts:
            # to avoid duplicate
            if item['articleId'] not in articles_stored:
                writer.writerow(item)
                articles_stored.add(item['articleId'])
    
   
##checkpoint: June 2 1:39am done 14 zones extraction. articles from May29-Jun2.

# =============================================================================
# 
# 【寵物獸醫地圖】全港160間獸醫診所資料　求診手冊即學即用
# 急病往往令人手足無措，而毛孩病了更令寵主徬徨。新一年《香港01》為各寵主準備了一個包括香港、九龍及新界的獸醫診所地圖，可讓寵主快速找到全港獸醫診所的資料，致電獸醫診所預約後再出門。
# 1546844400
# [{'reactionId': 'heart', 'totalCount': 3}, {'reactionId': 'sad', 'totalCount': 1}, {'reactionId': 'like', 'totalCount': 9}]
# PS5 面世　回顧PlayStation開發史　團結力量反任天堂霸權的抗爭
# Sony PlayStation 5 PS5 香港時間6月5日凌晨發表！回顧26年前SONY推出第1代遊戲機，背後開發秘話竟然是因為要對打任天堂的專橫賤招？PS的掘起，又如何帶動日本遊戲界變得先進開明？
# 1590915600
# [{'reactionId': 'laugh', 'totalCount': 1}, {'reactionId': 'like', 'totalCount': 1}]
# 親子討論區熱話：有多少媽媽最愛的男人是自己老公？
# 愛情同婚姻到底係同一件事定要分開嚟睇？其實從細到大都經常都會聽到人講：「最後嗰個，往往唔係最愛嗰個！」聽落去有人會覺得好荒謬，質疑如果唔
# 1590897900
# [{'reactionId': 'laugh', 'totalCount': 1}]
# 【理財】逆市投資要懂分優質股、中伏股　6大秘訣減股票投資風險
# 在經濟衰退時，格外留意市場局勢，尋找機會買入優質及具潛力的資產，令財富繼續增值。一些表免面風光的公司，在經濟下行時，較易構成風險；相反，
# 1590901320
# [{'reactionId': 'like', 'totalCount': 2}]
# =============================================================================







# =============================================================================

## brief infos about 3 related articles -- quick way to scrap title+description+socialReactions of multiple articles
# article_dict['props']['pageProps']['initialState']['article']['entities']['briefArticles']
# Out[48]: 
# {'441829': {'id': 441829,
#   'type': 1,
#   'data': {'articleId': 441829,
#    'canonicalUrl': 'https://www.hk01.com/18區新聞/441829/春日花開-紅花風鈴木粉嶺中心綻放-龍友-擠滿行人天橋',
#    'publishUrl': '/18區新聞/441829/春日花開-紅花風鈴木粉嶺中心綻放-龍友-擠滿行人天橋',
#    'redirectUrl': None,
#    'title': '【春日花開】紅花風鈴木粉嶺中心綻放\u3000「龍友」擠滿行人天橋',
#    'authors': [{'publishName': '呂凝敏'},
#     {'publishName': '王譯揚'},
#     {'publishName': '余睿菁'}],
#    'mainCategoryId': 422,
#    'mainCategory': '18區新聞',
#    'categories': [{'categoryId': 422,
#      'publishName': '18區新聞',
#      'publishUrl': 'https://www.hk01.com/channel/422/18區新聞'}],
#    'isFeatured': 1,
#    'isSponsored': 0,
#    'contentType': 'article',
#    'detailPageTopDisplay': 'video',
#    'displayMode': 'big_image',
#    'description': '踏入3月，天氣回暖，又是百花爭妍的季節。粉嶺中心近祥華邨一帶，近日有數棵紅花風鈴木盛開，吸引不少途經人士駐足拍照及「打卡」，行人天橋上擠滿賞花客，相當熱鬧。',
#    'imageCount': 12,
#    'video': '24d4bc0d-8f20-4344-8280-d28b7ae1c58f',
#    'mainImage': 4084569,
#    'originalImage': {'mediaId': 4082978,
#     'originalWidth': 1920,
#     'originalHeight': 1279,
#     'caption': '',
#     'cdnUrl': 'https://cdn.hk01.com/di/media/images/4082978/org/1bedc29a444e1e698ad01e4a5e06504d.jpg/c33N8vHlozFzpdCfDaPp52UE97c2xzNse1uGuntbhro'},
#    'thumbnails': [4084569, 4083026, 4083024],
#    'blockReaction': False,
#    'blockComment': False,
#    'socialReactions': [{'reactionId': 'heart', 'totalCount': 1},
#     {'reactionId': 'like', 'totalCount': 7}],
#    'commentCount': 1,
#    'publishTime': 1583057989,
#    'lastModifyTime': 1583209853}},
#  '442819': {'id': 442819,
#   'type': 1,
#   'data': {'articleId': 442819,
#    'canonicalUrl': 'https://www.hk01.com/18區新聞/442819/春日花開-多圖-南昌風鈴木滿天開花-沙田繡球花綻放',
#    'publishUrl': '/18區新聞/442819/春日花開-多圖-南昌風鈴木滿天開花-沙田繡球花綻放',
#    'redirectUrl': None,
#    'title': '【春日花開‧多圖】南昌風鈴木滿天開花！沙田繡球花綻放',
#    'authors': [{'publishName': '黃文軒'}],
#    'mainCategoryId': 422,
#    'mainCategory': '18區新聞',
#    'categories': [{'categoryId': 422,
#      'publishName': '18區新聞',
#      'publishUrl': 'https://www.hk01.com/channel/422/18區新聞'}],
#    'isFeatured': 1,
#    'isSponsored': 0,
#    'contentType': 'photostory',
#    'detailPageTopDisplay': 'image',
#    'displayMode': 'big_image',
#    'description': '踏入春天，天氣回暖，百花爭妍鬥艷。香港有不少賞花熱點，如南昌公園內的黃花風鈴木、沙田公園色彩繽紛的繡球花，還有紅彤彤的木棉花。其中南昌公園的黃花風鈴木已悄悄在今年初開花，想要打卡留倩影，便要捉緊時間了。攝影：郭倩雯',
#    'imageCount': 15,
#    'mainImage': 4096249,
#    'originalImage': {'mediaId': 4094877,
#     'originalWidth': 1920,
#     'originalHeight': 1280,
#     'caption': '',
#     'cdnUrl': 'https://cdn.hk01.com/di/media/images/4094877/org/7edccf81179490f1cdbba851ebc7d7db.jpg/xJnLhs1VKd9m7Aewq7ZXBYKe60SGUK7FFK1B5hStQeY'},
#    'thumbnails': [4096249, 4094810, 4094809],
#    'blockReaction': False,
#    'blockComment': False,
#    'socialReactions': [],
#    'commentCount': 0,
#    'publishTime': 1583229139,
#    'lastModifyTime': 1583236817}},
#  '468171': {'id': 468171,
#   'type': 1,
#   'data': {'articleId': 468171,
#    'canonicalUrl': 'https://www.hk01.com/18區新聞/468171/圖輯-中環美利大廈百年古樹-節果決明-開花-白與嫣紅滿樹梢',
#    'publishUrl': '/18區新聞/468171/圖輯-中環美利大廈百年古樹-節果決明-開花-白與嫣紅滿樹梢',
#    'redirectUrl': None,
#    'title': '【圖輯】中環美利大廈百年古樹「節果決明」開花\u3000白與嫣紅滿樹梢',
#    'authors': [{'publishName': '黃偉民'}],
#    'mainCategoryId': 422,
#    'mainCategory': '18區新聞',
#    'categories': [{'categoryId': 422,
#      'publishName': '18區新聞',
#      'publishUrl': 'https://www.hk01.com/channel/422/18區新聞'}],
#    'isFeatured': 1,
#    'isSponsored': 0,
#    'contentType': 'photostory',
#    'detailPageTopDisplay': 'image',
#    'displayMode': 'big_image',
#    'description': '',
#    'imageCount': 10,
#    'mainImage': 4421658,
#    'originalImage': {'mediaId': 4420444,
#     'originalWidth': 1920,
#     'originalHeight': 1080,
#     'caption': '',
#     'cdnUrl': 'https://cdn.hk01.com/di/media/images/4420444/org/aabbdfadd9e3e5067f57004216adbd67.jpg/rQcUtfU_8cDUwjIEtbbiidt3sxU-1qGKqFRgt6hUYLc'},
#    'thumbnails': [4421658, 4420373, 4420372],
#    'blockReaction': False,
#    'blockComment': False,
#    'socialReactions': [],
#    'commentCount': 0,
#    'publishTime': 1588409931,
#    'lastModifyTime': 1588417621}}}
# =============================================================================
