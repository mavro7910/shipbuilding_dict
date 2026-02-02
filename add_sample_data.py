#!/usr/bin/env python3
"""
샘플 데이터 추가 스크립트
"""

from db.database import ShipbuildingDB


def add_sample_data():
    """샘플 조선업 용어 데이터 추가"""
    db = ShipbuildingDB()
    
    sample_terms = [
        {
            'abbreviation': 'LNG',
            'full_term': 'Liquefied Natural Gas',
            'definition': '액화천연가스. 천연가스를 냉각하여 액화시킨 것으로, -162°C에서 기체 상태의 천연가스를 액체로 만들어 부피를 약 1/600로 줄인 것입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'FPSO',
            'full_term': 'Floating Production Storage and Offloading',
            'definition': '부유식 원유생산저장하역설비. 해상 유전에서 원유를 생산, 저장, 하역하는 부유식 설비입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'DWT',
            'full_term': 'Deadweight Tonnage',
            'definition': '재화중량톤수. 선박이 안전하게 적재할 수 있는 최대 화물 중량을 나타내는 단위입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'GT',
            'full_term': 'Gross Tonnage',
            'definition': '총톤수. 선박의 전체 용적을 나타내는 단위로, 선박의 크기를 표시하는 국제적인 기준입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'LPG',
            'full_term': 'Liquefied Petroleum Gas',
            'definition': '액화석유가스. 프로판이나 부탄을 주성분으로 하는 석유가스를 상온에서 가압하여 액화시킨 것입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'VLCC',
            'full_term': 'Very Large Crude Carrier',
            'definition': '초대형 원유운반선. 20만~32만 DWT급의 대형 유조선을 말합니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'ULCC',
            'full_term': 'Ultra Large Crude Carrier',
            'definition': '초초대형 원유운반선. 32만 DWT 이상의 초대형 유조선을 말합니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'TEU',
            'full_term': 'Twenty-foot Equivalent Unit',
            'definition': '20피트 컨테이너 환산 단위. 컨테이너선의 적재 능력을 나타내는 단위로, 길이 20피트 컨테이너 1개를 기준으로 합니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'ABS',
            'full_term': 'American Bureau of Shipping',
            'definition': '미국선급협회. 선박 및 해양구조물의 설계, 건조, 운영에 대한 안전 기준을 제정하고 검사하는 국제적인 선급협회입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'IMO',
            'full_term': 'International Maritime Organization',
            'definition': '국제해사기구. 해운의 안전과 선박에 의한 해양오염 방지에 관한 국제협력을 목적으로 설립된 UN 산하 전문기구입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'SOLAS',
            'full_term': 'Safety of Life at Sea',
            'definition': '해상인명안전협약. 선박의 안전 기준을 규정한 국제협약으로, 선박 건조 및 운항 시 준수해야 할 안전 요건을 정하고 있습니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'MARPOL',
            'full_term': 'Marine Pollution',
            'definition': '선박에 의한 해양오염 방지협약. 선박의 운항으로 인한 해양오염을 방지하기 위한 국제협약입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'FRP',
            'full_term': 'Fiber Reinforced Plastic',
            'definition': '섬유강화플라스틱. 유리섬유, 탄소섬유 등으로 강화한 복합재료로, 선박 건조에 사용됩니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'GPS',
            'full_term': 'Global Positioning System',
            'definition': '위성항법시스템. 인공위성을 이용하여 전 지구적으로 정확한 위치를 파악할 수 있는 시스템입니다.',
            'image_path': ''
        },
        {
            'abbreviation': 'AIS',
            'full_term': 'Automatic Identification System',
            'definition': '선박자동식별장치. 선박의 위치, 침로, 속력 등의 정보를 자동으로 송수신하는 시스템입니다.',
            'image_path': ''
        }
    ]
    
    print('샘플 데이터 추가 중...')
    success_count = 0
    
    for term in sample_terms:
        if db.add_term(
            term['abbreviation'],
            term['full_term'],
            term['definition'],
            term['image_path']
        ):
            success_count += 1
            print(f"✓ {term['abbreviation']} 추가 완료")
        else:
            print(f"✗ {term['abbreviation']} 추가 실패 (이미 존재할 수 있습니다)")
    
    print(f'\n총 {success_count}/{len(sample_terms)}개의 용어가 추가되었습니다.')
    db.close()


if __name__ == '__main__':
    add_sample_data()