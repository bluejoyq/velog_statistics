
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOADING_WAIT_TIME = 3
def init_driver():
    driver = uc.Chrome()
    driver.get('https://velog.io')
    return driver
def do_login(driver):
    driver.find_element(By.XPATH,'//button[text()="로그인"]').click()
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[text()="새 글 작성"]')
        )
    )

def wait_for_infinite_scroll(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")   

    while True:
        # Scroll down to bottom                                                     
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)                                              
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);") 
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height            
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:                                          
            break

        last_height = new_height
def get_posts_links(driver):
    driver.find_element(By.XPATH,'//button[text()="새 글 작성"]/../div').click()
    WebDriverWait(driver, LOADING_WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[text()="내 벨로그"]')
        )
    )
    driver.find_element(By.XPATH,'//div[text()="내 벨로그"]').click()
    WebDriverWait(driver, LOADING_WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a/h2/..')
        )
    )
    wait_for_infinite_scroll()
    return [elem.get_attribute('href') 
        for elem in driver.find_elements(By.XPATH,'//a/h2/..')]

def get_post_info(driver, post_link):
    result = {}
    result['url'] = post_link
    driver.get(post_link)
    WebDriverWait(driver, LOADING_WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[text()="통계"]')
        )
    )
    result['title'] = driver.find_element(By.XPATH, '//h1').text
    driver.find_element(By.XPATH, '//button[text()="통계"]').click()
    WebDriverWait(driver, LOADING_WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'value')
        )
    )
    spans = driver.find_elements(By.CLASS_NAME, 'value')
    result['total_view'] = int(spans[0].text.replace(',',''))
    result['today_view'] = int(spans[1].text.replace(',',''))
    result['yesterday_view'] = int(spans[2].text.replace(',',''))
    return result

def get_velog_info():
    driver = init_driver()
    do_login(driver)
    
    result = []
    
    for post_link in get_posts_links(driver):
        result.append(get_post_info(driver, post_link))
    return result


