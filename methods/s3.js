const AWS = require('aws-sdk');
const {bucketName} = require('../config.json');

function alert(string) {
    console.log(string);
}

async function createAlbum(s3, albumName) {
    albumName = albumName.trim();
    if (!albumName) {
        return alert("Album names must contain at least one non-space character.");
    }
    if (albumName.indexOf("/") !== -1) {
        return alert("Album names cannot contain slashes.");
    }
    var albumKey = encodeURIComponent(albumName);
    await s3.headObject({ Key: albumKey }, function(err, data) {
        if (!err) {
            return alert("Album already exists.");
        }
        if (err.code !== "NotFound") {
            return alert("There was an error creating your album: " + err.message);
        }
        s3.putObject({ Key: albumKey }, function(err, data) {
            if (err) {
                return alert("There was an error creating your album: " + err.message);
            }
            alert("Successfully created album.");
        });
    });
}

async function addPhoto(files, albumName) {
    if (!files.length) {
        return alert("Please choose a file to upload first.");
    }
    for (var index = 0; index < files.length; index++) {
        var file = files[index];
        var fileName = file.name;
        console.log(file, fileName);
        var albumPhotosKey = encodeURIComponent(albumName) + "/";
    
        var photoKey = albumPhotosKey + fileName;
    
        // Use S3 ManagedUpload class as it supports multipart uploads
        var upload = new AWS.S3.ManagedUpload({
            params: {
                Bucket: bucketName,
                Key: photoKey,
                Body: file,
                ACL: "public-read"
            }
        });
        
        try {
            var promise = upload.promise();
        
            await promise.then(
                function(data) {
                    alert("Successfully uploaded photo.");
                    viewAlbum(albumName);
                },
                function(err) {
                    return alert("There was an error uploading your photo: ", err.message);
                }
            );
        } catch(err) {
            console.log(err);
        }
    }
}

module.exports = {createAlbum, addPhoto};
