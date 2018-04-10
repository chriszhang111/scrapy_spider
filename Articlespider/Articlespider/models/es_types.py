from datetime import datetime

from elasticsearch_dsl import Completion
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.analysis import CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=['localhost'])


class CustomAnalyzer_(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer_("ik_max_word",filter=["lowercase"])

class Article(DocType):
    """
    model for article in jobbole
    """
    suggest_ = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()  ##no need to seprate and analyze
    # url_object_id = Keyword()
    front_img_url = Keyword()
    # front_img_path = Keyword()
    like_num = Integer()
    record_num = Integer()
    comment_num = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = "article"







if __name__ == '__main__':
    Article.init()