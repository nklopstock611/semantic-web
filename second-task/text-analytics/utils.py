import re
import json
from statistics import mean

metadata_path = '/semantic-web/second-task/metadata_keywords_2.json'
seen_pdfs_path = '/semantic-web/first-task/pdf-downloader/publication_dates_2.json'

pattern = r'^[A-Za-z0-9 !@#$%^&*()_+\-=\[\]\{\};:"\\|,.<>\/?]*$'
pattern_replace = r'[^A-Za-z0-9]'
pattern_kewords = r'[^A-Za-z]'

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

def delete_specific_papers(papers: list) -> None:
    """
    Process to delete specific papers from the metadata.
    There are some examples of papers with references that do not make sense:
    Example: "reference_paper_country": " pages 1{17"
    We need to remove these papers from the metadata.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    for each_paper in papers:
        try:
            print('DELETING:', papers_metadata[each_paper]['paper_title'])
            papers_metadata.pop(each_paper)
        except KeyError:
            print('Key not found in dictionary')

    create_json(papers_metadata)

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

def contains_only_accented_or_ascii(title: str) -> bool:
    return bool(re.match(pattern, title))

def replace_in() -> None:
    """
    Process to replace some characters like whitespaces or other symbols.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    keys_to_remove = []

    for each_paper in papers_metadata:
        papers_metadata[each_paper]['paper_title'] = re.sub(pattern_replace, '_', papers_metadata[each_paper]['paper_title'])
        print('REPLACING', papers_metadata[each_paper]['paper_title'])
        if papers_metadata[each_paper]['paper_title'] == '':
            keys_to_remove.append(each_paper)

        papers_metadata[each_paper]['paper_introduction'] = re.sub(pattern_replace, '_', papers_metadata[each_paper]['paper_introduction'])
        papers_metadata[each_paper]['paper_abstract'] = re.sub(pattern_replace, '_', papers_metadata[each_paper]['paper_abstract'])
        papers_metadata[each_paper]['paper_conclusions'] = re.sub(pattern_replace, '_', papers_metadata[each_paper]['paper_conclusions'])

        for each_author in papers_metadata[each_paper]['paper_authors']:
            each_author['paper_author_forename'] = re.sub(pattern_replace, '_', each_author['paper_author_forename'])
            each_author['paper_author_surname'] = re.sub(pattern_replace, '_', each_author['paper_author_surname'])
            each_author['paper_author_affiliation'] = re.sub(pattern_replace, '_', each_author['paper_author_affiliation'])
            each_author['paper_author_address_line'] = re.sub(pattern_replace, '_', each_author['paper_author_address_line'])
            each_author['paper_author_post_code'] = re.sub(pattern_replace, '_', each_author['paper_author_post_code'])
            each_author['paper_author_settlement'] = re.sub(pattern_replace, '_', each_author['paper_author_settlement'])
            each_author['paper_author_country'] = re.sub(pattern_replace, '_', each_author['paper_author_country'])

        for each_reference in papers_metadata[each_paper]['paper_references']:
            each_reference['reference_paper_title'] = re.sub(pattern_replace, '_', each_reference['reference_paper_title'])
            print('REPLACING', each_reference['reference_paper_title'])
            if each_reference['reference_paper_title'] == '':
                keys_to_remove.append(each_paper)

            for each_author in each_reference['reference_paper_authors']:
                each_author['reference_paper_author_forename'] = re.sub(pattern_replace, '_', each_author['reference_paper_author_forename'])
                each_author['reference_paper_author_surname'] = re.sub(pattern_replace, '_', each_author['reference_paper_author_surname'])

            each_reference['reference_paper_city'] = re.sub(pattern_replace, '_', each_reference['reference_paper_city'])
            each_reference['reference_paper_country'] = re.sub(pattern_replace, '_', each_reference['reference_paper_country'])
            each_reference['reference_paper_meeting'] = re.sub(pattern_replace, '_', each_reference['reference_paper_meeting'])
            each_reference['reference_paper_note'] = re.sub(pattern_replace, '_', each_reference['reference_paper_note'])

        for each_keyword in papers_metadata[each_paper]['paper_key_words']['entities']:
            if type(each_keyword) != str or re.search(r'\d', each_keyword):
                print('EACH KEYWORD:', each_keyword)
                papers_metadata[each_paper]['paper_key_words']['entities'].remove(each_keyword)
            else:
                each_keyword = re.sub(pattern_replace, '_', each_keyword)

    # removes the papers with empty titles
    try:
        for key in keys_to_remove:
            papers_metadata.pop(key)
    except KeyError:
        print('Key not found in dictionary')

    create_json(papers_metadata)        

