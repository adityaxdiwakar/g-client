let {PythonShell} = require('python-shell');

send_message = function() {
    var seconds = new Date()
    console.log(seconds/1000*1000)
    message = document.getElementById('message-box').value
    document.getElementById('message-box').value = ""
    let options = {
        mode: 'text',
        scriptPath: 'app_engine/',
        args: ["send", 45892925, message]
    }
    PythonShell.run('main.py', options, function (err, results) {
        if (err) throw err;
        console.log('results', results);
    });
}   

