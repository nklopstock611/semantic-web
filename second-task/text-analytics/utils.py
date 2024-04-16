import json

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

def main():
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
        
if __name__ == "__main__":
    main()