import json
import textrazor
import urllib

credentials_path = '/home/estudiante/semantic-web/credentials.json'

with open(credentials_path, "r") as f:
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
    trans_resp = None
    full_response = {}
    response = {}
    response["paper_id"] = json_obj_id

    response["paper_downloaded_pdf"] = json_obj["paper_downloaded_pdf"]

    try:
        title = json_obj["paper_title"] if "paper_title" in json_obj else ""
        introduction = json_obj["paper_introduction"] if "paper_introduction" in json_obj else ""
        abstract = json_obj["paper_abstract"] if "paper_abstract" in json_obj else ""
        conclusions = json_obj["paper_conclusions"] if "paper_conclusions" in json_obj else ""
        
        # response["paper_title"] = title if title is not None else 'N/A'
        # if title != 'N/A':
        #     trans_resp = transform_response(client.analyze(title))
        # response["paper_title_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]} if trans_resp is not None else None

        # introduction = json_obj["paper_introduction"] if "paper_introduction" in json_obj else "N/A"
        # if introduction != 'N/A':
        #     trans_resp = transform_response(client.analyze(introduction))
        # response["paper_introduction_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]} if trans_resp is not None else None

        # abstract = json_obj["paper_abstract"] if "paper_abstract" in json_obj else "N/A"
        # if abstract != 'N/A':
        #     trans_resp = transform_response(client.analyze(abstract))
        # response["paper_abstract_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]} if trans_resp is not None else None

        # conclusions = json_obj["paper_conclusions"] if "paper_conclusions" in json_obj else "N/A"
        # if conclusions != 'N/A':
        #     trans_resp = transform_response(client.analyze(conclusions))
        # response["paper_conclusions_data"] = {"entities": trans_resp[0], "topics": trans_resp[1]} if trans_resp is not None else None
        
        response["paper_title"] = title
        response["paper_introduction"] = introduction
        response["paper_abstract"] = abstract
        response["paper_conclusions"] = conclusions
        
        text_to_analyze = title + '\n' + introduction + '\n' + abstract + '\n' + conclusions
        trans_resp = transform_response(client.analyze(text_to_analyze))
        response["paper_key_words"] = {"entities": trans_resp[0], "topics": trans_resp[1]}

        response["paper_publication_year"] = json_obj["paper_publication_year"] if "paper_publication_year" in json_obj else ""
        response["paper_authors"] = json_obj["paper_authors"]
        response["paper_references"] = json_obj["paper_references"]

        full_response[json_obj_id] = response
    except AttributeError:
        print("ERROR: Paper with no title!?")
    except urllib.error.HTTPError:
        print("ERROR: HTTP 400 Code")
    except textrazor.TextRazorAnalysisException:
        print('ERROR: TextRazor returned HTTP Code 400')
    

    return full_response

