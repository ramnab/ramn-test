# Tagging details for Cloudformation Resources


## CAPITA-CONNECT\CAPITA\reporting\rta\templates\account-setup.yml

```  
Type: AWS::S3::Bucket 

    s3-capita-ccm-prd-common-dev-rta-agentschedule

      Tags:
        -
            Key: "tech:ApplicationID"
            Value: "capita-ccm-rta-webapp"
        -
            Key: "tech:Environment"
            Value: dev
        -
            Key: "bus:BusinessUnit"
            Value: ccm
        -
            Key: "sec:Compliance"
            Value: PII
```

```
Type: AWS::S3::Bucket 

    s3-capita-ccm-dev-common-dev-lambdas-eu-central-1

      Tags:
        -
            Key: "tech:ApplicationID"
            Value: "capita-ccm-rta-webapp"
        -
            Key: "tech:Environment"
            Value: dev
        -
            Key: "bus:BusinessUnit"
            Value: ccm
        -
            Key: "sec:Compliance"
            Value: PII
```

## CAPITA-CONNECT\CAPITA\reporting\rta\templates\api.yml

```
Type: AWS::Serverless::Function

      Tags:
        -
            Key: "tech:ApplicationID"
            Value: "capita-ccm-rta-webapp"
        -
            Key: "tech:Environment"
            Value: dev
        -
            Key: "bus:BusinessUnit"
            Value: ccm

```


## CAPITA-CONNECT\CAPITA\reporting\rta\templates\cdn.yml
```
  25,5:     Type: AWS::S3::Bucket
    s3-capita-ccm-common-dev-rta-webapp

      Tags:
        -
            Key: "tech:ApplicationID"
            Value: "capita-ccm-rta-webapp"
        -
            Key: "tech:Environment"
            Value: dev
        -
            Key: "bus:BusinessUnit"
            Value: ccm
        -
            Key: "sec:Compliance"
            Value: Normal
        
```

```
  37,5:     Type: AWS::CloudFront::Distribution

      Tags:
        -
            Key: "tech:ApplicationID"
            Value: "capita-ccm-rta-webapp"
        -
            Key: "tech:Environment"
            Value: dev
        -
            Key: "bus:BusinessUnit"
            Value: ccm
        
```
