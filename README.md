# aws-upload-api
API to validate and upload json payload to s3

# How-To: 
`curl -i -X POST -d @test.json  https://laxzjvk6s5.execute-api.us-west-1.amazonaws.com/prod/upload   -H 'cache-control: no-cache'   -H 'content-type: application/json'
`
* Use the above command to upload a JSON payload to the S3 bucket
* The API gives either of the two responses:
    * `{ status: "uploaded", error: "" }`
    * `{ status: "not uploaded", error: "not valid json" }`
    * The uploaded payloads can be viewed at: https://console.aws.amazon.com/s3/buckets/sraouploadbucket/?region=us-east-2&tab=overview
    
# Architecture: 

![Architecture](https://github.com/shrivardhan92/wiki-repo/blob/master/images/uploadAPI.jpeg "Architecture and Flow")
