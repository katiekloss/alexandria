import alexandria.search
import alexandria.couch
import web
import json

class SimpleSearch:
    def GET(self, query):
        results = alexandria.search.perform_simple_search(query)
        db = alexandria.couch.getDatabase()
        file_list = []
        for hash in results:
            pair = db.view('files/by_hash', key=hash)
            pair = [x for x in pair][0].value
            file_list.append([pair[0], pair[1]])
        return json.dumps(file_list)

urls = (
    "/search/simple/(.*)", "SimpleSearch"
)

app = web.application(urls, locals())
