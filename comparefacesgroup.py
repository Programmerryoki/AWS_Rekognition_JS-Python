"""
Time Ii takes to label the image:
 - 50 sec for target image
 - 17 seconds per source / people to check

Required Permissions:
 - rekognition:CreateCollection
 - rekognition:DeleteCollection
 - rekognition:DeleteFaces
 - rekognition:DetectFaces
 - rekognition:IndexFaces
 - rekognition:SearchFacesByImage
"""

import os
from PIL import Image, ImageDraw, ImageFont
import json
import boto3


def draw_name(bb, im, text, draw):
    lx = round(bb["Left"] * im.size[0])
    ly = round(bb["Top"] * im.size[1])
    rx = round((bb["Left"] + bb["Width"]) * im.size[0])
    ry = round((bb["Top"] + bb["Height"]) * im.size[1])
    # print(lx,ly,rx,ry)
    draw.rectangle((lx, ly, rx, ry), outline=(0, 0, 0), width=5)
    draw.text((lx, ly), text, font=ImageFont.truetype("arial.ttf", int(im.size[1] * bb["Height"] * 0.3)))


def rotate_image(targetfile, saveimg):
    client = boto3.client('rekognition')
    imagetarget = open(targetfile, 'rb')

    print("detecting faces")

    response = client.detect_faces(
        Image={'Bytes': imagetarget.read()},
        Attributes=["ALL"]
    )

    with open("detect_face.json", "w") as file:
        json.dump(response, file, indent=4)

    # Rotating Images
    with Image.open(targetfile) as image:
        try:
            oc = response['OrientationCorrection']
            if oc == "ROTATE_90":
                image = image.rotate(90, expand=True)
            elif oc == "ROTATE_180":
                image = image.rotate(180, expand=True)
            elif oc == "ROTATE_270":
                image = image.rotate(270, expand=True)
        except:
            pass
        finally:
            image.copy().save(saveimg)
    imagetarget.close()


def label_faces(targetfile, srcimg):
    print("label faces")

    client = boto3.client('rekognition')

    imagetarget = open(targetfile, 'rb')

    cid = "faces"
    try:
        client.create_collection(
            CollectionId=cid
        )
    except:
        pass
    client.index_faces(
        CollectionId=cid,
        Image={'Bytes': imagetarget.read()}
    )

    nfiles = str(len(os.listdir(srcimg)))
    for i in range(1, len(os.listdir(srcimg)) + 1):
        filename = os.listdir(srcimg)[i - 1]

        print("\nChecking " + str(i) + " / " + nfiles + " : " + filename)
        imagesource = open(srcimg + filename, 'rb')

        print("\twaiting response")

        response = client.search_faces_by_image(
            CollectionId=cid,
            Image={'Bytes': imagesource.read()},
            FaceMatchThreshold=90
        )

        if len(response["FaceMatches"]) == 0:
            print("\tNot In Picture")
            continue

        print("\tdrawing")
        # Bounding Box
        with Image.open(targetfile).copy() as im:
            draw = ImageDraw.Draw(im)
            matchface = max(response['FaceMatches'], key=lambda x: x['Similarity'])
            bb = matchface['Face']['BoundingBox']
            draw_name(bb, im, filename.split(".")[0], draw)
            im.save(targetfile)

        if matchface:
            client.delete_faces(
                CollectionId=cid,
                FaceIds=[matchface['Face']['FaceId']]
            )

        with open("./result_json/result_" + filename + ".json", "w") as file:
            json.dump(response, file, indent=4)

        imagesource.close()
    imagetarget.close()

    with Image.open(targetfile) as im:
        draw = ImageDraw.Draw(im)
        faces = client.list_faces(CollectionId=cid)['Faces']
        for face in faces:
            bb = face['BoundingBox']
            draw_name(bb, im, "?", draw)
        im.save(targetfile)

    client.delete_collection(
        CollectionId=cid
    )

    with Image.open(targetfile) as im:
        im.show()


def main():
    target_file = './testimg/IMG-2082.JPG'
    saveimg = "result_" + target_file.split(".")[1].split("/")[-1] + ".jpg"
    srcimg = "./srcimg/"
    rotate_image(target_file, saveimg)
    label_faces(saveimg, srcimg)
    print("Done!")


if __name__ == "__main__":
    main()
