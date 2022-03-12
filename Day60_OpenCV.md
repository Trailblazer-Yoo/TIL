# TIL(Today I Learned)

___

> Mar/12th/2022_Multi campus_유선종 Day60

## OpenCV
OpenCV는 이미지를 변형하고 확인하는 데 사용되는 라이브러리다. 주로 컴퓨터 비전이나 딥러닝에서 사용되는데, 대부분의 언어와 모든 os 체제에서 제공되기 때문에 이미지나 영상을 다룬다면 필수적으로 알고 넘어가야 하는 라이브러리다. 오늘은 이 OpenCV의 기초에 대해 살펴보겠다.

### 1. 이미지에 대한 이해
1. 이미지는 픽셀 단위의 크기와 RGB값의 색상으로 이루어져 있다.
2. 예를 들어, 우리가 보는 유튜브 영상의 1080p은 가로 1080, 세로 780의 픽셀로 이루어진 영상 크기를 의미한다. 영상은 60fps라면 1초에 60장의 이미지가 출력되는 것을 의미한다.
3. 여기에 유튜브는 컬러이다. 컬러는 기본 흑백 화면에서 RED, GREEN, BLUE 값을 조합하여 색깔을 만들어내는 것을 의미한다.
4. 이러한 이미지는 컴퓨터에서는 숫자값으로 변환하여 이미지를 출력하며, 이미지는 (가로, 세로, RGB)의 3차원으로 이루어진 행렬값이다.
5. 우리는 3차원의 행렬로 이루어진 숫자값을 이용하여 CNN을 통해 딥러닝을 수행하는데 사용한다.

<img src="https://user-images.githubusercontent.com/97590480/158020318-fc0a168a-b419-4278-9406-c781b14e0d68.png">

> 포토샵을 들어가보면 색깔을 선택할 때 RGB 값이 0 ~ 255 사이의 값으로 되어있는 것을 볼 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/158020443-230e1f0d-1e37-460b-ad31-fe92422e5beb.png">

> 위에서 행렬 요소 하나가 픽셀 한 단위를 의미한다.

<img src="https://user-images.githubusercontent.com/97590480/158020437-c568e026-600b-4e88-a23c-283ec3cc9c3c.png">

> 흑백은 0 ~ 255 값을 가지며, 255은 흰색, 0는 검은색을 의미한다.

### 2. OpenCV 코딩
기본적으로 이미지는 4차원 데이터라는 것을 인식한 상태에서 코딩을 진행하자.

#### 1. 영상 파일 불러오기 및 출력
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('cat.bmp')                                                             #line 1

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))                                        #line 2
plt.show()
```
1. [line 1]에서 `cv2.imread()` 명령어는 cv2를 불러와 `imread()` 매서드를 실행하는데, 괄호 안에는 내가 열고 싶은 이미지 경로를 입력한다.
    - `imread()` 매서드에는 속성을 지정할 수 있는데, 주로 사용하는 속성은 `cv2.IMREAD_COLOR`, `cv2.IMREAD_GRAYSCALE`, `cv2.IMREAD_UNCHANGED`이다.
    - `cv2.imread('cat.bmp', cv2.IMREAD_COLOR)`는 BGR기반의 컬러 이미지를 불러온다. 기본값이다.
    - `cv2.imread('cat.bmp', cv2.IMREAD_GRAYSCALE)`는 이미지를 흑백 이미지로 불러온다.
    - `cv2.imread('cat.bmp', cv2.IMREAD_UNCHANGED)`는 이미지를 변환하지 않고 그대로 불러온다. 만약에 CMYK 기반의 이미지나 png 파일이라면 이 속성을 입력해준다.
2. [line 2]에서 `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` 중에서 `cvtColor` 는 이미지를 속성에 따라 변환해주는 매서드이다. 
    - `cv2.COLOR_BGR2RGB`는 BGR 기반의 이미지를 RGB로 바꿔준다. cv2에서는 이미지를 불러올때 BGR로 불러오므로 컬러 이미지를 RGB기반으로 바꿔줘야 한다.
    - `plt.imshow()`는 matplotlib에서 제공하는 이미지를 시각화하는 명령어이다.

___
```python
if img is None:                                                                         #line 5
    print('Image load Failed!')
    sys.exit()

cv2.imwrite('cat_gray.png', img)                                                        #line 4
```
1. [line 5]에서 만약 파일이 존재하지 않는다면 'Image load Failed!'를 출력하고 명령을 빠져나오는 명령어를 넣어준다.
2. [line 6]에서 `cv2.imwrite('cat_gray.png', img)`는 img라는 이미지 객체를 'cat_gray.png`이름으로 된 파일로 저장해주는 명령어이다.

___

