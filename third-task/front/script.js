import axios from 'https://cdn.skypack.dev/axios';

const host = 'localhost:8000';

const dropArea = document.getElementById('drop-area');
const dropAreaText = document.getElementById('drop-area-text');
const fileInput = document.getElementById('file-input');
const resultInsertDiv = document.getElementById('result-insert');
const resultQsDiv = document.getElementById('result-qs');
const inputTitle = document.getElementById('input-keyword-q');
const inputAuthor = document.getElementById('input-author-q');
const autocompleteTitleDiv = document.getElementById('autocomplete-title');
const autocompleteAuthorDiv = document.getElementById('autocomplete-author');

// Evitar comportamiento predeterminado para eventos de arrastrar y soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Manejar el archivo cuando se suelta en el área
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Manejar el archivo cuando se selecciona desde el explorador
fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    handleFiles(files);
});

dropArea.addEventListener('click', () => {
    fileInput.click();
});

function handleFiles(files) {
    for (const file of files) {
        if (file.type === 'application/pdf') {
            updateDropAreaText(file.name);
            uploadFile(file);
        } else {
            alert('Por favor, selecciona un archivo PDF.');
        }
    }
}

function updateDropAreaText(fileName) {
    dropAreaText.textContent = `Archivo seleccionado: ${fileName}`;
}

let currentMetadata = {};

async function uploadFile(file) {
    const url = `http://${host}/add_pdf`;
    const formData = new FormData();
    formData.append('file', file);

    try {
        console.log('Uploading file...');
        const response = await axios.post(url, formData);
        currentMetadata = response.data[Object.keys(response.data)[0]];

        currentMetadata.idno = Object.keys(response.data)[0]
        currentMetadata.paper_downloaded_pdf = response.data[Object.keys(response.data)[0]].paper_downloaded_pdf

        console.log('Success:', response.data);
        displayResult(response.data);
    } catch (error) {
        console.error('Error during file upload:', error);
        alert(`Hubo un error al subir el archivo: ${error.message}`);
        if (error.response) {
            console.log('Error details:', error.response.data);
        }
    }    
}

function displayResult(data) {
    resultInsertDiv.innerHTML = '';
    const paperKey = Object.keys(data)[0]; 
    const paper = data[paperKey];

    const titleSection = document.createElement('div');
    titleSection.className = 'result-section';
    titleSection.innerHTML = `
        <h3>Título</h3>
        <input id="paperTitle" type="text" value="${paper.paper_title}">
        <h3>Fecha de Publicación</h3>
        <input id="publicationDate" type="text" placeholder="Introduce la fecha de publicación del paper (formato YYYY-MM-DD)" value="${paper.paper_publication_date ? paper.paper_publication_date : ''}">
        <h3>Introducción</h3>
        <textarea id="paperIntroduction" placeholder="Introduce una introducción del paper...">${paper.paper_introduction ? paper.paper_introduction : ''}</textarea>
        <h3>Abstract</h3>
        <textarea id="paperAbstract" placeholder="Introduce el abstract del paper...">${paper.paper_abstract}</textarea>
        <h3>Conclusiones</h3>
        <textarea id="paperConclusions" placeholder="Introduce una conclusión del paper...">${paper.paper_conclusions ? paper.paper_conclusions : ''}</textarea>
        <h3>Keywords</h3>
        <input id="paperKeywords" type="text" placeholder="Introduce palabras clave del paper (separadas por ',')" value="${paper.paper_keywords ? paper.paper_keywords : ''}">
    `;
    resultInsertDiv.appendChild(titleSection);

    const authorsSection = document.createElement('div');
    authorsSection.className = 'result-section';
    authorsSection.innerHTML = '<h3>Autores del Paper</h3>';

    let authorCount = 1; // Inicia un contador para numerar a los autores
    paper.paper_authors.forEach(author => {
        const authorDiv = document.createElement('div');
        authorDiv.className = 'author-section';
        authorDiv.innerHTML = `
            <h4>Autor ${authorCount}</h4>
            <div class="name-section">
                <input id="authorForename${authorCount}" type="text" placeholder="Nombre" value="${author.paper_author_forename}">
                <input id="authorSurname${authorCount}" type="text" placeholder="Apellido" value="${author.paper_author_surname}">
                <input id="authorEmail${authorCount}" type="text" placeholder="Email" value="${author.paper_author_email}">
                <input id="authorAffiliation${authorCount}" type="text" placeholder="Afiliación" value="${author.paper_author_affiliation}">
            </div>
            <div class="address-section">
                <input id="authorAddress${authorCount}" type="text" placeholder="Dirección" value="${author.paper_author_address_line}">
                <input id="authorPostCode${authorCount}" type="text" placeholder="Código Postal" value="${author.paper_author_post_code}">
                <input id="authorCity${authorCount}" type="text" placeholder="Ciudad" value="${author.paper_author_settlement}">
                <input id="authorCountry${authorCount}" type="text" placeholder="País" value="${author.paper_author_country}">
            </div>
        `;
        authorsSection.appendChild(authorDiv);
        authorCount++;
    });
    resultInsertDiv.appendChild(authorsSection);

    if (paper) {
        document.getElementById('submit-btn').style.display = 'block';
        document.getElementById('result-insert').style.display = 'block';
        document.getElementById('proximity-recommend-btn').style.display = 'block';
        document.getElementById('author-recommend-btn').style.display = 'block';
        document.getElementById('author-recommend-btn').style.display = 'block';
        document.getElementById('execute-q-btn').style.display = 'none';
        document.getElementById('h2-keyword-q').style.display = 'none';
        document.getElementById('input-keyword-q').style.display = 'none';
        document.getElementById('h2-author-q').style.display = 'none';
        document.getElementById('input-author-q').style.display = 'none';
        document.getElementById('result-qs').style.display = 'none';
        autocompleteTitleDiv.style.display = 'none';
        autocompleteAuthorDiv.style.display = 'none';
    }
}

