# KOfish(Korean fast and interactive Style Handler)
### 부자연스러운 한국어를 자연스러운 한국어로 변환하는 Cross Aligned Model

<br> 
GAN을 모태로하는 Style Transfer모델은 이미지 분야에서 주로 연구되어 왔으나, 2017년을 기점으로 자연어처리에서도 연구되었습니다.<br/>
최근 3년 동안 연구된 자연어 분야에서의 style transfer는 주로 감성 분석에 바탕해 긍정문을 부정문으로, 혹은 부정문을 긍정문으로 바꾸는 작업이 주된 작업이었습니다.<br/>
KOfish에서는 한국의 작가 웹진 브런치에서 크롤링한 데이터와 AI hub 구어체 데이터와 이를 역번역한 데이터를 통해 원문인 자연스러운 한국어와 역번역문인 부자연스러운 한국어 말뭉치 쌍을 가지고서 Style Trainsfer를 진행했습니다

Baseline 코드로 사용된 엄의섭님의 코드 (https://blog.diyaml.com/teampost/Text-Style-Transfer/)에서 데이터를 브런치 데이터로 바꾸고 classifier를 bart로 적용하는 등 자연스러운 한국어 변환 태스크를 수행하기 위한 변형을 가미하였습니다.


 ## 📌 Dependancy 
-   `python == 3.7 `
-   `pytorch >= 1.4.0`
  


 ## 📝 EXAMPLES
 ### ● DATA
 ### 1-1. 브런치 데이터 크롤러<br/>
 본 프로젝트에서는 보다 자연스러운 구어체를 필요로 했습니다. 따라서 게시글 작성자에 의해 1차 정제가 이뤄진 문장을 크롤링 하고자 했습니다.<br/>
 브런치라는 사이트에 게재된 게시글은 준전문가라고 볼 수 있는 작성자에 의한 1차 정제가 이뤄진 문장이며, 타 사이트에 비해 비교적 깨끗한 상태라고 판단했습니다. 따라서 해당 사이트를 크롤링했습니다.
-  브런치 구조(https://brunch.co.kr/)<br/>
   #브런치 사이트 구조에 대한 기술.<br/>
   
   브런치 사이트는 (2021.10.31. 기준) 총 24개의 카테고리로 구성 되어있습니다.
   ```
   1:우리집 반려동물, 2:글쓰기 코치, 9:직장인 현실조언
   13:뮤직 인사이드
   32:영화리뷰, 33:IT/트랜드, 34:그림/웹툰, 39:사진/촬영, 35:스타트업 경험담, 38:지구한바퀴 세계여행
   40:책, 42:멘탈관리/심리탐구, 43:디자인스토리, 44:사랑/이별, 45:건강/운동, 46:감성 에세이
   50:요리/레시피, #52:인문학/철학, 56:멋진 캘리그래피, 59:육아이야기,
   64:문화/예술, #67:시사/이슈 69:쉽게읽는 역사
   77:건출/설계
   ```
   카테고리 별 리스트 페이지로 이동이 되며, 리스트 페이지로 이동시 마우스 드래그를 통해 **이전 게시물을 로드**합니다.<br/>
   웹 브라우저 개발자 도구(f12 function key)를 활성화 하여 Network 카테고리에서 업로드를 확인 할 수 있으며 업로드 되는 링크는 다음과 같습니다.<br/>
   https://api.brunch.co.kr/v1/top/keyword/group/38?publishTime=1635554744000&pickContentId=<br/>
   게시물을 내려 개발자 도구 Network 카테고리에서 로드되는 Name을 선택시, Header 카테고리에서 디테일한 정보를 확인할 수 있습니다.<br/>
   해당 경로의 Query String Parameters 업데이트를 통해 **이전 게시물에 접근**이 가능하다는 것을 알 수 있습니다.
   ```
   #Query String Prameters
   publishTime: 1635464409000
   pickContentId: 
   ```
   앞서 말씀드린 경로 업데이트를 통해 추가적인 라이브러리 없이 게시물을 계속해서 로드하고 크롤링 할 수 있습니다.<br/>
   해당 크롤러는 게시글 리스트 업데이트를 통해 게시글 유저명을 추출하였고, 추출된 아이디를 통해 게시글 디테일 페이지에 접근할 수 있었습니다.<br/>
   유저별 200개의 게시글에 접근했고 존재하지 않거나 비공개 상태인 게시글은 무시한 채, 공개 게시글을 크롤링했습니다.<br/>
   이와같은 접근과 크롤링을 반복한 크롤러입니다.
   
   
-  브런치 크롤링 순서<br/>
   브런치 사이트 크롤링 순서는 다음과 같습니다.<br/>
   1) 브런치 카테고리별 리스트 내에서 게시글 접근<br/>
     1-1) 게시글 리스트에서 확인할 수 있는 로드 패턴을 파악<br/>
     1-2) 앞서 언급한 Network 카테고리에서 확인할 수 있는 publishTime 값을 수정하여 리스트를 업로드<br/>
   2) 게시글의 유저 아이디 접근<br/>
     2-1) 게시글 리스트에서 유저 아이디 추출
     2-2) 게시글 디테일 페이지의 경로는 다음과 같습니다.https://brunch.co.kr/@rlrmadks/165 <br/>
     　　※ 간혹 다음과 같은 패턴의 경로를 확인할 수 있습니다.<br/>
        　　 　https://brunch.co.kr/@27dbad9229ae4b3/16<br/>
        　　 　이와같은 경로는 무시한 채 진행했습니다.<br/>
     2-3) 유저 이름과 번호로 게시글 디렉토리가 구성되어 있는 것을 확인<br/>
     2-4) 유저별 게시글을 0번부터 200번까지 접근하여 존재하는 게시글을 크롤링<br/>
     2-5) 유저의 게시글의 접근이 끝나면 다음 유저아이디에 접근하며, 게시글 리스트를 게속해서 로드하고 유저명을 업데이트<br/>
     2-6) 접근과 크롤링을 반복



