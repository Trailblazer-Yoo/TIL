# TIL(Today I Learned)

___

> Fab/3th/2022_Multi campus_유선종 Day23

## mysql 비밀번호 분실
어제 mysql 비밀번호 오류가 떠서 해결하느라 애를 먹었다. 결론적으로 내 mac에서 발생한 비밀번호 오류는 brew에서 설치한 mysql과 mysql 홈페이지에서 다운받은 mysql과 충돌이 일어나서 접속이 안된 것 같다. 둘다 삭제한 뒤 mysql 홈페이지에서 다운받으니 잘 된다. 그래서 오늘은 비밀번호 분실시 해결방법을 기록해놓으려 한다.
> brew와 홈페이지에서 다운받는 것 중에서 brew에서 다운받는 것이 에러가 덜 뜨고 안정적이라고 한다. 하지만 우리 mysql은 m1칩이 탑재된 버전도 지원하기 때문에 나는 홈페이지에서 다운로드 받았다.
___
### brew로 설치된 mysql 삭제하기
1. homebrew로 설치한 경우 터미널을 키고 다음 코드를 하나하나 입력해주자.

```python
brew services stop mysql
```
brew에서 mysql 서버를 중지시키는 명령어이다.

2. 명령어 하나만 입력해주면 삭제가 되는데 혹시 작동하지 않는다면 그 밑에 수동으로 하나하나 삭제하는 방법을 같이 첨부하겠다.

```python
brew uninstall --force mysql
```

위의 코드를 입력하면 삭제가 완료된다.

```python
which mysql
```

mysql 설치 경로를 확인해줘야한다. 만약, 설치 경로가 `/usr/local/bin/mysql`라면 아래 코드를 그대로 입력하면 되고 아니라면 설치 경로에 따라 수정해줘야한다.

```python
sudo rm -rf /usr/local/mysql
sudo rm -rf /usr/local/bin/mysql
sudo rm -rf /usr/local/var/mysql
sudo rm -rf /usr/local/Cellar/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /tmp/mysql.sock.lock
sudo rm -rf /tmp/mysqlx.sock.lock
sudo rm -rf /tmp/mysql.sock
sudo rm -rf /tmp/mysqlx.sock
sudo rm ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
```

그리고 재부팅을 한 후 homebrew로 재설치해주면 된다.

3. 홈페이지에서 받은 mysql을 삭제하는 방법은 환경설정 -> 맨 아래에 보이는 mysql 클릭 -> Uninstall 클릭 이다. 재설치했다는 것은 설치를 한번 해봤다는 의미이므로 설치하는 방법은 생략하겠다.

<img width = "75%" src="https://user-images.githubusercontent.com/97590480/152305906-0b484bf1-2b6a-460d-9350-c5d1837f4cf6.png">

> Unintall을 해주면 자동으로 삭제해주니 삭제하고 다시 홈페이지에 가서 설치해주면 된다.

<img width = "75%" src="https://user-images.githubusercontent.com/97590480/152306129-3e0e440c-0cfd-491d-9f32-e21c1f02e2ee.png">

> 위의 Community Server을 클릭하고 자기 맥에 맞는 버전을 설치하면 된다. 주소는 `https://dev.mysql.com/downloads/` 이다.
___
### 비밀번호 재설정
나처럼 두 mysql이 충돌해서 접속이 안되는 문제가 발생한 것이 아니라 비밀번호를 단순히 잊어버렸다면 다음 절차를 이용해서 비밀번호를 재설정해주자.

1. 실행중인 mysql 서버를 종료한다.

```python
mysql.server stop
```

2. mysql을 mysql이 설치된 폴더에서 실행시켜주자. 터미널을 키면 보통 home에 있기 때문에 cd 명령어를 통해서 이동합시다. 만약, brew로 설치했다면 경로가 다를 것이다.. 아래 코드를 참조하자.

```python
cd ..
cd ..
## root 폴더까지 이동
cd /usr/local/mysql/bin
## 홈페이지에서 설치한 경우의 경로
cd /usr/local/opt/mysql/bin
## homebrew로 설치한 경우
```

3. 비밀번호 없이도 들어갈 수 있는 명령어를 입력해준다.

```python
mysqld_safe --skip-grant-tables &
```

> 한번 입력하면 계속 비밀번호 없이 들어갈 수 있다.

4. mysql에 비밀번호 없이 접속해준다.

```python
mysql -u root
```

> 만약에 access denied 됐다면 위의 명령어를 잘못 쳤을 가능성이 크다. 혹은 어떤 에러땜에 발생한 문제이므로 컴퓨터를 다시 껐다 키고 1.에서부터 다시 진행해주자.

5. 아래의 명령어를 통해서 비밀번호를 변경해주자.

```python
UPDATE mysql.user SET authentication_string='????' WHERE user='root';
flush privileges;
```

> flush privileges는 권한을 적용하는 명령어이다. 바꾼 비밀번호를 한번 더 도장 쾅쾅 찍는 느낌이다.

- 혹시 안된다면 밑의 명령어를 입력해보자.

```python
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY '????';
```

> 이렇게 해도 안되면 삭제했다가 다시 깔자. 검색하는 것보다 이게 더 빠를 수 있다.