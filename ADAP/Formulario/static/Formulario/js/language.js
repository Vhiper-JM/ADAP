// Define constants for flags and elements to translate
const flags = document.getElementById('flags');

// Function to change language
const changeLanguage = async (language, textsToChange) => {
    try {
        // Fetch JSON data for the selected language
        console.log(`Fetching language data for ${language}`);
        const requestJson = await fetch(`../../../static/Formulario/languages/${language}.json`);
        if (!requestJson.ok) {
            throw new Error("Failed to fetch language data.");
        }
        console.log(`Language data fetched successfully for ${language}`);
        const texts = await requestJson.json();

        console.log("Received JSON data:", texts);

        // Log all translations available in the JSON file
        for (const section in texts) {
            if (Object.hasOwnProperty.call(texts, section)) {
                console.log(`Translations for ${section}:`, texts[section]);
            }
        }

        // Iterate over elements to translate and update content
        for (const textToChange of textsToChange) {
            const section = textToChange.dataset.section;
            const value = textToChange.dataset.value;

            console.log(`Translating ${section} ${value}`);

            // Accessing translations directly
            if (texts[section] && texts[section][value]) {
                console.log(`Translation found for ${section} ${value}`);
                textToChange.textContent = texts[section][value];  // Use textContent for all, simplifies handling
            } else {
                console.log(`Translation not found for ${section} ${value}`);
            }
        }
    } catch (error) {
        console.error("Error fetching or processing language data:", error);
    }
};

// Event listener for language change
flags.addEventListener("click", (e) => {
    if (e.target.parentElement.dataset.language) {
        console.log("Language change event triggered");
        const textsToChange = document.querySelectorAll("[data-section]");
        changeLanguage(e.target.parentElement.dataset.language, textsToChange);
    }
});

// Initial language load (you can adjust this based on your default language)
window.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded event triggered");
    const textsToChange = document.querySelectorAll("[data-section]");
    changeLanguage("es", textsToChange); // Set initial language to Spanish
});
