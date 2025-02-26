// Listen for download events
chrome.downloads.onCreated.addListener((downloadItem) => {
    console.log("Download started:", downloadItem.filename);
  
    // Send download details to the main application
    chrome.runtime.sendMessage({
      type: "download_started",
      filename: downloadItem.filename,
      url: downloadItem.url,
      fileSize: downloadItem.fileSize,
      mimeType: downloadItem.mimeType
    });
  });
  
  // Listen for messages from the popup or other parts of the extension
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "check_duplicate") {
      // Simulate duplicate detection (replace with actual API call)
      const isDuplicate = Math.random() > 0.5; // Randomly decide if it's a duplicate
      sendResponse({ isDuplicate });
    }
  });