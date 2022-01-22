# TIL(Today I Learned)

___

> Jan/21th/2022_Multi campus_유선종 Day10
## 데이터 시각화 matplotlib 2일차
어제에 이어서 데이터를 여러 시각화 방식으로 표현해보자

### 1. baxplot
- baxplot은 통계학에서 3분위수와 1분위수 값을 범위로 갖는 사각형을 그리고 그 안에 2분위수(중앙값) 사각형 밖에는 최댓값과 최솟값, 그 밖에는 점으로 이상점(outlier)을 시각화한 명령어이다.

```python
import matplotlib.pyplot as plt
import random
result = []
for i in range(13):
    result.append(random.randint(1,1000))
print(sorted(result))
plt.boxplot(result)
plt.show()
```

<img src="https://user-images.githubusercontent.com/97590480/150621312-9c5144fc-7203-4b93-8f01-68e5c4e2024b.png">>

> 첫번째 줄에 리스트 안에 있는 값들을 boxplot으로 표현한 것이다. 노란색 줄은 중앙값이고, 상자의 윗쪽 값은 3분위수, 아래 값은 1분위수이다. 그리고 일직선에 수직으로 표시된 양 끝값은 최댓값과 최솟값이다.

<img src="https://user-images.githubusercontent.com/97590480/150621478-bcda0d44-8714-4cf2-abe4-3a71352a99e7.png">

위의 이미지는 Day08에서 설명한 포인터와 관련된 자료이다. 이런식으로 각 월에 대한 boxplot을 표시할 수 있다. 자세한 코드는 아래와 같다.

```python
import matplotlib.pyplot as plt
import csv
month = []
for i in range(1,13):
    f = open('seoul.csv')
    data = csv.reader(f)
    next(data)
    box = []
    for row in data:
        if row[-1] != '' and int(row[0].split('.')[1]) == i: box.append(float(row[-2]))
    month.append(box)
    f.seek(0)
    f.close()
plt.boxplot(month)
plt.show()
```
___
### 2. 파이 도형
파이 도형은 원 안에 각 데이터가 차지하는 비율을 표시해준다.

```python
size = [2441, 2312, 1031, 1233]
label = ['A','B','C','O']
plt.axis('equal')
color = ['darkmagenta','deeppink','hotpink','pink']
plt.pie(size, labels = label, autopct = '%.1f%%', colors = color, explode= (0,0,0.1,0))
plt.legend()
plt.show()
```

<img src="https://user-images.githubusercontent.com/97590480/150621582-190ac0b7-ef7e-4d08-bb31-435e7bcd3536.png">

- label은 각 데이터에 대한 제목을 설정해준다.
- `plt.axis('equal')`은 파이 차트가 찌그러지게 나올 수 있는데, 이를 방지하기 위해 원형으로 만들어주는 명령어이다. 필요하면 찾아서 넣자.
- color는 색깔을 넣는 명령어이다.
- `plt.pie(size)`를 실행하면 size데이터 안에 있는 데이터의 크기만큼 차지하는 비율을 파이 차트로 표시해준다. 예를들어, A의 데이터가 차지하는 비율을 구하면 2441/(2441+2312+1031+1233) * 100 = 34.8% 가 나오게 된다.
- `plt.pie` 안에 조건들을 설정할 수 있는데, labels 는 파이차트에 설정해둔 제목을 넣어주는 명령어이다. autopct는 파이차트 안에 숫자를 표시해주는 기능이다. %.1f%%는 소수점 1자리까지 표시하는 float 데이터라는 의미이다. 뒤에 %%를 두번 씀으로써 '%'가 나오도록 설정했다. colors는 색까르, explode는 특정 데이터를 강조하기 위해 쪼개서 나오게 만들어주는 명령어이다.
- `plt.ledend()`를 입력하면 옆에 범례가 표시된다.
___
### 3. scatter
scatter는 산포도라고 하며, 각 데이터가 어떤 범위안에 퍼져있고 그 크기가 얼마인지 표시해준다.
```python
plt.scatter([1,2,3,4],[10,30,20,40])
plt.show()
```

