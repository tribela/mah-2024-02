# Kucing Kacang

##

2024-02-18
마스토돈 웹훅은 로컬 게시물에 대해서만 동작합니다. 리모트 게시물은 검증하지 못합니다. 죄송합니다
대신 로컬에서 날뛰는 스팸 계정에 대해서는 동작하도록 하겠습니다

## 하는 일

마스토돈 서버로 들어오는 게시물을 검사해서 검은 고양이 스팸이라면 계정을 정지시켜버립니다


## 사용법

### 관리자용 토큰 생성

https://<인스턴스 주소>/settings/applications
1. 위 페이지로 가서 "새로운 애플리케이션" 버튼을 통해 새 앱 생성 화면으로 갑니다
2. "범위"에서 다른 기본으로 선택된 항목을 모두 지우고 `admin:write:accounts`(계정에 모더레이션 조치 취하기) 항목에만 체크한 후 "제출"을 누릅니다
3. "액세스 토큰"에 적힌 토큰을 잘 적어둡니다

### 웹훅 생성

1. https://<인스턴스 주소>/admin/webhooks/ 페이지로 들어갑니다
2. "활성화된 이벤트" 목록에서 `status.created`만 체크합니다
3. 엔드포인트 URL에는 다음과 같이 입력합니다. 위에서 잘 적어 둔 액세스 토큰을 이용합니다

`https://kucingkacang.kjwon15.net/hooks/<인스턴스 주소>/<액세스 토큰>`

예시

> `https://kucingkacang.kjwon15.net/hooks/qdon.space/lskdfjskldjfklsdjfkls`
