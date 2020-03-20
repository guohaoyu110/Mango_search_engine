# !/usr/bin/env python

'''
 created by Haoyu Guo
'''

import sys
from sanic import Blueprint
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic.response import html, json, text 

from monkey.config import Config  
from monkey.common.doc_search import doc_search

bp_home = Blueprint(__name__)
bp_home.static('/statics', Config.BASE_DIR + '/statics/')

# 开启异步特性，要求3.6+
enbale_async = sys.version_info >= (3, 6)

# jinja2 config
env = Environment(
    loader=PackageLoader('views.bp_home', '../templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=enable_async)

async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    rendered_template = await template.render_async(**kwargs)
    return html(rendered_template)

# @bp_home.route('/')
async def index(request):
    return await template('index.html')
    #return text('index')

# @bp_home.route('/search')
async def index(request):
    query = str(request.args.get('q','')).strip()
    if query:
        cache_result = await request.app.cache.get(query)
        if cache_result:
            # 如果存在缓存
            result = cache_result
        else:
            # 不存在则去数据库查找
            mongo_db = request.app.mongo_db
            result = await doc_search(query=query, mongo_db=mongo_db)
            await request.app.cache.set(query, result)
        # 为了能够看出加了缓存后查询时间的差异，小数点向后移动到6位
        time_cost = float('%.6f' % (time.time() - start))
        return await template(
            'search.html',
            title=query,
            result=result,
            count=len(result),
            time_cost=time_cost
        )
        # return await template('search.html', title=query, result=result)
    else:
        return await template('index.html')
    #return json(result)

