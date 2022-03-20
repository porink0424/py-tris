const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

// windowを作成
app.on('ready', () => {
    // mainWindowを作成
    let mainWindow = new BrowserWindow({width: 400, height: 300});
    // Electronに表示するhtmlを指定
    mainWindow.loadFile(__dirname + '/index.html');

    mainWindow.on('closed', function() {
        mainWindow = null;
    });
});
