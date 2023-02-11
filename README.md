# DataReconciliation

## Data Reconciliation의 이해
공장의 단위 공정에서 수많은 변수 데이터가 수집될 때, 다양한 측정 오차가 포함되어 있음.

공정 분석은 보통 물질 수지와 열 수지를 만족하는 것으로 시작되는데 측정 오차가 포함된 상태에서는 이들을 만족시키기 어려움.

이러한 문제를 해결하기 위한 방법으로 <big><strong><ins>데이터 보정(Data Reconciliation; DR)</ins></strong></big> 기법을 사용함.

DR이란 측정값의 통계적 확률 분포를 이용하여 물질 수지와 열 수지를 만족하도록 측정값의 오차를 소거하는 기술임.

DR은 측정값 내 노이즈의 종류에 따라 <strong> White Noise 보정, Gross Error 보정</strong>으로 나눌 수 있다.

### 1. <strong> White Noise 보정</strong>
<pre>
무작위 형태의 오차(White Noise, Random Error)가 있는 경우의 DR기법은 비선형 최적화 문제를 구성함.
목적함수는 다음의 식과 같이 최소제곱법(Least Square)에 의한 2차식으로 표현가능함.
White Noise 보정의 DR 기법은 최적화 문제의 해, 보정값을 구함.
</pre>

### 2. <strong> Gross Error 보정</strong>
<pre>
측정값에 편향 오차가 포함되어 있다면 White Noise 보정에 별도의 과정이 필요함. 
Gross Error(편향 오차)를 제거하지 않고 White Noise 보정을 실시한다면 갖고 있는 Gross Error(편향 오차)는 보정되겠지만 
다른 변수의 측정값에 오차를 떠넘기게 되어 정상적인 측정값을 갖는 변수의 입장에서는 데이터 보정을 실행하지 않는 것보다 못하게 됨.

즉,  1) Gross Error(편향 오차) 보정을 하기 위해서는 Gross Error(편향 오차)가 있는지 확인한 후, 
     2) Gross Error(편향 오차)를 갖는 변수를 찾아내어, 
     3) Gross Error(편향 오차)를 제거하여 데이터 보정을 실시해야 함.
    
이를 아래처럼 표현할 수 있다. 
     1) Global Test 실시 : Fault Detection 단계 진행
     2) Fault Identification 단계 진행
     3) Reconstruction 단계 진행
</pre>

### 3. Gross Error 보정
#### Global Test Eq.
![image](https://user-images.githubusercontent.com/80809187/218258962-6e7c8f31-316b-41ea-a34a-cead9dbb3832.png)
<pre>
측정값 과 보정값의 차이가 큰 변수에 편향 오차가 존재할 가능성이 크기에 Global Test의 r(감마 혹은 검정치)가 커질 것임.
r(감마 혹은 검정치)를 판단하는 기준치로는 카이-제곱(χ2) 통계량을 이용함.
아래의 식과 같이 r(감마 혹은 검정치)가 카이-제곱(χ2) 기준치보다 크면 Gross Error(편향 오차)가 존재한다고 판단 </pre>
</pre>

#### Global Test - Chi square
![image](https://user-images.githubusercontent.com/80809187/218258986-a923279c-c6dc-42c3-8fbe-5e286438174a.png)

<pre>
다음의 3가지 단계 중 1) 을 통해 Gross Error(편향 오차)의 존재를 판단함. 
     1) Global Test 실시 : Fault Detection 단계 진행
     2) Fault Identification 단계 진행
     3) Reconstruction 단계 진행

Gross Error가 탐지되면 어느 변수가 Gross Error를 갖고 있는지 확인하는 Identification(식별) 단계를 수행함.
Identification(식별) 단계에서는 여러가지 알고리즘이 있겠지만, 이 논문(출처 참고)에서는 순서에 따른 시행착오법을 이용함.
측정값과 보정값의 차이가 가장 큰 측정 변수부터 Global Test의 검정치 산출 공식에서 제외하여 검정치를 산출함.
즉, 검정치를 한번 더 계산한다. 한 개의 변수를 제외한 채로. 
만약 재계산된 검정치가 기준치보다 낮아졌다면 해당 변수에서 기준치를 초과하게 만드는 원인이 있다고 판단하는 것임.
이 과정을 측정값과 보정값의 차이의 순서대로 변수 전체에 반복함.
</pre>

<pre>단, 내가 이해한 바로는 이 방법은 Gross Error가 1개 있다고 가정한 것임. 2개이상 편향오차가 발생하지 않는다고 가정한 것임. 
공정 내에 다양한 측정 센서들이 동시에 고장나지 않는다라는 현장 엔지니어들의 소견도 그랬음.

다만 아쉬운 것은 이 논문(출처 참고)에는 1개 일 때와 2개 이상 일 때를 구분했으나 2개 이상일 때에 대해서 실습이라던가, 
별도의 공부를 아직 까지 진행하지 못함.

<u>데이터 보정을 통해서 공장 내 존재하는 노이즈를 보정할 수 있다면 데이터 분석 및 공정 모니터링에 많은 도움이 될 것으로 기대함.</u>
 <ul>
참고 문헌:
Martini, A, Coco, D, Sorce, A, Traverso, A, & Levorato, P. "Gross Error Detection Based on Serial Elimination: Applications to an Industrial Gas Turbine." Proceedings of the ASME Turbo Expo 2014: Turbine Technical Conference and Exposition. Volume 3A: Coal, Biomass and Alternative Fuels; Cycle Innovations; Electric Power; Industrial and Cogeneration. Düsseldorf, Germany. June 16–20, 2014. V03AT07A024. ASME. https://doi.org/10.1115/GT2014-26746

Data Processing and Reconciliation for Chemical Process Operations
1st Edition - October 11, 1999
Authors: José Romagnoli, Mabel Sanchez
eBook ISBN: 9780080530277

Miao, Yu & Su, Hongye & Rong, Gang & Chu, Jian. (2009). Industrial Processes: Data Reconciliation and Gross Error Detection. Measurement and Control. 42. 209-215. 10.1177/002029400904200704. 
</ul>
</pre>

## 실습 자료 다운
데이터 보정 실습 자료인 DR_Example_v1.xlsm 파일을 다운로드 이후 아래의 단계를 통해 사용할 수 있다.

> 다운로드 한 파일 우클릭 => 속성 선택 => 보안: 차단해제 클릭 후 확인

![image](https://user-images.githubusercontent.com/80809187/218258473-c40ea01d-8ca7-4169-8bcb-a51e19c502f3.png)


## Python Code
아래의 라이브러리가 반드시 필요합니다.
```
pip install gekko
```

예제
```
dr = DR()
# 참고자료 내 Jacobian 행렬
jacobian = [[1, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, -1]]
# 참고자료 내 계측값(현재값)
measured_x = [100, 150, 80, 250, 330.0, 250, 110, 100, 80, 60, 40, 40, 50, 60, 90, 150]
# 참고자료 내 표준편차
sigma = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]

answer_x = [100, 150, 80, 250, 330.0, 120, 110, 100, 80, 60, 40, 40, 50, 60, 90, 150]

x_recon = dr.reconciliate(jacobian, measured_x, sigma_from_data=sigma)
```
