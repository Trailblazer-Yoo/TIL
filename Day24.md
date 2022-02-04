# TIL(Today I Learned)

___

> Fab/4th/2022_Multi campus_유선종 Day24

## mysql 3일차
이번에는 mysql에서 제공하는 GUI 환경의 작업환경을 제공하는 workbench에 대해서 알아보고자 한다. GUI란 graphical user interface의 줄임말로 우리가 평소에 사용하는 윈도우즈 같은 환경을 말한다. 즉, mysql은 터미널같은 cmd 환경에서도 작업이 가능하지만 사용자의 편의를 위해 시각적으로 편리한 workbench도 지원한다.

### 1. workbench 살펴보기
workbench를 설치하는 방법은 mysql 홈페이지에서 다운을 받으면 되기 때문에 따로 설명을 하지는 않겠다. workbench를 설치하고 실행하면 다음과 같은 화면이 나오게 된다.

<img src="https://user-images.githubusercontent.com/97590480/152449397-36919597-67f1-47e8-89c2-a2c74da2b672.png">

> 설치하고 바로 실행했기 때문에 user가 root밖에 없는 것을 확인할 수 있다. 보통은 root말고 다른 아이디를 생성해서 작업한다.

- 저기서 Local instance 3306 을 클릭해서 작업환경에 들어가자. 비밀번호가 설정되어 있다면 설치할 때 입력했던 비밀번호를 입력해주면 된다.

<img src="https://user-images.githubusercontent.com/97590480/152449713-38dba712-cd4b-429f-9128-df4d7e1ebebf.png">

- 여기서 우리가 주로 들어가게 될 창은 저 `schemas`라는 탭이다. 스키마는 데이터베이스와 동일한 단어로 사용된다는 것을 잊지말자. 스키마를 클릭하면 다양한 DB들이 존재하는 것을 볼 수 있다.
> 처음 설치하면 스키마에 sys밖에 없다. 나는 mysql에서 예시 DB를 다운받거나 내가 직접 데이터를 입력한 것들이 존재하기에 DB들이 많은 것이다. employees는 mysql에서 제공하는 예시 DB이므로 다운받아서 사용해보자.

<img src="https://user-images.githubusercontent.com/97590480/152508486-43ef5477-9ac4-42b2-8aad-b578ec8df8d2.png">

- 위의 사진을 보면 테이블 위에서 오른쪽 마우스를 클릭하고 `select rows`를 클릭하면 현재 테이블의 모든 행들을 보여준다.
- 옆에 보면 `SELECT * FROM employees.departments;`가 입력되어 있는 것을 볼 수 있다. `select rows`를 클릭하면 옆의 명령어를 쿼리에서 실행해서 결과창을 보여주는 것이다.
- 즉, 모든 명령어는 쿼리를 통해 실행이 된다. 테이블을 보는 것은 오른쪽 클릭으로 들어가는게 편할 수 있지만, 대부분의 작업은 쿼리문을 작성하는 것이 편하다.

<img src="https://user-images.githubusercontent.com/97590480/152509671-9686d476-ed65-4d2f-85a2-dbe2407333a8.png">

- 위의 사진 또한 테이블을 우클릭으로 생성하는 방법이다. 테이블을 생성하기 위해서는 `create table [테이블이름] values [필드 이름 및 조건]` 쿼리문을 작성해야 한다.
- 하지만 나는 테이블을 만들 때에는 우클릭이 더 편하다고 생각한다.
> 그렇다고 쿼리문을 무시하면 안된다. 나중에 파이썬으로 DB를 조작할때 쿼리문 작성은 필수이다.

___
### 2.EER 다이어그램
EER 다이어그램은 테이블간의 관계를 도식화하여 보여주는 기능을 말한다. MS ACCESS에서 관계 설정과 비슷한 기능이다. EER 다이어그램에서 1:N 등의 관계를 설정할 수 있고, 테이블을 만들수도 있다. 이전에 우리가 계층형 DBMS, 관계형 DBMS 같은 것들을 얘기한적이 있는데, EER 다이어그램에서 DBMS의 구조를 설정한다.

<img src="https://user-images.githubusercontent.com/97590480/152510359-b305a651-3417-4b3d-9a51-86b64918b204.png">

> File -> New Model 을 클릭하자.

<img src="https://user-images.githubusercontent.com/97590480/152510375-28d2f161-66f9-42e1-aba9-d7ec691570bc.png">

> 들어가면 위와 같은 화면이 나오게 된다. 여기서 새로운 EER 다이어그램을 생성하고 싶다면 Add Diagram을 클릭하자

<img src="https://user-images.githubusercontent.com/97590480/152511810-cb65e757-290e-4653-b935-949d613f2877.png">

- Add Diagram을 클릭하면 위와 같은 화면이 나온다. 여기서 저 빨간색 동그라미를 클릭해서 하얀 모눈종이 위에 드래그 해주면 새로운 테이블이 생성된다.
- 그리고 새로 생성된 테이블을 두번 클릭하면 다음과 같은 화면이 나온다.

<img src="https://user-images.githubusercontent.com/97590480/152512003-23620279-bf06-4d7e-9cae-11b1209a2322.png">

> workbench 스키마 화면에서 테이블을 만들 때와 동일한 화면이 나온다.

<img src="https://user-images.githubusercontent.com/97590480/152512278-c0e295d0-397e-4b57-9322-83e8fbeef43e.png">

- 위의 사진에서 Database -> forward Engineering을 클릭하면 EER Diagram에서 생성했던 테이블을 다른 DBMS에 보내준다. 여기서는 root밖에 없으므로 아무런 설정을 하지 않으면 root의 스키마에 EER Diagram의 mydb라는 스키마가 생성되고 그 안에 테이블들이 만들어진다.
- 반대로 Database -> reverse Engineering을 클릭하면 root나 다른 user의 스키마에서 테이블을 가져온다.
