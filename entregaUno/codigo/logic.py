import os
import extractor as extr

def verify_paper_object(author_name: str, paper_name: str, paper_year: int) -> tuple:
    """
    Verifies if paper_name has an object associated with author_name.
    """
    author_name_tuple = (author_name[0], author_name[2:]) # author name format: "<name initial>\s<full last name>"
    authors = extr.get_papers_from_author(author_name_tuple)
    
    for each_author in authors:
        papers_list = each_author['papers']
        for each_paper in papers_list:
            if each_paper['title'] == paper_name and each_paper['year'] == paper_year:
                return (paper_name, each_paper['paperId'], each_paper['year'])

    return None

def get_pdf_link(author_name: str, paper_name: str, paper_year: int) -> str:
    """
    If it exists, returns the link to the pdf of the paper.
    """
    paper_id = verify_paper_object(author_name, paper_name, paper_year)[1]
    if paper_id:
        paper = extr.get_paper(paper_id)
        if paper['isOpenAccess']:
            return paper['openAccessPdf']
        else:
            return None
    else:
        return None

def download_pdf(author_name: str, paper_name: str, paper_year: int) -> None:
    """
    Downloads the pdf of the paper.
    """
    pdf_link = get_pdf_link(author_name, paper_name, paper_year)
    if pdf_link:
        filepath = os.path.join('./pdfs', os.path.basename(pdf_link))
        with open(filepath, 'wb') as f:
            f.write(extr.requests.get_pdf(pdf_link).content)
    else:
        return None
