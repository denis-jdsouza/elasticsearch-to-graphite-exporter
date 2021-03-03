#!/usr/bin/env python3.6
from socket import socket
from elasticsearch import Elasticsearch
import dateutil.parser as dp
import defs

# Graphite-Carbon Deatils
CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003  # plaintext port

# Time-range to query Elasticsearch (change values as per requirements)
start_time = "now-60s"
end_time = "now"
interval = "1m"


def iso8601_to_epoc(time_string):
    """ Function to convert ISO8601 to epoc time """
    epoc_time = dp.parse(time_string).strftime('%s')
    return epoc_time


def es_query(query_index):
    """ Function to query Elasticsearch """
    payload = defs.ES_QUERY_STRING[0] % (
        defs.ES_LUCENE_QUERY[query_index], start_time, end_time, start_time, end_time, interval)
    es = Elasticsearch([defs.ES_DOMAIN[query_index]])
    response = es.search(index=defs.ES_INDICES[query_index], body=payload)
    buckets = response['aggregations']['2']['buckets']
    return buckets


def process_metrics(buckets, query_index):
    """ Function to process Elasticsearch data into Graphite format """
    lines_list = []
    for bucket in buckets:
        lines = defs.GRAPHITE_TAGS[query_index] % (
            bucket['doc_count'], iso8601_to_epoc(bucket['key_as_string']))
        lines_list.append(lines)
    return lines_list


def send_metrics_graphite(message):
    """ Function to send metrics to Graphite/Carbon """
    sock = socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message.encode())
    sock.close()


if __name__ == "__main__":
    metrics_count = 0
    loop_count = -1
    for query in defs.ES_LUCENE_QUERY:
        metrics_count += 1
        loop_count += 1
        query_index = loop_count
        buckets = es_query(query_index)
        if buckets != []:
            message = process_metrics(buckets, query_index)
            message_formatted = '\n'.join(message) + '\n'
            print(message_formatted)
            send_metrics_graphite(message_formatted)
        else:
            print(f'No hits for query: {query}')
            metrics_count -= 1
    print(f'Metrics sent for: {str(metrics_count)} queries')
