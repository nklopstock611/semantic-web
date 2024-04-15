import textrazor

textrazor.api_key = "9ad7e5c1d1d4e1e5c48a628a3f4e00519739d386c2f556ad917b1e13"

client = textrazor.TextRazor(extractors=["entities", "topics"])
text = """
"""
# response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")
response = client.analyze(text)

for entity in response.entities():
    print(entity.id, entity.relevance_score, entity.confidence_score, entity.dbpedia_types, entity.wikipedia_link)

print('==================================================================================================================================')

for topic in response.topics():
    print(topic.id, topic.label, topic.score)
