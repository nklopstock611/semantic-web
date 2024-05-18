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

async function uploadFile(file) {
    const url = 'http://localhost:8000/add_pdf';
    const formData = new FormData();
    formData.append('file', file);

    try {
        console.log('Uploading file...');
        const response = await axios.post(url, formData);
        
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
    const paperKey = Object.keys(data)[0];  // Tomar la primera clave del objeto recibido
    const paper = data[paperKey];

    // Crear sección para el título del paper
    const titleSection = document.createElement('div');
    titleSection.className = 'result-section';
    titleSection.innerHTML = `
        <h3>Título del Paper</h3>
        <input type="text" value="${paper.paper_title}">
    `;
    resultDiv.appendChild(titleSection);

    // Crear sección para los autores del paper
    const authorsSection = document.createElement('div');
    authorsSection.className = 'result-section';
    authorsSection.innerHTML = `<h3>Autores del Paper</h3>`;

    let authorCount = 1; // Inicia un contador para numerar a los autores
    paper.paper_authors.forEach(author => {
        const authorData = author;
        const authorDiv = document.createElement('div');
        authorDiv.className = 'author-section';

        const nameSection = document.createElement('div');
        nameSection.className = 'name-section';
        nameSection.innerHTML = `
            <h4>Autor ${authorCount}</h4>
            <input type="text" placeholder="Nombre" value="${authorData.paper_author_forename}">
            <input type="text" placeholder="Apellido" value="${authorData.paper_author_surname}">
            <input type="email" placeholder="Email" value="${authorData.paper_author_email}">
            <input type="text" placeholder="Afiliación" value="${authorData.paper_author_affiliation}">
        `;

        const addressSection = document.createElement('div');
        addressSection.className = 'address-section';
        addressSection.innerHTML = `
            <h4>Dirección Autor ${authorCount}</h4>
            <input type="text" placeholder="Dirección" value="${authorData.paper_author_address_line}">
            <input type="text" placeholder="Código Postal" value="${authorData.paper_author_post_code}">
            <input type="text" placeholder="Ciudad" value="${authorData.paper_author_settlement}">
            <input type="text" placeholder="País" value="${authorData.paper_author_country}">
        `;

        authorDiv.appendChild(nameSection);
        authorDiv.appendChild(addressSection);
        authorsSection.appendChild(authorDiv);
        authorCount++; // Incrementa el contador después de agregar cada autor
    });
    resultDiv.appendChild(authorsSection);

}
