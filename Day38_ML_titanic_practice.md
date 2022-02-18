# TIL(Today I Learned)

___

> Fab/18th/2022_Multi campus_유선종 Day38

## 머신러닝 타이타닉 실습
오늘 해볼 내용은 kaggle에서 제공하고 있는 타이타닉의 데이터를 가지고 생존자와 비생존자의 차이를 가져온 요소들이 무엇인지 분석하는 실습을 할 것이다. 특히, 데이터 전처리(preprocessing) 및 의사결정나무(DecisionTree)를 사용하여 지도 학습 중에서 분류를 이용하여 생존에 결정적인 요소를 분류할 것이다.

### 1. 데이터 탐색
데이터 탐색이란 데이터 EDA라고도 하며, 데이터의 분석에 앞서 전체적으로 데이터의 특징을 파악하고 다양한 각도로 접근하는 것을 말한다.
#### 1. 데이터 살펴보기
우선 데이터를 분석하기 전에 특성변수들이 어떤 식으로 구성이 되어 있는지 확인해야 한다. 우선 데이터를 불러오자. 데이터는 `https://www.kaggle.com/c/titanic/data` 링크를 타고 들어가 다운을 받아도 되고, kaggle API를 다운받고 `kaggle competitions download -c titanic`을 입력하면 쉽게 다운이 가능하다. 그러나 우리는 API에 대해 배우지 않았으므로 홈페이지에 다운받자.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

titanic_df = pd.read_csv(r'./titanic/titanic_train.csv')                                                #line 1
titanic_df.head(3)                                                                                      #line 2
```

<src="https://user-images.githubusercontent.com/97590480/154664639-fb789a07-24c2-45bd-b6ef-9b3a6204c075.png">

1. [line 1]에서 다운받은 데이터를 같은 폴더에 위치시키고 `pd.read_csv`를 이용해서 데이터를 읽어온다.
2. [line 2]에서 어떤 열로 구성되어 있고 어떤 데이터가 들어가 있는지 간단히 확인하기 위해 `.head(3)`매서드를 이용해서 3행까지의 데이터만 불러온다.
3. 위의 이미지를 보면, 1열에는 승객ID, 2열에는 생존여부, 3열에는 승실의 클래스, 4열에는 이름, 5열에는 성별, 6열에는 형제수, 7열에는 부모님의 수, 8열에는 티켓번호, 9열에는 티켓요금, 10열에는 사물함 번호, 11열에는 승선한 위치를 나타내는 데이터이다.
    - 이중에서 2열은 우리의 목표가 되는 label 데이터가 될 것이고, 나머지는 feature 데이터가 된다.

___

```python
print('DataFrame 크기 : ',titanic_df.shape)
```

<img src="https://user-images.githubusercontent.com/97590480/154665441-d9d5a07e-7e57-45ff-b56a-8a22cc661dbe.png">

- `.shape`매서드를 이용해서 해당 데이터의 행과 열의 수를 쉽게 볼 수 있다. 총 891개의 데이터를 가지고 있다.

___

```python
print(titanic_df.info())
```

<img src="https://user-images.githubusercontent.com/97590480/154665832-3bb4737c-3598-4ea6-b540-5f73c1e707f0.png">

- `.info()`매서드를 이용하면 데이터의 타입과 Null 값의 갯수, 데이터의 갯수를 볼 수 있다. 여기서 Age와 Cabin, Embarked의 데이터에는 누락된 데이터가 존재한다. 누락된 값이 많지 않다면 평균값으로 대체하는 등의 보정을 실시할수도 있고, 반면에 누락된 값이 유의미하게 많다면 NaN값으로 대체하여 누락된 채로 분석을 실시할 수도 있을 것이다.

___

#### 2. 기술통계 및 그래프 확인


```python
print(titanic_df.describe())
```

<img src="https://user-images.githubusercontent.com/97590480/154666331-f5e8bcc0-0b1b-430f-a054-e3f2eb066179.png">

- `.describe()`매서드를 이용해서 데이터의 기술 통계량을 구할 수 있다. 여기서 기술 통계가 유의미한 데이터는 Age와 Fare 정도로 보인다.

```python
print('Sex값 분포 : \n', titanic_df['Sex'].value_counts())
print('\n Cabin값 분포 : \n', titanic_df['Cabin'].value_counts())
print('\n Embarked값 분포 : \n', titanic_df['Embarked'].value_counts())
```

<img src="https://user-images.githubusercontent.com/97590480/154670119-38d22de7-9244-4b59-b4e9-2a36c1e0e0ca.png">

1. 여기서 `.value_counts()`매서드는 값들의 갯수를 받는 명령어이다. 
2. 위의 이미지를 보면 남성이 여성보다 약 30% 많은 것을 볼 수 있다. 또한, Cabin은 골고루 분포가 되어있는 것을 볼 수 있고, Embarked는 S가 대부분을 차지하는 것을 볼 수 있다.
> 추측하건데 S가 출발지였을 가능성이 높다.
___

```python
value_counts = titanic_df['Pclass'].value_counts()
print(value_counts)
```

<img src="https://user-images.githubusercontent.com/97590480/154670801-6a0b41f6-a819-44d5-9570-42228d250f67.png">

- Pclass에서 가장 많은 비중을 차지하는 class는 3클래스로 아마 가장 저렴한 클래스일 가능성이 놓다. 반면에, 가장 적은 비중을 차지하는 것은 2클래스로 보통 숫자가 낮을수록 비싼 class일 가능성이 높기 때문에 비쌀수록 비중이 적어지는 수요의 법칙과는 다른 비중을 보인다.
> 추측하건데 타이타닉이 그만큼 초호화 여객선이였을 가능성이 높다.

```python
print(titanic_df.groupby(['Pclass', 'Survived'])['Survived'].count())
```

<img src="https://user-images.githubusercontent.com/97590480/154680252-557e9842-c34e-4456-ac37-95a00e6c02a0.png">

- `.groupby(['Pclass', 'Survived'])['Survived'].count()` 매서드는 Pclass와 survived의 열로 묶어주는 매서드인데 여기에 ['survived']인덱싱을 하고 `count()` 매서드를 사용하여 1과 0의 값이 아닌 1과 0의 갯수의 데이터가 출력되도록 명령어를 입력한다.
- 이미지를 보면 class 3의 생존율이 119/491 * 100 = 약 24%인데 반해 class 1의 생존율은 136/216 * 100 = 62%로 클래스에 따른 생존율에 차이가 존재하는 것으로 보아 클래스와 생존 여부의 상관관계가 존재할 가능성이 높다.

```python
print(titanic_df.groupby(['Sex', 'Survived'])['Survived'].count())
```

<img src="https://user-images.githubusercontent.com/97590480/154681128-b17ae295-8285-4122-9038-130fd9135e91.png">

- 이미지를 보면 여성의 생존율이 남성보다 압도적으로 높은 것을 볼 수 있다. 추측하건데 여성 중에서 상대적으로 약자인 어린이나 노약자의 비율이 높을 가능성이 있다.

```python
print(titanic_df.groupby(['SibSp', 'Survived'])['Survived'].count())
```

<img src="https://user-images.githubusercontent.com/97590480/154681805-7c54ff7d-52be-42a3-9fd1-0ce8448045e1.png">

- 이미지를 보면 형제의 수와 생존율에 따른 선형관계는 없어보이지만 단정짓기는 힘들다.

```python
print(titanic_df.groupby(['Parch', 'Survived'])['Survived'].count())
```

<img src="https://user-images.githubusercontent.com/97590480/154682200-dff5df2c-8579-4764-80ad-d219b823e72f.png">

- 이미지를 보면 대부분 Parch가 0에 몰려 있지만 겉으로 보기에는 선형관계가 있다고 단정짓기 힘들다.
___
```python
def get_category(age):
    cat =  ''
    if age <= -1: cat = 'Unkown'
    elif age <= 5: cat = 'Baby'
    elif age <= 12: cat = 'Child'
    elif age <= 18: cat = 'Teenager'
    elif age <= 25: cat = 'Student'
    elif age <= 35: cat = 'Young Adult'
    elif age <= 60: cat = 'Adult'
    else: cat = 'Elderly'
        
    return cat

