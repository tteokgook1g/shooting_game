'''
프로젝트에 사용할 함수
'''

import math


def get_direction(src: tuple[float, float], dst: tuple[float, float]) -> tuple[float, float]:
    'src에서 dst방향의 단위벡터 반환'
    d = math.sqrt((dst[0] - src[0])**2 + (dst[1] - src[1])**2)
    return ((dst[0]-src[0])/d, (dst[1]-src[1])/d)
