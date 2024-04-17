import json
from statistics import mean

metadata_path = '/workspaces/semantic-web/second-task/metadata_keywords_2.json'
seen_pdfs_path = '/workspaces/semantic-web/first-task/pdf-downloader/publication_dates_2.json'

def create_json(metadata: dict) -> None:
    """
    Updates a json file.
    """
    with open(metadata_path, 'r') as f:
        json_dict = json.load(f)

    json_dict.clear()
    json_dict.update(metadata)

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

def transform_seen_pdfs(data_dict: dict) -> dict:
    """
    Transforms the cache of seen PDFs to an easier structure:
    {
        "<paper_downloaded_pdf>": "<paper_title>",
    }
    """
    transformed_seen_pdfs = {}
    for each in data_dict:
        transformed_seen_pdfs[data_dict[each][3]] = each

    return transformed_seen_pdfs

def paper_equals(paper_one: dict, paper_two: dict) -> bool:
    """
    Compares a paper object and the papers from the cache of seen PDFs.
    """
    return (paper_one['paper_downloaded_pdf'] in paper_two), paper_one['paper_downloaded_pdf']

def correct_titles():
    """
    Process to replace None titles or titles with "strange" symbols with the
    actual title.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    with open(seen_pdfs_path, 'r', encoding='utf-8') as f:
        seen_pdfs = json.load(f)

    for each_paper in papers_metadata:
        print(papers_metadata[each_paper]['paper_title'])
        transformed_seen_pdfs = transform_seen_pdfs(seen_pdfs)
        same, pdf_file = paper_equals(papers_metadata[each_paper], transformed_seen_pdfs)
        print(same)
        if same:
            papers_metadata[each_paper]['paper_title'] = transformed_seen_pdfs[pdf_file]
            print(papers_metadata[each_paper]['paper_title'])

    create_json(papers_metadata)

def normalize_scores(scores: dict, type: str) -> dict:
    """
    Normalization of the relevance and confidence scores of each entity and topic
    using the Min-Max method.
    """
    if type == 'entities':
        relevance_scores = [entry['relevance_score'] for entry in scores]
        confidence_scores = [entry['confidence_score'] for entry in scores]
    elif type == 'topics':
        relevance_scores = [entry['score'] for entry in scores]

    min_relevance = min(relevance_scores)
    max_relevance = max(relevance_scores)
    if type == 'entities':
        min_confidence = min(confidence_scores)
        max_confidence = max(confidence_scores)

    for entry in scores:
        if type == 'entities':
            entry['relevance_score'] = (entry['relevance_score'] - min_relevance) / (max_relevance - min_relevance)
            entry['confidence_score'] = (entry['confidence_score'] - min_confidence) / (max_confidence - min_confidence)
        elif type == 'topics':
            entry['score'] = (entry['score'] - min_relevance) / (max_relevance - min_relevance)

    return scores

def sort_scores(scores: list, type: str) -> list:
    """
    Sorts the scores of the entities and topics in descending order.
    """
    if type == 'entities':
        scores.sort(key=lambda x: x['relevance_score'], reverse=True)
        # scores.sort(key=lambda x: x['confidence_score'], reverse=True)
    elif type == 'topics':
        scores.sort(key=lambda x: x['score'], reverse=True)

    return scores

def evaluate_scores(scores: list, type: str) -> list:
    """
    entities:
    relevance_score: acceptance range [(mean_relevance - (mean_relevance * 0.1)) -> of the current paper, 0.97]
    confidence_score: acceptance range [(mean_confidence - (mean_confidence * 0.1)) -> of the current paper, 0.97]

    topics:
    relevance_score: acceptance range [(mean_relevance - (mean_relevance * 0.1)) -> of the current paper, 0.97]
    """
    normalized_scores = normalize_scores(scores, type)
    
    if type == 'entities':
        relevance_scores = [entry['relevance_score'] for entry in normalized_scores]
        confidence_scores = [entry['confidence_score'] for entry in normalized_scores]
    elif type == 'topics':
        relevance_scores = [entry['score'] for entry in normalized_scores]

    mean_relevance = mean(relevance_scores)
    if type == 'entities':
        mean_confidence = mean(confidence_scores)
    
    for entry in normalized_scores:
        if type == 'entities':
            if (entry['relevance_score'] > 0.97 or entry['relevance_score'] < (mean_relevance - (mean_relevance * 0.1))):
                normalized_scores.remove(entry)
        elif type == 'topics':
            if (entry['score'] > 0.97 or entry['score'] < (mean_relevance - (mean_relevance * 0.1))):
                normalized_scores.remove(entry)

    if type == 'entities':
        normalized_scores = sort_scores(normalized_scores, type)
    elif type == 'topics':
        normalized_scores = sort_scores(normalized_scores, type)

    return normalized_scores

def scores_evaluation():
    """
    Process to evaluate each score of each entity in a given TextRazor response.
    Remove the entities that do not match the defined parameters.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    for each_paper in papers_metadata:
        entities = papers_metadata[each_paper]['paper_key_words']['entities']
        topics = papers_metadata[each_paper]['paper_key_words']['topics']

        papers_metadata[each_paper]['paper_key_words']['entities'] = evaluate_scores(entities, 'entities')
        papers_metadata[each_paper]['paper_key_words']['topics'] = evaluate_scores(topics, 'topics')
        break

if __name__ == "__main__":
    # correct_titles()
    scores_evaluation()
