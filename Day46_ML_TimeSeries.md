# TIL(Today I Learned)

___

> Fab/26th/2022_Multi campus_유선종 Day46

## 시계열
- 우리는 머신러닝 중에서 지도 학습에 대해 알아보았고, 지도 학습에서 분류와 회귀 중에 회귀에 대해 알아보았다. 회귀에서는 규제가 없는 회귀와 규제가 있는 회귀에 대해 알아보았다.
- 이번에는 시간이 포함이 되는지의 유무에 따라 시계열과 횡단면 분석으로 나눌 수 있다.
- 시계열은 시간의 흐름에 따른 독립변수와 종속변수와의 관계를 파악하는 분석이다.
- 경제학에서 시계열은 매우매우 중요하지만 머신러닝에서는 다소 중요도가 떨어지는 부분이 있다. 그래서 간단하게 짚고 넘어가도록 하겠다.

### 1. 시계열 설치
시계열 분석을 제공하는 라이브러리는 페이스북에서 개발한 fbpropht 라이브러리를 사용한다. 그러나 맥에서는 호환이 잘 되지 않아서 가상환경을 만들어서 설치를 해줘야 한다.

- 여기서 가상환경이란 쉽게 생각해서 하나의 컴퓨터에 두 개의 디스크를 분할하는 것이랑 비슷하다고 생각하면 된다. 혹은 아이디를 하나 더 만든다고 생각하면 쉽다.
- 아나콘다를 통해서 가상환경을 만들 수 있는데, 이때 가상환경은 아주 기본적인 것들을 빼면 설치된 라이브러리가 없으므로 같이 설치해줘야 한다.
- 터미널에서 다음 명령어를 입력하면 fpprophet이 설치된 가상환경을 만들어준다. 그 전에, pystan이 깔려있다는 조건이 필요하다. 그러므로 다음 명령어를 차례로 실행해주자.    
```python
pip install pystan
conda create --name [가상환경이름] fbprophet -c conda-forge -c defaults --override-channels
```
> [가상환경이름]에는 내가 설정할 가상환경 이름을 입력해주면 된다.

가상환경이 설치됐다면 분석을 위해 주피터 노트북에 추가할 필요가 있다. 다음의 명령어를 입력해주자.

```
conda activate [가상환경이름]
pip install jupyter notebook
pip install ipykernel
python -m ipykernel install --user --name [가상환경이름] --display-name "[표시할 가상환경이름]"
```
> 내가 만든 가상환경을 activate를 이용하여 들어가서 가상환경에 주피터노트북과 ipykernel을 깔아준다. ipykernel은 주피터 노트북을 설치하면 같이 설치되지만 혹시 모르니 설치해준다. 그리고 다음 명령어를 입력해주면 가상환경이 잘 추가되는 것을 볼 수 있다.

여기서 위에서 입력한 코드처럼 입력하지 않는다면 오류가 날 가능성이 높다. 왜냐하면 내가 4시간 헤매봤으니 잘 안다. 괜히 base환경에 fbprophet을 설치하려는 뻘짓하지 말고 가상환경을 새로 만들어주는 것이 가장 현명하고 빠른 방법이다.
___

### 2. 시계열 분석 실습
이제 실습을 해보자.

#### 1. 데이터 전처리
```python
import numpy as np
import pandas as pd
from fbprophet import Prophet

df = pd.read_csv('./avocado.csv')
print(df.head())
```
<img src="https://user-images.githubusercontent.com/97590480/155841457-94d62688-4b69-416a-b50b-10d75c39a40e.png">

- 아보카도 데이터를 불러서 출력하면 위의 이미지처럼 나오는데 저기서 중요한 것은 날짜 데이터가 포함된다는 것이다.
- 날짜에 따른 종속변수는 가격, 나머지는 독립변수로 설정된다.
___

```python
df.groupby('type').mean()
```

<img src="https://user-images.githubusercontent.com/97590480/155841715-2c80146d-858e-4388-bdd7-fd4b0aad1e50.png">

