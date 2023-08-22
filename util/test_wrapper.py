def test_wrapper(test_func):
    def wrapper(*args, **kwargs):
        # 테스트 시작 전 테스트 함수 이름 출력
        print ('\n['+test_func.__name__.upper()+']')
        return test_func(*args, **kwargs)
    return wrapper