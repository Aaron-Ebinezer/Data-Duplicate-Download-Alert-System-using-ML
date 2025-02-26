document.getElementById("checkDuplicate").addEventListener("click", () => {
    document.getElementById("status").textContent = "Checking for duplicates...";
  
    // Send a message to the background script to check for duplicates
    chrome.runtime.sendMessage({ type: "check_duplicate" }, (response) => {
      if (response.isDuplicate) {
        document.getElementById("status").textContent = "Duplicate found!";
      } else {
        document.getElementById("status").textContent = "No duplicate found.";
      }
    });
  });