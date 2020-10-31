const AWS = require('aws-sdk');
const {bucketName} = require('../config.json');

const client = new AWS.Rekognition();
const s3 = new AWS.S3({
    params: {Bucket: bucketName}
});

function getS3object() {
    var files = [];
    s3.listObjectsV2({
        Bucket: bucketName
    }, (err, data) => {
        if (err) console.log(err, err.stack);
        else files = data['Contents'];
    });
    return files
}

function label_faces(s3object) {
    
}

module.exports = {label_faces, getS3object};