import numpy as np  
from functools import reduce
from math import sqrt

class CosineSimilarity(object):
    '''
    余弦相似性计算相似度
    '''
    def __init__(self, init_query, target_data):
        '''
        相似化相似度计算类
        '''
        self.init_query = init_query
        self.target_data = target_data
    
    def create_vector(self):
        '''
        创建兴趣向量
        return word_vector = {} 文本以及文本向量 index: value 例如 [[1, 2, 1, 1, 2, 0, 1], [1, 2, 1, 2, 2, 1, 1]]
        '''
        index, value = self.target_data['index'], self.target_data['value']
        word_vector = {
            'index': index,
            'value': []
        }
        title_vector, value_vector = [], []
        all_word = set(self.init_query + value)
        for each_word in all_word:
            title_num = self.init_query.count(each_word)
            value_num = value.count(each_word)
            title_vector.append(title_num)
            value_vector.append(value_num)
        word_vector['value'].append(title_num)
        word_vector['value'].append(value_vector)
        return word_vector

    def calculate(self, wordVector):
        '''
        计算余弦相似度
        return: 返回各个用户相似度值
        '''
        result_dic = {}
        value = wordVector['value']

        value_arr = np.array(value)
        # 余弦相似性
        squares = []
        numerator = reduce(lambda x, y: x + y, value_arr[0] * value_arr[1])
        square_title, square_data = 0.0, 0.0
        for num in range(len(value_arr[0])):
            square_title += pow(value_arr[0][num], 2)
            square_data += pow(value_arr[1][num], 2)
        squares.append(sqrt(square_title))
        squares.append(sqrt(square_data))
        mul_of_squares = reduce(lambda x, y: x*y, squares)
        value = float(('%.5f' % (numerator / mul_of_squares)))
        result_dic['index'] = wordVector['index']
        result_dic['value'] = value
        return result_dic

if __name__ == '__main__':
    value = ['c', 'programming language', 'learn']
    data = {
        'index': 'learn c programming language book'
        'value': ['learn', 'c', 'prgramming', 'language', 'book']
    }
    cos = CosineSimilarity(value, data)
    vector = cos.create_vector()
    result = cos.calculate(vector)
    print(result)
    


