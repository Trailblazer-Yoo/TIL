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
