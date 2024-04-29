// Define constants for flags and elements to translate
const flags = document.getElementById('flags');

// Function to change language
const changeLanguage = async (language, textsToChange) => {
    try {
        // Fetch JSON data for the selected language
        const requestJson = await fetch(`../../../static/Inicio_sesion/languages/${language}.json`);
        if (!requestJson.ok) {
            throw new Error("Failed to fetch language data.");
        }
        const texts = await requestJson.json();

        console.log("Received JSON data:", texts);

        // Iterate over elements to translate and update content
        for (const textToChange of textsToChange) {
            const section = textToChange.dataset.section;
            const value = textToChange.dataset.value;

            console.log(`Translating ${section} ${value}`);

            if (texts[section] && texts[section][value]) {
                if (value === "submit-btn") {
                    textToChange.value = texts[section][value];
                } else if (value === "email-placeholder") {
                    const emailInput = document.querySelector("input[type='email']");
                    if (emailInput) {
                        emailInput.placeholder = texts[section][value];
                    }
                } else if (value === "password-placeholder") {
                    const passwordInput = document.querySelector("input[type='password']");
                    if (passwordInput) {
                        passwordInput.placeholder = texts[section][value];
                    }
                } else {
                    textToChange.textContent = texts[section][value];
                }
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
        const textsToChange = document.querySelectorAll("[data-section]");
        changeLanguage(e.target.parentElement.dataset.language, textsToChange);
    }
});

// Initial language load (you can adjust this based on your default language)
window.addEventListener("DOMContentLoaded", () => {
    const textsToChange = document.querySelectorAll("[data-section]");
    changeLanguage("es", textsToChange); // Set initial language to Spanish
});
