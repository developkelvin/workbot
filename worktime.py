import time
import os

DEFAULT_PATH = os.path.join(os.getcwd(), 'worklog')

SUCCESS = 1
FAILURE = 2
START_INFO_NOT_EXIST = 3

def start_work(author):
    result = dict()
    
    status_code = SUCCESS
    try:
        start_time = time.time() # float
        unique_id = str(author.id) + str(author.discriminator) # author.id가 유저 별로 변하지 않는 고유 아이디라고 가정
        save_path = os.path.join(DEFAULT_PATH, unique_id+'.log')
        with open(save_path, 'w', encoding='utf8') as f:
            f.write(str(start_time))
    except Exception as e:
        print(e)
        status_code = FAILURE

    result['status_code'] = status_code

    return result

def end_work(author):
    result = dict()
    status_code = SUCCESS
    try:
        start_time = float(0)
        end_time = time.time() # float
        unique_id = str(author.id) + str(author.discriminator) # author.id가 유저 별로 변하지 않는 고유 아이디라고 가정
        save_path = os.path.join(DEFAULT_PATH, unique_id+'.log')
        with open(save_path, 'r', encoding='utf8') as f:
            start_time = f.readline()
            start_time = float(start_time)

        os.remove(save_path)
    except FileNotFoundError as ffe:
        status_code = START_INFO_NOT_EXIST
    except Exception as e:
        print(e)
        status_code = FAILURE
    
    assert end_time - start_time > 0

    result['status_code'] = status_code
    time_diff = end_time - start_time

    time_ = time_diff
    day = time_ // (24 * 3600)
    time_ = time_ % (24 * 3600)
    hour = time_ // 3600
    time_ %= 3600
    minutes = time_ // 60
    time_ %= 60
    seconds = time_

    result['time_diff'] = time_diff
    result['msg'] = f'근무 시간 : {day}일 {hour}시간 {minutes}분 {seconds:0.0f}초'

    return result
    

