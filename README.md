# Semantic Web Project

This project is divided in three main tasks.
- **Task 1**: Get academic paper related data from different data sources and extract all the metadata possible.
- **Task 2**: Create a knowledge graph with the data extracted in Task 1.
- **Task 3**: Create a web application that allows users to query the knowledge graph created in Task 2 and get specific PDFs.

## Task 1
We divided this task in two subtasks:
- **Subtask 1.1**: Get academic paper related data from different data sources (i.e. Academic Scholar API).
- **Subtask 1.2**: Extract all the metadata possible from the data obtained in Subtask 1.1. using tools like GROBID.

### Subtask 1.1
We used the Academic Scholar API to get academic paper related data. We used the following query to get the data.

To run the code, first you need to install the required libraries. You can do this by running the following command:

```pip install -r requirements.py``` 

This will install all the required libraries for all the tasks.

After installing the required libraries, you can start by going into the `/semantic-web/first-task/pdf-downloader/` directory. There, you'll find four main python scripts:
- `main.py`: Runs all the code in the correct order.
- `requester.py`: Does all the requests to the Academic Scholar API.
- `logic.py`: Has the logic to verify the existence of papers and its attributes.
- `utils.py`: We'll use this script in the second task.

To run the code, you can use the following command:

```
cd first-task/pdf-downloader
python main.py
```

And it will start doing the requests and downloading the PDFs. Important to note: at the beginnig of each file, there will be some variables with specific paths. You can change them to your specific paths.

### Subtask 1.2
Now that we have a big number of PDFs, we can start extracting metadata from them. We used GROBID to extract the metadata.

To run the code, first you need to install scipdf_parser and the model. You can do this by running the following commands:

```
pip install git+https://github.com/titipata/scipdf_parser
python -m spacy download en_core_web_sm
```

Now, we have to start the GROBID server. You can do this by running the following command:

```
docker-compose up -d
```

With the server up and running, we can run the actual code!

In the `pdf-info-extractor` directory, you'll find the following files:
- `main.py`: Runs all the code in the correct order.
- `xml_analyzer.py`: Analyzes the XML files generated by GROBID.
- `extractor.py`: Creates the JSON file with the metadata extracted.
- `webscraper.py`: Automation of what you would do manually in the GROBID website. (We do not use this file. It was part of the starting test-phase of the project. We left it to show the evolution of the project)

To run the code, you can use the following command:

```
cd first-task/pdf-downloader
python main.py
```

And it will start analyzing the XML files and creating the JSON file with the metadata extracted. Important to note: at the beginnig of each file, there will be some variables with specific paths. You can change them to your specific paths.

## Task 2
We divided this task in three subtasks:
- **Subtask 2.1**: Adjust the metadata from the previous task.
- **Subtask 2.2**: Use TextRazor to get the entities and keywords from each text in each paper.
- **Subtask 2.3**: Model all classes and properties, and instances.

### Subtask 2.1
After presenting the first task, we realized we weren't sure of the number of referenced papers we had downloaded. So, we implemented a quick function that get a list of every referenced paper from each paper in the JSON and does a request for its PDF (if able, it downloads it).

You can find that code in `/semantic-web/first-task/pdf-downloader/utils.py`.

With this process, we managed to get more or less 2000 more PDFs.

### Subtask 2.2
With a more complete metadata, the next step was using tools like TextRazor to get keywords from the introduction, abstract and conclusion of each paper.

If you go into the `/semantic-web/second-task/text-analytics/` directory, you'll find three files:

- `main.py`: Runs all the code in the correct order.
- `text_analytics.py`: Gets the keywords and entities for each paper and updates the JSON metadata file.
- `utis.py`: File with data cleaning processes.

To run the code, you can use the following command:

```
cd second-task/text-analytics
python main.py
```

And the requests to TextRazor will begin. This will update the JSON metadata file. The data cleaning processes must be executed next with the following command:

```
python utils.py
```

