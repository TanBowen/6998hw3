import json
import boto3
from botocore.vendored import requests


def lambda_handler(event, context):
    #q = "show me photos with Tree in them"
    print(event['q'])
    q = event['q']

    client = boto3.client('lex-runtime')
    lex_response = client.post_text(
        botAlias='$LATEST',
        # 'Prod'
        botName='PhotoAlbum',
        inputText=q,
        userId='search-photos',
    )
    print(json.dumps(lex_response, indent=2))

    # keywords = event['message'].split(" ")
    keywords = []
    keyWordOne = lex_response['slots']['keyWordOne']
    keyWordTwo = lex_response['slots']['keyWordTwo']
    if keyWordOne is not None:
        keywords.append(keyWordOne)
    if keyWordTwo is not None:
        keywords.append(keyWordTwo)

    # Search the keywords in ElasticSearch
    results = search(keywords)
    print(json.dumps({"results": results}, indent=2))
    print(type(json.dumps({"results": results})))
    return {
        'statusCode': 200,
        'body': json.dumps({"results": results})
    }


def search(keywords):
    results = []
    for keyword in keywords:
        vpc_endpoint = "https://vpc-elasticphotos-unknkut2kzumewb3w67boaouye.us-east-1.es.amazonaws.com"
        search_url = vpc_endpoint + "/elasticphotos/_search?q=" + keyword
        response = requests.get(search_url)
        response = response.json()
        print(json.dumps(response, indent=2))
        for hit in response["hits"]["hits"]:
            _source = hit["_source"]
            objectKey = _source["objectKey"]
            bucket = _source["bucket"]
            labels = _source["labels"]
            result = {"url": "https://s3.amazonaws.com/" + bucket + "/" + objectKey, "labels": labels}
            results.append(result)
    return results


"""
response syntax:
{
  "results": [
    {
      "url": "string",
      "labels": [
        "string"
      ]
    }
  ]
}
"""
