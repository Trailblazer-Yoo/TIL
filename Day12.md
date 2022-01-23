# TIL(Today I Learned)

___

> Jan/23th/2022_Multi campus_유선종 Day12
## 과제 성적관리 프로그램
오늘은 과제에 대한 해설을 하고자 한다.

<img src="https://user-images.githubusercontent.com/97590480/150683184-81fd2d9a-ec14-4593-9d66-3aab81e3cb6b.png">

```python
data_k={'홍길동':90,'김기영':77,'곽진수':88}
data_e={'홍길동':88,'김기영':66,'곽진수':99}
data_m={'홍길동':55,'김기영':100,'곽진수':98}
data_H={'국어':90,'영어':88,'수학':55}
data_K={'국어':77,'영어':66,'수학':100}
data_G={'국어':88,'영어':99,'수학':98}
data_all={'Hk':90,'Kk':77,'Gk':88,'He':88,'Ke':66,'Ge':99,'Hm':55,'Km':100,'Gm':98}
class Grade:
    def Total(self,data):
        L = []
        L = list(data.keys())
        a = 0
        for i in range(len(data)):
            k = data.get(L[i])
            a += k
        return a
    def Average(self,data):
        L = []
        L=list(data.keys())
        a = 0
        for i in range(len(data)):
            k = data.get(L[i])
            a += k
        return int(a/len(data))
        
a = Grade()
            
a1 = a.Total(data_H)
a2 = a.Average(data_H)
a3 = a.Total(data_K)
a4 = a.Average(data_K)
a5 = a.Total(data_G)
a6 = a.Average(data_G)
a7 = a.Total(data_k)
a8 = a.Total(data_e)
a9 = a.Total(data_m)
a10 = a.Total(data_all)
a11 = a.Average(data_all)
a12 = a.Average(data_k)
a13 = a.Average(data_e)
a14 = a.Average(data_m)

f = open('성적.txt','w')
f.write(f"""
이름   국어  영어  수학    총점  평균
===============================
홍길동  90   88   55  : {a1}   {a2}
김기영  77   66   100 : {a3}   {a4}
곽진수  88   99   98  : {a5}   {a6}
===============================
총점   {a7}  {a8}  {a9}   {a10}   {a11}
평균   {a12}   {a13}   {a14}     {a11}   {a11}""")
f.close()
```
___
### 1. 딕셔너리형 자료
```python
data_k={'홍길동':90,'김기영':77,'곽진수':88}
data_e={'홍길동':88,'김기영':66,'곽진수':99}
data_m={'홍길동':55,'김기영':100,'곽진수':98}
data_H={'국어':90,'영어':88,'수학':55}
data_K={'국어':77,'영어':66,'수학':100}
data_G={'국어':88,'영어':99,'수학':98}
data_all={'Hk':90,'Kk':77,'Gk':88,'He':88,'Ke':66,'Ge':99,'Hm':55,'Km':100,'Gm':98}
```
- 우선 데이터를 딕셔너리 형태로 저장하라는 조건이 있기 때문에 딕셔너리형으로 저장했다.
- 클래스에서 get 명령어를 사용할거기 때문에 자료의 행과 열의 데이터 및 모든 데이터에 대한 자료를 저장했다.

```python
class Grade:
    def Total(self,data):
        L = []
        L = list(data.keys())
        a = 0
        for i in range(len(data)):
            k = data.get(L[i])
            a += k
        return a
    def Average(self,data):
        L = []
        L=list(data.keys())
        a = 0
        for i in range(len(data)):
            k = data.get(L[i])
            a += k
        return int(a/len(data))
```
- Grade라는 클래스를 만들었는데, 총점을 계산하는 함수와 평균을 구하는 함수로 설정했다.
- `L = list(data.keys())`를 사용하면 key값들을 리스트 형태로 저장해준다.
- `k = data.get(L[i])`를 이용해서 value값을 뽑아낸다. 예를 들어, 홍길동의 '국어'에 대한 키값이 L의 0번째에 들어있다. 그러면 `k = data.get('국어')`이므로 홍길동의 국어 점수인 90이 k에 들어가게 된다.
- 이걸 반복해서 모두 더하면 총점, 총점을 len을 이용해 데이터 갯수로 나눠주면 평균이 된다.
  
```python
f = open('성적.txt','w')
f.write(f"""
이름   국어  영어  수학    총점  평균
===============================
홍길동  90   88   55  : {a1}   {a2}
김기영  77   66   100 : {a3}   {a4}
곽진수  88   99   98  : {a5}   {a6}
===============================
총점   {a7}  {a8}  {a9}   {a10}   {a11}
평균   {a12}   {a13}   {a14}     {a11}   {a11}""")
f.close()
```
- 조건에서 성적.txt에 입력하라는 조건이 있으므로 f = open 명령어를 이용해서 성적.txt를 연다.
- f.write를 print와 동일하다고 생각하고 입력해주면 된다.
- f.close()는 꼭 잊지말고 넣어주자.