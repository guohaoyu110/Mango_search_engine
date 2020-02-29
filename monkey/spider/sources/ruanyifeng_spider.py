# 不能让博客的服务器压力过大造成宕机或者造成自己的ip被封禁， 为了保证爬虫的友好性，可以设定随机休眠，并且
# 伪造一个user_agent, 输入如下代码到文件中：

import random 
import sys

from ruia import AttrField, Item, Request, Spider, TextField
from ruia import middleware

sys.path.append('./')

from monkey.database.motor_base import motor_base

class ArchivesItem(Item):
    '''
    e.g http://www.ruanyifeng.com/blog/archives.html
    '''
    target_item = TextField(css_select='div#beta-inner li.module-list-item')
    href = AttrField(css_select='li.module-list-item>a',attr='href')

class ArticleListItem(Item):
    '''
    e.g http://www.ruanyifeng.com/blog/essays
    '''
    target_item = TextField(css_select='') 