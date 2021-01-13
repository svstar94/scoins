# 최종 목표 : 자동화 프로그램

# 수입 or 지출
#  1 = 수입
# -1 = 지출

IorE = [1, -1]

if IorE == 1:
    File_Name = 'income.csv'
elif IorE == -1:
    File_Name = 'expense.csv'

# 카테고리
Category = [
    ['수익', ['월급', '외주', '보너스', '이익배당금']],
    ['성장', ['자기계발']],
    ['생활', ['식사', '미용', '의복', '생활용품', '통신비', '교통비', '주거비']],
    ['여가', ['커피', '게임', ' 보험', '여행', '문화']],
    ['기타', ['기타', '병원', '경조사', '애완동물']]
]
# 0 : 수익 - 월급, 외주, 보너스, 이익배당금, 투자 - 펀드, 연금
# 1 : 성장 - 자기계발
# 2 : 생활 - 식사, 미용, 의복, 생활용품, 통신비, 교통비
# 3 : 여가 - 커피, 게임, 보험, 여행, 문화
# 4 : 기타 - 기타, 병원, 경조사, 애완동물

Big_Category = 0
Mid_Category = 0

Base_Ctg = Category[Big_Category]
Top_Ctg = Base_Ctg[0]
Mid_Ctg = Base_Ctg[1][Mid_Category]

comment = ''

Coins = ''

if __name__ == "__main__":
    with open(File_Name, 'a') as f:
        f.write(f'{Top_Ctg}, {Mid_Ctg}, {comment}, {Coins}')
    