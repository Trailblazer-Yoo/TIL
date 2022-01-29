# TIL(Today I Learned)

___

> Jan/29th/2022_Multi campus_유선종 Day18

## folium
이번에는 맵 위에 데이터를 시각화하는 folium 라이브러리에 대해 간단히 알아보고자 한다.
> 이전에 나는 import 하는 pandas나 folium 등에 대해 모듈이라고 말했는데, 일반적으로는 라이브러리라고 많이 말을 한다. 그러나 둘다 동일한 것을 지칭하는 말이므로 모듈이라고 해도 되고 라이브러리라고 말해도 된다. 회사의 지침을 따르자.
___
###  1. Jupiter Notebook
쥬피터 노트북은 folium을 위해 필요한 것은 아니다. 그러나 우리가 파이썬을 다양한 환경에서 사용할 수 있는데, 나는 주로 많이 사용하는 Visual Studio Code에서 파이썬을 사용했다. 하지만 이번에는 쥬피터 노트북을 사용할 것이다.
> 만약 VSC에서 folium을 실행하면 시각화된 내용이 뜨지 않고 html로 저장해서 봐야 한다. 반면에 쥬피터 노트북은 웹에서 파이썬을 실행해주기 때문에 시각화된 결과를 바로 보여준다. 번거로움을 줄이기 위해 쥬피터 노트북을 사용하자.

- 쥬피터 노트북은 아나콘다를 설치하면 기본적으로 제공해주는 환경이다. 아나콘다를 이미 설치한 사람이 있을 수도 있고 없을 수도 있지만, 데이터분석을 위해서 아나콘다는 무조건 설치해야 하기 때문에 설치해주자.

<img src="https://user-images.githubusercontent.com/97590480/151650578-8c5e22c1-996f-440c-8786-b35d48ebe9ac.png">

>쥬피터 노트북을 실행하면 다음과 같은 창이 나온다. 역시 home 화면부터 시작하는 것을 볼 수 있다. 우리가 실행하고자 하는 파일은 home 파일에 넣자.

### 2. folium 맵 종류
우선 folium을 이용해서 맵을 만들어보자.

<img src="https://user-images.githubusercontent.com/97590480/151650756-5b908aef-8822-41f3-98e8-44fd67ef2ed9.png">

```python
import folium
seoul_map = folium.Map(location = [37.55, 126.98], zoom_start = 12)
seoul_map
```

- `folium.Map(location = ['위도', '경도'])` 는 위도와 경도에 해당하는 위치의 지도를 만드는 명령어이다. 만든다고 해서 그 부분만 짤라서 만드는게 아니라 축소화 확대를 통해 다른 지역까지 볼 수 있다.
- `zoom_start` 는 얼마나 확대해서 출력해줄지 알려주는 명령어이다. 좀더 확대하고 싶다면 숫자를 높이면 된다.
- 쥬피터노트북은 print(seoul_map)을 할 필요 없이 출력할 변수만 입력해주면 출력해준다.
___
다른 종류의 지도를 사용할 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/151650991-4408bd85-61ff-4e65-9682-ff53225e1de9.png">

> tiles = 'Stamen Terrain' 명령어를 추가해서 위의 스타일의 지도를 불러올 수 있다. 산이나 강 같은 지형지물에 특화된 지도이다.

<img src="https://user-images.githubusercontent.com/97590480/151651002-3e92a2d6-00a8-4fdb-b8d3-f02848f6c3f6.png">

> tiles = 'Stamen Toner' 명령어를 추가해서 위의 스타일의 지도를 불러올 수 있다. 큰 도로를 강조하고 싶다면 이 지도를 사용하자.
___

### 3. 서울에 위치한 대학교 표시하기
이번에는 folium을 이용해서 서울에 위치한 대학교를 지도 위에 마커로 표시하고 대학 이름을 팝업창에 넣는 작업을 해보자.

<img src="https://user-images.githubusercontent.com/97590480/151651116-690d8959-f2f5-464b-8a61-413c1b5338bf.png">

각 대학들의 이름과 위도, 경도를 엑셀에 정리해서 넣은 후, pandas 명령어인 pd.read_excel을 이용해서 엑셀을 불러온다.

<img src="https://user-images.githubusercontent.com/97590480/151651331-56e41fa7-da30-451c-882b-fc72e7dd82ca.png">

```python
seoul_map = folium.Map(location = [37.55, 126.98], tiles = 'Stamen Terrain', zoom_start = 12)
for name, lat, lng in zip(df.학교, df.위도, df.경도):
    folium.Marker([lat, lng],popup = name).add_to(seoul_map)
seoul_map
```

1. `folium.Map` 명령어를 이용해서 서울의 지도를 불러온다.
2. `zip` 명령어는 괄호 안의 데이터를 짝지어서 하나로 만들어준다. 예를들어, 엑셀의 데이터를 파이썬에 불러오면 다음과 같다.
   - df.학교 = ['KAIST 서울캠퍼스', 'KC대학교', '가톨릭대학교(성신교정)', ...]
   - df.위도 = [37.592573, 37.592573, 37.585922, ...]
   - df.경도 = [127.046737, 126.854797, 127.004328, ...]
   - 즉 위의 데이터들을 zip을 사용해서 ('KAIST 서울캠퍼스', 37.592573, 127.046737)의 튜플 데이터로 바꿔준다.
   - 튜플 데이터를 name, lat lng의 변수 안에 각각 담아서 for문을 이용해 하나하나 folium.Marker안에 넣어준다.
3. `folium.Marker` 명령어는 마커를 생성해주는 명령어이고, `['위도', '경도']`, `popup = '팝업창에 들어갈 내용'`을 요소로 받는다. 그리고 생성한 마커를 .add_to(seoul_map)을 이용해서 이미 불러온 지도 위에 마커를 위치시킨다.
- 이런 식으로 지도 위에 다양한 요소들을 생성할 수 있다. ~~수업에서는 매우 간단한 내용만 다뤘기 때문에 여기까지 다루도록 하겠다.~~
