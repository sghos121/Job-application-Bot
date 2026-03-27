chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "fillForm") {
    chrome.storage.local.get("sohamData", (result) => {
      const data = result.sohamData;
      if (!data) return;

      // Define mappings for common field names
      const mappings = {
        firstName: ["first_name", "firstname", "first-name", "given-name"],
        lastName: ["last_name", "lastname", "last-name", "family-name"],
        email: ["email", "e-mail"],
        phone: ["phone", "tel", "mobile", "contact"],
        linkedin: ["linkedin", "linkdin"],
        github: ["github"]
      };

      // Find all input fields on the page
      const inputs = document.querySelectorAll('input, textarea');

      inputs.forEach(input => {
        const name = (input.name || "").toLowerCase();
        const id = (input.id || "").toLowerCase();
        const placeholder = (input.getAttribute('placeholder') || "").toLowerCase();
        const combined = name + id + placeholder;

        // Loop through our mappings to see if this input matches anything
        for (const [key, keywords] of Object.entries(mappings)) {
          if (keywords.some(kw => combined.includes(kw))) {
            input.value = data[key];
            // Trigger events so the website knows the text changed
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
          }
        }
      });

      // Special Logic for F-1 OPT Visa Questions
      const labels = document.querySelectorAll('label');
      labels.forEach(label => {
        const text = label.innerText.toLowerCase();
        
        // If the question is about sponsorship, try to click "Yes"
        if (text.includes("sponsorship") || text.includes("authorized")) {
            // This is a common pattern: click the radio button near this label
            const radio = label.parentElement.querySelector('input[type="radio"][value*="yes" i]');
            if (radio) radio.click();
        }
      });

      console.log("Soham's Autofiller: Done!");
    });
  }
});