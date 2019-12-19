/**
 * BASIC Authentication
 *
 * Simple authentication script intended to be run by Amazon Lambda to
 * provide Basic HTTP Authentication for a static website hosted in an
 * Amazon S3 bucket through Couldfront.
 *
 */
 
'use strict';

var secretManager = require('./secretManager');

exports.handler = (event, context, callback) => {
    
    // Get request and request headers
    const request = event.Records[0].cf.request;
    const headers = request.headers;
    const reqUri = request.uri;
    
    const content = `
        <\!DOCTYPE html>
        <html lang="en">
          <head>
            <title>GSR-Customer Survey</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
          </head>
          <body>
            <p>You have been logged out. It is a good idea to close this browser tab!</p>
          </body>
        </html>
        `;
    
    //call secretManager
    secretManager.secretManager("prod/Secret-CustomerSurvey", function(secrets) {
            
            //Check if the request is for logout
            if (reqUri.includes("logoff")) {
                const response = {
                    status: '401',
                    statusDescription: 'Unauthorized',
                    headers: {
                        'www-authenticate': [{
                            key: 'WWW-Authenticate', 
                            value:'Basic'
                        }],
                        'cache-control': [{
                            key: 'Cache-Control',
                            value: 'max-age=60'
                        }],
                        'content-type': [{
                            key: 'Content-Type',
                            value: 'text/html'
                        }],
                        'content-encoding': [{
                            key: 'Content-Encoding',
                            value: 'UTF-8'
                        }],
                    },
                    body: content,
                };
                callback(null, response);                
            }
            
            //If it's not a logout request, process it further
            const authSecrets = JSON.parse(secrets);
            var keys = Object.keys(authSecrets);
            
            const authUser = authSecrets[keys[0]];
            const authPass = authSecrets[keys[1]];
            
            // Construct the Basic Auth string
            const authString = 'Basic ' + new Buffer(authUser + ':' + authPass).toString('base64');
         
            // Require Basic authentication
            if (typeof headers.authorization == 'undefined' || headers.authorization[0].value != authString) {
                const body = 'Unauthorized, please refresh/reload this page and use correct credentials';
                const response = {
                    status: '401',
                    statusDescription: 'Unauthorized',
                    body: body,
                    headers: {
                        'www-authenticate': [{
                            key: 'WWW-Authenticate', 
                            value:'Basic'
                        }],
                        'cache-control': [{
                            key: 'Cache-Control',
                            value: 'max-age=60'
                        }],
                        'content-type': [{
                            key: 'Content-Type',
                            value: 'text/html'
                        }],
                        'content-encoding': [{
                            key: 'Content-Encoding',
                            value: 'UTF-8'
                        }],
                    },
                };
                callback(null, response);
            }

            // Continue request processing if authentication passed
            callback(null, request); 
            });
};