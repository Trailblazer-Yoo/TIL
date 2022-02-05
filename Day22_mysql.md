# TIL(Today I Learned)

___

> Fab/2nd/2022_Multi campus_유선종 Day22

## mySQL2
오늘은 원래 mysqlworkbench에서 실행해보려 했으나 mysql 접속이 안되는 문제가 발생해서 늦은 시간까지 해결하는데 애를 먹고 있다. 그래서 오늘은 짧게 SELECT문에 대해 알아보고자 한다.

### 1. SELECT문
SELECT문의 기본 구조는 다음과 같다.

```sql
SELECT 필드이름 FROM 테이블이름 WHERE 조건식;
```

1. 필드는 열(column)을 의미한다. 
2. 테이블이름은 내가 사용할 테이블의 이름을 말한다.
3. 조건식은 내가 원하는 조건들을 입력하는 곳인데, 만약 이름이 박보영인 사람을 찾고 싶다면 `WHERE name = '박보영'`처럼 입력하면 된다. 예시를 보자

```sql
SELECT * FROM usertbl WHERE birth >= 1970 AND height >= 170;
```
- 위의 SELECT문은 usertbl이라는 테이블에서 태어난 연도가 1970년보다 같거나 크고 키가 170보다 같거나 큰 데이터를 가진 데이터의 모든 필드를 보여달라는 의미이다.
- WHERE 조건문에 들어가는 조건식은 다양한데 여기서는 5개만 다루도록 하겠다.
___
#### 1. BETWEEN, AND, IN(), LIKE

```sql
SELECT IDname, height From usertbl WHERE height BETWEEN 180 and 183;
```
- 위의 SELECT문은 usertbl이라는 테이블에서 height가 180과 183 사이에 있는 사람의 IDname과 height 필드를 불러오는 기능을 수행한다.
- 여기서 BETWEEN은 ~사이에 라는 의미로, `height >= 180 and height <= 183;`과 동일한 의미이다.

```sql
SELECT IDname, addr From usertbl WHERE addr = '서울' OR addr = '경기' OR addr = '세종';
SELECT IDname, addr From usertbl WHERE addr IN('서울','경기','세종');
```
- 위의 두 셀렉트문은 동일한 기능을 수행한다. usertbl 테이블에서 주소가 서울 또는 경기 또는 세종인 사람의 이름과 주소 필드를 불러온다.
- 조건문에서 OR의 기능을 수행하는 것이 IN()이다.

```sql
SELECT IDname, addr From usertbl WHERE IDname LIKE '_용%';
```

- 위의 SELECT문은 usertbl 테이블에서 '용'을 포함하는 이름을 가진 사람의 이름과 주소를 불러온다.
- LIKE는 완벽히 똑같지는 않지만 일부를 포함하는 것이 있을때 해당 글자를 찾기 위해 사용하는 조건식이다. 글자 앞에 '_', 글자 뒤에 '%'를 넣어줌으로써 글자 앞뒤에는 어떤 글자가 들어가도 괜찮다는 의미가 된다.

```sql
SELECT IDname, height FROM usertbl WHERE height >= ANY(SELECT height FROM usertbl WHERE addr = '경남');
```

- 위의 셀렉트문은 지역이 경남인 사람의 키보다 크거나 같은 사람을 추출하는 의미이다.
- 여기서 ANY()는 괄호 안의 조건안의 어떤 것도 포함할 경우 라는 의미이다. 즉, or과 같은 의미인데 만약 조건에 맞는 키가 180, 183 두개가 나왔다면 둘중에 하나만 해당해도 출력해준다.
> 여기서는 더 넓은 범위를 포함하는 180만 있어도 똑같은 결과가 출력된다.

```sql
SELECT IDname, height FROM usertbl WHERE height >= ALL(SELECT height FROM usertbl WHERE addr = '경남');
```

- 반면에 위의 셀렉트문은 ALL이 들어감으로써 해당 조건에 모두 포함되어야 한다는 뜻이다.
- 위에서는 180보다 크면 됐지만, 이번에는 180보다 크고 183보다 작은 사람들은 포함되지 않는다.