let allQuestions = [];
let currentPage = 0;
const QUESTIONS_PER_PAGE=5;
let questionsDiv;

function getSourceFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("src");
}

document.addEventListener("DOMContentLoaded", async () => {
    questionsDiv = document.getElementById("questions");
    const sourceName = getSourceFromURL();
    if (!sourceName) {
        document.getElementById("questions").innerHTML = "Veuillez fournir un fichier source via ?src=nom.qtex";
        return;
    }
    const xmlFile = sourceName.replace(".qtex",".xml");
    
    if (!xmlFile) {
    document.body.innerHTML = "<p>Aucun fichier XML fourni.</p>";
    return;
  }

  try {
    const response = await fetch("./"+xmlFile);
    const xmlText = await response.text();
    
    // ÉTAPE CRUCIALE : On extrait les questions du texte XML reçu
    extractQuestions(xmlText, sourceName); 
    // On affiche la première page
    renderQuestion();
  } catch (err) {
    console.error("Erreur de chargement XML:", err);
    document.getElementById("questions").innerHTML = "Erreur de chargement du fichier XML.";
  }
});


function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function extractQuestions(xmlText, sourceName) {
    const parser = new DOMParser();
    const xml = parser.parseFromString(xmlText, "text/xml");

    xml.querySelectorAll("question").forEach(q => {
        const type = q.getAttribute("type");
        if (type === "category") return;

        allQuestions.push({
            type,
            title: q.querySelector("name > text")?.textContent ?? "(sans titre)",
            html: q.querySelector("questiontext > text")?.textContent ?? "",
            answers: Array.from(q.querySelectorAll("answer")).map(a => ({
                html: a.querySelector("text")?.textContent ?? "",
                fraction: parseFloat(a.getAttribute("fraction") ?? "0")
            })),
            source: sourceName
        });
    });
}

function renderQuestion() {
    questionsDiv.innerHTML = "";
    if (allQuestions.length === 0) return;
    const start = currentPage * QUESTIONS_PER_PAGE; 
    const end = start + QUESTIONS_PER_PAGE;
    const pageQuestions = allQuestions.slice(start, end);

    pageQuestions.forEach((q, qIndex) => {
        const div = document.createElement("div");
        div.className = "question";
        div.innerHTML = `
        <div class="q-type">Source : ${q.source}</div>
        <div class="q-type">Type : ${q.type}</div>
        <div class="q-title">Name : ${q.title}</div>
        <div class="q-text">${q.html}</div>`;

        if (q.type === "multichoice" || q.type === "truefalse") {
            const form = document.createElement("form");
            form.className = "answers-container";     
            const answers = [...q.answers];
            shuffle(answers);
            const correctCount = answers.filter(a => a.fraction > 0).length;
            const inputType = (q.type === "multichoice" && correctCount > 1) ? "checkbox" : "radio";
            answers.forEach((a) => {
                const label = document.createElement("label");
                label.className = "answer";
    
                const input = document.createElement("input");
                input.type = inputType;
                input.name = `q_${qIndex}`;
                input.dataset.correct = a.fraction > 0;
    
                label.appendChild(input);
                label.insertAdjacentHTML("beforeend", " " + a.html);
                form.appendChild(label);
            });

            const button = document.createElement("button");
            button.type = "button";
            button.textContent = "Valider";
            button.style.marginTop = "10px";
            button.onclick = () => window.correctQuestion(form);

            div.appendChild(form);
            div.appendChild(button);
        }
        questionsDiv.appendChild(div);
    });
    if (window.MathJax) {
        MathJax.typesetPromise([questionsDiv]);
    }
}

window.correctQuestion = function(form) {
    const inputs = form.querySelectorAll("input");
    inputs.forEach(input => {
        input.disabled = true; // Désactive les champs après validation
        const label = input.parentElement;
        const isCorrect = input.dataset.correct === "true";
        const checked = input.checked;

        if (isCorrect) {
            label.classList.add("correct"); // Applique le style vert
        }
        if (checked && !isCorrect) {
            label.classList.add("incorrect"); // Applique le style rouge
        }
    });
};