const submitBtn = document.getElementById('submit-btn');

submitBtn.addEventListener('click', async () => {
    try {
        console.log('Enviando información al servidor...');
        const payload = {
            [currentMetadata.idno]: {
                paper_title: document.getElementById('paperTitle').value,
                paper_publication_date: document.getElementById('publicationDate').value,
                paper_introduction: document.getElementById('paperIntroduction').value,
                paper_abstract: document.getElementById('paperAbstract').value,
                paper_conclusions: document.getElementById('paperConclusions').value,
                paper_keywords: document.getElementById('paperKeywords').value,
                paper_downloaded_pdf: currentMetadata.paper_downloaded_pdf,
                paper_authors: Array.from(document.querySelectorAll('.author-section')).map((section, index) => ({
                    paper_author_forename: document.getElementById(`authorForename${index + 1}`).value,
                    paper_author_surname: document.getElementById(`authorSurname${index + 1}`).value,
                    paper_author_email: document.getElementById(`authorEmail${index + 1}`).value,
                    paper_author_affiliation: document.getElementById(`authorAffiliation${index + 1}`).value,
                    paper_author_address: document.getElementById(`authorAddress${index + 1}`).value,
                    paper_author_post_Code: document.getElementById(`authorPostCode${index + 1}`).value,
                    paper_author_city: document.getElementById(`authorCity${index + 1}`).value,
                    paper_author_country: document.getElementById(`authorCountry${index + 1}`).value
                })),
                paper_references: currentMetadata.paper_references // Asume que 'currentMetadata' tiene los datos correctos
            }
        };

        const response = await axios.post(`http://${host}/insert_data`, payload);
        console.log('Respuesta recibida:', response.data);
        alert('Datos enviados exitosamente!');
    } catch (error) {
        console.error('Error al enviar datos:', error);
        alert(`Error al enviar datos: ${error.message}`);
    }
});

let q_type = '';
let previousContent = '';

document.getElementById('proximity-recommend-btn').addEventListener('click', () => {
    displayInputField("cercanía");
});

document.getElementById('author-recommend-btn').addEventListener('click', () => {
    displayInputField("autor");
});

document.getElementById('execute-q-btn').addEventListener('click', async () => {
    await executeQuery(q_type);
});

async function getRecommendationsByKeywords(paperTitle) {
    const url = `http://${host}/recommendations/${paperTitle}`;
    try {
        const response = await axios.get(url);
        return response.data; // Retorno los datos obtenidos
    } catch (error) {
        console.error('Error when getting data:', error);
        throw error; // Propagación del error para manejo externo
    }    
}

