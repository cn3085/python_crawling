# python_crawling
# Image/HTML content Scraper

## 개발 환경
| 항목 | 내용 |
| --- | --- |
| OS | Windows 10 |
| Lang | python 3.7.4 |
| WebDriver | Chrome Driver 78.x |
| Library | selenium |

## 사용 방법

1. config.py 생성 후 suyuURL, suyuID, suyuPWD, tistoryURL, tistoryID,  tistoryPWD 입력
2. main.py에서 max_page 변수 적절히 입력
3. 실행


## 로직

1. suyu104 로그인
2. tistory로그인
3. 해당 페이지가 존재하는지 확인 (404시 다음 페이지로 이동)
4. 모듈네임 가져와서 매칭될 모듈네임 만들어줌
5. 등록날짜 가져오기
6. 게시글 제목 가져오기
7. 본문 가져오기
7.1 사전작업 - 본문에서 필요없는 태그들 삭제
7.2 본문에서 이미지 가져와서 저장하기
7.3. 파일 제목 만들기
7.4. 이미지 모두 저장
7.5 img src 변경 본문에서 suyu_URL 삭제하기
8. post 요청 보내기

## 이슈
1. csv 파일 저장시 특정 HTML 태그가 깨지는 문
