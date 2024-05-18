import axios from 'https://cdn.skypack.dev/axios';

const dropArea = document.getElementById('drop-area');
const dropAreaText = document.getElementById('drop-area-text');
const fileInput = document.getElementById('file-input');
const resultDiv = document.getElementById('result');

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
    const url = 'http://localhost:8000/add_pdf';
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
    resultDiv.innerHTML = '';
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
    resultDiv.appendChild(titleSection);

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
    resultDiv.appendChild(authorsSection);

    if (paper) {
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.style.display = 'block';
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

        const response = await axios.post('http://localhost:8000/insert_data', payload);
        console.log('Respuesta recibida:', response.data);
        alert('Datos enviados exitosamente!');
    } catch (error) {
        console.error('Error al enviar datos:', error);
        alert(`Error al enviar datos: ${error.message}`);
    }
});
