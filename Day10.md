# TIL(Today I Learned)

___

> Jan/21th/2022_Multi campus_유선종 Day10
## 데이터 시각화 matplotlib
데이터를 수집하고 분석을 했다면 그것들을 시각화하는 작업이 매우 중요하다. 시각화를 통해서 데이터의 특징 등을 한눈에 보기 쉽고 남들에게 설명할 때에도 시각화가 잘된 자료를 제공해야 한다.   이전에 pandas에서 행렬에 관한 모듈을 제공했듯이, matplotlib에서 시각화에 관한 모듈을 제공한다. 자세하게 알아보자

### 1. plot
- plot은 데이터를 x축과 y축을 가지는 2차원 직교좌표계로 나타내준다.
```python
import matplotlib.pyplot as plt
plt.plot([10,20,30,40])
plt.show()
```
이런 명령어를 입력한다면 다음과 같은 그림이 나온다.

<img src="https://user-images.githubusercontent.com/97590480/150542876-f736a41c-8960-4abb-b880-4a82d543a641.png">

여기서 나온 그래프는 (0,10), (1,20), (2,30), (3,40) 점을 이은 1차 함수이다.
> 즉, x값에 대한 정의를 하지 않으면 0부터 값을 넣기 시작하고, 1의 간격으로 값을 할당한다.

```python
import matplotlib.pyplot as plt
plt.plot([1,2,3,4], [12,43,25,15])
plt.show()
```
이런 식으로 x값에 대한 값을 [1,2,3,4]로 할당하면 그게 맞춰서 y값이 할당된다.

<img src="https://user-images.githubusercontent.com/97590480/150543438-0c38d51a-3652-41d1-8097-2d67d61dc1fc.png">

> 이 이미지를 보면 1부터 값이 시작하는 것을 알 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/150543663-60b948ef-fd20-4b63-983d-9ac212b90e50.png">

```python
import matplotlib.pyplot as plt
plt.title('legend')
plt.plot([10,20,30,40], label = 'asc')
plt.plot([40,30,20,10], label = 'desc')
plt.legend(loc = 2)
plt.show()
```
- 위의 사진에서 그래프 위에 legend라는 제목이 생긴것을 볼 수 있는데, `plt.title('legen')` 명령어를 사용하면 제목을 넣을 수 있다.
- 또한 plot 명령어를 두번 썼는데 동일한 좌표계에 표시되는 것을 볼 수 있다. 또한, label 명령어를 통해 그래프에 이름을 지을 수 있다.
- 또한 `plt.legend()`은 그래프 옆에 범례를 표시해준다. loc를 설정해주면 범례의 위치를 조절할 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/150544393-8dd2a0bd-fc63-437d-b993-6b26531bd23d.png">

```python
import matplotlib.pyplot as plt
plt.title('linestyle')
plt.plot([10,20,30,40], color = 'r', linestyle = '--', label = 'dashed')
plt.plot([40,30,20,10], color = 'g', ls = ':', label = 'dotted')
plt.legend()
plt.show()
```

- 위에서 plot 명령어 안에 다양한 설정을 할 수 있는데, color는 색깔을 지정할 수 있고 linestyl은 그래프의 선 스타일을 지정할 수 있다.

#### 서울 기온 그래프
너무 단순한 예들만 보여줬으니 좀더 복잡한 데이터를 사용해서 시각화해보자.

<img src="https://user-images.githubusercontent.com/97590480/150544875-7d1c379d-0d1c-49b8-98c5-0acd4dadd064.png">

```python
import csv
import matplotlib.pyplot as plt
f = open('seoul.csv')
data = csv.reader(f)
next(data)
low = []
high = []
for row in data:
    if row[-1] != '':
        if row[0].split('.')[1] == '9' and row[0].split('.')[2] == '28':
            low.append(float(row[-2]))
            high.append(float(row[-1]))
plt.plot(high, 'blue')
plt.plot(low,'red')
plt.show()
```
- 여기서 `import csv`는 텍스트 자료에 대한 모듈을 불러오는 것을 의미한다.
- `open('seoul.csv')`를 사용해서 서울의 1904년부터 2022년 기온 데이터 파일을 연다. 연 파일을 f에 넣는다.
- `data = csv.reader(f)`는 seoul.csv 파일에 있는 데이터를 읽는 명령어이다.
- `next(data)`는 첫번째 자료를 읽거나 할당받고 포인터를 아랫줄로 내린다.
> 포인터는 Day08에서 자세히 설명했지만 간단히 설명하자면 데이터를 읽을 때 포인터가 위치한 데이터를 읽는다. 따라서 포인터가 내려감에 따라 데이터를 차근차근 읽게 된다. next를 사용하는 이유는 첫번째 데이터가 ['날짜','평균기온','최저기온','최고기온']의 문자 자료이기 때문에 next를 안하면 숫자 데이터가 아니기 때문에 오류가 발생한다.
- `for row in data`는 포인터가 있는 자료의 행을 읽는 명령어이다. for문이므로 데이터의 모든 자료들을 읽을때까지 반복된다.
- `if row[-1] != ''`는 중간에 누락된 데이터들이 있기 때문에 빈칸으로 쓰여진 데이터를 구별해주기 위해서 만약 row[-1]의 데이터 빈칸이 아닐 경우라는 조건을 달아줬다.
- `if row[0].split('.')[1] == '9' and row[0].split('.')[2] == '28'`는 내 생일 데이터만 불러오는 작업이다.
   - row[0]의 데이터는 날짜 데이터로 `2022.1.21` 이런 식으로 되어있다. 따라서 `split('.')` 명령어를 이용해서 점(.)을 제거해준다.
   - split을 사용하면 ['2022','1','21']의 스트링을 포함한 리스트 데이터로 전환되는데, 바로 뒤에 [1]의 인덱싱 명령어를 사용해서 월과 일의 데이터를 추출한다.
- `low.append(float(row[-2]))`는 append가 리스트에 새로운 데이터를 추가하는 명령어이다. 따라서 for문이 반복되면서 데이터들이 차곡차곡 low 리스트에 들어오게 된다.
- 이런 식으로 데이터를 리스트에 모아서 plot 명령어를 사용하면 위에와 같은 그래프가 나오게 된다.

### 2. hist
- hist는 히스토그램을 나타내주는 명령어이다. 예시를 보자.

<img src="https://user-images.githubusercontent.com/97590480/150547220-2406556b-8fbf-484c-87f1-cef1f9c5ab70.png">

```python
import random
import matplotlib.pyplot as plt
dice = []
for i in range(100):
    dice.append(random.randint(1,6))
plt.hist(dice, bins = 6)
plt.show()
```
- `import random`은 무작위의 숫자를 할당하고 싶을때 사용하는 모듈이다.
- `randint(1,6)`을 사용해서 1,2,3,4,5,6 중 무작위로 한개를 선택한다. 이 과정을 총 100번 한다.
- `plt.hist(dice, bins = 6)`을 사용해서 이와 관련된 히스토그램을 그릴 수 있다. bins는 범위를 나타내는데, bins = 6이면 1~6까지의 데이터를 표시해준다. 기본값은 10이기 때문에 bins명령어를 생략한다면 1~10까지의 범위를 가진 히스토그램이 나타나게 된다.