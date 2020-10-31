const fs = require('fs');

function readlocalfile(filepath) {
    let localfiles = [];
    fs.readdir(filepath, (err, files) => {
        if (err) return console.error(err);

        files.forEach((filename) => {
            fs.readFile(filepath + filename, (err, data) => {
                if (err) return console.error(err);
                localfiles.push(data);
            });
        });
    });
    return localfiles;
}

module.exports = readlocalfile;
