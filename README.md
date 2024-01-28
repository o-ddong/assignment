
# 구현 완료한 기능

---
- 유저 및 상품 관련 API 및 validation 처리
  - 유저 - 회원가입, 로그인, 로그아웃 구현
  - 상품 - 조회(pagination), 생성, 상세 조회, 수정, 삭제, 검색 구현
  - JWT - refresh_token 구현
- 로그인 유저 판단 및 접근 제어
- DB 관련 테이블에 대한 DDL 생성
- JWT token 발행 및 인증 제어
- docker 및 docker-compose 반영
- 테스트 케이스 반영


# 보완 필요한 기능
- 상품 키워드 검색 기능



## 사용 기술

---
#### Service
- MySQL 5.7.44
- Django 4.1
- djangorestframework 3.14.0
- pycryptodomex==3.20.0
- PyJWT==2.8.0
- PyMySQL==1.1.0
- gunicorn==21.2.0

#### Test
- pytest==8.0.0 
- pytest-django==4.7.0
- pytest-cov 4.0.0
- coverage==7.4.1


## DB ERD

---
- <a href="https://dbdiagram.io/d/payhere-65b6a33eac844320aee38442">DB ERD 상세 내역입니다.</a>



## Unit Test Coverage

---
- pytest를 이용하여 간단한 unittest 구현

<img src="https://velog.velcdn.com/images/odh0112/post/bf9032a2-9069-4437-9ba2-06de5b62f0bf/image.png" align="left">

