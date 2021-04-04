# 0403資料分析爬取存入-部分功能尚無法執行
# 0401愚人節成功版本-V1
# 0331成功完成 150頁標題+連結爬取
import requests
from bs4 import BeautifulSoup
import json
import os

folderName = '104爬蟲資料分析/'
if not os.path.exists(folderName):
    os.mkdir(folderName)

"""
=================================此行開始為先爬取第一頁各職位標題及連結==============================================
"""

url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=1&mode=s&jobsource=2018indexpoc'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
}

page = 1
print('You r now in Page 1')
"""
動用以下for迴圈可以選擇欲爬取頁數
"""
for i in range(0, 1):
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')


    titleSoupList = soup.select('h2.b-tit')

    a = 3
    No = 1
    for i in range(20):
        try:
            titleSoup = titleSoupList[a]
            title = titleSoup.select('a')
            """
            測試存入資料夾
            """
            try:
                with open(folderName + title[0].text + '.txt', 'w', encoding='utf-8') as f:
                    f.write(title[0].text)
            except FileNotFoundError:
                with open(folderName + title[0].text.replace('/','-') + '.txt', 'w', encoding='utf-8') as f:
                    f.write(title[0].text)
            except OSError:
                pass
    #         =====================
            print(str(No) + '. ' + title[0].text +'\n')
            No += 1
            articleUrl = 'https:' + title[0]['href']
            print(articleUrl + '\n')
    #         =====================
            """
            ========================此行開始為內容頁爬取=====================
            """

            Code = articleUrl[27: 32]
    #         print(Code)
            contentUrl = 'https://www.104.com.tw/job/ajax/content/' + Code + '?jobsource=jolist_c_relevance'
    #         print(contentUrl)
            headers = {
                "Referer": "https://www.104.com.tw/job/" + str(Code), 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
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
            x1 = '【公司名稱】'
            y1 = jsonHeader['custName'] + '\n\n'
            custName = x1 + '\n' + y1
            print(custName)

            """
            00工作內容
            """
            jsonDetail = lst2jsonData[0]['jobDetail']
            x2 = '【工作內容】'
            y2 = jsonDetail['jobDescription'] + '\n'
            jobDescription = x2 + '\n' + y2
            print(jobDescription)
            
            """
            00-1職缺類別 - 0403成功寫入
            """
            jsonDetail = lst2jsonData[0]['jobDetail']
            jobDetCat = jsonDetail['jobCategory']
            x3 = '【職缺類別】'            
            # print(x3)

            jDCseq = 0
            jDCNo = 1
            yJD = 0
            YJDyJD = ""
            for i in jobDetCat:
                Answer = str(jDCNo) + '. ' + jobDetCat[jDCseq:jDCseq+1][0]['description'] + ' '
            #     print(Answer)
                for i in range(len(Answer)):
                    ch = Answer[i]
                    YJDyJD += ch
                    yJD += 1
            #     print(YJDyJD)

                jDCseq += 1
                jDCNo += 1
            # print(YJDyJD)
            jobCategory = x3 + '\n' + YJDyJD + '\n\n'
            print(jobCategory)
            
            """
            00-2工作待遇
            """
            jobDetSal = jsonDetail['salary']
            x4 = '【工作待遇】'
            y4 = ' ' + jobDetSal + '\n'
            jobSalary = x4 + '\n' + y4 + '\n'
            print(jobSalary)
            
            """
            00-3工作性質
            """
            jobDetJT = jsonDetail['jobType']
            x5 = '【工作性質】'
            print(x5)
            # print(jobDetJT)
            if jobDetJT == 1:
                y5 = ' ' + '全職'
                print(y5)
            else:
                y5 = ' ' + '非全職'
                print(y5)
            jobType = x5 + '\n' + y5 + '\n' + '\n'
            print('\n')

            """
            00-4上班地點
            """
            jobDetAddRe = jsonDetail['addressRegion']
            jobDetAddDe = jsonDetail['addressDetail']
            jobDetIndAr = jsonDetail['industryArea']
            x6 = '【上班地點】'
            y6 = ' ' + jobDetAddRe + jobDetAddDe + jobDetIndAr + '\n'
            jobLocation = x6 + '\n' + y6 + '\n'
            print(jobLocation)
    # 'workType'

            """
            01要求技能總dict
            """
            jsonDetail = lst2jsonData[0]['condition']
            # print(type(jsonDetail))
    #         print(jsonDetail['specialty'])#此key對應的value是一個list
    #         print('\n')

            """
            01-1技術項dict - 0403成功寫入
            """
            jobConSpe = jsonDetail['specialty']
            x7 = '【要求技能】'
            jCSseq = 0
            jCSNo = 1
            yJCS = 0
            YJCSyjCS = ""
            for i in jobConSpe:
                Answer = str(jCSNo) + '. ' + jobConSpe[jCSseq:jCSseq+1][0]['description'] + ' '    
                for i in range(len(Answer)):
                    ch = Answer[i]
                    YJCSyjCS += ch
                    yJCS += 1    
                jCSseq += 1
                jCSNo += 1
            jobSpecialty = x7 + '\n' + YJCSyjCS + '\n\n'
            print(jobSpecialty)

            """
            01-2其他技能項dict - 0403成功寫入
            """
            jobConOther = jsonDetail['skill']
            x8 = '【相關能力】'
            jCOseq = 0
            jCONo = 1
            yCO = 0
            YCOyCO = ""
            for i in jobConOther:
                Answer = str(jCONo) + '. ' + jobConOther[jCOseq:jCOseq+1][0]['description'] + ' '    
                for i in range(len(Answer)):
                    ch = Answer[i]
                    YCOyCO += ch
                    yCO += 1         
                jCOseq += 1
                jCONo += 1
            jobSkill = x8 + '\n' + YCOyCO + '\n\n'
            print(jobSkill)

            """
            01-3工作經驗
            """
            jobConExp = jsonDetail['workExp']
            x9 = '【工作經驗】'
            y9 = ' ' + jobConExp + '\n'
            jobworkExp = x9 + '\n' + y9 + '\n'
            print(jobworkExp)

            """
            01-4學歷要求
            """
            jobConEdu = jsonDetail['edu']
            x10 = '【學歷要求】'
            y10 = ' ' + jobConEdu + '\n'
            jobEdu = x10 + '\n' + y10 + '\n'
            print(jobEdu)
            
            """
            01-5科系要求-其下面為list - 0403成功寫入
            因此print(' ' + jobConMaj)這行不可加str
            """
            jobConMaj = jsonDetail['major']
            x11 = '【科系要求】'
            jCMseq = 0
            jCMNo = 1
            yCM = 0
            YCMyCM = ""
            for i in jobConMaj:
                Answer = str(jCMNo) + '. ' + jobConMaj[jCMseq:jCMseq+1][0] + ' '
                for i in range(len(Answer)):
                    ch = Answer[i]
                    YCMyCM += ch
                    yCM += 1  
                jCMseq += 1
                jCMNo += 1
            jobMajor = x11 + '\n' + YCMyCM + '\n\n'
            print(jobMajor)

            """
            01-6語文條件 - 0403成功寫入
            """
            jobConLan = jsonDetail['language']
            x12 = '【語文條件】'
            jCLseq = 0
            jCLNo = 1
            yCL = 0
            YCLyCL=""
            for i in jobConLan:
                Answer = str(jCLNo) + '. ' + jobConLan[jCLseq:jCLseq+1][0]['language'] + ': ' + jobConLan[jCLseq:jCLseq+1][0]['ability']
                for i in range(len(Answer)):
                    ch = Answer[i]
                    YCLyCL += ch
                    yCL += 1 
                jCLseq += 1
                jCLNo += 1
            jobLanguage = x12 + '\n' + YCLyCL + '\n\n'
            print(jobLanguage)

            """
            01-7其他
            """
            jobConElse = jsonDetail['other']
            x13 = '【其他】'
            y13 = jobConElse
            jobLOther = x13 + '\n' + y13 + '\n\n'
            print(jobLOther)

            """
            02-1福利制度
            """
            jobWelfare = lst2jsonData[0]['welfare']
            jobWelWel = jobWelfare['welfare']
            x14 = '【福利制度】'
            y14 = jobWelWel
            jobWelfare = x14 + '\n' + y14 + '\n'
            print(jobWelfare)
            
            """
            ======================此行開始為內容頁細部爬取結束=====================
            """
        
            a += 1
            """
            測試存入資料夾
            """
            try:
                with open(folderName + title[0].text + '.txt', 'w', encoding='utf-8') as f:
                    f.write(custName)
                    f.write(jobDescription)
                    f.write(jobCategory)
                    f.write(jobSalary)
                    f.write(jobType)
                    f.write(jobLocation)
                    f.write(jobSpecialty)
                    f.write(jobSkill)
                    f.write(jobworkExp) 
                    f.write(jobEdu)
                    f.write(jobMajor)
                    f.write(jobLanguage)
                    f.write(jobLOther)
                    f.write(jobWelfare)
            except FileNotFoundError:
                with open(folderName + title[0].text.replace('/','-') + '.txt', 'w', encoding='utf-8') as f:
                    f.write(custName)
                    f.write(jobDescription)
                    f.write(jobCategory)
                    f.write(jobSalary)
                    f.write(jobType)
                    f.write(jobLocation)
                    f.write(jobSpecialty)
                    f.write(jobSkill)
                    f.write(jobworkExp)
                    f.write(jobEdu)
                    f.write(jobMajor)
                    f.write(jobLanguage)
                    f.write(jobLOther)
                    f.write(jobWelfare)
            except FileNotFoundError:
                with open(folderName + title[0].text.replace('\\') + '.txt', 'w', encoding='utf-8') as f:
                    f.write(custName)
                    f.write(jobDescription)
                    f.write(jobCategory)
                    f.write(jobSalary)
                    f.write(jobType)
                    f.write(jobLocation)
                    f.write(jobSpecialty)
                    f.write(jobSkill)
                    f.write(jobworkExp)
                    f.write(jobEdu)
                    f.write(jobMajor)
                    f.write(jobLanguage)
                    f.write(jobLOther)
                    f.write(jobWelfare)
            except OSError:
                pass
#             暫時無法寫入: 00-1職缺類別 /  01-1技術項dict / 01-2其他技能項dict / 01-5科系要求-其下面為list / 01-6語文條件
        except IndexError:
            print(str(No) + '. ' + title[0].text +'\n')
        
        print('========')
    page += 1
    newUrl = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=' + str(page) + '&mode=s&jobsource=2018indexpoc'
    print('\n\n' + '*Warning* You will now enter Page ' + str(page) + ': ' + newUrl + '\n\n')
    url = newUrl
# # 第三筆href開始為職務
