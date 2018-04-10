from elasticsearch_dsl import Completion
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.analysis import CustomAnalyzer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])
class CustomAnalyzer_(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer_("ik_max_word",filter=["lowercase"])

class LagouType(DocType):
    suggest_ = Completion(analyzer=ik_analyzer)
    url = Keyword()
    url_object_id = Keyword()
    title = Text(analyzer="ik_max_word")
    salary = Text(analyzer="ik_max_word")
    city = Keyword()
    work_years = Text(analyzer="ik_max_word")
    degree_need = Text(analyzer="ik_max_word")
    job_type = Keyword()
    publish_time = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")
    job_advantage = Text(analyzer="ik_max_word")
    job_desc = Text(analyzer="ik_max_word")
    job_addr = Text(analyzer="ik_max_word")
    company_name = Text(analyzer="ik_max_word")
    company_url = Text(analyzer="ik_max_word")
    crawl_time = Date()

    class Meta:
        index = "lagou"
        doc_type = "job"

if __name__ == '__main__':
    LagouType.init()
    print(connections.get_connection().cluster.health())