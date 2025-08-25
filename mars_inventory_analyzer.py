#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
화성 기지 인화물질 분류 프로그램
Mars Base Inventory List에서 인화성 물질을 찾아 분류하는 프로그램
"""


def read_csv_file(filename):
    """
    CSV 파일을 읽어서 리스트로 반환하는 함수
    
    Args:
        filename (str): 읽을 CSV 파일명
        
    Returns:
        list: CSV 데이터를 담은 리스트
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # 헤더와 데이터를 분리
            if lines:
                header = lines[0].strip().split(',')
                print(f'CSV 파일 컬럼: {header}')
                print('-' * 50)
                
                # 각 행을 딕셔너리로 변환
                for line in lines[1:]:
                    line = line.strip()
                    if line:  # 빈 줄이 아닌 경우에만 처리
                        values = line.split(',')
                        if len(values) == len(header):
                            row_dict = {}
                            for i, value in enumerate(values):
                                if header[i].strip().lower() in ['flammability', '인화성']:
                                    # 인화성 지수는 float로 변환
                                    try:
                                        row_dict[header[i].strip()] = float(value.strip())
                                    except ValueError:
                                        row_dict[header[i].strip()] = 0.0
                                else:
                                    row_dict[header[i].strip()] = value.strip()
                            data.append(row_dict)
                
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return []
    except IOError as e:
        print(f'오류: 파일 읽기 중 문제가 발생했습니다. {e}')
        return []
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')
        return []
    
    return data


def print_inventory_data(data):
    """
    인벤토리 데이터를 출력하는 함수
    
    Args:
        data (list): 출력할 데이터 리스트
    """
    if not data:
        print('출력할 데이터가 없습니다.')
        return
    
    print('=== 화성 기지 입고 물질 목록 ===')
    for i, item in enumerate(data, 1):
        print(f'{i:2d}. ', end='')
        for key, value in item.items():
            if isinstance(value, float):
                print(f'{key}: {value:.2f}, ', end='')
            else:
                print(f'{key}: {value}, ', end='')
        print()  # 줄바꿈
    print()


def sort_by_flammability(data):
    """
    인화성 지수가 높은 순으로 정렬하는 함수
    
    Args:
        data (list): 정렬할 데이터 리스트
        
    Returns:
        list: 인화성 지수로 정렬된 리스트
    """
    # 인화성 컬럼명 찾기
    flammability_key = None
    if data:
        for key in data[0].keys():
            if key.lower() in ['flammability', '인화성']:
                flammability_key = key
                break
    
    if flammability_key is None:
        print('인화성 지수 컬럼을 찾을 수 없습니다.')
        return data
    
    # 인화성 지수가 높은 순으로 정렬 (내림차순)
    sorted_data = sorted(data, key=lambda x: x[flammability_key], reverse=True)
    return sorted_data


def filter_dangerous_materials(data, threshold=0.7):
    """
    인화성 지수가 임계값 이상인 위험물질을 필터링하는 함수
    
    Args:
        data (list): 필터링할 데이터 리스트
        threshold (float): 인화성 지수 임계값
        
    Returns:
        list: 위험물질 리스트
    """
    dangerous_materials = []
    
    # 인화성 컬럼명 찾기
    flammability_key = None
    if data:
        for key in data[0].keys():
            if key.lower() in ['flammability', '인화성']:
                flammability_key = key
                break
    
    if flammability_key is None:
        print('인화성 지수 컬럼을 찾을 수 없습니다.')
        return []
    
    for item in data:
        if item[flammability_key] >= threshold:
            dangerous_materials.append(item)
    
    return dangerous_materials


def save_to_csv(data, filename):
    """
    데이터를 CSV 파일로 저장하는 함수
    
    Args:
        data (list): 저장할 데이터 리스트
        filename (str): 저장할 파일명
    """
    if not data:
        print('저장할 데이터가 없습니다.')
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # 헤더 작성
            headers = list(data[0].keys())
            file.write(','.join(headers) + '\n')
            
            # 데이터 작성
            for item in data:
                values = []
                for header in headers:
                    if isinstance(item[header], float):
                        values.append(f'{item[header]:.2f}')
                    else:
                        values.append(str(item[header]))
                file.write(','.join(values) + '\n')
        
        print(f'데이터가 {filename}에 성공적으로 저장되었습니다.')
        
    except IOError as e:
        print(f'오류: 파일 저장 중 문제가 발생했습니다. {e}')
    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')


def main():
    """
    메인 함수
    """
    print('=== 화성 기지 인화물질 분류 프로그램 ===\n')
    
    # 1. CSV 파일 읽기
    inventory_data = read_csv_file('Mars_Base_Inventory_List.csv')
    
    if not inventory_data:
        print('프로그램을 종료합니다.')
        return
    
    # 2. 읽어온 데이터 출력
    print_inventory_data(inventory_data)
    
    # 3. 인화성 지수가 높은 순으로 정렬
    sorted_data = sort_by_flammability(inventory_data)
    print('=== 인화성 지수가 높은 순으로 정렬된 목록 ===')
    print_inventory_data(sorted_data)
    
    # 4. 인화성 지수가 0.7 이상인 위험물질 필터링
    dangerous_materials = filter_dangerous_materials(sorted_data, 0.7)
    print('=== 인화성 지수 0.7 이상 위험물질 목록 ===')
    if dangerous_materials:
        print(f'총 {len(dangerous_materials)}개의 위험물질이 발견되었습니다.')
        print_inventory_data(dangerous_materials)
    else:
        print('인화성 지수 0.7 이상의 위험물질이 없습니다.')
    
    # 5. 위험물질을 CSV 파일로 저장
    if dangerous_materials:
        save_to_csv(dangerous_materials, 'Mars_Base_Inventory_danger.csv')
    
    print('\n프로그램이 완료되었습니다.')


if __name__ == '__main__':
    main()
