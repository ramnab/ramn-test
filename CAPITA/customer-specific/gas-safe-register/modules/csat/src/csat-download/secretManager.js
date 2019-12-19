/**
 * A module which fetches the SecretData for the provided Secret Name.
 *
 */
    'use strict';
    
    // Load the AWS SDK
    var AWS = require('aws-sdk'),
        region = "eu-central-1",
        secretName = "prod/Secret-CustomerSurvey",
        secret,
        decodedBinarySecret;
        
    // Create a Secrets Manager client
    var client = new AWS.SecretsManager({
            region: region
        });
    
    module.exports.secretManager = (secretName, callback) => {
        var secrets;
        client.getSecretValue({SecretId: secretName}, function(err, data) {
            if (err) {
                console.log("There is an error: "+ err.code);
                if (err.code === 'DecryptionFailureException')
                    console.log("The request was failed due to decryption failure: " + err.message);
                else if (err.code === 'InternalServiceErrorException')
                    console.log("The request failed due to Internal Service error: " + err.message);
                else if (err.code === 'InvalidParameterException')
                    console.log("The request had invalid params: " + err.message);
                else if (err.code === 'InvalidRequestException')
                    console.log("The request was invalid due to: " + err.message);
                else if (err.code === 'ResourceNotFoundException')
        			console.log("The requested secret " + secretName + " was not found");
            }
            else {
                // Decrypts secret using the associated KMS CMK.
                // Depending on whether the secret is a string or binary, one of these fields will be populated.
        		//console.log("Data: "+ data);
                if ('SecretString' in data) {
                    secrets = data.SecretString;
                } else {
                    let buff = Buffer.from(data.SecretBinary, 'base64');
                    decodedBinarySecret = buff.toString('ascii');
                }
            }
            
            //Process the retrieved data.
            callback(secrets);
        }); 
        
    };