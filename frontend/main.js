const { app, BrowserWindow, Notification, ipcMain } = require('electron');
const path = require('path');
const axios = require('axios');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
    });

    mainWindow.loadFile('index.html');
    mainWindow.webContents.openDevTools();
}

function enviarURLParaAnalisis(url) {
    console.log(`Enviando URL para análisis: ${url}`);
    axios.post(`http://127.0.0.1:5000/analizar-url`, {
        url: url
    })
    .then(response => {
        const data = response.data;
        console.log(`Respuesta del servidor:`, data.sospechosa);

        if (data.sospechosa) {
            mostrarNotificacion(url);
        } else {
            mainWindow.webContents.send('resultado', `La URL ${url} es segura.`);
        }
    })
    .catch(error => {
        console.error('Error al enviar la URL:', error.message);
        mainWindow.webContents.send('resultado', `Error al analizar la URL: ${error.message}`);
    });
}

function mostrarNotificacion(url) {
    new Notification({ title: 'Alerta de Phishing', body: `URL sospechosa detectada: ${url}` }).show();
}

app.whenReady().then(() => {
    createWindow();

    ipcMain.on('analizar-url', (event, url) => {
        console.log(`Recibida URL desde la interfaz para analizar: ${url}`);
        enviarURLParaAnalisis(url);
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});