import requests
import json

headers = {
    'authority': 'news.like.naver.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=100&sid2=264&oid=469&aid=0000524959',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=AT4DAGL7BIUF6; NDARK=Y; ASID=6e0aec0e00000173d731654000000056; NRTK=ag#20s_gr#0_ma#-2_si#-2_en#-2_sp#-2; _gid=GA1.2.273718387.1599034732; nx_ssl=2; _ga=GA1.1.1405891036.1597913286; _ga_7VKFYR6RV1=GS1.1.1599093971.2.1.1599094428.39; nid_inf=-1356522491; NID_AUT=VPB4Cw7DuOxSaXzpRzulAcBYDLQ+7EdcsuH7JNxNDdUBVRRzoNfucZScArMxpR8h; NID_JKL=NeklsPTU1E7pJxCyj/aRm2cy5F7YNt+o3XH9KOGYuFs=; NIPD=1; page_uid=U1vdhsp0J1sss7qVMI0ssssss0N-185932; BMR=s=1599141677551&r=https%3A%2F%2Fm.blog.naver.com%2Fkiddwannabe%2F221177292446&r2=https%3A%2F%2Fwww.google.com%2F; NID_SES=AAABi4FiFHpCvf+6CzSQQNAlKmnLqD0dAs6uHIO6FJehoZsUFnmQVGmvP40EhEYoY9edYDskwttl+gqlwU3TSCMh7tGMpes8pmvVAlt1iXwt9xgUYysDzxBA+oUDmhKV7FR4UUJhK4s9m8gEFftIykCOrbrys578eS+VFbtumyFcpAgQflzD6tk5Q6CtuokWlHkLvaZBPFuW7vB54a30XnCNKilZ7TBUp1xjw4mKpCvsPf4zMOBcQG0W10uls2/OfPW4M44WQ9SxCQEOejOEzhczKMtInOrNb2kCvCWwHmTq9h/41ZwAMuO9oBsp4GlNNDcEwclWcMLR071mIn5IvOxf4diKWpJuZ7E8mu0LwW4jOYGvX2bZSvfA06Nq4u8lcjgCsjiSK9gDoqh0cjgZSceMI6ulLjK/I+3qsjI8mlAr6OCqtrStutuF3/ODzVU6ZN/8YsTPyU45IpIvxe71S9W9x53vDPeiT+vxmkr64QNTrlMXQmp3jiE64YjbChYQMzAqKebHtthrUlUIsMqWEMOn1K4=',
}
oid = '469'
aid = '0000524959'

params = (
    ('suppress_response_codes', 'true'),
    ('callback', 'jQuery1124030611268362423094_1599146012993'),
    ('q', f'NEWS[ne_{oid}_{aid}]|NEWS_SUMMARY[{oid}_{aid}]|NEWS_MAIN[ne_{oid}_{aid}]'),
    ('isDuplication', 'false'),
    ('_', '1599146012994'),
)
print(params)
response = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery1124030611268362423094_1599146012993&q=NEWS%5Bne_022_0003498839%5D%7CNEWS_SUMMARY%5B022_0003498839%5D%7CNEWS_MAIN%5Bne_022_0003498839%5D&isDuplication=false&_=1599146012994', headers=headers)

text = response.text
page = text.replace('/**/jQuery1124030611268362423094_1599146012993(','').replace(');','')
page = json.loads(page)

result = 0
for re in page['contents'][0]['reactions'] :
    result += int(re['count'])

print(result)
