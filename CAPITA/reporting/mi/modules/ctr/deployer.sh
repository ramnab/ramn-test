#!/usr/bin/env bash

CLIENT=$1
ENV=$(echo $2 | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2)) }')
ENV_LOWER=$(echo $2 | awk '{print tolower($0)}')
ENV_UPPER=$(echo $2 | awk '{print toupper($0)}')

DIRECTORY=`dirname $0`


echo """
----------------------------------------------------
                   ctr solution
                   ------------

"""

echo """

               Deploying CTR resources
               -----------------------

"""



cf sync -y --context ${DIRECTORY}/../../transforms/config-ccm-${CLIENT}-${ENV_LOWER}.yml \
   ${DIRECTORY}/ctr-resources.stacks


echo """

               Update the CTR Firehose
               -----------------------

"""


aws lambda invoke --function-name lmbMiFirehoseModder-ccm-$ENV_UPPER \
                  --payload "{
  \"debug\": true,
  \"ResourceProperties\": {
    \"FirehoseName\": \"kfh-ccm-ctr-${ENV_LOWER}\",
    \"Prefix\": \"contact_record/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"ErrorPrefix\": \"errors/contact_record/!{firehose:error-output-type}/clientname=${CLIENT}/rowdate=!{timestamp:yyyy-MM-dd}/\",
    \"TransformationDb\": \"gl_ccm_${ENV_LOWER}\",
    \"TransformationTable\": \"glt_ctr_${ENV_LOWER}\",
    \"TransformationRole\": \"rl_mi_ctr_${ENV_LOWER}\"
  }
}" result.txt


python ${DIRECTORY}/../../scripts/tag-firehose.py -f kfh-ccm-ctr-${ENV_LOWER} \
                    -t sec:Compliance:PII bus:BusinessUnit:ccm bus:ClientName:${CLIENT} \
                       tech:Environment:${ENV_LOWER} tech:ApplicationID:capita-ccm-connect \
                       tech:ApplicationRole:reporting



rm result.txt

echo """

                  ctr solution: complete
----------------------------------------------------


"""