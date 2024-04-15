import os
import json
import requester as reqr

pdf_path = '/semantic-web/firstTask/pdf-downloader/pdfs/'

def save_data_in_json(data: dict, file_path: str='publication_dates_2.json'):
    """
    Saves data in publication_dates.json file.
    """
    try:
        with open(file_path, 'r') as f:
            json_dict = json.load(f)
    except FileNotFoundError:
        json_dict = {}

    json_dict.update(data)

    with open(file_path, 'w') as f:
        json.dump(json_dict, f, indent=4)

def verify_paper_object(author_name: str, paper_name: str, paper_year: int) -> tuple:
    """
    Verifies if paper_name has an object associated with author_name.
    """
    author_name_tuple = (author_name[0], author_name[2:]) # author name format: "<name initial>\s<full last name>"
    authors = reqr.get_papers_from_author(author_name_tuple)

    if authors:
        for each_author in authors:
            if each_author:
                papers_list = each_author['papers']
                for each_paper in papers_list:
                    if each_paper['title'] == paper_name:
                        return each_paper['paperId']

    return None

def evaluate_authors(paper: dict) -> str:
    """
    Evaluates the authors of the papers and returns the first instance of the target paper.
    """
    authors = paper['authors']
    if authors:
        for each_author in authors:
            if each_author:
                paper_name = paper['title']
                paper_year = paper['year']
                paper_id = verify_paper_object(each_author, paper_name, paper_year)
                if paper_id:
                    return paper_id

    return None

def get_pdf_link(paper: dict) -> str:
    """
    If it exists, returns the link to the pdf of the paper.
    """
    paper_found = reqr.find_paper(paper['title'])
    if paper_found:
        print(f"Paper: {paper_found['title']}")
        print(f"PDF: {paper_found['isOpenAccess']}")
        if paper_found['isOpenAccess'] and paper_found['openAccessPdf']:
            return paper_found['openAccessPdf']['url']

    return None

def download_pdf(paper: dict) -> None:
    """
    Downloads the pdf of the paper.
    """
    pdf_link = get_pdf_link(paper)
    if pdf_link:
        print(f"Downloading: {pdf_link}")
        save_data_in_json({ paper['title']: [ paper['year'], os.path.basename(pdf_link) ]})
        with open(pdf_path + {os.path.basename(pdf_link)}, 'wb') as f:
            f.write(reqr.get_pdf(pdf_link).content)
    
    return None
