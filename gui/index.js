const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

// serverを立てる
const fs = require('fs');
const spawn = require('child_process').spawn;
const node = spawn(
    'node',
    ['server.js']
);
node.stdout.on('data', (data) => {
    process.stdout.write(data);
    fs.writeFile("output.txt", data, {flag: 'a'}, (err) => {
        if (err) throw err;
    });
})

// windowを作成
app.on('ready', () => {
    // mainWindowを作成
    let mainWindow = new BrowserWindow({width: 400, height: 300});
    // Electronに表示するhtmlを指定
    mainWindow.loadFile(__dirname + '/index.html');

    mainWindow.on('closed', function() {
        mainWindow = null;
        node.kill();
    });
});
