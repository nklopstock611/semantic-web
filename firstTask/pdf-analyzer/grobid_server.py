from grobid_client.grobid_client import GrobidClient

if __name__ == "__main__":
    pdf_file = 'SSDBM09_PTS'
    client = GrobidClient(config_path="./config.json")
    client.process("processFulltextDocument", f"/workspaces/semantic-web/entregaUno/pdfs/{pdf_file}.pdf", output=f"/workspaces/semantic-web/entregaUno/pdfs/{pdf_file}-out/", consolidate_citations=True, tei_coordinates=True, force=True)