<img src="https://user-images.githubusercontent.com/97590480/150621857-37de3142-317b-49eb-b604-134484a1072e.png">

- 여기서 중요한 것은 scatter는 __위치값과 크기값__ 을 가진다는 것이다. 여기서 `[1,2,3,4]`는 x축값, `[10,30,20,40]`은 y축값을 표시하는 위치값이다. 즉, 위에서 크기값이 설정되어있지 않기 때문에 동일한 크기의 원이 표시된다.
- 그렇다면 크기값이 포함되어있는 scatter 그래프를 보자.

```python
plt.scatter([1,2,3,4],[10,30,20,40],s = [100,200,300,400])
plt.show()
```

<img src="https://user-images.githubusercontent.com/97590480/150621951-e5f915f9-74ab-40b3-98ef-4428877897e2.png">

- s = [100,200,300,400] 이라는 scale(크기)값을 설정해주니 원의 크기가 달라진 것을 볼 수 있다. scatter 그래프는 이런 식으로 위치값과 크기값을 가진다는 것을 이해하자.
  
<img src="https://user-images.githubusercontent.com/97590480/150622050-5eaacd0d-537f-4ac0-a9ad-bb70b8e6ebbd.png">

```python
plt.scatter([1,2,3,4],[10,30,20,40], s = [100,200,300,400], c = range(4), cmap = 'jet')
plt.colorbar()
plt.show()
```
- scatter 함수에 위와 같이 색깔과 colorbar를 설정할 수 있다.
- `c = range(4)`는 색깔 범위를 0 ~ 3까지 설정한다는 명령어이다. 옆에 컬러바를 보면 0에서 3까지 표시된 것을 볼 수 있다.
- `cmap = 'jet'`는 scale의 크기가 가장 낮은 것을 파란색, 높은 것을 빨간색으로 설정하는 명령어이다. 인구 밀도같은 그림을 표시할때 이런 식으로 표현하는 경우가 많기 때문에 시각적으로 사람들이 익숙하게 받아들일 수 있는 좋은 명령어이다.
- `plt.colorbar()`는 옆에 컬러바를 표시해주는 명령어이다. 왠만하면 같이 넣어주자.

___
## seaborn
seabon은 기존의 matplotlib의 심화편이라고 생각하면 좋다. 고급 통계에 관한 다양한 시각화 기능을 제공하기 때문에 간단한 것은 matplotlib으로, 좀더 상세한 데이터 시각화를 하려면 seaborn을 사용하자.

### 1. regplot
<img src="https://user-images.githubusercontent.com/97590480/150622211-848ea95f-d303-49f6-9ad4-c47b8b4fa3ab.png">

```python
import matplotlib.pyplot as plt
import seaborn as sns

titanic = sns.load_dataset('titanic')

sns.set_style('darkgrid')
fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

sns.regplot(x = 'age', y = 'fare', data = titanic, ax = ax1)
sns.regplot(x = 'age', y = 'fare', data = titanic, ax = ax2, fit_reg=False)
plt.show()
```
- matplotlib에서 실행했던 scatter 함수가 여기서는 regplot으로 표시가 된다. 사실 sns.scatter 명령어가 있지만, regplot 명령어는 scatter와 line을 포함하는 상위 명령어이기 때문에 regplot으로 산점도를 표시할 수 있다.
- `sns.set_style`은 뒷 배경을 설정하는 명령어이다.
- `fig = plt.figure(figsize = (15,5))`는 차트를 생성하는 명령어인데, figsize를 통해 밑변과 높이를 설정할 수 있다.
- `ax1 = fig.add_subplot(1,2,1)`은 plt.figure로 생성한 차트 안에 데이터가 들어갈 공간을 마련한다고 생각하면 된다. (1,2,1)은 1행 2열의 공간을 생성하는데 그 중 첫번째 공간이라는 뜻이다. (1,2,2)는 두번째 공간이라고 생각하면 된다.
> 우리가 plot함수를 그냥 두번 작성할 경우 동일한 직교좌표계에 두개의 plot이 동시에 표시되는 것을 볼수 있었다. 위의 figure와 fig.add_subplot은 데이터 분석을 하나의 직교좌표계에 표시하는 것이 아닌 따로따로 표시해주고 싶을때 사용하는 명령어라고 생각하면 된다. 즉, 큰 박스안에 조그마한 박스를 차곡차곡 넣는다고 생각하면 된다.
- `sns.regplot(x = 'age', y = 'fare)`은 x 축에 age 데이터, y축에 fare 데이터가 표시된다. 만약, 나이가 20살이고 임금이 1000불이면 해당 데이터에 점으로 표시가 된다.
- data = titanic은 데이터로 titanic을 사용하는데, seaborn에서는 titanic이라는 예시 데이터셋을 제공한다.
-  ax = ax1은 데이터 그래프를 어떤 작은 상자에 담을지 설정해주는 명령어이다.
-  fig_reg = False는 회귀선을 표시하지 않는 것을 말한다. 혹은 kind = 'scatter'를 입력해주면 동일한 그래프가 표시된다.
___
### 2. barplot

