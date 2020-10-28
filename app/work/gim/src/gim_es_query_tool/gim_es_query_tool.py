# Read FNSKU data by PAId from ES
import boto3
import certifi
from string import Template
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection

# max sqs send batch is limited by aws, which is 10.
MAX_SQS_BATCH_SIZE = 10
ES_QUERY_BATCH_SIZE = 100


def send_to_backfill_sqs(backfill_result):
    sqs = boto3.resource('sqs')
    backfill_queue = sqs.get_queue_by_name(QueueName='GIMRedriveFNSkuBackfill')
    backfill_msg = Template('''{ "hashKey": "$HASH_KEY" }''')
    msg_list = []
    msg_id = 1
    for item in backfill_result['hits']['hits']:
        hash_key = item['_id']
        message_item = {'Id': str(msg_id), 'MessageBody': backfill_msg.substitute(HASH_KEY=hash_key)}
        msg_id += 1
        msg_list.append(message_item)

    # send list to SQS
    breakdown_lists = [msg_list[i:i + MAX_SQS_BATCH_SIZE] for i in range(0, len(msg_list), MAX_SQS_BATCH_SIZE)]
    for breakdown_list in breakdown_lists:
        print(breakdown_list)
        backfill_queue.send_messages(Entries=breakdown_list)
        print("{} msg(s) sent".format(len(breakdown_list)))


def query_rest_result(es, pa_id, total_size):
    current_index = ES_QUERY_BATCH_SIZE
    while current_index < total_size:
        reset_result = query_es_result(es, pa_id, current_index)
        send_to_backfill_sqs(reset_result)
        current_index += ES_QUERY_BATCH_SIZE


def query_es_result(es, pa_id, from_index):
    doc = Template(''' {
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
     }''')
    return es.search(index="fnsku_inventory", body=doc.substitute(PA_ID=pa_id), size=ES_QUERY_BATCH_SIZE,
                     from_=from_index)


def backfill_es_to_sqs(local_profile_name, pa_id):
    esendpoint = {
        'gim-beta-na': "search-gim-es-cluster-5tc4hckizngvpcagmzc6weahuu.us-east-1.es.amazonaws.com",
        'gim-beta-eu': "search-gim-es-cluster-y2l3k3logbcxis7ubzi7qo4q6e.eu-west-1.es.amazonaws.com",
        'gim-beta-fe': "search-gim-es-cluster-5yrtjwqelleldb3he4mz4nmasy.us-west-2.es.amazonaws.com",
        'gim-gamma-na': "search-gim-es-cluster-of3otpp4nmeohnromybu7tikse.us-east-1.es.amazonaws.com",
        'gim-gamma-eu': "search-gim-es-cluster-w3xjultvzchw4dzhntmuyhrscm.eu-west-1.es.amazonaws.com",
        'gim-gamma-fe': "search-gim-es-cluster-pdnkb5xehzg7ukvafjl6lwrooq.us-west-2.es.amazonaws.com",
        'gim-prod-na': "search-gim-es-cluster-ag7472dxpyeve7g26eb7a3vxia.us-east-1.es.amazonaws.com",
        'gim-prod-eu': "search-gim-es-cluster-wppvdm4yjqtbvpchad4gabajd4.eu-west-1.es.amazonaws.com",
        'gim-prod-fe': "search-gim-es-cluster-cludnch3ouyuptm2xnhsuqqyvu.us-west-2.es.amazonaws.com",
    }

    boto3.setup_default_session(profile_name=local_profile_name)
    session = boto3.session.Session(profile_name=local_profile_name)
    credentials = session.get_credentials().get_frozen_credentials()

    awsauth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_token=credentials.token,
        aws_host=esendpoint[local_profile_name],
        aws_region=session.region_name,
        aws_service='es'
    )

    es = Elasticsearch(
        hosts=[{'host': esendpoint[local_profile_name], 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        ca_certs=certifi.where(),
        connection_class=RequestsHttpConnection
    )

    result = query_es_result(es, pa_id, 0)
    total_size = result['hits']['total']
    if total_size > 0:
        send_to_backfill_sqs(result)
        if total_size > ES_QUERY_BATCH_SIZE:
            query_rest_result(es, pa_id, total_size)