def correct_titles() -> None:
    """
    Process to replace None titles or titles with "strange" symbols with the
    actual title.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    with open(seen_pdfs_path, 'r', encoding='utf-8') as f:
        seen_pdfs = json.load(f)

    keys_to_remove = []

    for each_paper in papers_metadata:
        ascii = contains_only_accented_or_ascii(papers_metadata[each_paper]['paper_title'])
        if ascii:
            print(papers_metadata[each_paper]['paper_title'])
            transformed_seen_pdfs = transform_seen_pdfs(seen_pdfs)
            same, pdf_file = paper_equals(papers_metadata[each_paper], transformed_seen_pdfs)
            print(same)
            if same:
                papers_metadata[each_paper]['paper_title'] = transformed_seen_pdfs[pdf_file]
                print(papers_metadata[each_paper]['paper_title'])
        else:
            print('Title with strange symbols:', papers_metadata[each_paper]['paper_title'])
            keys_to_remove.append(each_paper)

    # removes the papers with "strange" symbols (not ASCII except accented characters)
    for key in keys_to_remove:
        papers_metadata.pop(key)

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

    if relevance_scores:
        min_relevance = min(relevance_scores)
        max_relevance = max(relevance_scores)
    if type == 'entities' and confidence_scores:
        min_confidence = min(confidence_scores)
        max_confidence = max(confidence_scores)

    if relevance_scores:
        for entry in scores:
            if type == 'entities':
                entry['relevance_score'] = (entry['relevance_score'] - min_relevance) / (max_relevance - min_relevance) if (max_relevance - min_relevance) != 0 else 0
                entry['confidence_score'] = (entry['confidence_score'] - min_confidence) / (max_confidence - min_confidence) if (max_relevance - min_relevance) != 0 else 0
            elif type == 'topics':
                entry['score'] = (entry['score'] - min_relevance) / (max_relevance - min_relevance) if (max_relevance - min_relevance) != 0 else 0

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

def get_names(scores: list, type: str) -> list:
    """
    Get the names of the entities and topics.
    """
    names = []
    if type == 'entities':
        for entry in scores:
            names.append(entry['id'])
    elif type == 'topics':
        for entry in scores:
            names.append(entry['label'])

    return names

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

    if relevance_scores:
        mean_relevance = mean(relevance_scores)
    if type == 'entities' and confidence_scores:
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

    names_list = get_names(normalized_scores, type)
    return names_list

def scores_evaluation() -> None:
    """
    Process to evaluate each score of each entity in a given TextRazor response.
    Remove the entities that do not match the defined parameters.
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        papers_metadata = json.load(f)

    for each_paper in papers_metadata:
        print('Evaluating Scores From', papers_metadata[each_paper]['paper_title'])

        entities = papers_metadata[each_paper]['paper_key_words']['entities']
        topics = papers_metadata[each_paper]['paper_key_words']['topics']

        papers_metadata[each_paper]['paper_key_words']['entities'] = evaluate_scores(entities, 'entities')
        papers_metadata[each_paper]['paper_key_words']['topics'] = evaluate_scores(topics, 'topics')

    create_json(papers_metadata)

if __name__ == "__main__":
    delete_specific_papers([
                            '2C126818AC116F9229A1B6F1705FF56F',
                            'A1D7BC7612D1AE54F075431D0521C87C',
                            'F5F0EECA59C37FD5B4CBBAA386A759D8',
                            'A17BCC590445D275508799CE4CFF45D4',
                            '97EBC19FDB76FAC13FC665366529CAE5',
                            '9DB8F5ED3A070C46E65DEFADC098484A',
                            '92E6E63A8B6FEF1361F1015BF50A253F',
                            '176B0BCE26DB2F2BE3B4F462E1B937B7',
                            '881C2D9AAB190A909FF6A90ED51858E2',
                            'D2DCBFBC986D62AAD9B95B7416C9842D',
                            'E18DA4CF2B1BE338072B0F2CC5D0C853'
    ])
    correct_titles()
    scores_evaluation()
    replace_in()
