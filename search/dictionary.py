import urllib.request, json, re

import path

with open(path.KEY_PATH, 'r') as data_file:
    data = json.load(data_file)


def search_keyword_by_naver_dic(input_text):
    client_id = data['search_api-id']  # key.json 파일의 search_api-id 부분을 입력
    client_secret = data['search_api-secret']  # key.json 파일의 search_api-secret 부분을 입력
    encText = urllib.parse.quote(input_text)  # url에 한글 검색어를 입력할 수 있도록 인코딩해주는 모듈(quote : 공백을 '%20'으로 인코딩 시킴)
    url = "https://openapi.naver.com/v1/search/encyc.json?display=1&query=" + encText  # 백과사전 검색요청 URL
    request = urllib.request.Request(url)  # Request 객체를 생성

    # response 헤더 정보를 추가 (api key)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)  # HTTP 요청에 대한 응답을 받아옴
    rescode = response.getcode()

    if rescode == 200:  # HTTP 200 OK
        response_body = response.read()  # 요청 결과에 대한 응답 body를 읽음
        dict = json.loads(response_body.decode('utf-8'))  # UTF-8 스트링을 JSON으로 파싱

        list = dict['items']  # dict의 items 항목
        result = list[0]  # list의 첫 번째 항목
        result2 = result['description']  # result의 description 항목

        result3 = re.sub('</*b>|[[]|[]]|[(]|[)]|[-]', '', result2)  # 정규표현식으로 불필요한 태그 제거
        result4 = re.findall('^.*?[.]', result3)  # 첫 문장이 끝나는 부분까지만을 추출

        return result4[0]  # 추출한 리스트의 첫 번째 항목을 반환
    else:
        # print("Error Code:" + rescode)

        # 단어에 대한 결과값이 나오지 않은 경우
        return '해당 내용을 찾을 수 없습니다.'


if __name__ == '__main__':
    """
    테스트 코드
    """
    search_keyword_by_naver_dic('백과사전')
