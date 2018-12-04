import json
import boto3
import datetime
from datetime import timedelta
import constant

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # Agreed time format YYYYMMDDHHMm
    datetimePrefix = '%Y%m%d%H'
    datetimeFormat = '%Y%m%d%H%M'
    fileNameFormat = '%Y%m%d-%H%M%S%f'

    # to search for folders
    timePrefix = datetime.datetime.now().strftime(datetimePrefix)

    # for finding time delta
    timeNow = datetime.datetime.now().strftime(datetimeFormat)

    # list all folders within the hour and select the most recent
    response = s3_client.list_objects_v2(
        Bucket=constant.S3_BUCKET,
        MaxKeys=12,
        Prefix=timePrefix)
    # try build list and sort in descending order
    keyList = list()
    latestFolder = ''
    uploadFileName = ''
    uploadFolderPath = ''
    try:
        contents = response['Contents']
        for key in contents:
            keyList.append(key['Key'].split("/")[0])
        keyList.sort(reverse=True)
    except KeyError:
        pass

    # some arbitrary value greater than the agreed time delta of 5 mins
    minDiff = 1000
    if keyList:
        recentFolder = keyList[0].replace("/", "")
        diff = datetime.datetime.strptime(timeNow, datetimeFormat)\
            - datetime.datetime.strptime(recentFolder, datetimeFormat)
        minDiff = diff.seconds / 60
        latestFolder = keyList[0]

    # check time delta
    if minDiff <= 5:
        # do not create folder use latest folder
        uploadFileName = 'payload-'\
            + datetime.datetime.now().strftime(fileNameFormat) + '.json'
        uploadFolderPath = latestFolder + '/' + uploadFileName
    else:
        # create a new folder and upload
        uploadFileName = 'payload-'\
            + datetime.datetime.now().strftime(fileNameFormat) + '.json'
        uploadFolderPath = timeNow + '/' + uploadFileName

    # upload payload
    s3_client.put_object(
        Body=json.dumps(event),
        Bucket=constant.S3_BUCKET,
        Key=uploadFolderPath)

    return {
        "status": "uploaded",
        "error": ""
    }
