const c_button = document.getElementById("convert");
c_button.onclick = () => {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {message: "convert"}, () => {
            if(chrome.runtime.lastError) {}
        });
    });
};