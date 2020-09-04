import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time

headers = {
    'authority': 'news.like.naver.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=100&sid2=265&oid=008&aid=0004466515',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=AT4DAGL7BIUF6; NDARK=Y; ASID=6e0aec0e00000173d731654000000056; NRTK=ag#20s_gr#0_ma#-2_si#-2_en#-2_sp#-2; nx_ssl=2; nid_inf=-1356522491; NID_AUT=VPB4Cw7DuOxSaXzpRzulAcBYDLQ+7EdcsuH7JNxNDdUBVRRzoNfucZScArMxpR8h; NID_JKL=NeklsPTU1E7pJxCyj/aRm2cy5F7YNt+o3XH9KOGYuFs=; NIPD=1; BMR=s=1599141677551&r=https%3A%2F%2Fm.blog.naver.com%2Fkiddwannabe%2F221177292446&r2=https%3A%2F%2Fwww.google.com%2F; _gid=GA1.2.351956304.1599206190; _ga=GA1.1.1405891036.1597913286; _ga_7VKFYR6RV1=GS1.1.1599206189.3.1.1599206213.36; page_uid=U1cH/lprvh8ssONI6Asssssste4-239842; NID_SES=AAABldmeDJmGObeP4LfuAGrgPq+raDpW04ZJGw8y+TroWVU3EGF0/SIiaZWHdVPPADPpffLz/SAhVdxIoELbjH+SjYKtnpT1wRW2v4G+QAOE1gU5iWJRdQyVUl4PDIFF6GWykJ9mCB7X3bkAluTpg1ohLgG11owPLDU1QvKUu132CHXr0vSytRnRvqvOuLF5hGuW0wO5n5RzAqaKlfYHMOxXeVfF/l2YxO3J/GBsm1qC2jI0d7iPfa6ty+YmzRlfTRlJPimqsLkueNXF7Edu5ah/59sJz+CjqL5ihKjKLUofHVpQYeZjLMNlZyAVUJ4gy3Pudl8d8+F+CsxVhufGCZWA8tBMAEz0uEIKxqoXnNYI5TnynTL5f/L0HbWlpQs/OBXnKep4etJbjjsjpRDhMC6hSQjMdphV972XapIDGwZtAwJq4g0u/pfAjIG1WbwKjLIuP+KnsHzdVeIpcdfBQzeqeBk7aUiGx2H57rMd5ruOyRyfGt+bKHB4/K7oe+3LQNNgodQBqcqJ0JBS9uSi4rgCW3SCzh42CQc33hj/QAOmF3qn',
}

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery112405065232035148242_1599210137977&q=NEWS%5Bne_008_0004466515%5D%7CNEWS_SUMMARY%5B008_0004466515%5D%7CNEWS_MAIN%5Bne_008_0004466515%5D&isDuplication=false&_=1599210137978', headers=headers)

# 20180501 부터 오늘까지 반환 
# # yyyymmdd 일자를 datetime 객체로 변환 
def date_return(start, end) :
    start_date = datetime.strptime(start, '%Y%m%d') 
    end_date = datetime.strptime(end, '%Y%m%d') 

    # 날짜를 입력할 리스트 
    str_date_list = [] 
    while start_date.strftime('%Y%m%d') != end_date.strftime('%Y%m%d'): 
        str_date_list.append(start_date.strftime('%Y%m%d')) 
        start_date += timedelta(days=1)
    
    return str_date_list

def crawling(soup, date) :

    news_list = soup.select('ul.type06 > li')

    title_list = []
    url_list = []
    date_list = []
    count_list = []
    for news in news_list :
        # 뉴스에서 이미지가 있는 경우와 없는 경우 존재
        if len(news.select('dl > dt > a')) > 1 :
            title = news.select('dl > dt > a')[1].text.replace('\r','').replace('\t','').replace('\n','')
            url = news.select('dl > dt > a')[1]['href']
        else :
            title = news.select('dl > dt > a')[0].text.replace('\r','').replace('\t','').replace('\n','')
            url = news.select('dl > dt > a')[0]['href']

        # 각 기사 url에 접근해서 관심도, 즉 좋아요와 싫어요 눌린 개수 가져오기, 동적 크롤링이라 api 사용해야 함
        oid = url[-18:-15]
        aid = url[-10:]
        params = (
            ('suppress_response_codes', 'true'),
            ('callback', 'jQuery112405065232035148242_1599210137977'),
            ('q', f'NEWS[ne_{oid}_{aid}]|NEWS_SUMMARY[{oid}_{aid}]|NEWS_MAIN[ne_{oid}_{aid}]'),
            ('isDuplication', 'false'),
            ('_', '1599210137978'),
        )
        
        response = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
        text = response.text
        page = text.replace('/**/jQuery112405065232035148242_1599210137977(','').replace(');','')
        page = json.loads(page)

        result = 0
        for re in page['contents'][0]['reactions'] :
            result += int(re['count'])

        date_list.append(date)
        title_list.append(title)
        url_list.append(url)
        count_list.append(result)

    return date_list, title_list, url_list, count_list

def main() :
    news_dict = {
        'date' : [],
        'title' : [],
        'url' : [],
        'count' : []
    }

    date = date_return('20200801', '20200901')
    page = list(range(1, 100))
    url = 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=265&sid1=100&mid=shm'

    for d in date :
        time.sleep(5)
        for p in page :

            response = requests.get(url, params={'date':d, 'page':p})
            soup = BeautifulSoup(response.text, 'html.parser')

            date_list, title_list, url_list, count_list = crawling(soup, d)

            if len(news_dict['title']) != 0 :
                if news_dict['title'][:-1] == title_list[:-1] :
                    break

            news_dict['date'] += date_list
            news_dict['title'] += title_list
            news_dict['url'] += url_list
            news_dict['count'] += count_list
            
            print('ok' + str(d) + str(p))

        
    news_list_pd = pd.DataFrame(news_dict)
    news_list_pd.to_csv('naver_news_265_20200801_20200831.csv')
    print(news_list_pd)

if __name__ == "__main__":
    main()


