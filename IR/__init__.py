"""
Description for Package
"""
from IR.query import get_query, similarity_ranks
from IR.vectorizer import vectorize
from IR.highlightAlgo import makeHighlightBystreamer, ChangeToSecond, getTimeSection
from IR.chatAnalyze import ChatAnalyze, normalizing
from IR.repeatReplacer import RegexpReplacer, RepeatReplacer
from IR.evalfunc import cosine_func, distance_func

# 이 배열에 포함되는 모듈의 이름은 from [package name] import * 를 통해서도 참조될 수 있다.
__all__ = ['query', 'vectorizer', 'chatAnalyze',
           'repeatReplacer', 'evalfunc', 'highlightAlgo']
__version__ = '0.1.0'  # 패키지의 버전을 정의한다.
