"""
Description for Package
"""
from downloading.intersects import intersect
from downloading.tcd import getTwitchChat, checkArgument, readText, getStreamerName, download, initiate

# 이 배열에 포함되는 모듈의 이름은 from [package name] import * 를 통해서도 참조될 수 있다.
__all__ = ['intersects', 'tcd']
__version__ = '0.1.0'  # 패키지의 버전을 정의한다.
