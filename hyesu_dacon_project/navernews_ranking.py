import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 날짜를 문자열로 변경하기 위한 함수
def date_return(start, end) :
    start_date = datetime.strptime(start, '%Y%m%d') 
    end_date = datetime.strptime(end, '%Y%m%d') 

    # 날짜를 입력할 리스트 
    str_date_list = [] 
    while start_date.strftime('%Y%m%d') != end_date.strftime('%Y%m%d'): 
        str_date_list.append(start_date.strftime('%Y%m%d')) 
        start_date += timedelta(days=1)
    
    return str_date_list

# 크롤링 함수
def crawling(soup, date, section) :
    
    news_list = soup.select('div.ranking > ol.ranking_list > li')

    # section 구분 코드
    if section == '100' :
        section_text = 'politics'
    elif section == '101' :
        section_text = 'economy'
    else :
        section_text = 'Society'

    # 각 row값들 담을 리스트 생성
    section_list = []
    title_list = []
    date_list = []
    view_list = []

    # bs4이용해서 title, view 스크래핑
    # section_text와 date는 함수에서 받은 인자를 각 row에 넣어줌
    for li in news_list :
        title = li.select_one('div.ranking_text > div > a').get_text()
        view = li.select_one('div.ranking_view').get_text().replace(',','')
        
        date_list.append(date)
        section_list.append(section_text)
        title_list.append(title)
        view_list.append(int(view))

    return date_list, section_list, title_list, view_list

# 메인 함수
def main() :
    # 딕셔너리 생성, 초기화
    news_dict = {
        'date' : [],
        'section' : [],
        'title' : [],
        'view' : []
    }

    # 시작 날짜와 끝 날짜를 인자로 받는 date_return함수를 통해 date리스트 생성
    date = date_return('20200120', '20200901')

    # base url --- 파라미터로 각 section의 id값과 날짜 받음
    url = 'https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day'
    section_id = ['100', '101', '102']

    for d in date :
        for s in section_id :
            # url, params로 requests받을 url생성
            response = requests.get(url, params={'sectionId':s, 'date':d})
            soup = BeautifulSoup(response.text, 'html.parser')

            # 위에서 정의한 crawling함수를 통해 리스트에 값 받아오기
            date_list, section_list, title_list, view_list = crawling(soup, d, s)

            # 딕셔너리의 -> 각 column에 리스트 값 더하기 (리스트끼리는 +를 통해 더할 수 있음)
            news_dict['date'] += date_list
            news_dict['section'] += section_list
            news_dict['title'] += title_list
            news_dict['view'] += view_list

            # 스크래핑 코드 작동 여부를 확인하기 위함, 필수 x
            print('ok' + str(d))
            
    # 딕셔너리를 판다스 dataframe으로 변환하고 csv파일로 추출
    news_list_pd = pd.DataFrame(news_dict)
    news_list_pd.to_csv('naver_news_scraping_ranking_0120_0831.csv')
    print(news_list_pd)


if __name__ == "__main__":
    main()