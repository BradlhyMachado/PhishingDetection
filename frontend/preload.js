const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    analizarURL: (url) => ipcRenderer.send('analizar-url', url)
});