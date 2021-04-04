# Web_Scrapying_104-

# 0402完成版本-V.Complete01
# 0401愚人節成功版本-V1
# 0331成功完成 150頁標題+連結爬取
import requests
from bs4 import BeautifulSoup
import json

"""
=================================此行開始為先爬取第一頁各職位標題及連結==============================================
"""

url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001000&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=11&asc=0&page=1&mode=s&jobsource=104_new'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

page = 1
print('You r now in Page 1')
"""
動用以下for迴圈可以選擇欲爬取頁數
"""
for i in range(0, 5):
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')


    titleSoupList = soup.select('h2.b-tit')

    a = 3
    No = 1
    for i in range(20):
        titleSoup = titleSoupList[a]
        title = titleSoup.select('a')
        print(str(No) + '. ' + title[0].text +'\n')
        No += 1
        articleUrl = 'https:' + title[0]['href']
        print(articleUrl + '\n')
        
        """
        ========================此行開始為內容頁爬取=====================
        """
        
        Code = articleUrl[27: 32]
#         print(Code)
        contentUrl = 'https://www.104.com.tw/job/ajax/content/' + Code + '?jobsource=104_new'
#         print(contentUrl)
        headers = {
            "Referer": "https://www.104.com.tw/job/" + str(Code), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        res = requests.get(contentUrl, headers = headers)
        # print(res.text)
        jsonData = json.loads(res.text)
        # print(jsonData)
        jsonData
        lst2jsonData = list(jsonData.values())
        lst2jsonData[0]
        
        """
        公司名稱
        """
        jsonHeader = lst2jsonData[0]['header']
        print('【公司名稱】')
        print(jsonHeader['custName'] + '\n')
        
        """
        00工作內容
        """
        jsonDetail = lst2jsonData[0]['jobDetail']
        print('【工作內容】')
        print(jsonDetail['jobDescription'] + '\n')
        
        """
        00-1職缺類別
        """
        jsonDetail = lst2jsonData[0]['jobDetail']
        jobDetCat = jsonDetail['jobCategory']
        jDCseq = 0
        jDCNo = 1
        print('【職缺類別】')
        for i in jobDetCat:
            print(str(jDCNo) + '. ' + jobDetCat[jDCseq:jDCseq+1][0]['description'])
            jDCseq += 1
            jDCNo += 1
        print('\n')
        
        """
        00-2工作待遇
        """
        jobDetSal = jsonDetail['salary']
        print('【工作待遇】')
        print(' ' + jobDetSal + '\n')
        
        """
        00-3工作性質
        """
        jobDetJT = jsonDetail['jobType']
        print('【工作性質】')
        # print(jobDetJT)
        if jobDetJT == 1:
            print(' ' + '全職')
        else:
            print(' ' + '非全職')
        print('\n')

        """
        00-4上班地點
        """
        jobDetAddRe = jsonDetail['addressRegion']
        jobDetAddDe = jsonDetail['addressDetail']
        jobDetIndAr = jsonDetail['industryArea']
        print('【上班地點】')
        print(' ' + jobDetAddRe + jobDetAddDe + jobDetIndAr + '\n')
# 'workType'

        """
        01要求技能總dict
        """
        jsonDetail = lst2jsonData[0]['condition']
        # print(type(jsonDetail))
#         print(jsonDetail['specialty'])#此key對應的value是一個list
#         print('\n')

        """
        01-1技術項dict
        """
        jobConSpe = jsonDetail['specialty']
        jCSseq = 0
        jCSNo = 1
        print('【要求技能】')
        for i in jobConSpe:
            print(str(jCSNo) + '. ' + jobConSpe[jCSseq:jCSseq+1][0]['description'])
            jCSseq += 1
            jCSNo += 1
        print('\n')
        
        """
        01-2其他技能項dict
        """
        jobConOther = jsonDetail['skill']
        jCOseq = 0
        jCONo = 1
        print('【相關能力】')
        for i in jobConOther:
            print(str(jCONo) + '. ' + jobConOther[jCOseq:jCOseq+1][0]['description'])
            jCOseq += 1
            jCONo += 1
        print('\n')
        
        """
        01-3工作經驗
        """
        jobConExp = jsonDetail['workExp']
        print('【工作經驗】')
        print(' ' + jobConExp + '\n')
        
        """
        01-4學歷要求
        """
        jobConEdu = jsonDetail['edu']
        print('【學歷要求】')
        print(' ' + jobConEdu + '\n')
        
        """
        01-5科系要求-其下面為list
        因此print(' ' + jobConMaj)這行不可加str
        """
        jobConMaj = jsonDetail['major']
        jCMseq = 0
        jCMNo = 1
        print('【科系要求】')
        for i in jobConMaj:
            print(str(jCMNo) + '. ' + jobConMaj[jCMseq:jCMseq+1][0])
            jCMseq += 1
            jCMNo += 1
        print('\n')
        """
        01-6語文條件
        """
        jobConLan = jsonDetail['language']
        jCLseq = 0
        jCLNo = 1
        print('【語文條件】')
        for i in jobConLan:
            print(str(jCLNo) + '. ' + jobConLan[jCLseq:jCLseq+1][0]['language'] + ': ' + jobConLan[jCLseq:jCLseq+1][0]['ability'])
            jCLseq += 1
            jCLNo += 1
        print('\n')
        
        """
        01-7其他
        """
        jobConElse = jsonDetail['other']
        print('【其他】')
        print(jobConElse)
        print('\n')
        
        """
        02-1福利制度
        """
        jobWelfare = lst2jsonData[0]['welfare']
        jobWelWel = jobWelfare['welfare']
        print('【福利制度】')
        print(jobWelWel)
        print('\n')
        
        """
        ======================此行開始為內容頁細部爬取結束=====================
        """
        
        a += 1
        print('========')
    page += 1
    newUrl = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007001000&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=11&asc=0&page=' + str(page) + '&mode=s&jobsource=104_new'
    print('\n\n' + '*Warning* You will now enter Page ' + str(page) + ': ' + newUrl + '\n\n')
    url = newUrl
# # 第三筆href開始為職務
