import json
import textrazor

with open("/workspaces/semantic-web/credentials.json", "r") as f:
    json_obj = json.load(f)

textrazor.api_key = json_obj["API_KEY_TR"]
client = textrazor.TextRazor(extractors=["entities", "topics"])

def transform_response(response: textrazor.TextRazorResponse) -> list:
    entities = []
    entitites_set = set()
    for entity in response.entities():
        each = {}
        if entity.id not in entitites_set:
            entitites_set.add(entity.id)
            each["id"] = entity.id
            each["relevance_score"] = entity.relevance_score
            each["confidence_score"] = entity.confidence_score
            each["dbpedia_types"] = entity.dbpedia_types
            each["wikipedia_link"] = entity.wikipedia_link
            # print(entity.id, entity.relevance_score, entity.confidence_score, entity.dbpedia_types, entity.wikipedia_link)
            entities.append(each)
        
    topics = []
    topics_set = set()
    for topic in response.topics():
        each = {}
        if topic.label not in topics_set:
            topics_set.add(topic.label)
            each["id"] = topic.id
            each["label"] = topic.label
            each["score"] = topic.score
            # print(topic.id, topic.json, topic.label, topic.score)
            topics.append(each)

    return (entities, topics)

def get_analytics_json(json_obj: dict, json_obj_id: str) -> dict:
    full_response = {}
    response = {}
    response["paper_id"] = json_obj_id

    title = json_obj["paper_title"]
    response["title"] = title
    trans_resp = transform_response(client.analyze(title))
    response["paper_title_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]}

    introduction = json_obj["paper_introduction"] if "paper_introduction" in json_obj else " "
    trans_resp = transform_response(client.analyze(introduction))
    response["paper_introduction_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]}

    abstract = json_obj["paper_abstract"] if "paper_abstract" in json_obj else " "
    trans_resp = transform_response(client.analyze(abstract))
    response["paper_abstract_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]}

    conclusions = json_obj["paper_conclusions"] if "paper_conclusions" in json_obj else " "
    trans_resp = transform_response(client.analyze(conclusions))
    response["paper_conclusions_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]}
    
    response["paper_publication_year"] = json_obj["paper_publication_year"] if "paper_publication_year" in json_obj else ""
    response["paper_authors"] = json_obj["paper_authors"]
    response["paper_references"] = json_obj["paper_references"]

    full_response[json_obj_id] = response

    return full_response
