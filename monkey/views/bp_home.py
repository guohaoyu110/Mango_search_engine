# !/usr/bin/env python

'''
 created by Haoyu Guo
'''

import sys
from sanic import Blueprint
from sanic.response import html, json, text 

from monkey.config import Config  
from monkey.common.doc_search import doc_search

bp_home = Blueprint(__name__)
bp_home.static('/statics', Config.BASE_DIR + '/statics/')


# @bp_home.route('/')
async def index(request):
    return text('index')

# @bp_home.route('/search')
async def index(request):
    query = str(request.args.get('q','')).strip()
    mongo_db = request.app.mongo_db
    result = await doc_search(query=query, mongo_db=mongo_db)
    return json(result)

