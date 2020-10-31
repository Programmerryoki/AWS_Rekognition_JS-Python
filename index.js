const { bucketName } = require('./config.json');
const AWS = require('aws-sdk');
const fs = require('fs');
const {createAlbum, addPhoto} = require('./methods/s3');
const {label_faces, getS3object} = require('./methods/rekognition');
const readlocalfile = require('./methods/readlocalfile');

main();

function main() {
    var s3 = new AWS.S3({
        params: {Bucket: bucketName}
    });

    let files = fs.readdirSync('./srcimg/');
    console.log(files);

    // createAlbum(s3, 'srcimg');
    // addPhoto(files, 'srcimg');
    let images = getS3object();
    label_faces(images);
}
