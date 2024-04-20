const flags = document.getElementById('flags');
const textsToChange = document.querySelectorAll("[data-section]")

const changeLanguage = async (language) => {
    const requestJson = await fetch(`../../../static/Inicio_sesion/languages/${language}.json`);
    const texts = await requestJson.json()
    console.log(texts)
    for (const textToChange of textsToChange) {
        const section = textToChange.dataset.section;
        const value = textToChange.dataset.value;
        textToChange.innerHTML=texts[section][value];
    }
} 

flags.addEventListener("click", (e) => {
    changeLanguage(e.target.parentElement.dataset.language)
})