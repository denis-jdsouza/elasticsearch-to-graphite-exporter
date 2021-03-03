'''
The items in each of the tuples (ES_DOMAIN, ES_LUCENE_QUERY, ES_INDICES, GRAPHITE_TAGS) correspond to each other at a given index-number
Eg: item at ES_DOMAIN[0] corresponds to the items at ES_LUCENE_QUERY[0], ES_INDICES[0], GRAPHITE_TAGS[0]
'''

# Elasticsearch query string
ES_QUERY_STRING = [
    '{ "size": 0, "query": { "bool": { "must": [ { "query_string": { "analyze_wildcard": true, "query": "%s" } }, { "range": { "@timestamp": { "gte": "%s", "lte": "%s"}}}]}}, "aggs":{ "2":{ "date_histogram":{ "extended_bounds": { "min": "%s", "max": "%s"}, "field": "@timestamp", "interval": "%s", "min_doc_count": 0 }}}}'
]

# Elasticsearch domain-name/IP (different Elasticsearch endpoints are supported)
ES_DOMAIN = (
    'elasticsearch.example.com',
    'elasticsearch.example.com',
    'elasticsearch.example.com',
    'elasticsearch.example.com',
    'elasticsearch.example.com'
)

# Elasticsearch Lucene query (corresponding to 'ES_QUERY_STRING')
ES_LUCENE_QUERY = (
    r'level: \"warn\"',
    r'level: \"error\" NOT beat.name: \"test\"',
    'status: 200',
    'status: [400 TO 499]',
    'status: [500 TO 599]'
)

# Elasticsearch index
ES_INDICES = (
    "web-01-app-logs-*",
    "web-01-app-logs-*",
    "nginx-access-logs-*",
    "nginx-access-logs-*",
    "nginx-access-logs-*"
)

# Series-name/tags to be processes in Graphite format, corresponds to Elasticsearch Lucene query in 'ES_LUCENE_QUERY'
GRAPHITE_TAGS = (
    'level_warn.count;source=ES;type=logs;team=devops;app=web-01 %s %s',
    'level_error.count;source=ES;type=logs;team=devops;app=web-01 %s %s',
    '200_response.count;source=ES;type=logs;team=devops;app=nginx %s %s',
    '4xx_response.count;source=ES;type=logs;team=devops;app=nginx %s %s',
    '5xx_response.count;source=ES;type=logs;team=devops;app=nginx %s %s'
)