async function getRecommendationsByAuthor(author) {
    const url = `http://${host}/by_author/${author}`;
    try {
        const response = await axios.get(url);
        return response.data; // Retorno los datos obtenidos
    } catch (error) {
        console.error('Error when getting data:', error);
        throw error; // Propagación del error para manejo externo
    }    
}

function displayInputField(type) {
    if (type === "cercanía") {
        q_type = type
        document.getElementById('h2-author-q').style.display = 'none';
        document.getElementById('input-author-q').style.display = 'none';
        document.getElementById('result-insert').style.display = 'none';
        document.getElementById('result-qs').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
        autocompleteTitleDiv.style.display = 'none';
        autocompleteAuthorDiv.style.display = 'none';

        document.getElementById('h2-keyword-q').style.display = 'block';
        document.getElementById('input-keyword-q').style.display = 'block';
    } else if (type === "autor") {
        q_type = type
        document.getElementById('h2-keyword-q').style.display = 'none';
        document.getElementById('input-keyword-q').style.display = 'none';
        document.getElementById('result-insert').style.display = 'none';
        document.getElementById('result-qs').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
        autocompleteTitleDiv.style.display = 'none';
        autocompleteAuthorDiv.style.display = 'none';

        document.getElementById('h2-author-q').style.display = 'block';
        document.getElementById('input-author-q').style.display = 'block';
    }
    
    document.getElementById('execute-q-btn').style.display = 'block';
}

async function executeQuery(type) {
    try {
        if (type === "cercanía") {
            const keyword = document.getElementById('input-keyword-q').value;
            const data = await getRecommendationsByKeywords(keyword);
            displayKeywordsQuery(data);
        } else if (type === "autor") {
            const author = document.getElementById('input-author-q').value;
            const data = await getRecommendationsByAuthor(author);
            console.log(data);
            displayAuthorQuery(data);
        }
    } catch (error) {
        alert(`Error al realizar la consulta: ${error.message}`);
    }
}

async function displayKeywordsQuery(data) {
    document.getElementById('result-qs').style.display = 'block';
    resultQsDiv.innerHTML = '';
    const resultSection = document.createElement('div');
    resultSection.id = 'q-result-section-keywords';
    await data.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-section';
        resultDiv.innerHTML = `
            <h3>Título: ${result.paper}</h3>
            <h4>Nivel de cercanía: ${result.sharedKeywordsCount}</h4>
            <h4>Palabras clave compartidas:</h4>
            <ul>
                ${result.sharedKeywordNames.map(keyword => `<li>${keyword}</li>`).join('')}
            </ul>
            <button class="detail-btn" data-title="${(result.paper).toLowerCase().replace(/ /g, '_')}">Ver Detalle</button>
        `;
        resultSection.appendChild(resultDiv);
    });
    resultQsDiv.appendChild(resultSection);
    previousContent = resultQsDiv.innerHTML;
    addDetailButtonEventListeners();
}

async function displayAuthorQuery(data) {
    document.getElementById('result-qs').style.display = 'block';
    resultQsDiv.innerHTML = '';
    const resultSection = document.createElement('div');
    resultSection.id = 'q-result-section-authors';
    await data.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-section';
        let pdfAvailable = result.downloaded_pdf ? `<h4>PDF Disponible: ${result.downloaded_pdf}</h4>` : ''; // Muestra el h4 solo si downloaded_pdf no es null
        resultDiv.innerHTML = `
            <h3>Título: ${result.title}</h3>
            ${pdfAvailable}
            <button class="detail-btn" data-title="${(result.title).toLowerCase().replace(/ /g, '_')}">Ver Detalle</button>
        `;
        resultSection.appendChild(resultDiv);
    });
    resultQsDiv.appendChild(resultSection);
    previousContent = resultQsDiv.innerHTML;
    addDetailButtonEventListeners();
}

function addBackButton() {
    const backButton = document.createElement('button');
    backButton.textContent = "Atrás";
    backButton.onclick = function() {
        resultQsDiv.innerHTML = previousContent;
        addDetailButtonEventListeners(); 
    };
    resultQsDiv.append(backButton);
}