<img src="https://user-images.githubusercontent.com/97590480/150622740-9cef8a45-fe29-4fb9-ba39-47ecc13da7f2.png">

```python
import matplotlib.pyplot as plt
import seaborn as sns

titanic = sns.load_dataset('titanic')

fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(1,3,1)
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)

sns.barplot(x = 'sex', y = 'survived', data = titanic, ax = ax1)
sns.barplot(x = 'sex', y = 'survived', hue = 'class', data = titanic, ax = ax2)
sns.barplot(x = 'sex', y = 'survived', hue = 'class', dodge = False, data = titanic, ax = ax3)

ax1.set_title('titanic survived - sex')
ax1.set_title('titanic survived - sex/class')
ax1.set_title('titanic survived - sex/class(stacked)')
```

- 여기서는 막대 그래프에 좀더 다양한 기능들을 볼수 있다.
- `sns.barplot(x = 'sex', y = 'survived')`는 x축이 성별, y축이 생존여부에 관한 데이터를 표시해준다.
- `hue = 'class'`는 hue가 색조라는 뜻인데 색깔로 class라는 데이터로 sex와 survived로 표시된 데이터를 구분해준다. 즉 hue를 추가하면 2차원 데이터가 3차원 데이터로 변하고 그에 맞는 막대 그래프를 표시해준다.
- `dodge = False`는 누적 막대그래프를 표시할때 사용하는 명령어이다.
___

### 3. boxplot & violinplot
seaborn에서는 matplotlib과 동일한 boxplot을 제공한다. 거기에 violinplot이라는 boxplot보다 시각적으로 눈에 잘 들어오는 그래프를 제공한다.

<img src="https://user-images.githubusercontent.com/97590480/150622885-81b4451e-8fe7-4161-a03a-6cecb20891ca.png">

```python
import matplotlib.pyplot as plt
import seaborn as sns

titanic = sns.load_dataset('titanic')

fig = plt.figure(figsize = (15,5))
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

sns.boxplot(x = 'alive', y = 'age', data = titanic, ax = ax1)
sns.boxplot(x = 'alive', y = 'age', hue = 'sex', data = titanic, ax = ax2)
sns.violinplot(x = 'alive', y = 'age', data = titanic, ax = ax3)
sns.violinplot(x = 'alive', y = 'age',hue = 'sex', data = titanic, ax = ax4)
plt.show()
```
- boxplot은 동일하지만, violinplot에서는 boxplot에 빈도값을 동시에 표시해준다. violinplot을 통해 중앙값에 얼마나 많은 데이터가 몰려있는지, 분산에 대한 대략적인 시각화도 볼 수 있기 때문에 boxplot보다는 유용하다.

> 여기까지 통계 분석을 위한 데이터 시각화의 기초에 대해 마치도록 하겠다. 맵에 대한 시각화인 folium도 다루고 싶지만 연관성이 좀 떨어지기 때문에 나중에 다루도록 하겠다.