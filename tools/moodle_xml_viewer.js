let allQuestions = [];
let currentPage = 0;
const QUESTIONS_PER_PAGE = 5;
const fileInput = document.getElementById("fileInput");
const questionsDiv = document.getElementById("questions");

// Rendre la fonction globale pour le onclick
window.correctQuestion = function(form) {
    const inputs = form.querySelectorAll("input");
    inputs.forEach(input => {
        input.disabled = true;
        const label = input.parentElement;
        const isCorrect = input.dataset.correct === "true";
        const checked = input.checked;

        if (isCorrect) {
            label.classList.add("correct");
        }
        if (checked && !isCorrect) {
            label.classList.add("incorrect");
        }
    });
};

fileInput.addEventListener("change", async () => {
    allQuestions = [];
    currentPage = 0;
    const files = Array.from(fileInput.files).filter(f => f.name.endsWith(".xml"));

    for (const file of files) {
        const text = await file.text();
        extractQuestions(text, file.name);
    }
    renderPage();
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

function renderPage() {
    questionsDiv.innerHTML = "";
    if (allQuestions.length === 0) return;

    const start = currentPage * QUESTIONS_PER_PAGE;
    const end = start + QUESTIONS_PER_PAGE;
    const pageQuestions = allQuestions.slice(start, end);

    pageQuestions.forEach((q, qIndex) => {
        const div = document.createElement("div");
        div.className = "question";
        div.innerHTML = `
            <div class="q-type">Source : ${q.source} | Type : ${q.type}</div>
            <div class="q-title">${q.title}</div>
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

    // Mise à jour de l'UI de navigation
    const totalPages = Math.ceil(allQuestions.length / QUESTIONS_PER_PAGE);
    document.getElementById("pageInfo").textContent = `Page ${currentPage + 1} / ${totalPages}`;
    
    if (window.MathJax) {
        MathJax.typesetPromise([questionsDiv]);
    }
}

// Fonctions de navigation globales
window.nextPage = function() {
    if ((currentPage + 1) * QUESTIONS_PER_PAGE < allQuestions.length) {
        currentPage++;
        renderPage();
        window.scrollTo(0,0);
    }
};

window.prevPage = function() {
    if (currentPage > 0) {
        currentPage--;
        renderPage();
        window.scrollTo(0,0);
    }
};