-  브런치 크롤러 사용 방법<br/>
   1) 해당 크롤러는 경로 수정 및 카테고리 넘버 수정을 통해 작동이 가능합니다.<br/>
   ※ 자세한 사항은 아래 How to use 참고.　　　　　


-  브런치 크롤러 문제점<br/>
   ※ 해당 크롤러는 다양한 문제가 존재합니다.<br/>
   1) 해당 크롤러의 시스템은 **완전 자동화 되어있지 않습니다.**<br/>
   1-1) 카테고리 접근이 수동으로 기술되어 있으며, 그 이유는 **카테고리별 게시글 리스트와 디테일 페이지의 차이점**에 있습니다.<br/>
   카테고리별로 작고 큰 차이가 존재하며 발생하는 결함의 원인을 파악하지 않은 채 진행되었습니다.
   2) 앞서 언급한 publishTime의 패턴을 파악하지 않은 채 진행되었습니다. <br/>
   2-1) 해당 publishTime의 조작을 통해 리스트 업로드가 가능했지만, 정확한 패턴을 파악하지 않은채 숫자를 더하거나 빼는 등의 **기초 연산을 통해 접근**을 강행했습니다.<br/>
   따라서 **패턴에 근간한 순서적 리스트 업로드**가 아닌 **랜덤한 값으로 접근**하여 로드했습니다. 따라서 해당 문제로 인한 **중복 코퍼스가 발생**합니다.<br/>
   3) 비효율적 코드 진행<br/>
   3-1) 해당 크롤러는 접근 및 크롤링 그리고 전처리까지 한번에 모든 것을 자동화 시키기 위한 노력을 기반으로 제작했습니다.<br/>
   하지만 미숙한 코드 진행과 비효율적인 내부 트러블이 존재합니다.<br/>
   　　ex) 불필요한 (존재하지않는)게시글 접근<br/>
     　　수동으로 카테고리 수정<br/> 
     　　기초 연산을 근간으로 한 게시글 로드<br/>
     　　발생하는 결함을 피하기 위한 임시 코드<br/>
     　　반복 for문의 중복 사용 등



 ### 1-2. Korpora Library Data 한/영 자막
  코포라 라이브러리에서 제공하는 한/영 병렬 말뭉치 자막 데이터를 이용하여 데이터 구축.
  참조: https://github.com/ko-nlp/Korpora <br/>
  <br/><br/>
  
  
 ### ● Model
 본 프로젝트에서 사용한 Baseline Code는 저자인 Tianxiao Shen의 것이 아니다. 저자의 코드가 Papers with code 에 게재되어 있지만 python2.x , tensorflow1.x를 사용하고 있어 버전 상의 어려움으로 인하여 저자의 코드를 직접 구현한 동아리 DIYA의 엄의섭님 외 3인이 작성한 코드(각주 추가)를 바탕으로 구현하였다.

 
 #<hr width = "100%" color = "gray" size = "0.1">
 <br/><br/>
 
 ## ❔ How to use
 ### 1-1. Crawlier
   data/src/crawlier/crawlier.py 파일을 열어 저장경로와 카테고리 넘버를 수정 후 진행
   
   ```
   cd crawlier
   python crawlier.py
   
   ```
 ### 1-2. Korpora Library Data
   data/src/korpora/korpora.py 파일을 열어 로드/세이브 경로 설정 후 진행
   
   ```
   cd data/src/korpora
   python korpora.py
   
   ```
 ### 2-1. 브런치 데이터를 이용한 스타일 트랜스퍼 진행
 
  options.py 에서 모델이 저장 될 경로를 수정, train, test, val_text파일 설정
  
   1) Classifier 모델 훈련

       ```
       python bert_pretrained/classifier.py --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt" 
       
       ```
  
   1) Style Transfer 모델 훈련
      
      ```
      python train.py --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt"
      
      ```
   3) Transfer!

      ```
      python trasfer.py --mode "transfer" --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt"

      ```
   
 ### 2-2. 스타일 트랜스퍼 진행
 
   options.py 에서 train, test, val_text파일 설정 후 
    
   1) Classifier 모델 훈련

       ```
       python bert_pretrained/classifier.py --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt" 
       
       ```

   2) Style Transfer 모델 훈련
    
        ```
        python train.py --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt"

        ```
   3) Transfer!

        ```
        python trasfer.py --mode "transfer" --ckpt_path "./ckpt" --clf_ckpt_path "./clf_ckpt"

        ```

   
   ## ❕ Results

<img width="620" alt="스크린샷 2021-10-31 오후 12 31 27" src="https://user-images.githubusercontent.com/84896185/139566368-9796088f-ffd9-4ac4-8b15-17f5fbb5c7c3.png">





  ACC가 0.6의 결과는 참담했습니다.<br/>
  원인 딥러닝 모델이 **자연스러운 한국어**와 **부자연스러운 한국어**의 맥락 상의 차이를 발견하지 못했기 때문입니다.<br/>
  classifer도 구분확률이 0.5를 상회했기 때문에 **원문**과 **역번역문**의 **구분이 이루어지지 않는 것**을 확인할 수 있었습니다.<br/>
  bart classifier의 경우는 0.8이 넘는 구분 성능을 보여주었지만, 이 또한 **성능 평가 지표**로만 활용될 뿐 실제 훈련에 **영향을 주지 않기 때문**에 성능 향상에는 어려움을 겪었습니다. 

   ## 📔 References
    - https://blog.diyaml.com/teampost/Text-Style-Transfer/
    - Style Transfer from Non-Parallel Text by Cross-Alignment, Tianxiao Shen et al, NIPS 2017

