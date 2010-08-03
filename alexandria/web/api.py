import alexandria.search
import web
import json

class SimpleSearch:
    def GET(self, query):
        results = alexandria.search.perform_simple_search(query)
        return json.dumps(results)

urls = (
    "/search/simple/(.*)", "SimpleSearch"
)

app = web.application(urls, locals())
