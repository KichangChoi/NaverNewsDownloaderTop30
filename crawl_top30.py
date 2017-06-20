
import urllib3
from bs4 import BeautifulSoup
from crawl_news import split_text
from calculate_score import calculate

#'YYYY-MM-DD'
date = '20160707'

subject_no = [100, 101, 102, 103, 104, 105]
subject_name = ['정치', '경제', '사회', '생활_문화', '세계', 'IT_과학']

for i in range(0, 6):
    rank_url = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=' + str(subject_no[i]) + '&date=' + date
    connection_pool = urllib3.PoolManager()
    resp = connection_pool.request('GET', rank_url)
    soup = BeautifulSoup(resp.data, 'html.parser')

    tag_top3 = soup.find("div", { "class" : "ranking_top3 " })
    tag_top30 = soup.find_all("div", { "class" : "ranking_section" })


    url_list = []
    temp = None

    tag_list = tag_top3.findChildren()
    for tag in tag_list:
        temp_url = tag.get('href')
        if temp_url != None:
            if temp_url != temp:
                url_list.append(temp_url)
                temp = temp_url

    for top10 in tag_top30:
        for tag in top10.findChildren():
            temp_url = tag.get('href')
            if temp_url != None:
                url_list.append(temp_url)


#url = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=001&aid=0008524321'


#30개 url 리스트 만들기 분야별






    f = open(subject_name[i] + '_score.txt', 'w', encoding='utf-8')
    rank_no = 1

    for url_one in url_list:
        url = 'http://news.naver.com' + url_one
        print (url)
        news_text = split_text(url, rank_no, subject_name[i])
        news_score = calculate(news_text)

        f.write('Score : ')
        f.write(str(news_score))
        f.write(' | url : ' + url_one + '\n\n')

        rank_no += 1


    f.close()