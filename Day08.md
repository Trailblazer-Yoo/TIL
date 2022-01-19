# TIL(Today I Learned)

___

> Jan/18th/2022_Multi campus_유선종 Day7

### 파일에 관한 유의점
~~원래는 판다스에 대한 설명을 더 할 생각이였지만,~~ 오늘 데이터 시각화를 하면서 파일 불러오기에 관한 흥미로운 사실을 발견해서 기록해보고자 한다.   다음의 코드를 보자.
```python
import csv # csv 모듈 불러오기
f = open('seoul.csv') # seoul csv파일을 열기
data = csv.reader(f) # csv파일을 읽어와서 데이터에 넣기
next(data) # 첫번째 행에 날짜 등 불필요한 데이터 제거하고 포인터를 아래로 내리기
month = [[],[],[],[],[],[],[],[],[],[],[],[]] # 1월 ~ 12월 데이터를 넣을 데이터 상자
for row in data: 
    if row[-1] != '': # 만약 데이터가 비어있지 않다면
        month[int(row[0].split('-')[1])-1].append(float(row[-1])) # row[0]에 날짜 데이터가 있는데, '2019-08-12'형태이므로 split을 이용해서 '-'를 제거하고 월의 데이터를 받기 위해서는 3개 중 가운데 데이터를 선택해야 하므로 인덱싱[1]을 넣는다. 그리고 month상자에 [0]부터 넣기 때문에 -1을 해준다.
```
- 여기서 보면 for문 하나만 사용해서 데이터를 넣은 것을 볼 수 있다.
- 그런데 나는 month에 12개의 리스트 박스를 넣는 것이 귀찮아 이중for문을 사용했다.
- 하지만, 이중for문을 사용했더니 오류가 나타났다. 다음은 오류가 나온 코드이다.
```python
import csv
f = open('seoul.csv')
data = csv.reader(f)
month = []
for i in range(1,13):
    box = []
    for row in data:
        if nt(row[0].split('.')[1]) == i:
            box.append(float(row[-1]))
    month.append(box)
```
- 여기서 `for i in range(1,13)`은 월의 갯수를 나타낸다. 즉, i는 월을 나타내고 각 월 데이터들이 box안에 들어가서 month 리스트 박스에 추가되어서 최종적으로 month에 1~12월 데이터가 들어오게 만들었다.
- 그런데 1월 데이터만 box에 들어오고 나머지 2월부터는 데이터가 담기지 않았다.
- 여기서 나는 __파일의 포인터__ 라는 개념을 알게 됐다.
  - 원래 코드에서 2월부터 데이터가 담기지 않은 이유는 for row in data에서 데이터 파일의 포인터를 다 사용하기 때문에 더이상 진행이 안된다는 것이다.
  - 포인터란 우리가 텍스트를 작성할 때 작성하고 있는 줄을 가리키는 것을 말한다.
  - for 문으로 데이터 파일의 데이터를 읽으면 포인터가 맨 위에서 하나하나 내려가면서 결국 맨 밑줄에 다다른다.
  - 파일에서는 포인터가 있는 자리의 데이터만 읽을 수 있으므로 포인터가 마지막에 있다면 더이상 읽을 데이터가 없다.
- 결국 포인터를 처음으로 되돌릴 필요가 있었다. 올바르게 수정된 코드를 보자.

```python
mport csv
month = []
for i in range(1,13):
    f = open('seoul.csv')
    data = csv.reader(f)
    box = []
    for row in data:
        if row[-1] != '':
            if int(row[0].split('.')[1]) == i:
                box.append(float(row[-1]))
    month.append(box)
    f.seek(0)
```
- `f.seek(k)`는 k 위치에 포인터를 위치시켜준다. 즉, k = 0일때 맨 위로 포인터를 위치시킨다.
- 이렇게 돌릴경우 포인터가 for문을 만나서 맨 아래로 내려가다가 f.seek(0)을 만나서 다시 맨 위로 돌아가게 된다.
- __주의하자. 파일에서 for문을 돌릴 때에는 포인터라는 개념을 유념해야 한다.__