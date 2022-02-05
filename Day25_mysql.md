# TIL(Today I Learned)

___

> Fab/5th/2022_Multi campus_유선종 Day25

## mysql 4일차
오늘은 쿼리문을 작성해서 데이터를 입력하는 것을 알아보고자 한다.

### 1. 테이블 명령어
테이블을 만들려면 필드에 여러 속성들을 설정해줘야 하는데 필드가 숫자 데이터인지 문자열인지 설정하는 타입은 무조건 설정해줘야 한다. 그 외에 기본키나 Null 값을 허용하지 않는 속성 등 다양한 속성을 지정할 수 있다.

#### 1. 테이블 생성

```sql
DROP DATABASE IF EXISTS sqldb; -- 만약 sqldb가 존재하면 우선 삭제한다.
CREATE DATABASE sqldb;

USE sqldb;
CREATE TABLE usertbl -- 회원 테이블
( USERID  	CHAR(8) NOT NULL PRIMARY KEY, -- 사용자 아이디(PK)
  Name    	VARCHAR(10) NOT NULL, -- 이름
  BirthYear INT NOT NULL,  -- 출생년도
  Addr	  	CHAR(2) NOT NULL, -- 지역(경기,서울,경남 식으로 2글자만입력)
  Mobile1	CHAR(3), -- 휴대폰의 국번(011, 016, 017, 018, 019, 010 등)
  Mobile2	CHAR(8), -- 휴대폰의 나머지 전화번호(하이픈제외)
  Height    SMALLINT,  -- 키
  mDate    	DATE  -- 회원 가입일
```

1. `DROP DATABASE IF EXISTS sqldb`는 sqldb라는 스키마가 있을 경우에 삭제해주는 기능을 한다. IF EXISTS는 다른 명령어에서도 사용이 가능하다.
2. `CREATE DATABASE sqldb`는 sqldb 스키마를 생성해준다.
3. `USE sqldb`는 sqldb 스키마를 선택해주는 명령어이다. 스키마를 선택해주지 않으면 테이블이 만들어지지 않거나 엉뚱한 스키마에 생성된다.
4. `CREATE TABLE usertbl`은 usertbl이라는 테이블을 만들어준다.
5. 이제 필드를 형성해주면 된다.
    1. USERID 라는 필드는 8byte 문자열(CHAR(8))만 입력 가능하고 누락(NOT NULL)하면 안된다. 그리고 기본키(PRIMARY KEY)로 지정한다.
    > CHAR(8)은 character(8)의 약자로 'abcdefgh'까지 입력 가능하다.
    2. Name 필드는 8byte이상 입력이 가능한 문자열(VARCHAR(10))을 누락없이 입력해야 한다.
    > VARCHAR(10)는 variable character(10)로 기본적으로 10byte의 문자열을 입력하지만 그 이상도 입력할 수 있다. 실무에서는 char를 쓰지 않고 varchar을 씀으로써 오류나 추가적인 작업을 최대한 줄인다.
    3. BirthYear 필드는 숫자(INT)를 누락없이 입력해야 한다.
    > int는 integer의 약자로 파이썬에서 정수 데이터와 동일한 기능을 한다.
    4. Height 필드는 숫자(SMALLINT)를 입력하는데 누락이 가능하다.
    > 여기서 INT와 SMALLINT, TINYINT의 차이는 byte의 차이만 있을뿐 숫자를 입력하는 것은 동일하다. tinyint는 1byte로 0~255, smallint는 2byte로 -32768 ~ 32768, int는 4byte로 2천까지 입력 가능하다.
    5. mDate는 날짜(DATE) 데이터를 입력받는다. 여기서 날짜를 입력할때 문자열로 입력하며, 형식은 `2022-02-05`로 입력해줘야 한다.
___

#### 2. 테이블에 데이터 입력

```sql
INSERT INTO usertbl VALUES('LSG', '이승기', 1987, '서울', '011', '1111111', 182, '2008-8-8');
INSERT INTO usertbl VALUES('JYP', '조용필', 1950, '경기', '011', '4444444', 166, '2009-4-4');
INSERT INTO usertbl VALUES('SSK', '성시경', 1979, '서울', NULL, NULL, 186, '2013-12-12');
```

- `INSERT INTO usertbl VALUES()`를 사용하면 필드 순서에 맞게 값들이 입력된다.
- `INSERT INTO usertbl (name, BirthYear, Addr, USERID, Mobile1, Mobile2, Height, mDate) VALUES('조용필', 1950, '경기','JYP', '011', '4444444', 166, '2009-4-4');`를 입력하면 괄호안의 필드에 맞게 값이 입력된다. 순서가 달라도 해당 필드에 매칭되어 잘 입력이 된다.

___

- `AUTO_INCREMENT` 기능을 입력하면 인덱싱 기능을 수행할 수 있다. 예를 들어보자.

```sql
CREATE TABLE testTBL(id int AUTO_INCREMENT PRIMARY KEY, userName char(3), age int)
INSERT INTO testTBL VALUES (NULL, 'abc', 25);
INSERT INTO testTBL VALUES (NULL, 'def', 20);
INSERT INTO testTBL VALUES (NULL, 'ghi', 22);
```

- 위의 커리문을 입력하면 `1 abd 25`, `2 def 20` `3 ghi 22`의 데이터가 입력된다. 즉, id 필드에 NULL값을 입력했는데도 알아서 1씩 더해서 입력해준다. 이를 이용해서 데이터의 갯수를 간편하게 파악할 수 있다.
- `AUTO_INCREMENT = 100`을 입력하면 100부터 시작한다.
- `@@AUTO_INCREMENT_INCREMENT = 3`을 입력하면 1씩 증가하지 않고 3씩 증가하게 된다.

___

- 새로운 테이블에 원래 있던 테이블의 데이터를 입력하고 싶다면 다음과 같이 입력하면 된다.

```sql
INSERT INTO NEWTABLE VALUES (SELECT name, height from USER.USERTBL)
```

- 위에 쿼리문처럼 입력하면 USER 스키마에 있는 USERTBL 테이블에서 name과 height 필드의 데이터를 입력한다.

___

#### 테이블의 데이터 수정 및 삭제

1. 데이터를 수정하고 싶다면 `UPDATE 테이블이름 SET 필드 = 값, 필드 = 값, ... WHERE 조건`을 입력해주면 된다.
2. 데이터를 삭제하고 싶다면 `DELETE`를 입력하면 된다.

```sql
DELETE FROM userTBL WHERE name = '박보영';
DELETE FROM userTBL WHERE height >= 180 LIMIT 5;
```

- 위의 쿼리문은 이름이 '박보영'인 데이터를 삭제하는 명령어이다. 아래 쿼리문은 키가 180이상인 데이터를 5개만 삭제해주는 명령어이다.