function displayPaperDetails(data) {
    console.log('Paper details:', data);
    resultQsDiv.innerHTML = '';
    const resultSection = document.createElement('div');
    resultSection.id = 'q-result-section-authors';
    const resultDiv = document.createElement('div');
    resultDiv.className = 'result-section';
    let publicationDate = (data.data_properties[0].publication_date != null && data.data_properties[0].publication_date !== "NULL") ? data.data_properties[0].publication_date : 'No disponible';
    let abstract = data.data_properties[0].abstract ? `<h4>Abstract:</h4><p style="text-align: justify;">${data.data_properties[0].abstract}</p>` : '';
    console.log('Authors:', data.authors)
    let authors = (data.authors != [] && data.authors !== undefined) ? `<ul>${data.authors.map(author => `<li>${author}</li>`).join('')}</ul>` : 'No disponible';
    let pdfAvailable = data.data_properties[0].downloaded_pdf ? `<h4>PDF Disponible: ${data.data_properties[0].downloaded_pdf}</h4><button class="download-btn" data-title="${(data.data_properties[0].downloaded_pdf)}">Descargar</button>` : ''; // Muestra el h4 solo si downloaded_pdf no es null
    console.log('Authors:', data.data_properties[0].authors === undefined);
    resultDiv.innerHTML = `
        <h3>Título: ${data.data_properties[0].title}</h3>
        <h4>Fecha de Publicación: ${publicationDate}</h4>
        ${abstract}
        <h4>Autores:</h4>
        ${authors}
        ${pdfAvailable}
    `;
    resultSection.appendChild(resultDiv);
    resultQsDiv.appendChild(resultSection);
    addDownloadButtonEventListeners();
    addBackButton();
}

async function getPaperDetails(title) {
    const url = `http://${host}/by_paper/${title}`;
    try {
        const response = await axios.get(url);
        displayPaperDetails(response.data);
    } catch (error) {
        console.error('Error when getting data:', error);
        alert(`Error al obtener detalles del paper: ${error.message}`);
    }
}

async function downloadPdf(title) {
    const url = `http://${host}/download_pdf/${title}`;
    try {
        console.log('Downloading PDF...');
        const response = await axios.get(url, { responseType: 'blob' });
        const url_w = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url_w;
        link.setAttribute('download', `${title}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
    } catch (error) {
        console.error('Error during PDF download:', error);
        alert(`Error al descargar el PDF: ${error.message}`);
    }
}

function addDetailButtonEventListeners() {
    const buttons = document.querySelectorAll('.detail-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const title = this.getAttribute('data-title');
            console.log('Paper title:', title);
            getPaperDetails(title);
        });
    });
}

function addDownloadButtonEventListeners() {
    const buttons = document.querySelectorAll('.download-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const title = this.getAttribute('data-title');
            console.log('Paper title:', title);
            downloadPdf(title.replace('%2', '"'));
        });
    });
}

inputTitle.addEventListener('input', () => fetchSuggestions(inputTitle.value, 'paper'));
inputAuthor.addEventListener('input', () => fetchSuggestions(inputAuthor.value, 'author'));

async function fetchSuggestions(query, type) {
    if (query.length < 3) { // Comienza a buscar solo después de 3 caracteres para evitar demasiadas peticiones
        if (type === 'title') {
            autocompleteTitleDiv.style.display = 'none';
        } else {
            autocompleteAuthorDiv.style.display = 'none';
        }
        return;
    }

    const url = `http://${host}/autocomplete/${type}/${query}`;
    console.log('Fetching suggestions:', url);
    try {
        const response = await axios.get(url);
        displaySuggestions(response.data, type);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}

function displaySuggestions(suggestions, type) {
    let suggestionsDiv = type === 'paper' ? autocompleteTitleDiv : autocompleteAuthorDiv;
    console.log('Suggestions:', suggestions);
    console.log('Suggestions:', suggestionsDiv);
    suggestionsDiv.innerHTML = '';
    suggestionsDiv.style.display = 'block';
    suggestions.forEach(suggestion => {
        const div = document.createElement('div');
        div.textContent = suggestion.name;
        div.className = 'autocomplete-item';
        div.addEventListener('click', () => {
            if (type === 'paper') {
                inputTitle.value = suggestion.uri;
            } else {
                inputAuthor.value = suggestion.uri;
            }
            suggestionsDiv.style.display = 'none';
        });
        suggestionsDiv.appendChild(div);
    });
}