```python
if img is None:
    print('Image load Failed!')
    sys.exit()
    
cv2.namedWindow('image')                                                                #line 5
cv2.imshow('image', img)                                                                #line 6
cv2.waitKey()                                                                           #line 7

cv2.destroyAllWindows()                                                                 #line 8
```
1. [line 5]에서 'image'라는 창을 새로 띄운다.
2. [line 6]에서 'image'창에 이미지를 띄운다.
3. [line 7]에서 키보드의 키를 누를때까지 기다리는 명령어를 입력한다.
4. [line 8]에서 기다리고 있던 키를 입력하면 'image'창을 닫는 명령어를 입력한다. 괄호 안에 아무런 명령어가 없다면 모든 창을 닫고, 괄호 안에 해당 창 이름을 입력하면 그 창만 닫는다.

```python
cv2.imshow('image', img)
cv2.waitKey()

while True:
    if cv2.waitKey() == ord('q'):
        break

cv2.destroyAllWindows()
```
위의 코드처럼 `ord('q')`를 이용하면 q를 입력할경우 break로 빠져나와서 창을 닫게 된다.

___

### 2. matplotlib을 이용한 출력
```python
imgBGR = cv2.imread('cat.bmp')
imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

plt.axis('off')
plt.imshow(imgRGB)
plt.show()

imgGray = cv2.imread('cat.bmp', cv2.IMREAD_GRAYSCALE)

plt.axis('off')
plt.imshow(imgGray, cmap='gray')
plt.show()

plt.subplot(121), plt.axis('off'), plt.imshow(imgRGB)
plt.subplot(122), plt.axis('off'), plt.imshow(imgGray, cmap='gray')
plt.show()
```
`plt.imshow(imgGray, cmap='gray')`에서 `cmap='gray'`속성을 지정해주면 흑백 사진으로 출력해준다. 또한, subplot으로 묶어서 출력이 가능하다.

```python
import sys
import glob
import cv2

img_files = glob.glob('.\imgages\ *.jpg')                                                   #line 9

if not img_files:
    print("There are no jpg files in 'images' folder")
    sys.exit()
    
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('image', cv2.WND_PROD_FULLSCREEN, cv2.WINDOW_FULLSCREEN)              #line 10

cnt = len(img_files)
idx = 0

while True:
    img = cv2.imread(img_files[idx])
    
    if img is None:
        print('Image load failed!')
        break
        
    cv2.imshow('image', img)
    if cv2.waitKey(1000) >= 0:
        break
        
    idx += 1
    if idx >= cnt:
        idx = 0
        
cv2.destroyAllWindows()
```
1. [line 9]에서 `glob.glob('.\imgages\ *.jpg')` 명령어는 괄호 안의 path의 파일을 여는데, *는 모든 파일을 의미한다. 이 명령어로 for문을 사용할 필요가 없어진다.
2. [line 10]에서 창의 크기를 전체 화면으로 출력해주는 속성을 지정해주는 명령어이다.
3. 밑의 반복문은 여러 이미지를 출력하는 명령어이다. 이런 식으로 여러 이미지를 출력할 수 있다.

### 3. 기본 속성 활용
```python
import numpy as np
import cv2

img1 = np.empty((240, 320), dtype=np.uint8)                                                 #line 10
img2 = np.zeros((240, 320, 3), dtype=np.uint8)                                              #line 11
img3 = np.ones((240, 320), dtype=np.uint8) * 255                                            #line 12
img4 = np.full((240, 320, 3), (0, 255, 255), dtype=np.uint8)                                #line 13
```
1. [line 10]에서 `np.empty`는 영행렬을 생성하는 zeros와 동일한 0으로 구성된 배열을 생성해준다. 여기서 (240, 320)은 240행 320열의 영행렬을 생성한다. `np.unit8`은 데이터를 2의 8승인 256의 숫자값으로 표현하며, 0 ~ 255 의 값을 입력할 수 있다.
2. [line 11]에서 동일하게 0행렬을 생성하는데, 3은 RGB값이 들어간 값이므로 3차원의 영행렬을 생성해준다. 그러나 값이 0이므로 검정색 화면을 출력한다.
3. [line 12]에서 `np.ones`는 모든 값이 1인 행렬을 반환해주는데, 255를 곱했으므로 흰색 화면이 출력된다.
4. [line 13]에서 `np.full`은 (240, 320, 3)의 행렬의 요소들 모두에 (0, 255, 255)값을 넣어준다. 즉, RGB값을 입력해주는 명령어이고 여기서는 노란색이 출력된다.\

___

```python
img1 = cv2.imread('HappyFish.jpg')

img2 = img1[40:120, 30:150]

cv2.imshow('img1', img1)
cv2.waitKey()
cv2.destroyAllWindows()
```
위의 명령어는 이미지를 인덱싱하여 인덱싱하지 않은 부분인 (10, 30)을 제거해서 출력해준다. 이처럼 이미지를 자르고 수정할 수 있다.

<img src="https://user-images.githubusercontent.com/97590480/158022556-aaf668c8-1958-4bb4-9bb8-88bc871f3920.png">