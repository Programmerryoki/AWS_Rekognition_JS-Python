var {PythonShell} = require('python-shell');

PythonShell.run('comparefacesgroup.py', null, (err, result) => {
    if (err) console.error(err);
    console.log(result);
});

// var pyshell = new PythonShell('comparefacesgroup.py');
// pyshell.on('message', )