plt.figure(figsize = (10,6))

group_names = ['Unkonw', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Elderly']

titanic_df['Age_cat'] = titanic_df['Age'].apply(lambda x : get_category(x))
sns.barplot(x='Age_cat', y='Survived', hue = 'Sex', data = titanic_df, order=group_names)
titanic_df.drop('Age_cat', axis = 1, inplace = True)
```

<img src="https://user-images.githubusercontent.com/97590480/154682397-9953e105-8ead-4b84-9a2d-57fe072600f1.png">
 
1. 위의 코드는 데이터를 구간을 설정하여 나눠 분석한 데이터이다. seaborn은 우리가 이전에 데이터 시각화를 할 때 배웠으므로 코드 해석은 넘어가겠다. Day11을 참고하자.
2. 위의 바그래프를 보면 6세부터 12세 사이의 아이들의 생존률은 남성, 여성 구별없이 낮았고, 이를 제외하면 모든 연령대에서 여성의 생존률은 높았다.
> 추측하건데 생존한 사람들의 전제 조건은 시간, 구조용품, 침몰할 당시의 위치 등이 있을 것이다. 이때, 모든 구조용품은 아기들과 여성이 차지했을 가능성이 높고 나머지 인원들은 탈출을 했더라도 구명조끼나 구명보트 등의 구조용품에 제약이 생겨서 생존에 불리했을 가능성이 높다.

```python
sns.barplot(x='Pclass', y = 'Survived',hue = 'Sex', data = titanic_df)
```

<img src="https://user-images.githubusercontent.com/97590480/154683510-3435809f-4bf1-457d-a409-6e8b81942492.png">

1. 여기서는 클래스에 따른 차이가 나타나는 것을 알 수 있다. class 1에서의 생존률이 class 3보다 높은 것을 알 수 있는데, 이는 class 1의 위치가 가장 위쪽에 있을 가능성이 높고 반면에 class 3의 경우는 가장 아래쪽에 위치할 가능성이 높다.
2. 초기 위치값이 아래에 위치할수록 탈출할 시간과 공간 확보에 불리한 것은 배가 침몰한다는 특징이 있는 경우에 class 3의 생존률이 낮은 것은 어찌보면 당연하다고 할 수 있다.
___
- 우리는 데이터를 살펴보면서 데이터의 상관관계에 대해 분석해야 하나 여기 실습 자료에서는 연관분석에 대한 내용은 없었다. 실습에서 지정한 연관성이 높은 변수는 ID, Name, Ticket, Fare을 제외한 나머지 변수들로 지정했다.
- kaggle에서 다른 사람들의 코드를 참고해보면 변수 선택의 기준들이 각각 다르다. 우리는 어떤 변수를 선택해야 하는지조차도 사람의 주관이 들어가기 때문에 데이터 분석에 완벽한 답은 존재하지 않는다. 오히려 너무 완벽하다면 과적합(overfitting)문제가 발생할 가능성이 높다.
- 물론 정답에 가깝게 발전해왔기 때문에 머신러닝이 발전할 수 있었겠지만 데이터 전처리 단계는 만만하게 봐서는 안되는 단계이다. 데이터 탐색과 전처리 과정이 데이터 분석의 60~70%를 차지할 정도로 중요한 파트이다.