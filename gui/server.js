// expressモジュールをロードし、インスタンス化
var express = require("express");
var app = express();

// 3000番ポートでlisten
var server = app.listen(3000, function(){
    console.log("listening to PORT:" + server.address().port);
});

const spawn = require('child_process').spawn;
let python = null;

const getArgs = (data) => {
    const args = [];

    if (data.mode === 'inApp') {
        args.push('app');
    } else if (data.mode === 'inSim') {
        args.push('sim');
    } else {
        throw new Error("Invalid mode.");
    }

    return args;
}

const getOptions = (data) => {
    const options = [];

    if (data.multiPlay === 'true') {
        options.push('-m');
    }

    if (data.quickSearch === 'true') {
        options.push('-q');
    }

    return options;
};

// pythonのプロセスを開始するAPI
app.get("/api/start", function(req, res, next){
    python = spawn(
        'python', ['../main.py'].concat(getArgs(req.query)).concat(getOptions(req.query)));
    
    // todo: serverの標準出力で行われてしまうので、ソケット通信でやれるようにしたい
    python.stdout.on('data', (data) => {
        process.stdout.write(data);
    });

    res.json('process started.');
});

// pythonのプロセスを終了するAPI
app.get("/api/stop", function(req, res, next){
    python.kill();

    process.stdout.write('Stopped.\n\n\n');

    res.json('stopped.');
});
