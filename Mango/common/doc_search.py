'''
 created by Haoyu Guo
'''
# 之前的交互只是一个终端版本，所以此节的目的是利用Sanic编写一个web服务端界面进行交互。
# 将余弦相似度算法和搜索过程结合起来即可，修改doc_search 函数这一处地方最好
import asyncio
import pymongo

from operator import itemgetter

from monkey.common.common_tools import gen_stop_words, text_seg
from monkey.database.motor_base import MotorBase  
from monkey.utils.log import logger

stop_words = gen_stop_words()

async def doc_search(*, query: str, mongo_db = None) -> list:
    '''
    布尔查询
    param query:
    '''
    result = []
    try:
        if mongo_db is None:
            mongo_db = MotorBase().get_db()
        seg_query = text_seg(text=query, stop_words = stop_words)
        query_list, word_id_list, doc_id_list, final_query_list = [], [], [], []

        for each_word in seg_query:
            query_list.append(
                {
                    'word': each_word
                }
            )
        # 分词的词组转化成单词id 单词id最好加载到内存 节省一次数据库查询
        word_cursor = mongo_db.word_id.find(
            {"$or": query_list},
            {"word_id": 1, '_id': 0}
        )
        async for word in word_cursor:
            word_id_list.append(word)
        
        # 根据单词id找出文档
        index_cursor = mongo_db.inverted_index.find(
            {"$or": word_id_list},
            {'inverted_list': 1, 'word_tf': 1, '_id': 0}
        )
        async for index in index_cursor:
            cur_doc_id = 0
            # 将倒列表数据加载进内存
            for i in index['inverted_list']:
                cur_doc_id += i[0]
                doc_id_list.append(cur_doc_id)
        print(doc_id_list)
        # 根据文档id 找出文档详细信息
        for each_doc in set(doc_id_list):
            final_query_list.append(
                {
                    'doc_id': each_doc
                }
            )
        doc_cursor = mongo_db.doc_id.find(
            {"$or": final_query_list},
            {"_id": 0}
        )
        query_list = text_seg(query)

        async for doc in doc_cursor:
            # 对输出的结果计算余弦相似度
            doc_data = {
                'index': doc['title'],
                'value': text_seg(doc['title'].lower())
            }
            cos = CosinSimilarity(query_list, doc_data)
            vector = cos.create_vector()
            cs_res = cos.calculate(vector)
            doc['cs_value'] = cs_res['value']
            result.append(doc)
    except pymongo.errors.OperationFailure as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    # 根据余弦相似度的值进行排序
    result_sorted = sorted(
        result,
        reverse=True,
        key=itemgetter('cs_value')
    )
    return result_sorted

if __name__ == '__main__':
    res = asyncio.get_event_loop().run_until_complete(doc_search(query='c programming language'))
    for each in res:
        print(each['title'])
        print(each['cs_value'])
        