- 여기를 보면 일반(conventional) 아보카도와 유기농(organic) 아보카도가 있다.
- 우리는 일반 아보카도에 대한 평균 가격의 예측을 할거기 때문에 일반 아보카도만 뽑아오는 데이터 전처리를 해줘야 한다.
___

```python
df = df.loc[(df.type == 'conventional') & (df.region == 'TotalUS')]                                         #line 1
df['Date'] = pd.to_datetime(df['Date'])                                                                     #line 2
data = df[['Date', 'AveragePrice']].reset_index(drop=True)                                                  #line 3
data = data.rename(columns = {'Date' : 'ds', 'AveragePrice' : 'y'})                                         #line 4
print(data.head())
```

1. [line 1]에서 타입이 conventional이고 지역이 TotalUS인 데이터만 df에 넣어준다.
2. [line 2]에서 Date열의 날짜 데이터를 2022-02-26의 형태로 변환해준다.
3. [line 3]에서 날짜와 평균가격 열만 data에 담아준다. reset_index를 이용해서 기존의 행 인덱스를 제거해준다.
4. [line 4]에서 열 이름을 ds, y로 설정해준다.

<img src="https://user-images.githubusercontent.com/97590480/155841866-b9ce9b57-fded-4add-9e56-d00a8ffe3501.png">
___

```python
data.plot(x = 'ds', y = 'y', figsize = (16, 8))
```

<img src="https://user-images.githubusercontent.com/97590480/155841947-3561118f-52f3-4022-9131-9797d29174da.png">

plot 함수를 이용해서 데이터를 시각화해보면 위의 이미지처럼 나온다.
___

#### 2. 모델 학습
```python
TimeSeries = Prophet()
TimeSeries.fit(data)
future = TimeSeries.make_future_dataframe(periods = 365)
forecast = TimeSeries.predict(future)
print(forecast.tail())
```
1. 여기서는 이전에 했던 학습과정과 비슷하다.
2. 하지만 `make_future_dataframe(periods = 365)` 매서드를 이용해서 실제 데이터값은 없지만 예측을 해서 1년 동안의 예측을 future에 담아준다.
3. 그래서 실제로 1년동안의 데이터값이 생성이 됐고, 밑의 이미지를 보면 원래 데이터는 2018년까지인데 2019년의 데이터가 생긴 것을 볼 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/155842186-cca704fb-e92f-42a5-94ae-4a6fa4550923.png">

___

```python
fig1 = TimeSeries.plot(forecast)
fig2 = TimeSeries.plot_components(forecast)
```

<img src="https://user-images.githubusercontent.com/97590480/155842224-3c5f3cc3-f92c-44fe-8740-55adeed0134e.png">

<img src="https://user-images.githubusercontent.com/97590480/155842229-d545d7da-1ce6-4d7e-bb00-27565969b7af.png">

1. 위의 코드를 입력해보면 위의 이미지처럼 나온다.
2. 첫번째 이미지에서 검은색 점은 실제 아보카도의 데이터이고, 점이 표시가 되어있지 않은 파란색 그래프는 우리가 위에서 예측을 통해 생성한 2019년의 데이터이다.
3. 그래프를 보면 정상성을 만족하고 어느정도 순환하는 구조를 보이고 있다.
4. 밑의 이미지 중에서 위의 그래프는 추세선을 의미하고 2016년까지는 가격이 하락하는 추세를 보이다가 2017년까지는 상승하는 추세를 보인다. 그 이후로 다시 하락하는 추세선을 보인다.
> 오른쪽 파란색 영역은 어떤 신뢰구간 하에서 추세선이 위치할 가능성이 높은 영역을 표시한 것이다. 
5. 밑의 이미지 중에서 아래의 그래프는 1년 동안의 계절요인을 파악하는 그래프이다. 1년 중에서 가장 가격이 높은 때는 11월 쯤이고, 가장 가격이 낮을 때에는 2월 쯤이다.