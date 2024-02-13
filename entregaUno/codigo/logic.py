import extractor as extr

def verify_paper_object(author_name: str, paper_name: str, paper_year: int) -> tuple:
    author_name_tuple = (author_name[0], author_name[2:])
    authors = extr.get_papers_from_author(author_name_tuple)
    
    for each_author in authors:
        papers_list = each_author['papers']
        for each_paper in papers_list:
            if each_paper['title'] == paper_name and each_paper['year'] == paper_year:
                return (paper_name, each_paper['paperId'], each_paper['year'])

    return None

# print(verify_paper_object(
#                     'a descamps',
#                     'Enhancer-Driven Gene Expression (EDGE) enables the generation of cell type specific tools for the analysis of neural circuits',
#                     2020
#     )
# )

