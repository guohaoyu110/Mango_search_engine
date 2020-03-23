from ruia import AttrField, Item, Request, Spider, TextField
from ruia_ua import middleware

class ArchivesItem(Item):
    """
    eg: http://www.ruanyifeng.com/blog/archives.html
    """
    target_item = TextField(css_select='div#beta-inner li.module-list-item')
    href = AttrField(css_select='li.module-list-item>a', attr='href')

class ArticleListItem(Item):
    """
    eg: http://www.ruanyifeng.com/blog/essays/
    """
    target_item = TextField(css_select='div#alpha-inner li.module-list-item')
    title = TextField(css_select='li.module-list-item>a')
    href = AttrField(css_select='li.module-list-item>a', attr='href')


class BlogSpider(Spider):
    """
    针对博客源 https://www.ruanyifeng.com/blog/archives.html 的爬虫
    这里为了模拟ua，引入了一个ruia的第三方扩展
        - ruia-ua: https://github.com/howie6879/ruia-ua
        - pipenv install ruia-ua
        - 此扩展会自动为每一次请求随机添加 User-Agent
    """
    # 设置启动URL
    start_urls = ['https://www.ruanyifeng.com/blog/archives.html']
    # start_urls = ['https://blog.acolyer.org/archives/']
    # 爬虫模拟请求的配置参数
    request_config = {
        'RETRIES': 3,
        'DELAY': 1,
        'TIMEOUT': 200
    }
    # 请求信号量
    concurrency = 10
    blog_nums = 0

    async def parse(self, res):
        items = await ArchivesItem.get_items(html=res.html)
        for item in items:
            yield Request(
                item.href,
                callback=self.parse_item
            )

    async def parse_item(self, res):
        items = await ArticleListItem.get_items(html=res.html)
        BlogSpider.blog_nums += len(items)


if __name__ == '__main__':
    BlogSpider.start(middleware=middleware)
    print(f"Total blog number：{BlogSpider.blog_nums} ")