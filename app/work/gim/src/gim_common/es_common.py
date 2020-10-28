from string import Template

ES_QUERY_BATCH_SIZE = 200
QUERY_STRING = '''{
       "query": {
          "bool" : {
             "must" : [
                   {
                      "match" : {
                         "partnerAccountId.keyword" : "$PA_ID"
                      }
                   }
             ]
          }
       },
        "sort": [
            {
                "_id": {
                    "order": "asc"
                }
            }
        ]
     }'''


def query_es_result(es, pa_id, from_index):
    doc = Template(QUERY_STRING)
    return es.search(index="fnsku_inventory", body=doc.substitute(PA_ID=pa_id), size=ES_QUERY_BATCH_SIZE,
                     from_=from_index)


def query_next_page(es, pa_id, total_size, all_result):
    current_index = ES_QUERY_BATCH_SIZE
    while current_index < total_size:
        next_page_result = query_es_result(es, pa_id, current_index)
        all_result.extend(next_page_result['hits'])
        current_index += ES_QUERY_BATCH_SIZE


def get_all_es_result(es, pa_id):
    result = query_es_result(es, pa_id, 0)
    total_size = result['hits']['total']
    all_result = []
    all_result.extend(result['hits'])
    if total_size > 0:
        if total_size > ES_QUERY_BATCH_SIZE:
            query_next_page(es, pa_id, total_size, all_result)
    return all_result