def get_dummy_velog_info():
    return [{'url': 'https://velog.io/@bluejoyq/selenium%EC%9C%BC%EB%A1%9C-%EA%B5%AC%EA%B8%80-%EB%A1%9C%EA%B7%B8%EC%9D%B8%ED%95%98%EA%B8%B0', 'title': 'selenium으로 구글 로그인하기', 'view': 12}, {'url': 'https://velog.io/@bluejoyq/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4-%EA%B3%B5%ED%95%99%EB%A6%AC%ED%8C%A9%ED%84%B0%EB%A7%81-3%EC%9E%A5', 'title': '[소프트웨어 공학]리팩터링 3장', 'view': 14}, {'url': 'https://velog.io/@bluejoyq/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4-%EA%B3%B5%ED%95%99%EB%A6%AC%ED%8C%A9%ED%84%B0%EB%A7%81-2%EC%9E%A5', 'title': '[소프트웨어 공학]리팩터링 2장', 'view': 15}, {'url': 'https://velog.io/@bluejoyq/React-Redux-redux%EC%9D%98-state%EC%99%80-Modal2', 'title': '[React Redux] redux의 state와 Modal(2)', 'view': 18}, {'url': 'https://velog.io/@bluejoyq/Python-round%EC%99%80-float', 'title': '[Python] round와 float', 'view': 19}, {'url': 'https://velog.io/@bluejoyq/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%ED%80%B5-%EC%A0%95%EB%A0%ACquick-sort-vs-%EB%B3%91%ED%95%A9-%EC%A0%95%EB%A0%ACmerge-sort', 'title': '[알고리즘] 퀵 정렬(quick sort) vs 병합 정렬(merge sort)', 'view': 21}, {'url': 'https://velog.io/@bluejoyq/js%EB%A6%AC%ED%8C%A9%ED%84%B0%EB%A7%81-1%EC%9E%A5', 'title': '[소프트웨어 공학]리팩터링 1장', 'view': 22}, {'url': 'https://velog.io/@bluejoyq/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-KMP', 'title': '[알고 리즘] KMP', 'view': 22}, {'url': 'https://velog.io/@bluejoyq/%EB%B0%B1%EC%A4%80-1847%EB%B2%88-python', 'title': '[알고리즘] 백준 1847번 python', 'view': 26}, {'url': 'https://velog.io/@bluejoyq/%EC%82%BC%EC%84%B1%EB%85%B8%ED%8A%B8-%ED%85%9C%ED%94%8C%EB%A6%BF-%EC%9D%B4%EB%B6%84%ED%95%A0-%EB%85%B8%ED%8A%B8', 'title': '[삼성노트 템플릿] 이분할 노트', 'view': 33}, {'url': 'https://velog.io/@bluejoyq/python-%EB%B0%B1%EC%A4%80-4354%EB%B2%88-%EB%AC%B8%EC%9E%90%EC%97%B4-%EC%A0%9C%EA%B3%B1', 'title': '[알고리즘] 백준 4354번 문자열 제곱', 'view': 35}, {'url': 'https://velog.io/@bluejoyq/React-Redux-redux%EC%9D%98-state%EC%99%80-Modal1', 'title': '[React Redux] redux의 state와 Modal(1)', 'view': 41}, {'url': 'https://velog.io/@bluejoyq/Python-VSCode-%EA%B5%AC%EC%84%B1%EB%90%9C-%EB%94%94%EB%B2%84%EA%B7%B8-%EC%9C%A0%ED%98%95-python%EC%9D%B4%EA%B0%80-%EC%84%A4%EC%B9%98%EB%90%98%EC%97%88%EC%A7%80%EB%A7%8C-%EC%9D%B4-%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C-%EC%A7%80%EC%9B%90%EB%90%98%EC%A7%80-%EC%95%8A%EC%8A%B5%EB%8B%88%EB%8B%A4', 'title': "# [Python VSCode]  구성된 디버그 유형 'python'이(가) 설치되었지만 이 환경에서 지원되지 않습니다.", 'view': 55}, {'url': 'https://velog.io/@bluejoyq/python3', 'title': '[python3] 리스트 초기화 속도 차이', 'view': 62}, {'url': 'https://velog.io/@bluejoyq/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-2021-Winter-Coding-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8-%ED%9B%84%EA%B8%B0', 'title': '프로그래머스 2021 Winter Coding 코딩테스트 후기', 'view': 65}, {'url': 'https://velog.io/@bluejoyq/JS%EC%97%90%EC%84%9C%EC%9D%98-%ED%95%A8%EC%88%98-%EC%84%A0%EC%96%B8-%EB%B0%A9%EB%B2%95%EC%97%90-%EB%94%B0%EB%A5%B8-%EC%B0%A8%EC%9D%B4', 'title': '[JS] JS에서의 함수 선언 방법에 따른 차이', 'view': 91}, {'url': 'https://velog.io/@bluejoyq/Next.js-hot-reload-%EB%B0%98%EC%98%81%EC%9D%B4-%EC%95%88%EB%90%98%EB%8A%94-%EB%AC%B8%EC%A0%9C', 'title': '[Next JS] hot reload 반영이 안되는  문제', 'view': 100}, {'url': 'https://velog.io/@bluejoyq/react-toast-ui-editor', 'title': '[React] TOAST UI markdown Editor 사용하기', 'view': 1631}]
if  __name__  ==  "__main__" :
    datas = get_velog_info()
    datas.sort(key = lambda x : -x['total_view'])

    sum_total_view = 0
    sum_today_view = 0
    sum_yesterday_view = 0
    for i in range(len(datas)):
        data = datas[i]
        sum_total_view += data['total_view']
        sum_today_view += data['today_view']
        sum_yesterday_view += data['yesterday_view']
        print(i + 1, data['total_view'], data['today_view'], data['yesterday_view'], data['title'], data['url'])
    print(sum_total_view,sum_today_view, sum_yesterday_view)