'''
created by Haoyu Guo
'''
import asyncio
import math
from collections import Counter

from monkey.common.common_tools import gen_stop_words, text_seg
from monkey.database.motor_base import MotorBase  

mongo_db = MotorBase().get_db()
stop_words = gen_stop_words()

def elias_gamma_encode(X: int) -> str:
    '''
    Elias Gamma 算法对倒排列表的文档数值之差进行编码压缩
    '''
    e = int(math.log(X,2))
    d = int(X - math.pow(2,e))
    unary_code = '1'*e +'0'
    binary_d = bin(d).replace('0b','')
    binary_code = ('0'*e)[0:(e - len(binary_d))] + binary_d  
    return f"{unary_code}:{binary_code}"

def elias_gammma_decode(el_str: str) -> int:
    """
    elias gamma算法对倒排列表的文档数值之差进行解码
    """
    unary_code, binary_code = el_str.split(':')
    e = len(unary_code) - 1
    d = int(binary_code, 2)
    return pow(2,e) + d

async def gen_doc_word_id():
    '''
    为单词以及资源文档生成id
    '''
    cursor = mongo_db.source_docs.find({})
    word_list = []
    doc_id, word_id = 0, 0
    async for document in cursor:
        seg_title = text_seg(text=document['title'], stop_words=stop_words)
        doc_id += 1
        cur_item_data = {
            'doc_id': doc_id,
            'seg_title': seg_title,
            "seg_title_counter": Counter(seg_title),
            'title': document['title'],
            'urls': document['url']
        }

        await mongo_db.doc_id.update_one({
            'title': cur_item_data['title']},
            {'$set': cur_item_data},
            upsert = True)
        word_list += seg_title

    for key, value  in Counter(word_list).items():
        word_id += 1
        cur_item_data = {
            'word_id': word_id,
            'word': key,
            'tf': value 
        }

        await mongo_db.word_id.update_one({
            'word': cur_item_data['word']},
            {'$set': cur_item_data},
            upset=True)

async def gen_doc_inverted_index():
    '''
    首先运行程序生成id
    asyncio.get_event_loop().run_util_complete(gen_doc_word_id())
    再构建索引
    : return
    '''
    word_cursor = mongo_db.word_id.find({})
    async for each_word in word_cursor:
        word_id = each_word['word_id']
        word = each_word['word']
        tf = each_word['tf']
        doc_cursor = mongo_db.doc_id.find({"seg_title": word})
        cur_word_data, inverted_list = {}, []
        async for each_doc in doc_cursor:
            doc_id = each_doc['doc_id']
            seg_title_counter = each_doc['seg_title_counter']
            inverted_list.append((doc_id, seg_title_counter[word]))
        cur_word_data['word_id'] = word_id
        cur_word_data['word_if'] = tf
        cur_word_data['inverted_list'] = inverted_list
        await mongo_db.inverted_index.update_one({
            'word_id': cur_word_data['word_id']},
            {'$set': cur_word_data},
            upsert = True)

    print("索引构建成功")
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(gen_doc_inverted_index())



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(gen_doc_word_id())
    asyncio.get_event_loop().run_until_complete(gen_doc_inverted_index())
    # el_str = elias_gamma_encode(100)
    # print(elias_gamma_decode(el_str))