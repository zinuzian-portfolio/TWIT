# -*- coding: utf-8 -*-
from sklearn.metrics.pairwise import cosine_similarity



"""
To use this code 3 conditions are requried except query.

1. The list about svd vectors of each streamer. (the information about which index is belong to streamer should be saved)
2. Trained tf-idf model of sci-kit learn.
3. Trained svd model of ski-kit learn.
"""


def get_query(trained_tfidf, trained_svd, query):
    """
    trained_tfidf : Trained tf-idf model of sci-kit learn.
                    To create tf-idf matrix of query
                    
    trained_svd   : Trained svd model of sci-kit learn.
                    To fit given query into SVD matrix
                    
    query         : String.
                    The query user will insert.
    
    return        : Numpy.array
                    Matrix for of query
        
    """

    query_matrix = trained_tfidf.transform(query)
    result = trained_svd.transform(query_matrix)
    return result


def similarity_ranks(svd_list, m_query):
    """
    svd_list :  List. each element is numpy.arrary.
                The mean value of SVD vector for steamer's videos.
               
    m_query  :  Numpy.array
                SVD vector from the function get_query's result.
                
    return   :  List
                The ranking of cosine similarity about svd_list index (for each streamer)
    """
    temp = [cosine_similarity(m_query, y) for y in svd_list]
    return sorted(range(len(temp)), key=lambda k: temp[k], reverse =True)
    


