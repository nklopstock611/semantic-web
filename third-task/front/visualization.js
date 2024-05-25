import axios from 'https://cdn.skypack.dev/axios';
import * as d3 from "https://cdn.skypack.dev/d3@6";

const host = 'localhost:8000';

document.getElementById('ontology-btn').addEventListener('click', () => {
    window.location.href = 'index.html'; // Asegúrate de tener un archivo 'visualization.html'
});

async function getBubbleVisualizationData() {
    const url = `http://${host}/visualization/keywords_bubble`;
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function getKeywordsConnectionVisualizationData() {
    const url = `http://${host}/visualization/keywords_connection`;
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function createBubbleVisualization() {
    const dataFromServer = await getBubbleVisualizationData();
    const data = dataFromServer.filter(item => item.times > 130);
    const width = window.innerWidth - 35, height = window.innerHeight;

    // Crear SVG y el grupo principal
    const svg = d3.select("#bubbleChart")
        .attr("width", width)
        .attr("height", height);

    const contentGroup = svg.append("g"); // Este es el grupo principal para contenido y zoom

    const zoomHandler = d3.zoom()
        .on("zoom", (event) => {
            contentGroup.attr("transform", event.transform);
        })

    svg.call(zoomHandler);

    const nodes = data.map(d => ({...d, radius: Math.sqrt(d.times) * 5}));

    const simulation = d3.forceSimulation(nodes)
        .force("charge", d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(d => d.radius))
        .on("tick", ticked)
        .on("end", () => initialZoom(contentGroup, svg, width, height));  // Ajustar el zoom inicial después de la simulación

    const node = contentGroup.selectAll(".node")  // Asegúrate de seleccionar desde contentGroup
        .data(nodes)
        .enter().append("g")
        .attr("class", "node");

    node.append("circle")
        .attr("r", d => d.radius)
        .style("fill", d => getColorForValue(d.times));

    node.append("text")
        .text(d => d.keyword)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central")  
        .style("font-size", d => Math.max(10, d.radius / 3) + "px");

    function ticked() {
        node.attr("transform", d => `translate(${d.x},${d.y})`);
    }

    function initialZoom(g, svg, width, height) {
        const bounds = g.node().getBBox(),
              dx = bounds.width,
              dy = bounds.height,
              x = (bounds.x + bounds.width / 2),
              y = (bounds.y + bounds.height / 2),
              scale = 0.9 / Math.max(dx / width, dy / height),
              translate = [width / 2 - scale * x, height / 2 - scale * y];
    
        svg.transition()
            .duration(450)
            .call(zoomHandler.transform, d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale));
    }
}

async function createKeywordsBubbleChart() {
    const dataFromServer = await getKeywordsConnectionVisualizationData();

    // Asignación de coordenadas x, y y tamaño de burbujas
    const data = dataFromServer.map((d, index) => ({
        x: d.keyword_one,
        y: d.keyword_two,
        size: d.sharedPapers,
        label: d.sharedPapers,
    }));

    const width = window.innerWidth - 140, height = 400;
    const margin = { top: 20, right: 20, bottom: 50, left: 120 };  // Ajustar margen izquierdo para mover el gráfico a la derecha

    // Crear SVG
    const svg = d3.select("#networkChart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background-color", "#ffffff")  // Fondo blanco
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Escalas
    const xScale = d3.scalePoint()
        .domain(data.map(d => d.x))
        .range([50, width - 50])
        .padding(0.5);

    const yScale = d3.scalePoint()
        .domain(data.map(d => d.y))
        .range([50, height - 50])
        .padding(0.5);

    const sizeScale = d3.scaleSqrt()
        .domain([0, d3.max(data, d => d.size)])
        .range([5, 40]);  // Rango mínimo y máximo del radio de las burbujas

    const bubbles = svg.selectAll(".bubble")
        .data(data)
        .enter().append("g")
        .attr("class", "bubble-group");

    // Dibujar Burbujas
    bubbles.append("circle")
        .attr("class", "bubble")
        .attr("cx", d => xScale(d.x))
        .attr("cy", d => yScale(d.y))
        .attr("r", d => sizeScale(d.size))
        .style("fill", d => getColorForValue(d.size));

    // Añadir etiquetas de texto
    bubbles.append("text")
        .attr("x", d => xScale(d.x))
        .attr("y", d => yScale(d.y))
        .text(d => d.label)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "central")  
        .style("fill", "#000000")  
        .style("font-size", d => Math.max(10, d.radius / 3) + "px");  

    // Añadir Ejes
    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    svg.append("g")
        .attr("transform", `translate(0,${height - 50})`)
        .call(xAxis);

    svg.append("g")
        .attr("transform", "translate(0,0)")
        .call(yAxis);
}

function getColorForValue(value) {
    if (value > 200) return 'rgba(255, 99, 132, 0.8)'; // rojo
    if (value >= 150 && value <= 200) return 'rgba(54, 162, 235, 0.8)'; // azul
    return 'rgba(75, 192, 192, 0.8)'; // verde
}

async function initializeVisualizations() {
    await createBubbleVisualization();
    await createKeywordsBubbleChart();
}

document.addEventListener('DOMContentLoaded', initializeVisualizations);
