const toggle = document.getElementById('toggle');

chrome.storage.sync.get('enabled', data => {
    toggle.checked = !!data.enabled;
});

toggle.onchange = () => {
    chrome.storage.sync.set({enabled: toggle.checked});
};