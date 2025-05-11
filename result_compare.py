import pandas as pd

# 파일 경로 설정
default_path = 'guardrails_selfcheckResult_defaultDomain.xlsx'
custom_path = 'guardrails_selfcheckResult_militaryDomain.xlsx'

# 시트 목록
sheets = ['이데올로기 문제', '군사 기밀', '군기 문란']

# 결과 저장용
results = {}
for sheet in sheets:
    # 열 이름 무시하고 첫 번째 열로만 불러옴
    default_df = pd.read_excel(default_path, sheet_name=sheet, usecols="E", skiprows=1, nrows=700, header=None)
    custom_df = pd.read_excel(custom_path, sheet_name=sheet, usecols="E", skiprows=1, nrows=700, header=None)

    # 열 이름이 없으므로 0번째 컬럼 사용
    df = pd.DataFrame({
        'default': default_df.iloc[:, 0],
        'custom': custom_df.iloc[:, 0]
    })

    # 분류
    df['type'] = ''
    df.loc[(df['default'] == '통과') & (df['custom'] == '통과'), 'type'] = '미탐'
    df.loc[(df['default'] == '통과') & (df['custom'] == '필터링됨'), 'type'] = '정탐'
    df.loc[(df['default'] == '필터링됨') & (df['custom'] == '통과'), 'type'] = '오탐'

    # 인덱스는 실제 엑셀 행번호로 (E2부터 시작하니 +2)
    results[sheet] = {
        '미탐': [i+2 for i in df[df['type'] == '미탐'].index],
        '정탐': [i+2 for i in df[df['type'] == '정탐'].index],
        '오탐': [i+2 for i in df[df['type'] == '오탐'].index],
        'count': df['type'].value_counts().to_dict()
    }

# 출력
for sheet, data in results.items():
    print(f"\n📄 [시트: {sheet}]")
    print(f"  ✅ 미탐: {len(data['미탐'])}건 → 행 번호: {data['미탐']}")
    print(f"  🔥 정탐: {len(data['정탐'])}건 → 행 번호: {data['정탐']}")
    print(f"  ❌ 오탐: {len(data['오탐'])}건 → 행 번호: {data['오탐']}")