### Subtask 2.3
Lastly, we have to model all the classes and properties to fully duplicate the natural rules of the metadata we collected.

You can find the ontology RDF file in `/semantic-web/second-task/rdf-model/rdf_definition.ipynb`. In that file, you'll find the ontology model, the instances and some SPARQL and CYPHER (neo4j) queries. We recommend to download the RDF files (`/semantic-web/second-task/rdf-model/rdf-files`) and not no fully execute the Notebook. This, because the OWL inference closure function after loading the instances can take 60 minutes to finish.

In the `/semantic-web/second-task/rdf-model/semantic_instances_only.txt` file there's a link to a Google Drive folder. There, you'll the find JSON with all the metadata, both .rdf files (ontology and instances) and the neo4j database dump.

## Task 3
We divided this task in four subtasks:
- **Subtask 3.1**: Create a Neo4j database with the ontology and instances.
- **Subtask 3.2**: Build a FastAPI that can query the ontology and insert triples. This implies the data quality verification usign SHACL.
- **Subtask 3.3**: Create a web application that allows users to query the ontology created in Task 2 and get specific PDFs. Also, it should let users insert a new PDF and the gotten triples into the ontology.
- **Subtask 3.4**: Improve the web application so that it shows visualizations of the data.

### Subtask 3.1

In this first subtask, we created a Neo4j database with the ontology and instances. You can find the database dump in the Google Drive folder linked in the `semantic_instances_only.txt` file.

To run the database, we used a Docker container. You can run the following command to start the container:

```
sudo docker run -it --rm   --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs --user="$(id -u):$(id -g)"   -e NEO4J_AUTH=none   --env NEO4J_PLUGINS='["apoc","n10s"]'   neo4j:5.5.0
```

If there is a problem, run these two commands:
```
sudo chmod 777 $HOME/neo4j/logs
sudo chmod 777 $HOME/neo4j/data
```

**Note:** Although the dump exists, if you want to load the rdf files into the database, you can use the following commands once you enter `localhost:7474`:

```
CALL n10s.graphconfig.init({handleRDFTypes:"LABELS_AND_NODES"});

CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE

CALL n10s.rdf.import.fetch("file:/data/ontology_instances.rdf","RDF/XML");
```

Of course, the rdf file should be in the `/data/` directory of neo4j.

### Subtask 3.2

Once the database is up and running, we can run the API. You can find the main file in the `/semantic-web/third-task/api/` directory. There, you'll find the following files:

- `main.py`: Runs the FastAPI server.
- `db.py`: Has the connection to the Neo4j database and all the queries.
- `shacl.py`: Has the SHACL validation functions.
- `pdf_processor.py`: Has the functions to process the PDFs using GROBID.
- `gdrive.py`: Has the functions to download and insert PDFs from and to Google Drive.

To run the API, first you need to run the GROBID Docker container. You can do this by running the following command (standing on root directory):

```
docker-compose up -d
```

Now, to run the API:

```
cd third-task/api
uvicorn main:app --reload
```

### Subtask 3.3

With the API running, we can now run the web application. You can find the main file in the `/semantic-web/third-task/front/` directory. There, you'll also find the following files:

- `script.js`: Has the functions to interact with the API.
- `index.html`: The main HTML file.
- `style.css`: The CSS file.

To run the web application, you can use the following commands:

First, make sure to have all the required dependencies:

```
npm install
```

Then, run the application:

```
cd third-task/front
npm start
```

A new tab will open in your browser with the web application.

That's it! Now you can interact with the web application and the API!

### Subtask 3.4

In this subtask, we improved the web application so that it shows visualizations of the data. You can find the visualizations in the `/semantic-web/third-task/front/` directory. There, you'll find the following files:

- `visualization.js`: The functions to create the visualizations.
- `visualization.html`: The HTML file for the visualizations.

To see the visualizations, click on the "Visualizaciones" button in the web application (top left corner). There should be two bubble charts: one with the distribution of the number of papers that have a keyword and another with the top 10 most related keywords (the keywords that appear more times together).
