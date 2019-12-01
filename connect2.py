from selenium import webdriver
import pandas as pd
import datetime
import module_matcher
import urllib3
import openpyxl
import xlwt
import json

# 설정
driver = webdriver.Chrome('C:/Users/TJ/Downloads/chromedriver_win32/chromedriver')

# suyu104 로그인
driver.get('http://localhost:3000/member/login')
driver.find_element_by_xpath('//*[@id="USER_ID"]').send_keys('test')
driver.find_element_by_xpath('//*[@id="PASSWORD"]').send_keys('123456')
driver.find_element_by_xpath('//*[@id="frm"]/table/tbody/tr[1]/td[3]/input').click()

# tstory로그인
driver.get('https://www.tistory.com/auth/login')
driver.find_element_by_xpath('//*[@id="loginId"]').send_keys('trans.n2009@gmail.com')
driver.find_element_by_xpath('//*[@id="loginPw"]').send_keys('suyunomoaleph104!')
driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/button').click()

http = urllib3.PoolManager()
url = 'https://nomadist.tistory.com/'
results = []
max = 630
############################### 반복구간 ######################################
# for i in range(1, 100):
for i in [547]:
    # 0. 해당 페이지가 존재하는지 확인
    targetUrl = url + str(i)
    # response = http.request('GET', targetUrl)
    # status = response.status
    # if status == 404 :
    #     continue

    driver.get(targetUrl)
    # 1. 모듈네임 가져와서 매칭될 모듈네임 만들어줌
    _moduleName = driver.find_elements_by_class_name('category')
    if len(_moduleName) == 0:
        print(targetUrl + ' ::: 존재하지 않는 페이지')
        continue
    moduleName = _moduleName[0].find_elements_by_tag_name('a')[0].text
    moduleSrl = module_matcher.match(moduleName)

    # 2. 등록날짜 가져오기
    _regDate = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/p/span[1]').text
    regDate = datetime.datetime.strptime(_regDate, '%Y.%m.%d %H:%M')
    regDate = regDate.strftime('%Y%m%d%H%M%S')

    # 3. 게시글 제목 가져오기
    title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/h2/a').text

    # 4. 사전작업 - 본문에서 필요없는 태그들 삭제
    rm_target1 = driver.find_elements_by_class_name(
        'container_postbtn')  # 엘리먼트가 없어도 exception이 나지 않도록 find_elements로 리스트로 받아 확인하는 게 좋다
    if len(rm_target1) > 0:
        driver.execute_script('arguments[0].remove()', rm_target1[0])
    rm_target2 = driver.find_elements_by_class_name('tt-plugin')
    if len(rm_target2) > 0:
        driver.execute_script('arguments[0].remove()', rm_target2[0])
    rm_target3 = driver.find_elements_by_class_name('another_category')
    if len(rm_target3) > 0:
        driver.execute_script('arguments[0].remove()', rm_target3[0])

    # 5. 본문 긁어오기
    content = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]').get_attribute('innerHTML')

    document = {'MODULE_SRL': moduleSrl,
                'CATEGORY_SRL': 0,
                'LANG_CODE': 'ko',
                'IS_NOTICE': 'N',
                'TITLE': title,
                'TITLE_BOLD': 'N',
                'TITLE_COLOR': 'N',
                'CONTENT': content,
                'READED_COUNT': 0,
                'VOTED_COUNT': 0,
                'BLAMED_COUNT': 0,
                'COMMENT_COUNT': 0,
                'TRACKBACK_COUNT': 0,
                'UPLOADED_COUNT': 0,
                'PASSWORD': '',
                'USER_ID': 'suyu_webzine',
                'USER_NAME': '수유너머_웹진',
                'NICK_NAME': '수유너머_웹진',
                'MEMBER_SRL': 157936,
                'EMAIL_ADDRESS': 'suyunomo1041@gmail.com',
                'HOMEPAGE': '',
                'TAGS': '',
                'EXTRA_VARS': '',
                'REGDATE': regDate,
                'LAST_UPDATE': '',
                'LAST_UPDATER': '',
                'IPADDRESS': '115.89.186.2',
                'LIST_ORDER': '',
                'UPDATE_ORDER': '',
                'ALLOW_TRACKBACK': 'N',
                'NOTIFY_MESSAGE': 'N',
                'STATUS': 'PUBLIC',
                'COMMENT_STATUS': 'ALLOW',
                'TRASH': 'N'
                }

    # 5. post 요청 보내기
    data = document
    res = http.request('POST', '127.0.0.1:3000/s104/for_webzine', body=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    if res.status != 200:
        print(targetUrl + ' : error')

    print(targetUrl + ' ::: 크롤링 완료')
    results.append(document)

    driver.close()
############################### 반복구간 종료 ######################################

# ============================== 5. csv 파일 만들기
# data = pd.DataFrame(results)
# data.head(5)
# RESULT_PATH = 'C:/Users/TJ/Desktop/csv/'
# time = datetime.datetime.now()
# now = time.strftime('%Y-%m-%d_%H:%M:%S')
# # data.to_csv(RESULT_PATH+'webzine.csv', encoding='cp949')
# # data.to_csv(RESULT_PATH+'webzine.csv', encoding='euc-kr')
# # data.to_csv(RESULT_PATH+'webzine.csv', encoding='UTF-8')
# # data.to_csv(RESULT_PATH+'webzine.csv', encoding='utf-8-sig')
#
# data.to_excel(RESULT_PATH+'webzine.xls', encoding='utf-8-sig')

# ============================== 6. JSON 파일 만들기
# def toJson(data):
#     with open('mnet_chart.json', 'w', encoding='utf-8') as file :
#         json.dump(data, file, ensure_ascii=False, indent='\t')
#
# toJson(results)
