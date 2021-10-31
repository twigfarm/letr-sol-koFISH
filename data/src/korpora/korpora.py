# pip install Korpora 설치 필요

# 라이브러리 설치
import re
import pandas as pd
from Korpora import Korpora

corpus = Korpora.load("open_subtitles")
Korpora.corpus_list()
#Korpora.fetch("open_subtitles")

# korpora 한/영 자막 코퍼스 로드
corpus_text = corpus.get_all_texts() #한글자막

# 1차 전처리
cleaned_text = []
for i in corpus_text:
  re_sub = re.sub('-','', i)
  cleaned_text.append(re_sub.strip())

# 원문 데이터프레임 설정 및 레이블값 지정
korpora_0 = pd.DataFrame(cleaned_text, columns=['document'])
korpora_0['label'] = 0

# 역번역한 문장 로드
korpora_1 = pd.read_csv('data/raw/korpora_1.csv')
korpora_1.columns = ['document']
korpora_1['label'] = 1

# 원문&역번역문 병합
korpora_all = pd.DataFrame()
korpora_all.concat([korpora_0,korpora_1])

# 셔플링, 인덱스 초기화
korpora = korpora_all.sample(frac=1).reset_index(drop=True)

# 데이터 분할(train, test, validation)
train_korpora = pd.DataFrame()
test_korpora = pd.DataFrame()
val_korpora = pd.DataFrame()

train_korpora['document'] = korpora['document'][:1198252]
train_korpora['label'] = korpora['label'][:1198252]

test_korpora['document'] = korpora['document'][1198252:1598252]
test_korpora['label'] = korpora['label'][1198252:1598252]

val_korpora['document'] = korpora['document'][1598252:]
val_korpora['label'] = korpora['label'][1598252:]

# 분할된 데이터 저장
train_korpora.to_csv('data/before/cleaned/kopora_train.txt', sep='\t')
test_korpora.to_csv('data/before/cleaned/kopora_train.txt', sep='\t')
val_korpora.to_csv('data/before/cleaned/kopora_train.txt', sep='\t')