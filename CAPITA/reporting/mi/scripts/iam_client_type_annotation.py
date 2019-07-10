from typing import Union
from typing import List
from botocore.paginate import Paginator
from botocore.waiter import Waiter
from typing import Optional
from typing import Dict
from botocore.client import BaseClient


class Client(BaseClient):
    def add_client_id_to_open_id_connect_provider(self, OpenIDConnectProviderArn: str, ClientID: str):
        """
        Adds a new client ID (also known as audience) to the list of client IDs already registered for the specified IAM OpenID Connect (OIDC) provider resource.
        This operation is idempotent; it does not fail or return an error if you add an existing client ID to the provider.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AddClientIDToOpenIDConnectProvider>`_

        **Request Syntax**
        ::
          response = client.add_client_id_to_open_id_connect_provider(
              OpenIDConnectProviderArn='string',
              ClientID='string'
          )
        :type OpenIDConnectProviderArn: string
        :param OpenIDConnectProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM OpenID Connect (OIDC) provider resource to add the client ID to. You can get a list of OIDC provider ARNs by using the  ListOpenIDConnectProviders operation.
        :type ClientID: string
        :param ClientID: **[REQUIRED]**
          The client ID (also known as audience) to add to the IAM OpenID Connect provider resource.
        :returns: None
        """
        pass

    def add_role_to_instance_profile(self, InstanceProfileName: str, RoleName: str):
        """
        Adds the specified IAM role to the specified instance profile. An instance profile can contain only one role, and this limit cannot be increased. You can remove the existing role and then add a different role to an instance profile. You must then wait for the change to appear across all of AWS because of `eventual consistency <https://en.wikipedia.org/wiki/Eventual_consistency>`__ . To force the change, you must `disassociate the instance profile <http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DisassociateIamInstanceProfile.html>`__ and then `associate the instance profile <http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AssociateIamInstanceProfile.html>`__ , or you can stop your instance and then restart it.
        .. note::
          The caller of this API must be granted the ``PassRole`` permission on the IAM role by a permissions policy.
        For more information about roles, go to `Working with Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ . For more information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AddRoleToInstanceProfile>`_

        **Request Syntax**
        ::
          response = client.add_role_to_instance_profile(
              InstanceProfileName='string',
              RoleName='string'
          )
        :type InstanceProfileName: string
        :param InstanceProfileName: **[REQUIRED]**
          The name of the instance profile to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to add.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def add_user_to_group(self, GroupName: str, UserName: str):
        """
        Adds the specified user to the specified group.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AddUserToGroup>`_

        **Request Syntax**
        ::
          response = client.add_user_to_group(
              GroupName='string',
              UserName='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to add.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def attach_group_policy(self, GroupName: str, PolicyArn: str):
        """
        Attaches the specified managed policy to the specified IAM group.
        You use this API to attach a managed policy to a group. To embed an inline policy in a group, use  PutGroupPolicy .
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AttachGroupPolicy>`_

        **Request Syntax**
        ::
          response = client.attach_group_policy(
              GroupName='string',
              PolicyArn='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name (friendly name, not ARN) of the group to attach the policy to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to attach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def attach_role_policy(self, RoleName: str, PolicyArn: str):
        """
        Attaches the specified managed policy to the specified IAM role. When you attach a managed policy to a role, the managed policy becomes part of the role's permission (access) policy.
        .. note::
          You cannot use a managed policy as the role's trust policy. The role's trust policy is created at the same time as the role, using  CreateRole . You can update a role's trust policy using  UpdateAssumeRolePolicy .
        Use this API to attach a *managed* policy to a role. To embed an inline policy in a role, use  PutRolePolicy . For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AttachRolePolicy>`_

        **Request Syntax**
        ::
          response = client.attach_role_policy(
              RoleName='string',
              PolicyArn='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) of the role to attach the policy to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to attach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def attach_user_policy(self, UserName: str, PolicyArn: str):
        """
        Attaches the specified managed policy to the specified user.
        You use this API to attach a *managed* policy to a user. To embed an inline policy in a user, use  PutUserPolicy .
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/AttachUserPolicy>`_

        **Request Syntax**
        ::
          response = client.attach_user_policy(
              UserName='string',
              PolicyArn='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM user to attach the policy to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to attach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def can_paginate(self, operation_name: str = None):
        """
        Check if an operation can be paginated.
        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you\'d normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator(\"create_foo\")``.
        :return: ``True`` if the operation can be paginated,
            ``False`` otherwise.
        """
        pass

    def change_password(self, OldPassword: str, NewPassword: str):
        """
        Changes the password of the IAM user who is calling this operation. The AWS account root user password is not affected by this operation.
        To change the password for a different user, see  UpdateLoginProfile . For more information about modifying passwords, see `Managing Passwords <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ChangePassword>`_

        **Request Syntax**
        ::
          response = client.change_password(
              OldPassword='string',
              NewPassword='string'
          )
        :type OldPassword: string
        :param OldPassword: **[REQUIRED]**
          The IAM user\'s current password.
        :type NewPassword: string
        :param NewPassword: **[REQUIRED]**
          The new password. The new password must conform to the AWS account\'s password policy, if one exists.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ that is used to validate this parameter is a string of characters. That string can include almost any printable ASCII character from the space (\u0020) through the end of the ASCII character range (\u00FF). You can also include the tab (\u0009), line feed (\u000A), and carriage return (\u000D) characters. Any of these characters are valid in a password. However, many tools, such as the AWS Management Console, might restrict the ability to type certain characters because they have special meaning within that tool.
        :returns: None
        """
        pass

    def create_access_key(self, UserName: str = None) -> Dict:
        """
        Creates a new AWS secret access key and corresponding AWS access key ID for the specified user. The default status for new keys is ``Active`` .
        If you do not specify a user name, IAM determines the user name implicitly based on the AWS access key ID signing the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials. This is true even if the AWS account has no associated users.
        For information about limits on the number of keys you can create, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        .. warning::
          To ensure the security of your AWS account, the secret access key is accessible only during key and user creation. You must save the key (for example, in a text file) if you want to be able to access it again. If a secret key is lost, you can delete the access keys for the associated user and then create new keys.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateAccessKey>`_

        **Request Syntax**
        ::
          response = client.create_access_key(
              UserName='string'
          )

        **Response Syntax**
        ::
            {
                'AccessKey': {
                    'UserName': 'string',
                    'AccessKeyId': 'string',
                    'Status': 'Active'|'Inactive',
                    'SecretAccessKey': 'string',
                    'CreateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateAccessKey request.
            - **AccessKey** *(dict) --*
              A structure with details about the access key.
              - **UserName** *(string) --*
                The name of the IAM user that the access key is associated with.
              - **AccessKeyId** *(string) --*
                The ID for this access key.
              - **Status** *(string) --*
                The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
              - **SecretAccessKey** *(string) --*
                The secret key used to sign requests.
              - **CreateDate** *(datetime) --*
                The date when the access key was created.
        :type UserName: string
        :param UserName:
          The name of the IAM user that the new key will belong to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def create_account_alias(self, AccountAlias: str):
        """
        Creates an alias for your AWS account. For information about using an AWS account alias, see `Using an Alias for Your AWS Account ID <http://docs.aws.amazon.com/IAM/latest/UserGuide/AccountAlias.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateAccountAlias>`_

        **Request Syntax**
        ::
          response = client.create_account_alias(
              AccountAlias='string'
          )
        :type AccountAlias: string
        :param AccountAlias: **[REQUIRED]**
          The account alias to create.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of lowercase letters, digits, and dashes. You cannot start or finish with a dash, nor can you have two dashes in a row.
        :returns: None
        """
        pass

    def create_group(self, GroupName: str, Path: str = None) -> Dict:
        """
        Creates a new group.
        For information about the number of groups you can create, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateGroup>`_

        **Request Syntax**
        ::
          response = client.create_group(
              Path='string',
              GroupName='string'
          )

        **Response Syntax**
        ::
            {
                'Group': {
                    'Path': 'string',
                    'GroupName': 'string',
                    'GroupId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateGroup request.
            - **Group** *(dict) --*
              A structure containing details about the new group.
              - **Path** *(string) --*
                The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **GroupName** *(string) --*
                The friendly name that identifies the group.
              - **GroupId** *(string) --*
                The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the group. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the group was created.
        :type Path: string
        :param Path:
          The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group to create. Do not include the path in this value.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both \"ADMINS\" and \"admins\".
        :rtype: dict
        :returns:
        """
        pass

    def create_instance_profile(self, InstanceProfileName: str, Path: str = None) -> Dict:
        """
        Creates a new instance profile. For information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        For information about the number of instance profiles you can create, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateInstanceProfile>`_

        **Request Syntax**
        ::
          response = client.create_instance_profile(
              InstanceProfileName='string',
              Path='string'
          )

        **Response Syntax**
        ::
            {
                'InstanceProfile': {
                    'Path': 'string',
                    'InstanceProfileName': 'string',
                    'InstanceProfileId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'Roles': [
                        {
                            'Path': 'string',
                            'RoleName': 'string',
                            'RoleId': 'string',
                            'Arn': 'string',
                            'CreateDate': datetime(2015, 1, 1),
                            'AssumeRolePolicyDocument': 'string',
                            'Description': 'string',
                            'MaxSessionDuration': 123,
                            'PermissionsBoundary': {
                                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                'PermissionsBoundaryArn': 'string'
                            },
                            'Tags': [
                                {
                                    'Key': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateInstanceProfile request.
            - **InstanceProfile** *(dict) --*
              A structure containing details about the new instance profile.
              - **Path** *(string) --*
                The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **InstanceProfileName** *(string) --*
                The name identifying the instance profile.
              - **InstanceProfileId** *(string) --*
                The stable and unique string identifying the instance profile. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the instance profile. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date when the instance profile was created.
              - **Roles** *(list) --*
                The role associated with the instance profile.
                - *(dict) --*
                  Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                  - **Path** *(string) --*
                    The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **RoleName** *(string) --*
                    The friendly name that identifies the role.
                  - **RoleId** *(string) --*
                    The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **Arn** *(string) --*
                    The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                  - **CreateDate** *(datetime) --*
                    The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                  - **AssumeRolePolicyDocument** *(string) --*
                    The policy that grants an entity permission to assume the role.
                  - **Description** *(string) --*
                    A description of the role that you provide.
                  - **MaxSessionDuration** *(integer) --*
                    The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                  - **PermissionsBoundary** *(dict) --*
                    The ARN of the policy used to set the permissions boundary for the role.
                    For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                    - **PermissionsBoundaryType** *(string) --*
                      The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                    - **PermissionsBoundaryArn** *(string) --*
                      The ARN of the policy used to set the permissions boundary for the user or role.
                  - **Tags** *(list) --*
                    A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - *(dict) --*
                      A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                      - **Key** *(string) --*
                        The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                      - **Value** *(string) --*
                        The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                        .. note::
                          AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type InstanceProfileName: string
        :param InstanceProfileName: **[REQUIRED]**
          The name of the instance profile to create.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Path: string
        :param Path:
          The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :rtype: dict
        :returns:
        """
        pass

    def create_login_profile(self, UserName: str, Password: str, PasswordResetRequired: bool = None) -> Dict:
        """
        Creates a password for the specified user, giving the user the ability to access AWS services through the AWS Management Console. For more information about managing passwords, see `Managing Passwords <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateLoginProfile>`_

        **Request Syntax**
        ::
          response = client.create_login_profile(
              UserName='string',
              Password='string',
              PasswordResetRequired=True|False
          )

        **Response Syntax**
        ::
            {
                'LoginProfile': {
                    'UserName': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordResetRequired': True|False
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateLoginProfile request.
            - **LoginProfile** *(dict) --*
              A structure containing the user name and password create date.
              - **UserName** *(string) --*
                The name of the user, which can be used for signing in to the AWS Management Console.
              - **CreateDate** *(datetime) --*
                The date when the password for the user was created.
              - **PasswordResetRequired** *(boolean) --*
                Specifies whether the user is required to set a new password on next sign-in.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user to create a password for. The user must already exist.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Password: string
        :param Password: **[REQUIRED]**
          The new password for the user.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ that is used to validate this parameter is a string of characters. That string can include almost any printable ASCII character from the space (\u0020) through the end of the ASCII character range (\u00FF). You can also include the tab (\u0009), line feed (\u000A), and carriage return (\u000D) characters. Any of these characters are valid in a password. However, many tools, such as the AWS Management Console, might restrict the ability to type certain characters because they have special meaning within that tool.
        :type PasswordResetRequired: boolean
        :param PasswordResetRequired:
          Specifies whether the user is required to set a new password on next sign-in.
        :rtype: dict
        :returns:
        """
        pass

    def create_open_id_connect_provider(self, Url: str, ThumbprintList: List, ClientIDList: List = None) -> Dict:
        """
        Creates an IAM entity to describe an identity provider (IdP) that supports `OpenID Connect (OIDC) <http://openid.net/connect/>`__ .
        The OIDC provider that you create with this operation can be used as a principal in a role's trust policy. Such a policy establishes a trust relationship between AWS and the OIDC provider.
        When you create the IAM OIDC provider, you specify the following:
        * The URL of the OIDC identity provider (IdP) to trust
        * A list of client IDs (also known as audiences) that identify the application or applications that are allowed to authenticate using the OIDC provider
        * A list of thumbprints of the server certificate(s) that the IdP uses.
        You get all of this information from the OIDC IdP that you want to use to access AWS.
        .. note::
          Because trust for the OIDC provider is derived from the IAM provider that this operation creates, it is best to limit access to the  CreateOpenIDConnectProvider operation to highly privileged users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateOpenIDConnectProvider>`_

        **Request Syntax**
        ::
          response = client.create_open_id_connect_provider(
              Url='string',
              ClientIDList=[
                  'string',
              ],
              ThumbprintList=[
                  'string',
              ]
          )

        **Response Syntax**
        ::
            {
                'OpenIDConnectProviderArn': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateOpenIDConnectProvider request.
            - **OpenIDConnectProviderArn** *(string) --*
              The Amazon Resource Name (ARN) of the new IAM OpenID Connect provider that is created. For more information, see  OpenIDConnectProviderListEntry .
        :type Url: string
        :param Url: **[REQUIRED]**
          The URL of the identity provider. The URL must begin with ``https://`` and should correspond to the ``iss`` claim in the provider\'s OpenID Connect ID tokens. Per the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a hostname, like ``https://server.example.org`` or ``https://example.com`` .
          You cannot register the same provider multiple times in a single AWS account. If you try to submit a URL that has already been used for an OpenID Connect provider in the AWS account, you will get an error.
        :type ClientIDList: list
        :param ClientIDList:
          A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that\'s sent as the ``client_id`` parameter on OAuth requests.)
          You can register multiple client IDs with the same provider. For example, you might have multiple applications that use the same OIDC provider. You cannot register more than 100 client IDs with a single IAM OIDC provider.
          There is no defined format for a client ID. The ``CreateOpenIDConnectProviderRequest`` operation accepts client IDs up to 255 characters long.
          - *(string) --*
        :type ThumbprintList: list
        :param ThumbprintList: **[REQUIRED]**
          A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider\'s server certificates. Typically this list includes only one entry. However, IAM lets you have up to five thumbprints for an OIDC provider. This lets you maintain multiple thumbprints if the identity provider is rotating certificates.
          The server certificate thumbprint is the hex-encoded SHA-1 hash value of the X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string.
          You must provide at least one thumbprint when creating an IAM OIDC provider. For example, assume that the OIDC provider is ``server.example.com`` and the provider stores its keys at https://keys.server.example.com/openid-connect. In that case, the thumbprint string would be the hex-encoded SHA-1 hash value of the certificate used by https://keys.server.example.com.
          For more information about obtaining the OIDC provider\'s thumbprint, see `Obtaining the Thumbprint for an OpenID Connect Provider <http://docs.aws.amazon.com/IAM/latest/UserGuide/identity-providers-oidc-obtain-thumbprint.html>`__ in the *IAM User Guide* .
          - *(string) --*
            Contains a thumbprint for an identity provider\'s server certificate.
            The identity provider\'s server certificate thumbprint is the hex-encoded SHA-1 hash value of the self-signed X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string.
        :rtype: dict
        :returns:
        """
        pass

    def create_policy(self, PolicyName: str, PolicyDocument: str, Path: str = None, Description: str = None) -> Dict:
        """
        Creates a new managed policy for your AWS account.
        This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        For more information about managed policies in general, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreatePolicy>`_

        **Request Syntax**
        ::
          response = client.create_policy(
              PolicyName='string',
              Path='string',
              PolicyDocument='string',
              Description='string'
          )

        **Response Syntax**
        ::
            {
                'Policy': {
                    'PolicyName': 'string',
                    'PolicyId': 'string',
                    'Arn': 'string',
                    'Path': 'string',
                    'DefaultVersionId': 'string',
                    'AttachmentCount': 123,
                    'PermissionsBoundaryUsageCount': 123,
                    'IsAttachable': True|False,
                    'Description': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'UpdateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreatePolicy request.
            - **Policy** *(dict) --*
              A structure containing details about the new policy.
              - **PolicyName** *(string) --*
                The friendly name (not ARN) identifying the policy.
              - **PolicyId** *(string) --*
                The stable and unique string identifying the policy.
                For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
              - **Path** *(string) --*
                The path to the policy.
                For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **DefaultVersionId** *(string) --*
                The identifier for the version of the policy that is set as the default version.
              - **AttachmentCount** *(integer) --*
                The number of entities (users, groups, and roles) that the policy is attached to.
              - **PermissionsBoundaryUsageCount** *(integer) --*
                The number of entities (users and roles) for which the policy is used to set the permissions boundary.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
              - **IsAttachable** *(boolean) --*
                Specifies whether the policy can be attached to an IAM user, group, or role.
              - **Description** *(string) --*
                A friendly description of the policy.
                This element is included in the response to the  GetPolicy operation. It is not included in the response to the  ListPolicies operation.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was created.
              - **UpdateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was last updated.
                When a policy has only one version, this field contains the date and time when the policy was created. When a policy has more than one version, this field contains the date and time when the most recent policy version was created.
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The friendly name of the policy.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Path: string
        :param Path:
          The path for the policy.
          For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The JSON policy document that you want to use as the content for the new policy.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type Description: string
        :param Description:
          A friendly description of the policy.
          Typically used to store information about the permissions defined in the policy. For example, \"Grants access to production DynamoDB tables.\"
          The policy description is immutable. After a value is assigned, it cannot be changed.
        :rtype: dict
        :returns:
        """
        pass

    def create_policy_version(self, PolicyArn: str, PolicyDocument: str, SetAsDefault: bool = None) -> Dict:
        """
        Creates a new version of the specified managed policy. To update a managed policy, you create a new policy version. A managed policy can have up to five versions. If the policy has five versions, you must delete an existing version using  DeletePolicyVersion before you create a new version.
        Optionally, you can set the new version as the policy's default version. The default version is the version that is in effect for the IAM users, groups, and roles to which the policy is attached.
        For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreatePolicyVersion>`_

        **Request Syntax**
        ::
          response = client.create_policy_version(
              PolicyArn='string',
              PolicyDocument='string',
              SetAsDefault=True|False
          )

        **Response Syntax**
        ::
            {
                'PolicyVersion': {
                    'Document': 'string',
                    'VersionId': 'string',
                    'IsDefaultVersion': True|False,
                    'CreateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreatePolicyVersion request.
            - **PolicyVersion** *(dict) --*
              A structure containing details about the new policy version.
              - **Document** *(string) --*
                The policy document.
                The policy document is returned in the response to the  GetPolicyVersion and  GetAccountAuthorizationDetails operations. It is not returned in the response to the  CreatePolicyVersion or  ListPolicyVersions operations.
                The policy document returned in this structure is URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
              - **VersionId** *(string) --*
                The identifier for the policy version.
                Policy version identifiers always begin with ``v`` (always lowercase). When a policy is created, the first policy version is ``v1`` .
              - **IsDefaultVersion** *(boolean) --*
                Specifies whether the policy version is set as the policy's default version.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy version was created.
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy to which you want to add a new version.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The JSON policy document that you want to use as the content for this new version of the policy.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type SetAsDefault: boolean
        :param SetAsDefault:
          Specifies whether to set this version as the policy\'s default version.
          When this parameter is ``true`` , the new policy version becomes the operative version. That is, it becomes the version that is in effect for the IAM users, groups, and roles that the policy is attached to.
          For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        :rtype: dict
        :returns:
        """
        pass

    def create_role(self, RoleName: str, AssumeRolePolicyDocument: str, Path: str = None, Description: str = None,
                    MaxSessionDuration: int = None, PermissionsBoundary: str = None, Tags: List = None) -> Dict:
        """
        Creates a new role for your AWS account. For more information about roles, go to `IAM Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ . For information about limitations on role names and the number of roles you can create, go to `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateRole>`_

        **Request Syntax**
        ::
          response = client.create_role(
              Path='string',
              RoleName='string',
              AssumeRolePolicyDocument='string',
              Description='string',
              MaxSessionDuration=123,
              PermissionsBoundary='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )

        **Response Syntax**
        ::
            {
                'Role': {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string',
                    'MaxSessionDuration': 123,
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateRole request.
            - **Role** *(dict) --*
              A structure containing details about the new role.
              - **Path** *(string) --*
                The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **RoleName** *(string) --*
                The friendly name that identifies the role.
              - **RoleId** *(string) --*
                The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
              - **AssumeRolePolicyDocument** *(string) --*
                The policy that grants an entity permission to assume the role.
              - **Description** *(string) --*
                A description of the role that you provide.
              - **MaxSessionDuration** *(integer) --*
                The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the role.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type Path: string
        :param Path:
          The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to create.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
          Role names are not distinguished by case. For example, you cannot create roles named both \"PRODROLE\" and \"prodrole\".
        :type AssumeRolePolicyDocument: string
        :param AssumeRolePolicyDocument: **[REQUIRED]**
          The trust relationship policy document that grants an entity permission to assume the role.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type Description: string
        :param Description:
          A description of the role.
        :type MaxSessionDuration: integer
        :param MaxSessionDuration:
          The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default maximum of one hour is applied. This setting can have a value from 1 hour to 12 hours.
          Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don\'t specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`__ in the *IAM User Guide* .
        :type PermissionsBoundary: string
        :param PermissionsBoundary:
          The ARN of the policy that is used to set the permissions boundary for the role.
        :type Tags: list
        :param Tags:
          A list of tags that you want to attach to the newly created role. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
          .. note::
            If any one of the tags is invalid or if you exceed the allowed number of tags per role, then the entire request fails and the role is not created.
          - *(dict) --*
            A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
            - **Key** *(string) --* **[REQUIRED]**
              The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
            - **Value** *(string) --* **[REQUIRED]**
              The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
              .. note::
                AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :rtype: dict
        :returns:
        """
        pass

    def create_saml_provider(self, SAMLMetadataDocument: str, Name: str) -> Dict:
        """
        Creates an IAM resource that describes an identity provider (IdP) that supports SAML 2.0.
        The SAML provider resource that you create with this operation can be used as a principal in an IAM role's trust policy. Such a policy can enable federated users who sign-in using the SAML IdP to assume the role. You can create an IAM role that supports Web-based single sign-on (SSO) to the AWS Management Console or one that supports API access to AWS.
        When you create the SAML provider resource, you upload a SAML metadata document that you get from your IdP. That document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that the IdP sends. You must generate the metadata document using the identity management software that is used as your organization's IdP.
        .. note::
          This operation requires `Signature Version 4 <http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__ .
        For more information, see `Enabling SAML 2.0 Federated Users to Access the AWS Management Console <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-saml.html>`__ and `About SAML 2.0-based Federation <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateSAMLProvider>`_

        **Request Syntax**
        ::
          response = client.create_saml_provider(
              SAMLMetadataDocument='string',
              Name='string'
          )

        **Response Syntax**
        ::
            {
                'SAMLProviderArn': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateSAMLProvider request.
            - **SAMLProviderArn** *(string) --*
              The Amazon Resource Name (ARN) of the new SAML provider resource in IAM.
        :type SAMLMetadataDocument: string
        :param SAMLMetadataDocument: **[REQUIRED]**
          An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer\'s name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization\'s IdP.
          For more information, see `About SAML 2.0-based Federation <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`__ in the *IAM User Guide*
        :type Name: string
        :param Name: **[REQUIRED]**
          The name of the provider to create.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def create_service_linked_role(self, AWSServiceName: str, Description: str = None,
                                   CustomSuffix: str = None) -> Dict:
        """
        Creates an IAM role that is linked to a specific AWS service. The service controls the attached policies and when the role can be deleted. This helps ensure that the service is not broken by an unexpectedly changed or deleted role, which could put your AWS resources into an unknown state. Allowing the service to control the role helps improve service stability and proper cleanup when a service and its role are no longer needed. For more information, see `Using Service-Linked Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html>`__ in the *IAM User Guide* .
        To attach a policy to this service-linked role, you must make the request using the AWS service that depends on this role.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateServiceLinkedRole>`_

        **Request Syntax**
        ::
          response = client.create_service_linked_role(
              AWSServiceName='string',
              Description='string',
              CustomSuffix='string'
          )

        **Response Syntax**
        ::
            {
                'Role': {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string',
                    'MaxSessionDuration': 123,
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            - **Role** *(dict) --*
              A  Role object that contains details about the newly created role.
              - **Path** *(string) --*
                The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **RoleName** *(string) --*
                The friendly name that identifies the role.
              - **RoleId** *(string) --*
                The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
              - **AssumeRolePolicyDocument** *(string) --*
                The policy that grants an entity permission to assume the role.
              - **Description** *(string) --*
                A description of the role that you provide.
              - **MaxSessionDuration** *(integer) --*
                The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the role.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type AWSServiceName: string
        :param AWSServiceName: **[REQUIRED]**
          The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .
          Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS Services That Work with IAM <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`__ in the *IAM User Guide* and look for the services that have **Yes** in the **Service-Linked Role** column. Choose the **Yes** link to view the service-linked role documentation for that service.
        :type Description: string
        :param Description:
          The description of the role.
        :type CustomSuffix: string
        :param CustomSuffix:
          A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.
          Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :rtype: dict
        :returns:
        """
        pass

    def create_service_specific_credential(self, UserName: str, ServiceName: str) -> Dict:
        """
        Generates a set of credentials consisting of a user name and password that can be used to access the service specified in the request. These credentials are generated by IAM, and can be used only for the specified service.
        You can have a maximum of two sets of service-specific credentials for each supported service per user.
        The only supported service at this time is AWS CodeCommit.
        You can reset the password to a new service-generated value by calling  ResetServiceSpecificCredential .
        For more information about service-specific credentials, see `Using IAM with AWS CodeCommit\: Git Credentials, SSH Keys, and AWS Access Keys <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_ssh-keys.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateServiceSpecificCredential>`_

        **Request Syntax**
        ::
          response = client.create_service_specific_credential(
              UserName='string',
              ServiceName='string'
          )

        **Response Syntax**
        ::
            {
                'ServiceSpecificCredential': {
                    'CreateDate': datetime(2015, 1, 1),
                    'ServiceName': 'string',
                    'ServiceUserName': 'string',
                    'ServicePassword': 'string',
                    'ServiceSpecificCredentialId': 'string',
                    'UserName': 'string',
                    'Status': 'Active'|'Inactive'
                }
            }

        **Response Structure**
          - *(dict) --*
            - **ServiceSpecificCredential** *(dict) --*
              A structure that contains information about the newly created service-specific credential.
              .. warning::
                This is the only time that the password for this credential set is available. It cannot be recovered later. Instead, you will have to reset the password with  ResetServiceSpecificCredential .
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the service-specific credential were created.
              - **ServiceName** *(string) --*
                The name of the service associated with the service-specific credential.
              - **ServiceUserName** *(string) --*
                The generated user name for the service-specific credential. This value is generated by combining the IAM user's name combined with the ID number of the AWS account, as in ``jane-at-123456789012`` , for example. This value cannot be configured by the user.
              - **ServicePassword** *(string) --*
                The generated password for the service-specific credential.
              - **ServiceSpecificCredentialId** *(string) --*
                The unique identifier for the service-specific credential.
              - **UserName** *(string) --*
                The name of the IAM user associated with the service-specific credential.
              - **Status** *(string) --*
                The status of the service-specific credential. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user that is to be associated with the credentials. The new service-specific credentials have the same permissions as the associated user except that they can be used only to access the specified service.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type ServiceName: string
        :param ServiceName: **[REQUIRED]**
          The name of the AWS service that is to be associated with the credentials. The service you specify here is the only service that can be accessed using these credentials.
        :rtype: dict
        :returns:
        """
        pass

    def create_user(self, UserName: str, Path: str = None, PermissionsBoundary: str = None, Tags: List = None) -> Dict:
        """
        Creates a new IAM user for your AWS account.
        For information about limitations on the number of IAM users you can create, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateUser>`_

        **Request Syntax**
        ::
          response = client.create_user(
              Path='string',
              UserName='string',
              PermissionsBoundary='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )

        **Response Syntax**
        ::
            {
                'User': {
                    'Path': 'string',
                    'UserName': 'string',
                    'UserId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordLastUsed': datetime(2015, 1, 1),
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateUser request.
            - **User** *(dict) --*
              A structure with details about the new IAM user.
              - **Path** *(string) --*
                The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **UserName** *(string) --*
                The friendly name identifying the user.
              - **UserId** *(string) --*
                The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
              - **PasswordLastUsed** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                * The user never had a password.
                * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                This value is returned only in the  GetUser and  ListUsers operations.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the user.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type Path: string
        :param Path:
          The path for the user name. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to create.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. User names are not distinguished by case. For example, you cannot create users named both \"TESTUSER\" and \"testuser\".
        :type PermissionsBoundary: string
        :param PermissionsBoundary:
          The ARN of the policy that is used to set the permissions boundary for the user.
        :type Tags: list
        :param Tags:
          A list of tags that you want to attach to the newly created user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
          .. note::
            If any one of the tags is invalid or if you exceed the allowed number of tags per user, then the entire request fails and the user is not created.
          - *(dict) --*
            A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
            - **Key** *(string) --* **[REQUIRED]**
              The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
            - **Value** *(string) --* **[REQUIRED]**
              The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
              .. note::
                AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :rtype: dict
        :returns:
        """
        pass

    def create_virtual_mfa_device(self, VirtualMFADeviceName: str, Path: str = None) -> Dict:
        """
        Creates a new virtual MFA device for the AWS account. After creating the virtual MFA, use  EnableMFADevice to attach the MFA device to an IAM user. For more information about creating and working with virtual MFA devices, go to `Using a Virtual MFA Device <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`__ in the *IAM User Guide* .
        For information about limits on the number of MFA devices you can create, see `Limitations on Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        .. warning::
          The seed information contained in the QR code and the Base32 string should be treated like any other secret access information, such as your AWS access keys or your passwords. After you provision your virtual device, you should ensure that the information is destroyed following secure procedures.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/CreateVirtualMFADevice>`_

        **Request Syntax**
        ::
          response = client.create_virtual_mfa_device(
              Path='string',
              VirtualMFADeviceName='string'
          )

        **Response Syntax**
        ::
            {
                'VirtualMFADevice': {
                    'SerialNumber': 'string',
                    'Base32StringSeed': b'bytes',
                    'QRCodePNG': b'bytes',
                    'User': {
                        'Path': 'string',
                        'UserName': 'string',
                        'UserId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'PasswordLastUsed': datetime(2015, 1, 1),
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                    'EnableDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  CreateVirtualMFADevice request.
            - **VirtualMFADevice** *(dict) --*
              A structure containing details about the new virtual MFA device.
              - **SerialNumber** *(string) --*
                The serial number associated with ``VirtualMFADevice`` .
              - **Base32StringSeed** *(bytes) --*
                The base32 seed defined as specified in `RFC3548 <https://tools.ietf.org/html/rfc3548.txt>`__ . The ``Base32StringSeed`` is base64-encoded.
              - **QRCodePNG** *(bytes) --*
                A QR code PNG image that encodes ``otpauth://totp/$virtualMFADeviceName@$AccountName?secret=$Base32String`` where ``$virtualMFADeviceName`` is one of the create call arguments. ``AccountName`` is the user name if set (otherwise, the account ID otherwise), and ``Base32String`` is the seed in base32 format. The ``Base32String`` value is base64-encoded.
              - **User** *(dict) --*
                The IAM user associated with this virtual MFA device.
                - **Path** *(string) --*
                  The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UserName** *(string) --*
                  The friendly name identifying the user.
                - **UserId** *(string) --*
                  The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
                - **PasswordLastUsed** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                  * The user never had a password.
                  * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                  A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                  This value is returned only in the  GetUser and  ListUsers operations.
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the user.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
              - **EnableDate** *(datetime) --*
                The date and time on which the virtual MFA device was enabled.
        :type Path: string
        :param Path:
          The path for the virtual MFA device. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/).
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type VirtualMFADeviceName: string
        :param VirtualMFADeviceName: **[REQUIRED]**
          The name of the virtual MFA device. Use with path to uniquely identify a virtual MFA device.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def deactivate_mfa_device(self, UserName: str, SerialNumber: str):
        """
        Deactivates the specified MFA device and removes it from association with the user name for which it was originally enabled.
        For more information about creating and working with virtual MFA devices, go to `Enabling a Virtual Multi-factor Authentication (MFA) Device <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeactivateMFADevice>`_

        **Request Syntax**
        ::
          response = client.deactivate_mfa_device(
              UserName='string',
              SerialNumber='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user whose MFA device you want to deactivate.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SerialNumber: string
        :param SerialNumber: **[REQUIRED]**
          The serial number that uniquely identifies the MFA device. For virtual MFA devices, the serial number is the device ARN.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@:/-
        :returns: None
        """
        pass

    def delete_access_key(self, AccessKeyId: str, UserName: str = None):
        """
        Deletes the access key pair associated with the specified IAM user.
        If you do not specify a user name, IAM determines the user name implicitly based on the AWS access key ID signing the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteAccessKey>`_

        **Request Syntax**
        ::
          response = client.delete_access_key(
              UserName='string',
              AccessKeyId='string'
          )
        :type UserName: string
        :param UserName:
          The name of the user whose access key pair you want to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type AccessKeyId: string
        :param AccessKeyId: **[REQUIRED]**
          The access key ID for the access key ID and secret access key you want to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :returns: None
        """
        pass

    def delete_account_alias(self, AccountAlias: str):
        """
        Deletes the specified AWS account alias. For information about using an AWS account alias, see `Using an Alias for Your AWS Account ID <http://docs.aws.amazon.com/IAM/latest/UserGuide/AccountAlias.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteAccountAlias>`_

        **Request Syntax**
        ::
          response = client.delete_account_alias(
              AccountAlias='string'
          )
        :type AccountAlias: string
        :param AccountAlias: **[REQUIRED]**
          The name of the account alias to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of lowercase letters, digits, and dashes. You cannot start or finish with a dash, nor can you have two dashes in a row.
        :returns: None
        """
        pass

    def delete_account_password_policy(self):
        """
        Deletes the password policy for the AWS account. There are no parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteAccountPasswordPolicy>`_

        **Request Syntax**
        ::
          response = client.delete_account_password_policy()
        :returns: None
        """
        pass

    def delete_group(self, GroupName: str):
        """
        Deletes the specified IAM group. The group must not contain any users or have any attached policies.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteGroup>`_

        **Request Syntax**
        ::
          response = client.delete_group(
              GroupName='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the IAM group to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_group_policy(self, GroupName: str, PolicyName: str):
        """
        Deletes the specified inline policy that is embedded in the specified IAM group.
        A group can also have managed policies attached to it. To detach a managed policy from a group, use  DetachGroupPolicy . For more information about policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteGroupPolicy>`_

        **Request Syntax**
        ::
          response = client.delete_group_policy(
              GroupName='string',
              PolicyName='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name (friendly name, not ARN) identifying the group that the policy is embedded in.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name identifying the policy document to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_instance_profile(self, InstanceProfileName: str):
        """
        Deletes the specified instance profile. The instance profile must not have an associated role.
        .. warning::
          Make sure that you do not have any Amazon EC2 instances running with the instance profile you are about to delete. Deleting a role or instance profile that is associated with a running instance will break any applications running on the instance.
        For more information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteInstanceProfile>`_

        **Request Syntax**
        ::
          response = client.delete_instance_profile(
              InstanceProfileName='string'
          )
        :type InstanceProfileName: string
        :param InstanceProfileName: **[REQUIRED]**
          The name of the instance profile to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_login_profile(self, UserName: str):
        """
        Deletes the password for the specified IAM user, which terminates the user's ability to access AWS services through the AWS Management Console.
        .. warning::
          Deleting a user's password does not prevent a user from accessing AWS through the command line interface or the API. To prevent all user access, you must also either make any access keys inactive or delete them. For more information about making keys inactive or deleting them, see  UpdateAccessKey and  DeleteAccessKey .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteLoginProfile>`_

        **Request Syntax**
        ::
          response = client.delete_login_profile(
              UserName='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user whose password you want to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_open_id_connect_provider(self, OpenIDConnectProviderArn: str):
        """
        Deletes an OpenID Connect identity provider (IdP) resource object in IAM.
        Deleting an IAM OIDC provider resource does not update any roles that reference the provider as a principal in their trust policies. Any attempt to assume a role that references a deleted provider fails.
        This operation is idempotent; it does not fail or return an error if you call the operation for a provider that does not exist.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteOpenIDConnectProvider>`_

        **Request Syntax**
        ::
          response = client.delete_open_id_connect_provider(
              OpenIDConnectProviderArn='string'
          )
        :type OpenIDConnectProviderArn: string
        :param OpenIDConnectProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM OpenID Connect provider resource object to delete. You can get a list of OpenID Connect provider resource ARNs by using the  ListOpenIDConnectProviders operation.
        :returns: None
        """
        pass

    def delete_policy(self, PolicyArn: str):
        """
        Deletes the specified managed policy.
        Before you can delete a managed policy, you must first detach the policy from all users, groups, and roles that it is attached to. In addition, you must delete all the policy's versions. The following steps describe the process for deleting a managed policy:
        * Detach the policy from all users, groups, and roles that the policy is attached to, using the  DetachUserPolicy ,  DetachGroupPolicy , or  DetachRolePolicy API operations. To list all the users, groups, and roles that a policy is attached to, use  ListEntitiesForPolicy .
        * Delete all versions of the policy using  DeletePolicyVersion . To list the policy's versions, use  ListPolicyVersions . You cannot use  DeletePolicyVersion to delete the version that is marked as the default version. You delete the policy's default version in the next step of the process.
        * Delete the policy (this automatically deletes the policy's default version) using this API.
        For information about managed policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeletePolicy>`_

        **Request Syntax**
        ::
          response = client.delete_policy(
              PolicyArn='string'
          )
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to delete.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def delete_policy_version(self, PolicyArn: str, VersionId: str):
        """
        Deletes the specified version from the specified managed policy.
        You cannot delete the default version from a policy using this API. To delete the default version from a policy, use  DeletePolicy . To find out which version of a policy is marked as the default version, use  ListPolicyVersions .
        For information about versions for managed policies, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeletePolicyVersion>`_

        **Request Syntax**
        ::
          response = client.delete_policy_version(
              PolicyArn='string',
              VersionId='string'
          )
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy from which you want to delete a version.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type VersionId: string
        :param VersionId: **[REQUIRED]**
          The policy version to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consists of the lowercase letter \'v\' followed by one or two digits, and optionally followed by a period \'.\' and a string of letters and digits.
          For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        :returns: None
        """
        pass

    def delete_role(self, RoleName: str):
        """
        Deletes the specified role. The role must not have any policies attached. For more information about roles, go to `Working with Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ .
        .. warning::
          Make sure that you do not have any Amazon EC2 instances running with the role you are about to delete. Deleting a role or instance profile that is associated with a running instance will break any applications running on the instance.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteRole>`_

        **Request Syntax**
        ::
          response = client.delete_role(
              RoleName='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_role_permissions_boundary(self, RoleName: str):
        """
        Deletes the permissions boundary for the specified IAM role.
        .. warning::
          Deleting the permissions boundary for a role might increase its permissions by allowing anyone who assumes the role to perform all the actions granted in its permissions policies.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteRolePermissionsBoundary>`_

        **Request Syntax**
        ::
          response = client.delete_role_permissions_boundary(
              RoleName='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM role from which you want to remove the permissions boundary.
        :returns: None
        """
        pass

    def delete_role_policy(self, RoleName: str, PolicyName: str):
        """
        Deletes the specified inline policy that is embedded in the specified IAM role.
        A role can also have managed policies attached to it. To detach a managed policy from a role, use  DetachRolePolicy . For more information about policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteRolePolicy>`_

        **Request Syntax**
        ::
          response = client.delete_role_policy(
              RoleName='string',
              PolicyName='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) identifying the role that the policy is embedded in.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the inline policy to delete from the specified IAM role.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_saml_provider(self, SAMLProviderArn: str):
        """
        Deletes a SAML provider resource in IAM.
        Deleting the provider resource from IAM does not update any roles that reference the SAML provider resource's ARN as a principal in their trust policies. Any attempt to assume a role that references a non-existent provider resource ARN fails.
        .. note::
          This operation requires `Signature Version 4 <http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteSAMLProvider>`_

        **Request Syntax**
        ::
          response = client.delete_saml_provider(
              SAMLProviderArn='string'
          )
        :type SAMLProviderArn: string
        :param SAMLProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the SAML provider to delete.
        :returns: None
        """
        pass

    def delete_server_certificate(self, ServerCertificateName: str):
        """
        Deletes the specified server certificate.
        For more information about working with server certificates, see `Working with Server Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`__ in the *IAM User Guide* . This topic also includes a list of AWS services that can use the server certificates that you manage with IAM.
        .. warning::
          If you are using a server certificate with Elastic Load Balancing, deleting the certificate could have implications for your application. If Elastic Load Balancing doesn't detect the deletion of bound certificates, it may continue to use the certificates. This could cause Elastic Load Balancing to stop accepting traffic. We recommend that you remove the reference to the certificate from Elastic Load Balancing before using this command to delete the certificate. For more information, go to `DeleteLoadBalancerListeners <http://docs.aws.amazon.com/ElasticLoadBalancing/latest/APIReference/API_DeleteLoadBalancerListeners.html>`__ in the *Elastic Load Balancing API Reference* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteServerCertificate>`_

        **Request Syntax**
        ::
          response = client.delete_server_certificate(
              ServerCertificateName='string'
          )
        :type ServerCertificateName: string
        :param ServerCertificateName: **[REQUIRED]**
          The name of the server certificate you want to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_service_linked_role(self, RoleName: str) -> Dict:
        """
        Submits a service-linked role deletion request and returns a ``DeletionTaskId`` , which you can use to check the status of the deletion. Before you call this operation, confirm that the role has no active sessions and that any resources used by the role in the linked service are deleted. If you call this operation more than once for the same service-linked role and an earlier deletion task is not complete, then the ``DeletionTaskId`` of the earlier request is returned.
        If you submit a deletion request for a service-linked role whose linked service is still accessing a resource, then the deletion task fails. If it fails, the  GetServiceLinkedRoleDeletionStatus API operation returns the reason for the failure, usually including the resources that must be deleted. To delete the service-linked role, you must first remove those resources from the linked service and then submit the deletion request again. Resources are specific to the service that is linked to the role. For more information about removing resources from a service, see the `AWS documentation <http://docs.aws.amazon.com/>`__ for your service.
        For more information about service-linked roles, see `Roles Terms and Concepts\: AWS Service-Linked Role <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-linked-role>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteServiceLinkedRole>`_

        **Request Syntax**
        ::
          response = client.delete_service_linked_role(
              RoleName='string'
          )

        **Response Syntax**
        ::
            {
                'DeletionTaskId': 'string'
            }

        **Response Structure**
          - *(dict) --*
            - **DeletionTaskId** *(string) --*
              The deletion task identifier that you can use to check the status of the deletion. This identifier is returned in the format ``task/aws-service-role/<service-principal-name>/<role-name>/<task-uuid>`` .
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the service-linked role to be deleted.
        :rtype: dict
        :returns:
        """
        pass

    def delete_service_specific_credential(self, ServiceSpecificCredentialId: str, UserName: str = None):
        """
        Deletes the specified service-specific credential.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteServiceSpecificCredential>`_

        **Request Syntax**
        ::
          response = client.delete_service_specific_credential(
              UserName='string',
              ServiceSpecificCredentialId='string'
          )
        :type UserName: string
        :param UserName:
          The name of the IAM user associated with the service-specific credential. If this value is not specified, then the operation assumes the user whose credentials are used to call the operation.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type ServiceSpecificCredentialId: string
        :param ServiceSpecificCredentialId: **[REQUIRED]**
          The unique identifier of the service-specific credential. You can get this value by calling  ListServiceSpecificCredentials .
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :returns: None
        """
        pass

    def delete_signing_certificate(self, CertificateId: str, UserName: str = None):
        """
        Deletes a signing certificate associated with the specified IAM user.
        If you do not specify a user name, IAM determines the user name implicitly based on the AWS access key ID signing the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated IAM users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteSigningCertificate>`_

        **Request Syntax**
        ::
          response = client.delete_signing_certificate(
              UserName='string',
              CertificateId='string'
          )
        :type UserName: string
        :param UserName:
          The name of the user the signing certificate belongs to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type CertificateId: string
        :param CertificateId: **[REQUIRED]**
          The ID of the signing certificate to delete.
          The format of this parameter, as described by its `regex <http://wikipedia.org/wiki/regex>`__ pattern, is a string of characters that can be upper- or lower-cased letters or digits.
        :returns: None
        """
        pass

    def delete_ssh_public_key(self, UserName: str, SSHPublicKeyId: str):
        """
        Deletes the specified SSH public key.
        The SSH public key deleted by this operation is used only for authenticating the associated IAM user to an AWS CodeCommit repository. For more information about using SSH keys to authenticate to an AWS CodeCommit repository, see `Set up AWS CodeCommit for SSH Connections <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-credentials-ssh.html>`__ in the *AWS CodeCommit User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteSSHPublicKey>`_

        **Request Syntax**
        ::
          response = client.delete_ssh_public_key(
              UserName='string',
              SSHPublicKeyId='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user associated with the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SSHPublicKeyId: string
        :param SSHPublicKeyId: **[REQUIRED]**
          The unique identifier for the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :returns: None
        """
        pass

    def delete_user(self, UserName: str):
        """
        Deletes the specified IAM user. The user must not belong to any groups or have any access keys, signing certificates, MFA devices enabled for AWS, or attached policies.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteUser>`_

        **Request Syntax**
        ::
          response = client.delete_user(
              UserName='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_user_permissions_boundary(self, UserName: str):
        """
        Deletes the permissions boundary for the specified IAM user.
        .. warning::
          Deleting the permissions boundary for a user might increase its permissions by allowing the user to perform all the actions granted in its permissions policies.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteUserPermissionsBoundary>`_

        **Request Syntax**
        ::
          response = client.delete_user_permissions_boundary(
              UserName='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM user from which you want to remove the permissions boundary.
        :returns: None
        """
        pass

    def delete_user_policy(self, UserName: str, PolicyName: str):
        """
        Deletes the specified inline policy that is embedded in the specified IAM user.
        A user can also have managed policies attached to it. To detach a managed policy from a user, use  DetachUserPolicy . For more information about policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteUserPolicy>`_

        **Request Syntax**
        ::
          response = client.delete_user_policy(
              UserName='string',
              PolicyName='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) identifying the user that the policy is embedded in.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name identifying the policy document to delete.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def delete_virtual_mfa_device(self, SerialNumber: str):
        """
        Deletes a virtual MFA device.
        .. note::
          You must deactivate a user's virtual MFA device before you can delete it. For information about deactivating MFA devices, see  DeactivateMFADevice .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DeleteVirtualMFADevice>`_

        **Request Syntax**
        ::
          response = client.delete_virtual_mfa_device(
              SerialNumber='string'
          )
        :type SerialNumber: string
        :param SerialNumber: **[REQUIRED]**
          The serial number that uniquely identifies the MFA device. For virtual MFA devices, the serial number is the same as the ARN.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@:/-
        :returns: None
        """
        pass

    def detach_group_policy(self, GroupName: str, PolicyArn: str):
        """
        Removes the specified managed policy from the specified IAM group.
        A group can also have inline policies embedded with it. To delete an inline policy, use the  DeleteGroupPolicy API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DetachGroupPolicy>`_

        **Request Syntax**
        ::
          response = client.detach_group_policy(
              GroupName='string',
              PolicyArn='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM group to detach the policy from.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to detach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def detach_role_policy(self, RoleName: str, PolicyArn: str):
        """
        Removes the specified managed policy from the specified role.
        A role can also have inline policies embedded with it. To delete an inline policy, use the  DeleteRolePolicy API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DetachRolePolicy>`_

        **Request Syntax**
        ::
          response = client.detach_role_policy(
              RoleName='string',
              PolicyArn='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM role to detach the policy from.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to detach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def detach_user_policy(self, UserName: str, PolicyArn: str):
        """
        Removes the specified managed policy from the specified user.
        A user can also have inline policies embedded with it. To delete an inline policy, use the  DeleteUserPolicy API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/DetachUserPolicy>`_

        **Request Syntax**
        ::
          response = client.detach_user_policy(
              UserName='string',
              PolicyArn='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM user to detach the policy from.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy you want to detach.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :returns: None
        """
        pass

    def enable_mfa_device(self, UserName: str, SerialNumber: str, AuthenticationCode1: str, AuthenticationCode2: str):
        """
        Enables the specified MFA device and associates it with the specified IAM user. When enabled, the MFA device is required for every subsequent login by the IAM user associated with the device.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/EnableMFADevice>`_

        **Request Syntax**
        ::
          response = client.enable_mfa_device(
              UserName='string',
              SerialNumber='string',
              AuthenticationCode1='string',
              AuthenticationCode2='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user for whom you want to enable the MFA device.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SerialNumber: string
        :param SerialNumber: **[REQUIRED]**
          The serial number that uniquely identifies the MFA device. For virtual MFA devices, the serial number is the device ARN.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@:/-
        :type AuthenticationCode1: string
        :param AuthenticationCode1: **[REQUIRED]**
          An authentication code emitted by the device.
          The format for this parameter is a string of six digits.
          .. warning::
            Submit your request immediately after generating the authentication codes. If you generate the codes and then wait too long to submit the request, the MFA device successfully associates with the user but the MFA device becomes out of sync. This happens because time-based one-time passwords (TOTP) expire after a short period of time. If this happens, you can `resync the device <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_sync.html>`__ .
        :type AuthenticationCode2: string
        :param AuthenticationCode2: **[REQUIRED]**
          A subsequent authentication code emitted by the device.
          The format for this parameter is a string of six digits.
          .. warning::
            Submit your request immediately after generating the authentication codes. If you generate the codes and then wait too long to submit the request, the MFA device successfully associates with the user but the MFA device becomes out of sync. This happens because time-based one-time passwords (TOTP) expire after a short period of time. If this happens, you can `resync the device <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_sync.html>`__ .
        :returns: None
        """
        pass

    def generate_credential_report(self) -> Dict:
        """
        Generates a credential report for the AWS account. For more information about the credential report, see `Getting Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GenerateCredentialReport>`_

        **Request Syntax**
        ::
          response = client.generate_credential_report()

        **Response Syntax**
        ::
            {
                'State': 'STARTED'|'INPROGRESS'|'COMPLETE',
                'Description': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GenerateCredentialReport request.
            - **State** *(string) --*
              Information about the state of the credential report.
            - **Description** *(string) --*
              Information about the credential report.
        :rtype: dict
        :returns:
        """
        pass

    def generate_presigned_url(self, ClientMethod: str = None, Params: Dict = None, ExpiresIn: int = None,
                               HttpMethod: str = None):
        """
        Generate a presigned url given a client, its method, and arguments
        :type ClientMethod: string
        :param ClientMethod: The client method to presign for
        :type Params: dict
        :param Params: The parameters normally passed to
            ``ClientMethod``.
        :type ExpiresIn: int
        :param ExpiresIn: The number of seconds the presigned url is valid
            for. By default it expires in an hour (3600 seconds)
        :type HttpMethod: string
        :param HttpMethod: The http method to use on the generated url. By
            default, the http method is whatever is used in the method\'s model.
        :returns: The presigned url
        """
        pass

    def generate_service_last_accessed_details(self, Arn: str) -> Dict:
        """
        Generates a request for a report that includes details about when an IAM resource (user, group, role, or policy) was last used in an attempt to access AWS services. Recent activity usually appears within four hours. IAM reports activity for the last 365 days, or less if your region began supporting this feature within the last year. For more information, see `Regions Where Data Is Tracked <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html#access-advisor_tracking-period>`__ .
        .. warning::
          The service last accessed data includes all attempts to access an AWS API, not just the successful ones. This includes all attempts that were made using the AWS Management Console, the AWS API through any of the SDKs, or any of the command line tools. An unexpected entry in the service last accessed data does not mean that your account has been compromised, because the request might have been denied. Refer to your CloudTrail logs as the authoritative source for information about all API calls and whether they were successful or denied access. For more information, see `Logging IAM Events with CloudTrail <http://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html>`__ in the *IAM User Guide* .
        The ``GenerateServiceLastAccessedDetails`` operation returns a ``JobId`` . Use this parameter in the following operations to retrieve the following details from your report:
        *  GetServiceLastAccessedDetails – Use this operation for users, groups, roles, or policies to list every AWS service that the resource could access using permissions policies. For each service, the response includes information about the most recent access attempt.
        *  GetServiceLastAccessedDetailsWithEntities – Use this operation for groups and policies to list information about the associated entities (users or roles) that attempted to access a specific AWS service.
        To check the status of the ``GenerateServiceLastAccessedDetails`` request, use the ``JobId`` parameter in the same operations and test the ``JobStatus`` response parameter.
        For additional information about the permissions policies that allow an identity (user, group, or role) to access specific services, use the  ListPoliciesGrantingServiceAccess operation.
        .. note::
          Service last accessed data does not use other policy types when determining whether a resource could access a service. These other policy types include resource-based policies, access control lists, AWS Organizations policies, IAM permissions boundaries, and AWS STS assume role policies. It only applies permissions policy logic. For more about the evaluation of policy types, see `Evaluating Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html#policy-eval-basics>`__ in the *IAM User Guide* .
        For more information about service last accessed data, see `Reducing Policy Scope by Viewing User Activity <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GenerateServiceLastAccessedDetails>`_

        **Request Syntax**
        ::
          response = client.generate_service_last_accessed_details(
              Arn='string'
          )

        **Response Syntax**
        ::
            {
                'JobId': 'string'
            }

        **Response Structure**
          - *(dict) --*
            - **JobId** *(string) --*
              The job ID that you can use in the  GetServiceLastAccessedDetails or  GetServiceLastAccessedDetailsWithEntities operations.
        :type Arn: string
        :param Arn: **[REQUIRED]**
          The ARN of the IAM resource (user, group, role, or managed policy) used to generate information about when the resource was last used in an attempt to access an AWS service.
        :rtype: dict
        :returns:
        """
        pass

    def get_access_key_last_used(self, AccessKeyId: str) -> Dict:
        """
        Retrieves information about when the specified access key was last used. The information includes the date and time of last use, along with the AWS service and region that were specified in the last request made with that key.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetAccessKeyLastUsed>`_

        **Request Syntax**
        ::
          response = client.get_access_key_last_used(
              AccessKeyId='string'
          )

        **Response Syntax**
        ::
            {
                'UserName': 'string',
                'AccessKeyLastUsed': {
                    'LastUsedDate': datetime(2015, 1, 1),
                    'ServiceName': 'string',
                    'Region': 'string'
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetAccessKeyLastUsed request. It is also returned as a member of the  AccessKeyMetaData structure returned by the  ListAccessKeys action.
            - **UserName** *(string) --*
              The name of the AWS IAM user that owns this access key.
            - **AccessKeyLastUsed** *(dict) --*
              Contains information about the last time the access key was used.
              - **LastUsedDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the access key was most recently used. This field is null in the following situations:
                * The user does not have an access key.
                * An access key exists but has not been used since IAM began tracking this information.
                * There is no sign-in data associated with the user
              - **ServiceName** *(string) --*
                The name of the AWS service with which this access key was most recently used. The value of this field is "N/A" in the following situations:
                * The user does not have an access key.
                * An access key exists but has not been used since IAM started tracking this information.
                * There is no sign-in data associated with the user
              - **Region** *(string) --*
                The AWS region where this access key was most recently used. The value for this field is "N/A" in the following situations:
                * The user does not have an access key.
                * An access key exists but has not been used since IAM began tracking this information.
                * There is no sign-in data associated with the user
                For more information about AWS regions, see `Regions and Endpoints <http://docs.aws.amazon.com/general/latest/gr/rande.html>`__ in the Amazon Web Services General Reference.
        :type AccessKeyId: string
        :param AccessKeyId: **[REQUIRED]**
          The identifier of an access key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :rtype: dict
        :returns:
        """
        pass

    def get_account_authorization_details(self, Filter: List = None, MaxItems: int = None, Marker: str = None) -> Dict:
        """
        Retrieves information about all IAM users, groups, roles, and policies in your AWS account, including their relationships to one another. Use this API to obtain a snapshot of the configuration of IAM permissions (users, groups, roles, and policies) in your account.
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        You can optionally filter the results using the ``Filter`` parameter. You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetAccountAuthorizationDetails>`_

        **Request Syntax**
        ::
          response = client.get_account_authorization_details(
              Filter=[
                  'User'|'Role'|'Group'|'LocalManagedPolicy'|'AWSManagedPolicy',
              ],
              MaxItems=123,
              Marker='string'
          )

        **Response Syntax**
        ::
            {
                'UserDetailList': [
                    {
                        'Path': 'string',
                        'UserName': 'string',
                        'UserId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'UserPolicyList': [
                            {
                                'PolicyName': 'string',
                                'PolicyDocument': 'string'
                            },
                        ],
                        'GroupList': [
                            'string',
                        ],
                        'AttachedManagedPolicies': [
                            {
                                'PolicyName': 'string',
                                'PolicyArn': 'string'
                            },
                        ],
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                ],
                'GroupDetailList': [
                    {
                        'Path': 'string',
                        'GroupName': 'string',
                        'GroupId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'GroupPolicyList': [
                            {
                                'PolicyName': 'string',
                                'PolicyDocument': 'string'
                            },
                        ],
                        'AttachedManagedPolicies': [
                            {
                                'PolicyName': 'string',
                                'PolicyArn': 'string'
                            },
                        ]
                    },
                ],
                'RoleDetailList': [
                    {
                        'Path': 'string',
                        'RoleName': 'string',
                        'RoleId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'AssumeRolePolicyDocument': 'string',
                        'InstanceProfileList': [
                            {
                                'Path': 'string',
                                'InstanceProfileName': 'string',
                                'InstanceProfileId': 'string',
                                'Arn': 'string',
                                'CreateDate': datetime(2015, 1, 1),
                                'Roles': [
                                    {
                                        'Path': 'string',
                                        'RoleName': 'string',
                                        'RoleId': 'string',
                                        'Arn': 'string',
                                        'CreateDate': datetime(2015, 1, 1),
                                        'AssumeRolePolicyDocument': 'string',
                                        'Description': 'string',
                                        'MaxSessionDuration': 123,
                                        'PermissionsBoundary': {
                                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                            'PermissionsBoundaryArn': 'string'
                                        },
                                        'Tags': [
                                            {
                                                'Key': 'string',
                                                'Value': 'string'
                                            },
                                        ]
                                    },
                                ]
                            },
                        ],
                        'RolePolicyList': [
                            {
                                'PolicyName': 'string',
                                'PolicyDocument': 'string'
                            },
                        ],
                        'AttachedManagedPolicies': [
                            {
                                'PolicyName': 'string',
                                'PolicyArn': 'string'
                            },
                        ],
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                ],
                'Policies': [
                    {
                        'PolicyName': 'string',
                        'PolicyId': 'string',
                        'Arn': 'string',
                        'Path': 'string',
                        'DefaultVersionId': 'string',
                        'AttachmentCount': 123,
                        'PermissionsBoundaryUsageCount': 123,
                        'IsAttachable': True|False,
                        'Description': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'UpdateDate': datetime(2015, 1, 1),
                        'PolicyVersionList': [
                            {
                                'Document': 'string',
                                'VersionId': 'string',
                                'IsDefaultVersion': True|False,
                                'CreateDate': datetime(2015, 1, 1)
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetAccountAuthorizationDetails request.
            - **UserDetailList** *(list) --*
              A list containing information about IAM users.
              - *(dict) --*
                Contains information about an IAM user, including all the user's policies and all the IAM groups the user is in.
                This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                - **Path** *(string) --*
                  The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UserName** *(string) --*
                  The friendly name identifying the user.
                - **UserId** *(string) --*
                  The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
                - **UserPolicyList** *(list) --*
                  A list of the inline policies embedded in the user.
                  - *(dict) --*
                    Contains information about an IAM policy, including the policy document.
                    This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                    - **PolicyName** *(string) --*
                      The name of the policy.
                    - **PolicyDocument** *(string) --*
                      The policy document.
                - **GroupList** *(list) --*
                  A list of IAM groups that the user is in.
                  - *(string) --*
                - **AttachedManagedPolicies** *(list) --*
                  A list of the managed policies attached to the user.
                  - *(dict) --*
                    Contains information about an attached policy.
                    An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                    For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                    - **PolicyName** *(string) --*
                      The friendly name of the attached policy.
                    - **PolicyArn** *(string) --*
                      The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                      For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the user.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **GroupDetailList** *(list) --*
              A list containing information about IAM groups.
              - *(dict) --*
                Contains information about an IAM group, including all of the group's policies.
                This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                - **Path** *(string) --*
                  The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **GroupName** *(string) --*
                  The friendly name that identifies the group.
                - **GroupId** *(string) --*
                  The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the group was created.
                - **GroupPolicyList** *(list) --*
                  A list of the inline policies embedded in the group.
                  - *(dict) --*
                    Contains information about an IAM policy, including the policy document.
                    This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                    - **PolicyName** *(string) --*
                      The name of the policy.
                    - **PolicyDocument** *(string) --*
                      The policy document.
                - **AttachedManagedPolicies** *(list) --*
                  A list of the managed policies attached to the group.
                  - *(dict) --*
                    Contains information about an attached policy.
                    An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                    For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                    - **PolicyName** *(string) --*
                      The friendly name of the attached policy.
                    - **PolicyArn** *(string) --*
                      The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                      For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
            - **RoleDetailList** *(list) --*
              A list containing information about IAM roles.
              - *(dict) --*
                Contains information about an IAM role, including all of the role's policies.
                This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                - **Path** *(string) --*
                  The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **RoleName** *(string) --*
                  The friendly name that identifies the role.
                - **RoleId** *(string) --*
                  The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                - **AssumeRolePolicyDocument** *(string) --*
                  The trust policy that grants permission to assume the role.
                - **InstanceProfileList** *(list) --*
                  A list of instance profiles that contain this role.
                  - *(dict) --*
                    Contains information about an instance profile.
                    This data type is used as a response element in the following operations:
                    *  CreateInstanceProfile
                    *  GetInstanceProfile
                    *  ListInstanceProfiles
                    *  ListInstanceProfilesForRole
                    - **Path** *(string) --*
                      The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **InstanceProfileName** *(string) --*
                      The name identifying the instance profile.
                    - **InstanceProfileId** *(string) --*
                      The stable and unique string identifying the instance profile. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **Arn** *(string) --*
                      The Amazon Resource Name (ARN) specifying the instance profile. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **CreateDate** *(datetime) --*
                      The date when the instance profile was created.
                    - **Roles** *(list) --*
                      The role associated with the instance profile.
                      - *(dict) --*
                        Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                        - **Path** *(string) --*
                          The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                        - **RoleName** *(string) --*
                          The friendly name that identifies the role.
                        - **RoleId** *(string) --*
                          The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                        - **Arn** *(string) --*
                          The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                        - **CreateDate** *(datetime) --*
                          The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                        - **AssumeRolePolicyDocument** *(string) --*
                          The policy that grants an entity permission to assume the role.
                        - **Description** *(string) --*
                          A description of the role that you provide.
                        - **MaxSessionDuration** *(integer) --*
                          The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                        - **PermissionsBoundary** *(dict) --*
                          The ARN of the policy used to set the permissions boundary for the role.
                          For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                          - **PermissionsBoundaryType** *(string) --*
                            The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                          - **PermissionsBoundaryArn** *(string) --*
                            The ARN of the policy used to set the permissions boundary for the user or role.
                        - **Tags** *(list) --*
                          A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                          - *(dict) --*
                            A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                            - **Key** *(string) --*
                              The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                            - **Value** *(string) --*
                              The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                              .. note::
                                AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
                - **RolePolicyList** *(list) --*
                  A list of inline policies embedded in the role. These policies are the role's access (permissions) policies.
                  - *(dict) --*
                    Contains information about an IAM policy, including the policy document.
                    This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                    - **PolicyName** *(string) --*
                      The name of the policy.
                    - **PolicyDocument** *(string) --*
                      The policy document.
                - **AttachedManagedPolicies** *(list) --*
                  A list of managed policies attached to the role. These policies are the role's access (permissions) policies.
                  - *(dict) --*
                    Contains information about an attached policy.
                    An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                    For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                    - **PolicyName** *(string) --*
                      The friendly name of the attached policy.
                    - **PolicyArn** *(string) --*
                      The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                      For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the role.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **Policies** *(list) --*
              A list containing information about managed policies.
              - *(dict) --*
                Contains information about a managed policy, including the policy's ARN, versions, and the number of principal entities (users, groups, and roles) that the policy is attached to.
                This data type is used as a response element in the  GetAccountAuthorizationDetails operation.
                For more information about managed policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **PolicyName** *(string) --*
                  The friendly name (not ARN) identifying the policy.
                - **PolicyId** *(string) --*
                  The stable and unique string identifying the policy.
                  For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **Path** *(string) --*
                  The path to the policy.
                  For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **DefaultVersionId** *(string) --*
                  The identifier for the version of the policy that is set as the default (operative) version.
                  For more information about policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *Using IAM* guide.
                - **AttachmentCount** *(integer) --*
                  The number of principal entities (users, groups, and roles) that the policy is attached to.
                - **PermissionsBoundaryUsageCount** *(integer) --*
                  The number of entities (users and roles) for which the policy is used as the permissions boundary.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **IsAttachable** *(boolean) --*
                  Specifies whether the policy can be attached to an IAM user, group, or role.
                - **Description** *(string) --*
                  A friendly description of the policy.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was created.
                - **UpdateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was last updated.
                  When a policy has only one version, this field contains the date and time when the policy was created. When a policy has more than one version, this field contains the date and time when the most recent policy version was created.
                - **PolicyVersionList** *(list) --*
                  A list containing information about the versions of the policy.
                  - *(dict) --*
                    Contains information about a version of a managed policy.
                    This data type is used as a response element in the  CreatePolicyVersion ,  GetPolicyVersion ,  ListPolicyVersions , and  GetAccountAuthorizationDetails operations.
                    For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                    - **Document** *(string) --*
                      The policy document.
                      The policy document is returned in the response to the  GetPolicyVersion and  GetAccountAuthorizationDetails operations. It is not returned in the response to the  CreatePolicyVersion or  ListPolicyVersions operations.
                      The policy document returned in this structure is URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
                    - **VersionId** *(string) --*
                      The identifier for the policy version.
                      Policy version identifiers always begin with ``v`` (always lowercase). When a policy is created, the first policy version is ``v1`` .
                    - **IsDefaultVersion** *(boolean) --*
                      Specifies whether the policy version is set as the policy's default version.
                    - **CreateDate** *(datetime) --*
                      The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy version was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type Filter: list
        :param Filter:
          A list of entity types used to filter the results. Only the entities that match the types you specify are included in the output. Use the value ``LocalManagedPolicy`` to include customer managed policies.
          The format for this parameter is a comma-separated (if more than one) list of strings. Each string value in the list must be one of the valid values listed below.
          - *(string) --*
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :rtype: dict
        :returns:
        """
        pass

    def get_account_password_policy(self) -> Dict:
        """
        Retrieves the password policy for the AWS account. For more information about using a password policy, go to `Managing an IAM Password Policy <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingPasswordPolicies.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetAccountPasswordPolicy>`_

        **Request Syntax**
        ::
          response = client.get_account_password_policy()

        **Response Syntax**
        ::
            {
                'PasswordPolicy': {
                    'MinimumPasswordLength': 123,
                    'RequireSymbols': True|False,
                    'RequireNumbers': True|False,
                    'RequireUppercaseCharacters': True|False,
                    'RequireLowercaseCharacters': True|False,
                    'AllowUsersToChangePassword': True|False,
                    'ExpirePasswords': True|False,
                    'MaxPasswordAge': 123,
                    'PasswordReusePrevention': 123,
                    'HardExpiry': True|False
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetAccountPasswordPolicy request.
            - **PasswordPolicy** *(dict) --*
              A structure that contains details about the account's password policy.
              - **MinimumPasswordLength** *(integer) --*
                Minimum length to require for IAM user passwords.
              - **RequireSymbols** *(boolean) --*
                Specifies whether to require symbols for IAM user passwords.
              - **RequireNumbers** *(boolean) --*
                Specifies whether to require numbers for IAM user passwords.
              - **RequireUppercaseCharacters** *(boolean) --*
                Specifies whether to require uppercase characters for IAM user passwords.
              - **RequireLowercaseCharacters** *(boolean) --*
                Specifies whether to require lowercase characters for IAM user passwords.
              - **AllowUsersToChangePassword** *(boolean) --*
                Specifies whether IAM users are allowed to change their own password.
              - **ExpirePasswords** *(boolean) --*
                Indicates whether passwords in the account expire. Returns true if ``MaxPasswordAge`` contains a value greater than 0. Returns false if MaxPasswordAge is 0 or not present.
              - **MaxPasswordAge** *(integer) --*
                The number of days that an IAM user password is valid.
              - **PasswordReusePrevention** *(integer) --*
                Specifies the number of previous passwords that IAM users are prevented from reusing.
              - **HardExpiry** *(boolean) --*
                Specifies whether IAM users are prevented from setting a new password after their password has expired.
        :rtype: dict
        :returns:
        """
        pass

    def get_account_summary(self) -> Dict:
        """
        Retrieves information about IAM entity usage and IAM quotas in the AWS account.
        For information about limitations on IAM entities, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetAccountSummary>`_

        **Request Syntax**
        ::
          response = client.get_account_summary()

        **Response Syntax**
        ::
            {
                'SummaryMap': {
                    'string': 123
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetAccountSummary request.
            - **SummaryMap** *(dict) --*
              A set of key–value pairs containing information about IAM entity usage and IAM quotas.
              - *(string) --*
                - *(integer) --*
        :rtype: dict
        :returns:
        """
        pass

    def get_context_keys_for_custom_policy(self, PolicyInputList: List) -> Dict:
        """
        Gets a list of all of the context keys referenced in the input policies. The policies are supplied as a list of one or more strings. To get the context keys from policies associated with an IAM user, group, or role, use  GetContextKeysForPrincipalPolicy .
        Context keys are variables maintained by AWS and its services that provide details about the context of an API query request. Context keys can be evaluated by testing against a value specified in an IAM policy. Use ``GetContextKeysForCustomPolicy`` to understand what key names and values you must supply when you call  SimulateCustomPolicy . Note that all parameters are shown in unencoded form here for clarity but must be URL encoded to be included as a part of a real HTML request.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetContextKeysForCustomPolicy>`_

        **Request Syntax**
        ::
          response = client.get_context_keys_for_custom_policy(
              PolicyInputList=[
                  'string',
              ]
          )

        **Response Syntax**
        ::
            {
                'ContextKeyNames': [
                    'string',
                ]
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetContextKeysForPrincipalPolicy or  GetContextKeysForCustomPolicy request.
            - **ContextKeyNames** *(list) --*
              The list of context keys that are referenced in the input policies.
              - *(string) --*
        :type PolicyInputList: list
        :param PolicyInputList: **[REQUIRED]**
          A list of policies for which you want the list of context keys referenced in those policies. Each document is specified as a string containing the complete, valid JSON text of an IAM policy.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
          - *(string) --*
        :rtype: dict
        :returns:
        """
        pass

    def get_context_keys_for_principal_policy(self, PolicySourceArn: str, PolicyInputList: List = None) -> Dict:
        """
        Gets a list of all of the context keys referenced in all the IAM policies that are attached to the specified IAM entity. The entity can be an IAM user, group, or role. If you specify a user, then the request also includes all of the policies attached to groups that the user is a member of.
        You can optionally include a list of one or more additional policies, specified as strings. If you want to include *only* a list of policies by string, use  GetContextKeysForCustomPolicy instead.
         **Note:** This API discloses information about the permissions granted to other users. If you do not want users to see other user's permissions, then consider allowing them to use  GetContextKeysForCustomPolicy instead.
        Context keys are variables maintained by AWS and its services that provide details about the context of an API query request. Context keys can be evaluated by testing against a value in an IAM policy. Use  GetContextKeysForPrincipalPolicy to understand what key names and values you must supply when you call  SimulatePrincipalPolicy .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetContextKeysForPrincipalPolicy>`_

        **Request Syntax**
        ::
          response = client.get_context_keys_for_principal_policy(
              PolicySourceArn='string',
              PolicyInputList=[
                  'string',
              ]
          )

        **Response Syntax**
        ::
            {
                'ContextKeyNames': [
                    'string',
                ]
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetContextKeysForPrincipalPolicy or  GetContextKeysForCustomPolicy request.
            - **ContextKeyNames** *(list) --*
              The list of context keys that are referenced in the input policies.
              - *(string) --*
        :type PolicySourceArn: string
        :param PolicySourceArn: **[REQUIRED]**
          The ARN of a user, group, or role whose policies contain the context keys that you want listed. If you specify a user, the list includes context keys that are found in all policies that are attached to the user. The list also includes all groups that the user is a member of. If you pick a group or a role, then it includes only those context keys that are found in policies attached to that entity. Note that all parameters are shown in unencoded form here for clarity, but must be URL encoded to be included as a part of a real HTML request.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type PolicyInputList: list
        :param PolicyInputList:
          An optional list of additional policies for which you want the list of context keys that are referenced.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
          - *(string) --*
        :rtype: dict
        :returns:
        """
        pass

    def get_credential_report(self) -> Dict:
        """
        Retrieves a credential report for the AWS account. For more information about the credential report, see `Getting Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetCredentialReport>`_

        **Request Syntax**
        ::
          response = client.get_credential_report()

        **Response Syntax**
        ::
            {
                'Content': b'bytes',
                'ReportFormat': 'text/csv',
                'GeneratedTime': datetime(2015, 1, 1)
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetCredentialReport request.
            - **Content** *(bytes) --*
              Contains the credential report. The report is Base64-encoded.
            - **ReportFormat** *(string) --*
              The format (MIME type) of the credential report.
            - **GeneratedTime** *(datetime) --*
              The date and time when the credential report was created, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ .
        :rtype: dict
        :returns:
        """
        pass

    def get_group(self, GroupName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Returns a list of IAM users that are in the specified IAM group. You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetGroup>`_

        **Request Syntax**
        ::
          response = client.get_group(
              GroupName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Group': {
                    'Path': 'string',
                    'GroupName': 'string',
                    'GroupId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1)
                },
                'Users': [
                    {
                        'Path': 'string',
                        'UserName': 'string',
                        'UserId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'PasswordLastUsed': datetime(2015, 1, 1),
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetGroup request.
            - **Group** *(dict) --*
              A structure that contains details about the group.
              - **Path** *(string) --*
                The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **GroupName** *(string) --*
                The friendly name that identifies the group.
              - **GroupId** *(string) --*
                The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the group. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the group was created.
            - **Users** *(list) --*
              A list of users in the group.
              - *(dict) --*
                Contains information about an IAM user entity.
                This data type is used as a response element in the following operations:
                *  CreateUser
                *  GetUser
                *  ListUsers
                - **Path** *(string) --*
                  The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UserName** *(string) --*
                  The friendly name identifying the user.
                - **UserId** *(string) --*
                  The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
                - **PasswordLastUsed** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                  * The user never had a password.
                  * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                  A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                  This value is returned only in the  GetUser and  ListUsers operations.
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the user.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def get_group_policy(self, GroupName: str, PolicyName: str) -> Dict:
        """
        Retrieves the specified inline policy document that is embedded in the specified IAM group.
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        An IAM group can also have managed policies attached to it. To retrieve a managed policy document that is attached to a group, use  GetPolicy to determine the policy's default version, then use  GetPolicyVersion to retrieve the policy document.
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetGroupPolicy>`_

        **Request Syntax**
        ::
          response = client.get_group_policy(
              GroupName='string',
              PolicyName='string'
          )

        **Response Syntax**
        ::
            {
                'GroupName': 'string',
                'PolicyName': 'string',
                'PolicyDocument': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetGroupPolicy request.
            - **GroupName** *(string) --*
              The group the policy is associated with.
            - **PolicyName** *(string) --*
              The name of the policy.
            - **PolicyDocument** *(string) --*
              The policy document.
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group the policy is associated with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document to get.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_instance_profile(self, InstanceProfileName: str) -> Dict:
        """
        Retrieves information about the specified instance profile, including the instance profile's path, GUID, ARN, and role. For more information about instance profiles, see `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetInstanceProfile>`_

        **Request Syntax**
        ::
          response = client.get_instance_profile(
              InstanceProfileName='string'
          )

        **Response Syntax**
        ::
            {
                'InstanceProfile': {
                    'Path': 'string',
                    'InstanceProfileName': 'string',
                    'InstanceProfileId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'Roles': [
                        {
                            'Path': 'string',
                            'RoleName': 'string',
                            'RoleId': 'string',
                            'Arn': 'string',
                            'CreateDate': datetime(2015, 1, 1),
                            'AssumeRolePolicyDocument': 'string',
                            'Description': 'string',
                            'MaxSessionDuration': 123,
                            'PermissionsBoundary': {
                                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                'PermissionsBoundaryArn': 'string'
                            },
                            'Tags': [
                                {
                                    'Key': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetInstanceProfile request.
            - **InstanceProfile** *(dict) --*
              A structure containing details about the instance profile.
              - **Path** *(string) --*
                The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **InstanceProfileName** *(string) --*
                The name identifying the instance profile.
              - **InstanceProfileId** *(string) --*
                The stable and unique string identifying the instance profile. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the instance profile. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date when the instance profile was created.
              - **Roles** *(list) --*
                The role associated with the instance profile.
                - *(dict) --*
                  Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                  - **Path** *(string) --*
                    The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **RoleName** *(string) --*
                    The friendly name that identifies the role.
                  - **RoleId** *(string) --*
                    The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **Arn** *(string) --*
                    The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                  - **CreateDate** *(datetime) --*
                    The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                  - **AssumeRolePolicyDocument** *(string) --*
                    The policy that grants an entity permission to assume the role.
                  - **Description** *(string) --*
                    A description of the role that you provide.
                  - **MaxSessionDuration** *(integer) --*
                    The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                  - **PermissionsBoundary** *(dict) --*
                    The ARN of the policy used to set the permissions boundary for the role.
                    For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                    - **PermissionsBoundaryType** *(string) --*
                      The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                    - **PermissionsBoundaryArn** *(string) --*
                      The ARN of the policy used to set the permissions boundary for the user or role.
                  - **Tags** *(list) --*
                    A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - *(dict) --*
                      A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                      - **Key** *(string) --*
                        The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                      - **Value** *(string) --*
                        The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                        .. note::
                          AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type InstanceProfileName: string
        :param InstanceProfileName: **[REQUIRED]**
          The name of the instance profile to get information about.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_login_profile(self, UserName: str) -> Dict:
        """
        Retrieves the user name and password-creation date for the specified IAM user. If the user has not been assigned a password, the operation returns a 404 (``NoSuchEntity`` ) error.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetLoginProfile>`_

        **Request Syntax**
        ::
          response = client.get_login_profile(
              UserName='string'
          )

        **Response Syntax**
        ::
            {
                'LoginProfile': {
                    'UserName': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordResetRequired': True|False
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetLoginProfile request.
            - **LoginProfile** *(dict) --*
              A structure containing the user name and password create date for the user.
              - **UserName** *(string) --*
                The name of the user, which can be used for signing in to the AWS Management Console.
              - **CreateDate** *(datetime) --*
                The date when the password for the user was created.
              - **PasswordResetRequired** *(boolean) --*
                Specifies whether the user is required to set a new password on next sign-in.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user whose login profile you want to retrieve.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_open_id_connect_provider(self, OpenIDConnectProviderArn: str) -> Dict:
        """
        Returns information about the specified OpenID Connect (OIDC) provider resource object in IAM.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetOpenIDConnectProvider>`_

        **Request Syntax**
        ::
          response = client.get_open_id_connect_provider(
              OpenIDConnectProviderArn='string'
          )

        **Response Syntax**
        ::
            {
                'Url': 'string',
                'ClientIDList': [
                    'string',
                ],
                'ThumbprintList': [
                    'string',
                ],
                'CreateDate': datetime(2015, 1, 1)
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetOpenIDConnectProvider request.
            - **Url** *(string) --*
              The URL that the IAM OIDC provider resource object is associated with. For more information, see  CreateOpenIDConnectProvider .
            - **ClientIDList** *(list) --*
              A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see  CreateOpenIDConnectProvider .
              - *(string) --*
            - **ThumbprintList** *(list) --*
              A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see  CreateOpenIDConnectProvider .
              - *(string) --*
                Contains a thumbprint for an identity provider's server certificate.
                The identity provider's server certificate thumbprint is the hex-encoded SHA-1 hash value of the self-signed X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string.
            - **CreateDate** *(datetime) --*
              The date and time when the IAM OIDC provider resource object was created in the AWS account.
        :type OpenIDConnectProviderArn: string
        :param OpenIDConnectProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the OIDC provider resource object in IAM to get information for. You can get a list of OIDC provider resource ARNs by using the  ListOpenIDConnectProviders operation.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :rtype: dict
        :returns:
        """
        pass

    def get_paginator(self, operation_name: str = None) -> Paginator:
        """
        Create a paginator for an operation.
        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you\'d normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator(\"create_foo\")``.
        :raise OperationNotPageableError: Raised if the operation is not
            pageable.  You can use the ``client.can_paginate`` method to
            check if an operation is pageable.
        :rtype: L{botocore.paginate.Paginator}
        :return: A paginator object.
        """
        pass

    def get_policy(self, PolicyArn: str) -> Dict:
        """
        Retrieves information about the specified managed policy, including the policy's default version and the total number of IAM users, groups, and roles to which the policy is attached. To retrieve the list of the specific users, groups, and roles that the policy is attached to, use the  ListEntitiesForPolicy API. This API returns metadata about the policy. To retrieve the actual policy document for a specific version of the policy, use  GetPolicyVersion .
        This API retrieves information about managed policies. To retrieve information about an inline policy that is embedded with an IAM user, group, or role, use the  GetUserPolicy ,  GetGroupPolicy , or  GetRolePolicy API.
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetPolicy>`_

        **Request Syntax**
        ::
          response = client.get_policy(
              PolicyArn='string'
          )

        **Response Syntax**
        ::
            {
                'Policy': {
                    'PolicyName': 'string',
                    'PolicyId': 'string',
                    'Arn': 'string',
                    'Path': 'string',
                    'DefaultVersionId': 'string',
                    'AttachmentCount': 123,
                    'PermissionsBoundaryUsageCount': 123,
                    'IsAttachable': True|False,
                    'Description': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'UpdateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetPolicy request.
            - **Policy** *(dict) --*
              A structure containing details about the policy.
              - **PolicyName** *(string) --*
                The friendly name (not ARN) identifying the policy.
              - **PolicyId** *(string) --*
                The stable and unique string identifying the policy.
                For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
              - **Path** *(string) --*
                The path to the policy.
                For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **DefaultVersionId** *(string) --*
                The identifier for the version of the policy that is set as the default version.
              - **AttachmentCount** *(integer) --*
                The number of entities (users, groups, and roles) that the policy is attached to.
              - **PermissionsBoundaryUsageCount** *(integer) --*
                The number of entities (users and roles) for which the policy is used to set the permissions boundary.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
              - **IsAttachable** *(boolean) --*
                Specifies whether the policy can be attached to an IAM user, group, or role.
              - **Description** *(string) --*
                A friendly description of the policy.
                This element is included in the response to the  GetPolicy operation. It is not included in the response to the  ListPolicies operation.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was created.
              - **UpdateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was last updated.
                When a policy has only one version, this field contains the date and time when the policy was created. When a policy has more than one version, this field contains the date and time when the most recent policy version was created.
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the managed policy that you want information about.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :rtype: dict
        :returns:
        """
        pass

    def get_policy_version(self, PolicyArn: str, VersionId: str) -> Dict:
        """
        Retrieves information about the specified version of the specified managed policy, including the policy document.
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        To list the available versions for a policy, use  ListPolicyVersions .
        This API retrieves information about managed policies. To retrieve information about an inline policy that is embedded in a user, group, or role, use the  GetUserPolicy ,  GetGroupPolicy , or  GetRolePolicy API.
        For more information about the types of policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetPolicyVersion>`_

        **Request Syntax**
        ::
          response = client.get_policy_version(
              PolicyArn='string',
              VersionId='string'
          )

        **Response Syntax**
        ::
            {
                'PolicyVersion': {
                    'Document': 'string',
                    'VersionId': 'string',
                    'IsDefaultVersion': True|False,
                    'CreateDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetPolicyVersion request.
            - **PolicyVersion** *(dict) --*
              A structure containing details about the policy version.
              - **Document** *(string) --*
                The policy document.
                The policy document is returned in the response to the  GetPolicyVersion and  GetAccountAuthorizationDetails operations. It is not returned in the response to the  CreatePolicyVersion or  ListPolicyVersions operations.
                The policy document returned in this structure is URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
              - **VersionId** *(string) --*
                The identifier for the policy version.
                Policy version identifiers always begin with ``v`` (always lowercase). When a policy is created, the first policy version is ``v1`` .
              - **IsDefaultVersion** *(boolean) --*
                Specifies whether the policy version is set as the policy's default version.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy version was created.
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the managed policy that you want information about.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type VersionId: string
        :param VersionId: **[REQUIRED]**
          Identifies the policy version to retrieve.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consists of the lowercase letter \'v\' followed by one or two digits, and optionally followed by a period \'.\' and a string of letters and digits.
        :rtype: dict
        :returns:
        """
        pass

    def get_role(self, RoleName: str) -> Dict:
        """
        Retrieves information about the specified role, including the role's path, GUID, ARN, and the role's trust policy that grants permission to assume the role. For more information about roles, see `Working with Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ .
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetRole>`_

        **Request Syntax**
        ::
          response = client.get_role(
              RoleName='string'
          )

        **Response Syntax**
        ::
            {
                'Role': {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string',
                    'MaxSessionDuration': 123,
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetRole request.
            - **Role** *(dict) --*
              A structure containing details about the IAM role.
              - **Path** *(string) --*
                The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **RoleName** *(string) --*
                The friendly name that identifies the role.
              - **RoleId** *(string) --*
                The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
              - **AssumeRolePolicyDocument** *(string) --*
                The policy that grants an entity permission to assume the role.
              - **Description** *(string) --*
                A description of the role that you provide.
              - **MaxSessionDuration** *(integer) --*
                The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the role.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the IAM role to get information about.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_role_policy(self, RoleName: str, PolicyName: str) -> Dict:
        """
        Retrieves the specified inline policy document that is embedded with the specified IAM role.
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        An IAM role can also have managed policies attached to it. To retrieve a managed policy document that is attached to a role, use  GetPolicy to determine the policy's default version, then use  GetPolicyVersion to retrieve the policy document.
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        For more information about roles, see `Using Roles to Delegate Permissions and Federate Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetRolePolicy>`_

        **Request Syntax**
        ::
          response = client.get_role_policy(
              RoleName='string',
              PolicyName='string'
          )

        **Response Syntax**
        ::
            {
                'RoleName': 'string',
                'PolicyName': 'string',
                'PolicyDocument': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetRolePolicy request.
            - **RoleName** *(string) --*
              The role the policy is associated with.
            - **PolicyName** *(string) --*
              The name of the policy.
            - **PolicyDocument** *(string) --*
              The policy document.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role associated with the policy.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document to get.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_saml_provider(self, SAMLProviderArn: str) -> Dict:
        """
        Returns the SAML provider metadocument that was uploaded when the IAM SAML provider resource object was created or updated.
        .. note::
          This operation requires `Signature Version 4 <http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetSAMLProvider>`_

        **Request Syntax**
        ::
          response = client.get_saml_provider(
              SAMLProviderArn='string'
          )

        **Response Syntax**
        ::
            {
                'SAMLMetadataDocument': 'string',
                'CreateDate': datetime(2015, 1, 1),
                'ValidUntil': datetime(2015, 1, 1)
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetSAMLProvider request.
            - **SAMLMetadataDocument** *(string) --*
              The XML metadata document that includes information about an identity provider.
            - **CreateDate** *(datetime) --*
              The date and time when the SAML provider was created.
            - **ValidUntil** *(datetime) --*
              The expiration date and time for the SAML provider.
        :type SAMLProviderArn: string
        :param SAMLProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the SAML provider resource object in IAM to get information about.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :rtype: dict
        :returns:
        """
        pass

    def get_server_certificate(self, ServerCertificateName: str) -> Dict:
        """
        Retrieves information about the specified server certificate stored in IAM.
        For more information about working with server certificates, see `Working with Server Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`__ in the *IAM User Guide* . This topic includes a list of AWS services that can use the server certificates that you manage with IAM.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetServerCertificate>`_

        **Request Syntax**
        ::
          response = client.get_server_certificate(
              ServerCertificateName='string'
          )

        **Response Syntax**
        ::
            {
                'ServerCertificate': {
                    'ServerCertificateMetadata': {
                        'Path': 'string',
                        'ServerCertificateName': 'string',
                        'ServerCertificateId': 'string',
                        'Arn': 'string',
                        'UploadDate': datetime(2015, 1, 1),
                        'Expiration': datetime(2015, 1, 1)
                    },
                    'CertificateBody': 'string',
                    'CertificateChain': 'string'
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetServerCertificate request.
            - **ServerCertificate** *(dict) --*
              A structure containing details about the server certificate.
              - **ServerCertificateMetadata** *(dict) --*
                The meta information of the server certificate, such as its name, path, ID, and ARN.
                - **Path** *(string) --*
                  The path to the server certificate. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **ServerCertificateName** *(string) --*
                  The name that identifies the server certificate.
                - **ServerCertificateId** *(string) --*
                  The stable and unique string identifying the server certificate. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the server certificate. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UploadDate** *(datetime) --*
                  The date when the server certificate was uploaded.
                - **Expiration** *(datetime) --*
                  The date on which the certificate is set to expire.
              - **CertificateBody** *(string) --*
                The contents of the public key certificate.
              - **CertificateChain** *(string) --*
                The contents of the public key certificate chain.
        :type ServerCertificateName: string
        :param ServerCertificateName: **[REQUIRED]**
          The name of the server certificate you want to retrieve information about.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_service_last_accessed_details(self, JobId: str, MaxItems: int = None, Marker: str = None) -> Dict:
        """
        After you generate a user, group, role, or policy report using the ``GenerateServiceLastAccessedDetails`` operation, you can use the ``JobId`` parameter in ``GetServiceLastAccessedDetails`` . This operation retrieves the status of your report job and a list of AWS services that the resource (user, group, role, or managed policy) can access.
        .. note::
          Service last accessed data does not use other policy types when determining whether a resource could access a service. These other policy types include resource-based policies, access control lists, AWS Organizations policies, IAM permissions boundaries, and AWS STS assume role policies. It only applies permissions policy logic. For more about the evaluation of policy types, see `Evaluating Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html#policy-eval-basics>`__ in the *IAM User Guide* .
        For each service that the resource could access using permissions policies, the operation returns details about the most recent access attempt. If there was no attempt, the service is listed without details about the most recent attempt to access the service. If the operation fails, the ``GetServiceLastAccessedDetails`` operation returns the reason that it failed.
        The ``GetServiceLastAccessedDetails`` operation returns a list of services that includes the number of entities that have attempted to access the service and the date and time of the last attempt. It also returns the ARN of the following entity, depending on the resource ARN that you used to generate the report:
        * **User** – Returns the user ARN that you used to generate the report
        * **Group** – Returns the ARN of the group member (user) that last attempted to access the service
        * **Role** – Returns the role ARN that you used to generate the report
        * **Policy** – Returns the ARN of the user or role that last used the policy to attempt to access the service
        By default, the list is sorted by service namespace.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetServiceLastAccessedDetails>`_

        **Request Syntax**
        ::
          response = client.get_service_last_accessed_details(
              JobId='string',
              MaxItems=123,
              Marker='string'
          )

        **Response Syntax**
        ::
            {
                'JobStatus': 'IN_PROGRESS'|'COMPLETED'|'FAILED',
                'JobCreationDate': datetime(2015, 1, 1),
                'ServicesLastAccessed': [
                    {
                        'ServiceName': 'string',
                        'LastAuthenticated': datetime(2015, 1, 1),
                        'ServiceNamespace': 'string',
                        'LastAuthenticatedEntity': 'string',
                        'TotalAuthenticatedEntities': 123
                    },
                ],
                'JobCompletionDate': datetime(2015, 1, 1),
                'IsTruncated': True|False,
                'Marker': 'string',
                'Error': {
                    'Message': 'string',
                    'Code': 'string'
                }
            }

        **Response Structure**
          - *(dict) --*
            - **JobStatus** *(string) --*
              The status of the job.
            - **JobCreationDate** *(datetime) --*
              The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the report job was created.
            - **ServicesLastAccessed** *(list) --*
              A ``ServiceLastAccessed`` object that contains details about the most recent attempt to access the service.
              - *(dict) --*
                Contains details about the most recent attempt to access the service.
                This data type is used as a response element in the  GetServiceLastAccessedDetails operation.
                - **ServiceName** *(string) --*
                  The name of the service in which access was attempted.
                - **LastAuthenticated** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when an authenticated entity most recently attempted to access the service. AWS does not report unauthenticated requests.
                  This field is null if no IAM entities attempted to access the service within the `reporting period <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html#service-last-accessed-reporting-period>`__ .
                - **ServiceNamespace** *(string) --*
                  The namespace of the service in which access was attempted.
                  To learn the service namespace of a service, go to `Actions, Resources, and Condition Keys for AWS Services <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ in the *IAM User Guide* . Choose the name of the service to view details for that service. In the first paragraph, find the service prefix. For example, ``(service prefix: a4b)`` . For more information about service namespaces, see `AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__ in the *AWS General Reference* .
                - **LastAuthenticatedEntity** *(string) --*
                  The ARN of the authenticated entity (user or role) that last attempted to access the service. AWS does not report unauthenticated requests.
                  This field is null if no IAM entities attempted to access the service within the `reporting period <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html#service-last-accessed-reporting-period>`__ .
                - **TotalAuthenticatedEntities** *(integer) --*
                  The total number of authenticated entities that have attempted to access the service.
                  This field is null if no IAM entities attempted to access the service within the `reporting period <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html#service-last-accessed-reporting-period>`__ .
            - **JobCompletionDate** *(datetime) --*
              The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the generated report job was completed or failed.
              This field is null if the job is still in progress, as indicated by a ``JobStatus`` value of ``IN_PROGRESS`` .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
            - **Error** *(dict) --*
              An object that contains details about the reason the operation failed.
              - **Message** *(string) --*
                Detailed information about the reason that the operation failed.
              - **Code** *(string) --*
                The error code associated with the operation failure.
        :type JobId: string
        :param JobId: **[REQUIRED]**
          The ID of the request generated by the  GenerateServiceLastAccessedDetails operation.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :rtype: dict
        :returns:
        """
        pass

    def get_service_last_accessed_details_with_entities(self, JobId: str, ServiceNamespace: str, MaxItems: int = None,
                                                        Marker: str = None) -> Dict:
        """
        After you generate a group or policy report using the ``GenerateServiceLastAccessedDetails`` operation, you can use the ``JobId`` parameter in ``GetServiceLastAccessedDetailsWithEntities`` . This operation retrieves the status of your report job and a list of entities that could have used group or policy permissions to access the specified service.
        * **Group** – For a group report, this operation returns a list of users in the group that could have used the group’s policies in an attempt to access the service.
        * **Policy** – For a policy report, this operation returns a list of entities (users or roles) that could have used the policy in an attempt to access the service.
        You can also use this operation for user or role reports to retrieve details about those entities.
        If the operation fails, the ``GetServiceLastAccessedDetailsWithEntities`` operation returns the reason that it failed.
        By default, the list of associated entities is sorted by date, with the most recent access listed first.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetServiceLastAccessedDetailsWithEntities>`_

        **Request Syntax**
        ::
          response = client.get_service_last_accessed_details_with_entities(
              JobId='string',
              ServiceNamespace='string',
              MaxItems=123,
              Marker='string'
          )

        **Response Syntax**
        ::
            {
                'JobStatus': 'IN_PROGRESS'|'COMPLETED'|'FAILED',
                'JobCreationDate': datetime(2015, 1, 1),
                'JobCompletionDate': datetime(2015, 1, 1),
                'EntityDetailsList': [
                    {
                        'EntityInfo': {
                            'Arn': 'string',
                            'Name': 'string',
                            'Type': 'USER'|'ROLE'|'GROUP',
                            'Id': 'string',
                            'Path': 'string'
                        },
                        'LastAuthenticated': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string',
                'Error': {
                    'Message': 'string',
                    'Code': 'string'
                }
            }

        **Response Structure**
          - *(dict) --*
            - **JobStatus** *(string) --*
              The status of the job.
            - **JobCreationDate** *(datetime) --*
              The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the report job was created.
            - **JobCompletionDate** *(datetime) --*
              The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the generated report job was completed or failed.
            - **EntityDetailsList** *(list) --*
              An ``EntityDetailsList`` object that contains details about when an IAM entity (user or role) used group or policy permissions in an attempt to access the specified AWS service.
              - *(dict) --*
                An object that contains details about when the IAM entities (users or roles) were last used in an attempt to access the specified AWS service.
                This data type is a response element in the  GetServiceLastAccessedDetailsWithEntities operation.
                - **EntityInfo** *(dict) --*
                  The ``EntityInfo`` object that contains details about the entity (user or role).
                  - **Arn** *(string) --*
                    The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                    For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                  - **Name** *(string) --*
                    The name of the entity (user or role).
                  - **Type** *(string) --*
                    The type of entity (user or role).
                  - **Id** *(string) --*
                    The identifier of the entity (user or role).
                  - **Path** *(string) --*
                    The path to the entity (user or role). For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **LastAuthenticated** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the authenticated entity last attempted to access AWS. AWS does not report unauthenticated requests.
                  This field is null if no IAM entities attempted to access the service within the `reporting period <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html#service-last-accessed-reporting-period>`__ .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
            - **Error** *(dict) --*
              An object that contains details about the reason the operation failed.
              - **Message** *(string) --*
                Detailed information about the reason that the operation failed.
              - **Code** *(string) --*
                The error code associated with the operation failure.
        :type JobId: string
        :param JobId: **[REQUIRED]**
          The ID of the request generated by the ``GenerateServiceLastAccessedDetails`` operation.
        :type ServiceNamespace: string
        :param ServiceNamespace: **[REQUIRED]**
          The service namespace for an AWS service. Provide the service namespace to learn when the IAM entity last attempted to access the specified service.
          To learn the service namespace for a service, go to `Actions, Resources, and Condition Keys for AWS Services <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ in the *IAM User Guide* and choose the name of the service to view details for that service. In the first paragraph, find the service prefix. For example, ``(service prefix: a4b)`` . For more information about service namespaces, see `AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__ in the *AWS General Reference* .
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :rtype: dict
        :returns:
        """
        pass

    def get_service_linked_role_deletion_status(self, DeletionTaskId: str) -> Dict:
        """
        Retrieves the status of your service-linked role deletion. After you use the  DeleteServiceLinkedRole API operation to submit a service-linked role for deletion, you can use the ``DeletionTaskId`` parameter in ``GetServiceLinkedRoleDeletionStatus`` to check the status of the deletion. If the deletion fails, this operation returns the reason that it failed, if that information is returned by the service.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetServiceLinkedRoleDeletionStatus>`_

        **Request Syntax**
        ::
          response = client.get_service_linked_role_deletion_status(
              DeletionTaskId='string'
          )

        **Response Syntax**
        ::
            {
                'Status': 'SUCCEEDED'|'IN_PROGRESS'|'FAILED'|'NOT_STARTED',
                'Reason': {
                    'Reason': 'string',
                    'RoleUsageList': [
                        {
                            'Region': 'string',
                            'Resources': [
                                'string',
                            ]
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            - **Status** *(string) --*
              The status of the deletion.
            - **Reason** *(dict) --*
              An object that contains details about the reason the deletion failed.
              - **Reason** *(string) --*
                A short description of the reason that the service-linked role deletion failed.
              - **RoleUsageList** *(list) --*
                A list of objects that contains details about the service-linked role deletion failure, if that information is returned by the service. If the service-linked role has active sessions or if any resources that were used by the role have not been deleted from the linked service, the role can't be deleted. This parameter includes a list of the resources that are associated with the role and the region in which the resources are being used.
                - *(dict) --*
                  An object that contains details about how a service-linked role is used, if that information is returned by the service.
                  This data type is used as a response element in the  GetServiceLinkedRoleDeletionStatus operation.
                  - **Region** *(string) --*
                    The name of the region where the service-linked role is being used.
                  - **Resources** *(list) --*
                    The name of the resource that is using the service-linked role.
                    - *(string) --*
                      The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                      For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type DeletionTaskId: string
        :param DeletionTaskId: **[REQUIRED]**
          The deletion task identifier. This identifier is returned by the  DeleteServiceLinkedRole operation in the format ``task/aws-service-role/<service-principal-name>/<role-name>/<task-uuid>`` .
        :rtype: dict
        :returns:
        """
        pass

    def get_ssh_public_key(self, UserName: str, SSHPublicKeyId: str, Encoding: str) -> Dict:
        """
        Retrieves the specified SSH public key, including metadata about the key.
        The SSH public key retrieved by this operation is used only for authenticating the associated IAM user to an AWS CodeCommit repository. For more information about using SSH keys to authenticate to an AWS CodeCommit repository, see `Set up AWS CodeCommit for SSH Connections <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-credentials-ssh.html>`__ in the *AWS CodeCommit User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetSSHPublicKey>`_

        **Request Syntax**
        ::
          response = client.get_ssh_public_key(
              UserName='string',
              SSHPublicKeyId='string',
              Encoding='SSH'|'PEM'
          )

        **Response Syntax**
        ::
            {
                'SSHPublicKey': {
                    'UserName': 'string',
                    'SSHPublicKeyId': 'string',
                    'Fingerprint': 'string',
                    'SSHPublicKeyBody': 'string',
                    'Status': 'Active'|'Inactive',
                    'UploadDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetSSHPublicKey request.
            - **SSHPublicKey** *(dict) --*
              A structure containing details about the SSH public key.
              - **UserName** *(string) --*
                The name of the IAM user associated with the SSH public key.
              - **SSHPublicKeyId** *(string) --*
                The unique identifier for the SSH public key.
              - **Fingerprint** *(string) --*
                The MD5 message digest of the SSH public key.
              - **SSHPublicKeyBody** *(string) --*
                The SSH public key.
              - **Status** *(string) --*
                The status of the SSH public key. ``Active`` means that the key can be used for authentication with an AWS CodeCommit repository. ``Inactive`` means that the key cannot be used.
              - **UploadDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the SSH public key was uploaded.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user associated with the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SSHPublicKeyId: string
        :param SSHPublicKeyId: **[REQUIRED]**
          The unique identifier for the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :type Encoding: string
        :param Encoding: **[REQUIRED]**
          Specifies the public key encoding format to use in the response. To retrieve the public key in ssh-rsa format, use ``SSH`` . To retrieve the public key in PEM format, use ``PEM`` .
        :rtype: dict
        :returns:
        """
        pass

    def get_user(self, UserName: str = None) -> Dict:
        """
        Retrieves information about the specified IAM user, including the user's creation date, path, unique ID, and ARN.
        If you do not specify a user name, IAM determines the user name implicitly based on the AWS access key ID used to sign the request to this API.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetUser>`_

        **Request Syntax**
        ::
          response = client.get_user(
              UserName='string'
          )

        **Response Syntax**
        ::
            {
                'User': {
                    'Path': 'string',
                    'UserName': 'string',
                    'UserId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'PasswordLastUsed': datetime(2015, 1, 1),
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetUser request.
            - **User** *(dict) --*
              A structure containing details about the IAM user.
              .. warning::
                Due to a service issue, password last used data does not include password use from May 3, 2018 22:50 PDT to May 23, 2018 14:08 PDT. This affects `last sign-in <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_finding-unused.html>`__ dates shown in the IAM console and password last used dates in the `IAM credential report <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_getting-report.html>`__ , and returned by this GetUser API. If users signed in during the affected time, the password last used date that is returned is the date the user last signed in before May 3, 2018. For users that signed in after May 23, 2018 14:08 PDT, the returned password last used date is accurate.
                You can use password last used information to identify unused credentials for deletion. For example, you might delete users who did not sign in to AWS in the last 90 days. In cases like this, we recommend that you adjust your evaluation window to include dates after May 23, 2018. Alternatively, if your users use access keys to access AWS programmatically you can refer to access key last used information because it is accurate for all dates.
              - **Path** *(string) --*
                The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **UserName** *(string) --*
                The friendly name identifying the user.
              - **UserId** *(string) --*
                The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
              - **PasswordLastUsed** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                * The user never had a password.
                * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                This value is returned only in the  GetUser and  ListUsers operations.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the user.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type UserName: string
        :param UserName:
          The name of the user to get information about.
          This parameter is optional. If it is not included, it defaults to the user making the request. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_user_policy(self, UserName: str, PolicyName: str) -> Dict:
        """
        Retrieves the specified inline policy document that is embedded in the specified IAM user.
        .. note::
          Policies returned by this API are URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
        An IAM user can also have managed policies attached to it. To retrieve a managed policy document that is attached to a user, use  GetPolicy to determine the policy's default version, then use  GetPolicyVersion to retrieve the policy document.
        For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/GetUserPolicy>`_

        **Request Syntax**
        ::
          response = client.get_user_policy(
              UserName='string',
              PolicyName='string'
          )

        **Response Syntax**
        ::
            {
                'UserName': 'string',
                'PolicyName': 'string',
                'PolicyDocument': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  GetUserPolicy request.
            - **UserName** *(string) --*
              The user the policy is associated with.
            - **PolicyName** *(string) --*
              The name of the policy.
            - **PolicyDocument** *(string) --*
              The policy document.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user who the policy is associated with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document to get.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :rtype: dict
        :returns:
        """
        pass

    def get_waiter(self, waiter_name: str = None) -> Waiter:
        """
        Returns an object that can wait for some condition.
        :type waiter_name: str
        :param waiter_name: The name of the waiter to get. See the waiters
            section of the service docs for a list of available waiters.
        :returns: The specified waiter object.
        :rtype: botocore.waiter.Waiter
        """
        pass

    def list_access_keys(self, UserName: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Returns information about the access key IDs associated with the specified IAM user. If there is none, the operation returns an empty list.
        Although each user is limited to a small number of keys, you can still paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        If the ``UserName`` field is not specified, the user name is determined implicitly based on the AWS access key ID used to sign the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        .. note::
          To ensure the security of your AWS account, the secret access key is accessible only during key and user creation.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListAccessKeys>`_

        **Request Syntax**
        ::
          response = client.list_access_keys(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'AccessKeyMetadata': [
                    {
                        'UserName': 'string',
                        'AccessKeyId': 'string',
                        'Status': 'Active'|'Inactive',
                        'CreateDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListAccessKeys request.
            - **AccessKeyMetadata** *(list) --*
              A list of objects containing metadata about the access keys.
              - *(dict) --*
                Contains information about an AWS access key, without its secret key.
                This data type is used as a response element in the  ListAccessKeys operation.
                - **UserName** *(string) --*
                  The name of the IAM user that the key is associated with.
                - **AccessKeyId** *(string) --*
                  The ID for this access key.
                - **Status** *(string) --*
                  The status of the access key. ``Active`` means that the key is valid for API calls; ``Inactive`` means it is not.
                - **CreateDate** *(datetime) --*
                  The date when the access key was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName:
          The name of the user.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_account_aliases(self, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the account alias associated with the AWS account (Note: you can have only one). For information about using an AWS account alias, see `Using an Alias for Your AWS Account ID <http://docs.aws.amazon.com/IAM/latest/UserGuide/AccountAlias.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListAccountAliases>`_

        **Request Syntax**
        ::
          response = client.list_account_aliases(
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'AccountAliases': [
                    'string',
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListAccountAliases request.
            - **AccountAliases** *(list) --*
              A list of aliases associated with the account. AWS supports only one alias per account.
              - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_attached_group_policies(self, GroupName: str, PathPrefix: str = None, Marker: str = None,
                                     MaxItems: int = None) -> Dict:
        """
        Lists all managed policies that are attached to the specified IAM group.
        An IAM group can also have inline policies embedded with it. To list the inline policies for a group, use the  ListGroupPolicies API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. You can use the ``PathPrefix`` parameter to limit the list of policies to only those matching the specified path prefix. If there are no policies attached to the specified group (or none that match the specified path prefix), the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListAttachedGroupPolicies>`_

        **Request Syntax**
        ::
          response = client.list_attached_group_policies(
              GroupName='string',
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'AttachedPolicies': [
                    {
                        'PolicyName': 'string',
                        'PolicyArn': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListAttachedGroupPolicies request.
            - **AttachedPolicies** *(list) --*
              A list of the attached policies.
              - *(dict) --*
                Contains information about an attached policy.
                An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **PolicyName** *(string) --*
                  The friendly name of the attached policy.
                - **PolicyArn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name (friendly name, not ARN) of the group to list attached policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (/), listing all policies.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_attached_role_policies(self, RoleName: str, PathPrefix: str = None, Marker: str = None,
                                    MaxItems: int = None) -> Dict:
        """
        Lists all managed policies that are attached to the specified IAM role.
        An IAM role can also have inline policies embedded with it. To list the inline policies for a role, use the  ListRolePolicies API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. You can use the ``PathPrefix`` parameter to limit the list of policies to only those matching the specified path prefix. If there are no policies attached to the specified role (or none that match the specified path prefix), the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListAttachedRolePolicies>`_

        **Request Syntax**
        ::
          response = client.list_attached_role_policies(
              RoleName='string',
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'AttachedPolicies': [
                    {
                        'PolicyName': 'string',
                        'PolicyArn': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListAttachedRolePolicies request.
            - **AttachedPolicies** *(list) --*
              A list of the attached policies.
              - *(dict) --*
                Contains information about an attached policy.
                An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **PolicyName** *(string) --*
                  The friendly name of the attached policy.
                - **PolicyArn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) of the role to list attached policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (/), listing all policies.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_attached_user_policies(self, UserName: str, PathPrefix: str = None, Marker: str = None,
                                    MaxItems: int = None) -> Dict:
        """
        Lists all managed policies that are attached to the specified IAM user.
        An IAM user can also have inline policies embedded with it. To list the inline policies for a user, use the  ListUserPolicies API. For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. You can use the ``PathPrefix`` parameter to limit the list of policies to only those matching the specified path prefix. If there are no policies attached to the specified group (or none that match the specified path prefix), the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListAttachedUserPolicies>`_

        **Request Syntax**
        ::
          response = client.list_attached_user_policies(
              UserName='string',
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'AttachedPolicies': [
                    {
                        'PolicyName': 'string',
                        'PolicyArn': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListAttachedUserPolicies request.
            - **AttachedPolicies** *(list) --*
              A list of the attached policies.
              - *(dict) --*
                Contains information about an attached policy.
                An attached policy is a managed policy that has been attached to a user, group, or role. This data type is used as a response element in the  ListAttachedGroupPolicies ,  ListAttachedRolePolicies ,  ListAttachedUserPolicies , and  GetAccountAuthorizationDetails operations.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **PolicyName** *(string) --*
                  The friendly name of the attached policy.
                - **PolicyArn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) of the user to list attached policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (/), listing all policies.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_entities_for_policy(self, PolicyArn: str, EntityFilter: str = None, PathPrefix: str = None,
                                 PolicyUsageFilter: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists all IAM users, groups, and roles that the specified managed policy is attached to.
        You can use the optional ``EntityFilter`` parameter to limit the results to a particular type of entity (users, groups, or roles). For example, to list only the roles that are attached to the specified policy, set ``EntityFilter`` to ``Role`` .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListEntitiesForPolicy>`_

        **Request Syntax**
        ::
          response = client.list_entities_for_policy(
              PolicyArn='string',
              EntityFilter='User'|'Role'|'Group'|'LocalManagedPolicy'|'AWSManagedPolicy',
              PathPrefix='string',
              PolicyUsageFilter='PermissionsPolicy'|'PermissionsBoundary',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'PolicyGroups': [
                    {
                        'GroupName': 'string',
                        'GroupId': 'string'
                    },
                ],
                'PolicyUsers': [
                    {
                        'UserName': 'string',
                        'UserId': 'string'
                    },
                ],
                'PolicyRoles': [
                    {
                        'RoleName': 'string',
                        'RoleId': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListEntitiesForPolicy request.
            - **PolicyGroups** *(list) --*
              A list of IAM groups that the policy is attached to.
              - *(dict) --*
                Contains information about a group that a managed policy is attached to.
                This data type is used as a response element in the  ListEntitiesForPolicy operation.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **GroupName** *(string) --*
                  The name (friendly name, not ARN) identifying the group.
                - **GroupId** *(string) --*
                  The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`__ in the *IAM User Guide* .
            - **PolicyUsers** *(list) --*
              A list of IAM users that the policy is attached to.
              - *(dict) --*
                Contains information about a user that a managed policy is attached to.
                This data type is used as a response element in the  ListEntitiesForPolicy operation.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **UserName** *(string) --*
                  The name (friendly name, not ARN) identifying the user.
                - **UserId** *(string) --*
                  The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`__ in the *IAM User Guide* .
            - **PolicyRoles** *(list) --*
              A list of IAM roles that the policy is attached to.
              - *(dict) --*
                Contains information about a role that a managed policy is attached to.
                This data type is used as a response element in the  ListEntitiesForPolicy operation.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **RoleName** *(string) --*
                  The name (friendly name, not ARN) identifying the role.
                - **RoleId** *(string) --*
                  The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`__ in the *IAM User Guide* .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy for which you want the versions.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type EntityFilter: string
        :param EntityFilter:
          The entity type to use for filtering the results.
          For example, when ``EntityFilter`` is ``Role`` , only the roles that are attached to the specified policy are returned. This parameter is optional. If it is not included, all attached entities (users, groups, and roles) are returned. The argument for this parameter must be one of the valid values listed below.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (/), listing all entities.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type PolicyUsageFilter: string
        :param PolicyUsageFilter:
          The policy usage method to use for filtering the results.
          To list only permissions policies, set ``PolicyUsageFilter`` to ``PermissionsPolicy`` . To list only the policies used to set permissions boundaries, set the value to ``PermissionsBoundary`` .
          This parameter is optional. If it is not included, all policies are returned.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_group_policies(self, GroupName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the names of the inline policies that are embedded in the specified IAM group.
        An IAM group can also have managed policies attached to it. To list the managed policies that are attached to a group, use  ListAttachedGroupPolicies . For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. If there are no inline policies embedded with the specified group, the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListGroupPolicies>`_

        **Request Syntax**
        ::
          response = client.list_group_policies(
              GroupName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'PolicyNames': [
                    'string',
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListGroupPolicies request.
            - **PolicyNames** *(list) --*
              A list of policy names.
              This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
              - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group to list policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_groups(self, PathPrefix: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the IAM groups that have the specified path prefix.
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListGroups>`_

        **Request Syntax**
        ::
          response = client.list_groups(
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Groups': [
                    {
                        'Path': 'string',
                        'GroupName': 'string',
                        'GroupId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListGroups request.
            - **Groups** *(list) --*
              A list of groups.
              - *(dict) --*
                Contains information about an IAM group entity.
                This data type is used as a response element in the following operations:
                *  CreateGroup
                *  GetGroup
                *  ListGroups
                - **Path** *(string) --*
                  The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **GroupName** *(string) --*
                  The friendly name that identifies the group.
                - **GroupId** *(string) --*
                  The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the group. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the group was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. For example, the prefix ``/division_abc/subdivision_xyz/`` gets all groups whose path starts with ``/division_abc/subdivision_xyz/`` .
          This parameter is optional. If it is not included, it defaults to a slash (/), listing all groups. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_groups_for_user(self, UserName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the IAM groups that the specified IAM user belongs to.
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListGroupsForUser>`_

        **Request Syntax**
        ::
          response = client.list_groups_for_user(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Groups': [
                    {
                        'Path': 'string',
                        'GroupName': 'string',
                        'GroupId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListGroupsForUser request.
            - **Groups** *(list) --*
              A list of groups.
              - *(dict) --*
                Contains information about an IAM group entity.
                This data type is used as a response element in the following operations:
                *  CreateGroup
                *  GetGroup
                *  ListGroups
                - **Path** *(string) --*
                  The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **GroupName** *(string) --*
                  The friendly name that identifies the group.
                - **GroupId** *(string) --*
                  The stable and unique string identifying the group. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the group. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the group was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to list groups for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_instance_profiles(self, PathPrefix: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the instance profiles that have the specified path prefix. If there are none, the operation returns an empty list. For more information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListInstanceProfiles>`_

        **Request Syntax**
        ::
          response = client.list_instance_profiles(
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'InstanceProfiles': [
                    {
                        'Path': 'string',
                        'InstanceProfileName': 'string',
                        'InstanceProfileId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'Roles': [
                            {
                                'Path': 'string',
                                'RoleName': 'string',
                                'RoleId': 'string',
                                'Arn': 'string',
                                'CreateDate': datetime(2015, 1, 1),
                                'AssumeRolePolicyDocument': 'string',
                                'Description': 'string',
                                'MaxSessionDuration': 123,
                                'PermissionsBoundary': {
                                    'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                    'PermissionsBoundaryArn': 'string'
                                },
                                'Tags': [
                                    {
                                        'Key': 'string',
                                        'Value': 'string'
                                    },
                                ]
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListInstanceProfiles request.
            - **InstanceProfiles** *(list) --*
              A list of instance profiles.
              - *(dict) --*
                Contains information about an instance profile.
                This data type is used as a response element in the following operations:
                *  CreateInstanceProfile
                *  GetInstanceProfile
                *  ListInstanceProfiles
                *  ListInstanceProfilesForRole
                - **Path** *(string) --*
                  The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **InstanceProfileName** *(string) --*
                  The name identifying the instance profile.
                - **InstanceProfileId** *(string) --*
                  The stable and unique string identifying the instance profile. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the instance profile. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date when the instance profile was created.
                - **Roles** *(list) --*
                  The role associated with the instance profile.
                  - *(dict) --*
                    Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                    - **Path** *(string) --*
                      The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **RoleName** *(string) --*
                      The friendly name that identifies the role.
                    - **RoleId** *(string) --*
                      The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **Arn** *(string) --*
                      The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                    - **CreateDate** *(datetime) --*
                      The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                    - **AssumeRolePolicyDocument** *(string) --*
                      The policy that grants an entity permission to assume the role.
                    - **Description** *(string) --*
                      A description of the role that you provide.
                    - **MaxSessionDuration** *(integer) --*
                      The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                    - **PermissionsBoundary** *(dict) --*
                      The ARN of the policy used to set the permissions boundary for the role.
                      For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                      - **PermissionsBoundaryType** *(string) --*
                        The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                      - **PermissionsBoundaryArn** *(string) --*
                        The ARN of the policy used to set the permissions boundary for the user or role.
                    - **Tags** *(list) --*
                      A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                      - *(dict) --*
                        A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                        - **Key** *(string) --*
                          The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                        - **Value** *(string) --*
                          The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                          .. note::
                            AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. For example, the prefix ``/application_abc/component_xyz/`` gets all instance profiles whose path starts with ``/application_abc/component_xyz/`` .
          This parameter is optional. If it is not included, it defaults to a slash (/), listing all instance profiles. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_instance_profiles_for_role(self, RoleName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the instance profiles that have the specified associated IAM role. If there are none, the operation returns an empty list. For more information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListInstanceProfilesForRole>`_

        **Request Syntax**
        ::
          response = client.list_instance_profiles_for_role(
              RoleName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'InstanceProfiles': [
                    {
                        'Path': 'string',
                        'InstanceProfileName': 'string',
                        'InstanceProfileId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'Roles': [
                            {
                                'Path': 'string',
                                'RoleName': 'string',
                                'RoleId': 'string',
                                'Arn': 'string',
                                'CreateDate': datetime(2015, 1, 1),
                                'AssumeRolePolicyDocument': 'string',
                                'Description': 'string',
                                'MaxSessionDuration': 123,
                                'PermissionsBoundary': {
                                    'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                    'PermissionsBoundaryArn': 'string'
                                },
                                'Tags': [
                                    {
                                        'Key': 'string',
                                        'Value': 'string'
                                    },
                                ]
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListInstanceProfilesForRole request.
            - **InstanceProfiles** *(list) --*
              A list of instance profiles.
              - *(dict) --*
                Contains information about an instance profile.
                This data type is used as a response element in the following operations:
                *  CreateInstanceProfile
                *  GetInstanceProfile
                *  ListInstanceProfiles
                *  ListInstanceProfilesForRole
                - **Path** *(string) --*
                  The path to the instance profile. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **InstanceProfileName** *(string) --*
                  The name identifying the instance profile.
                - **InstanceProfileId** *(string) --*
                  The stable and unique string identifying the instance profile. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the instance profile. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date when the instance profile was created.
                - **Roles** *(list) --*
                  The role associated with the instance profile.
                  - *(dict) --*
                    Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                    - **Path** *(string) --*
                      The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **RoleName** *(string) --*
                      The friendly name that identifies the role.
                    - **RoleId** *(string) --*
                      The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                    - **Arn** *(string) --*
                      The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                    - **CreateDate** *(datetime) --*
                      The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                    - **AssumeRolePolicyDocument** *(string) --*
                      The policy that grants an entity permission to assume the role.
                    - **Description** *(string) --*
                      A description of the role that you provide.
                    - **MaxSessionDuration** *(integer) --*
                      The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                    - **PermissionsBoundary** *(dict) --*
                      The ARN of the policy used to set the permissions boundary for the role.
                      For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                      - **PermissionsBoundaryType** *(string) --*
                        The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                      - **PermissionsBoundaryArn** *(string) --*
                        The ARN of the policy used to set the permissions boundary for the user or role.
                    - **Tags** *(list) --*
                      A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                      - *(dict) --*
                        A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                        - **Key** *(string) --*
                          The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                        - **Value** *(string) --*
                          The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                          .. note::
                            AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to list instance profiles for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_mfa_devices(self, UserName: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the MFA devices for an IAM user. If the request includes a IAM user name, then this operation lists all the MFA devices associated with the specified user. If you do not specify a user name, IAM determines the user name implicitly based on the AWS access key ID signing the request for this API.
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListMFADevices>`_

        **Request Syntax**
        ::
          response = client.list_mfa_devices(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'MFADevices': [
                    {
                        'UserName': 'string',
                        'SerialNumber': 'string',
                        'EnableDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListMFADevices request.
            - **MFADevices** *(list) --*
              A list of MFA devices.
              - *(dict) --*
                Contains information about an MFA device.
                This data type is used as a response element in the  ListMFADevices operation.
                - **UserName** *(string) --*
                  The user with whom the MFA device is associated.
                - **SerialNumber** *(string) --*
                  The serial number that uniquely identifies the MFA device. For virtual MFA devices, the serial number is the device ARN.
                - **EnableDate** *(datetime) --*
                  The date when the MFA device was enabled for the user.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName:
          The name of the user whose MFA devices you want to list.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_open_id_connect_providers(self) -> Dict:
        """
        Lists information about the IAM OpenID Connect (OIDC) provider resource objects defined in the AWS account.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListOpenIDConnectProviders>`_

        **Request Syntax**
        ::
          response = client.list_open_id_connect_providers()

        **Response Syntax**
        ::
            {
                'OpenIDConnectProviderList': [
                    {
                        'Arn': 'string'
                    },
                ]
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListOpenIDConnectProviders request.
            - **OpenIDConnectProviderList** *(list) --*
              The list of IAM OIDC provider resource objects defined in the AWS account.
              - *(dict) --*
                Contains the Amazon Resource Name (ARN) for an IAM OpenID Connect provider.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :rtype: dict
        :returns:
        """
        pass

    def list_policies(self, Scope: str = None, OnlyAttached: bool = None, PathPrefix: str = None,
                      PolicyUsageFilter: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists all the managed policies that are available in your AWS account, including your own customer-defined managed policies and all AWS managed policies.
        You can filter the list of policies that is returned using the optional ``OnlyAttached`` , ``Scope`` , and ``PathPrefix`` parameters. For example, to list only the customer managed policies in your AWS account, set ``Scope`` to ``Local`` . To list only AWS managed policies, set ``Scope`` to ``AWS`` .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        For more information about managed policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListPolicies>`_

        **Request Syntax**
        ::
          response = client.list_policies(
              Scope='All'|'AWS'|'Local',
              OnlyAttached=True|False,
              PathPrefix='string',
              PolicyUsageFilter='PermissionsPolicy'|'PermissionsBoundary',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Policies': [
                    {
                        'PolicyName': 'string',
                        'PolicyId': 'string',
                        'Arn': 'string',
                        'Path': 'string',
                        'DefaultVersionId': 'string',
                        'AttachmentCount': 123,
                        'PermissionsBoundaryUsageCount': 123,
                        'IsAttachable': True|False,
                        'Description': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'UpdateDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListPolicies request.
            - **Policies** *(list) --*
              A list of policies.
              - *(dict) --*
                Contains information about a managed policy.
                This data type is used as a response element in the  CreatePolicy ,  GetPolicy , and  ListPolicies operations.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **PolicyName** *(string) --*
                  The friendly name (not ARN) identifying the policy.
                - **PolicyId** *(string) --*
                  The stable and unique string identifying the policy.
                  For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                  For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                - **Path** *(string) --*
                  The path to the policy.
                  For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **DefaultVersionId** *(string) --*
                  The identifier for the version of the policy that is set as the default version.
                - **AttachmentCount** *(integer) --*
                  The number of entities (users, groups, and roles) that the policy is attached to.
                - **PermissionsBoundaryUsageCount** *(integer) --*
                  The number of entities (users and roles) for which the policy is used to set the permissions boundary.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **IsAttachable** *(boolean) --*
                  Specifies whether the policy can be attached to an IAM user, group, or role.
                - **Description** *(string) --*
                  A friendly description of the policy.
                  This element is included in the response to the  GetPolicy operation. It is not included in the response to the  ListPolicies operation.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was created.
                - **UpdateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy was last updated.
                  When a policy has only one version, this field contains the date and time when the policy was created. When a policy has more than one version, this field contains the date and time when the most recent policy version was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type Scope: string
        :param Scope:
          The scope to use for filtering the results.
          To list only AWS managed policies, set ``Scope`` to ``AWS`` . To list only the customer managed policies in your AWS account, set ``Scope`` to ``Local`` .
          This parameter is optional. If it is not included, or if it is set to ``All`` , all policies are returned.
        :type OnlyAttached: boolean
        :param OnlyAttached:
          A flag to filter the results to only the attached policies.
          When ``OnlyAttached`` is ``true`` , the returned list contains only the policies that are attached to an IAM user, group, or role. When ``OnlyAttached`` is ``false`` , or when the parameter is not included, all policies are returned.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. This parameter is optional. If it is not included, it defaults to a slash (/), listing all policies. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type PolicyUsageFilter: string
        :param PolicyUsageFilter:
          The policy usage method to use for filtering the results.
          To list only permissions policies, set ``PolicyUsageFilter`` to ``PermissionsPolicy`` . To list only the policies used to set permissions boundaries, set the value to ``PermissionsBoundary`` .
          This parameter is optional. If it is not included, all policies are returned.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_policies_granting_service_access(self, Arn: str, ServiceNamespaces: List, Marker: str = None) -> Dict:
        """
        Retrieves a list of policies that the IAM identity (user, group, or role) can use to access each specified service.
        .. note::
          This operation does not use other policy types when determining whether a resource could access a service. These other policy types include resource-based policies, access control lists, AWS Organizations policies, IAM permissions boundaries, and AWS STS assume role policies. It only applies permissions policy logic. For more about the evaluation of policy types, see `Evaluating Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html#policy-eval-basics>`__ in the *IAM User Guide* .
        The list of policies returned by the operation depends on the ARN of the identity that you provide.
        * **User** – The list of policies includes the managed and inline policies that are attached to the user directly. The list also includes any additional managed and inline policies that are attached to the group to which the user belongs.
        * **Group** – The list of policies includes only the managed and inline policies that are attached to the group directly. Policies that are attached to the group’s user are not included.
        * **Role** – The list of policies includes only the managed and inline policies that are attached to the role.
        For each managed policy, this operation returns the ARN and policy name. For each inline policy, it returns the policy name and the entity to which it is attached. Inline policies do not have an ARN. For more information about these policy types, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>`__ in the *IAM User Guide* .
        Policies that are attached to users and roles as permissions boundaries are not returned. To view which managed policy is currently used to set the permissions boundary for a user or role, use the  GetUser or  GetRole operations.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListPoliciesGrantingServiceAccess>`_

        **Request Syntax**
        ::
          response = client.list_policies_granting_service_access(
              Marker='string',
              Arn='string',
              ServiceNamespaces=[
                  'string',
              ]
          )

        **Response Syntax**
        ::
            {
                'PoliciesGrantingServiceAccess': [
                    {
                        'ServiceNamespace': 'string',
                        'Policies': [
                            {
                                'PolicyName': 'string',
                                'PolicyType': 'INLINE'|'MANAGED',
                                'PolicyArn': 'string',
                                'EntityType': 'USER'|'ROLE'|'GROUP',
                                'EntityName': 'string'
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            - **PoliciesGrantingServiceAccess** *(list) --*
              A ``ListPoliciesGrantingServiceAccess`` object that contains details about the permissions policies attached to the specified identity (user, group, or role).
              - *(dict) --*
                Contains details about the permissions policies that are attached to the specified identity (user, group, or role).
                This data type is used as a response element in the  ListPoliciesGrantingServiceAccess operation.
                - **ServiceNamespace** *(string) --*
                  The namespace of the service that was accessed.
                  To learn the service namespace of a service, go to `Actions, Resources, and Condition Keys for AWS Services <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ in the *IAM User Guide* . Choose the name of the service to view details for that service. In the first paragraph, find the service prefix. For example, ``(service prefix: a4b)`` . For more information about service namespaces, see `AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__ in the *AWS General Reference* .
                - **Policies** *(list) --*
                  The ``PoliciesGrantingServiceAccess`` object that contains details about the policy.
                  - *(dict) --*
                    Contains details about the permissions policies that are attached to the specified identity (user, group, or role).
                    This data type is an element of the  ListPoliciesGrantingServiceAccessEntry object.
                    - **PolicyName** *(string) --*
                      The policy name.
                    - **PolicyType** *(string) --*
                      The policy type. For more information about these policy types, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>`__ in the *IAM User Guide* .
                    - **PolicyArn** *(string) --*
                      The Amazon Resource Name (ARN). ARNs are unique identifiers for AWS resources.
                      For more information about ARNs, go to `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
                    - **EntityType** *(string) --*
                      The type of entity (user or role) that used the policy to access the service to which the inline policy is attached.
                      This field is null for managed policies. For more information about these policy types, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>`__ in the *IAM User Guide* .
                    - **EntityName** *(string) --*
                      The name of the entity (user or role) to which the inline policy is attached.
                      This field is null for managed policies. For more information about these policy types, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>`__ in the *IAM User Guide* .
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type Arn: string
        :param Arn: **[REQUIRED]**
          The ARN of the IAM identity (user, group, or role) whose policies you want to list.
        :type ServiceNamespaces: list
        :param ServiceNamespaces: **[REQUIRED]**
          The service namespace for the AWS services whose policies you want to list.
          To learn the service namespace for a service, go to `Actions, Resources, and Condition Keys for AWS Services <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ in the *IAM User Guide* . Choose the name of the service to view details for that service. In the first paragraph, find the service prefix. For example, ``(service prefix: a4b)`` . For more information about service namespaces, see `AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces>`__ in the *AWS General Reference* .
          - *(string) --*
        :rtype: dict
        :returns:
        """
        pass

    def list_policy_versions(self, PolicyArn: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists information about the versions of the specified managed policy, including the version that is currently set as the policy's default version.
        For more information about managed policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListPolicyVersions>`_

        **Request Syntax**
        ::
          response = client.list_policy_versions(
              PolicyArn='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Versions': [
                    {
                        'Document': 'string',
                        'VersionId': 'string',
                        'IsDefaultVersion': True|False,
                        'CreateDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListPolicyVersions request.
            - **Versions** *(list) --*
              A list of policy versions.
              For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
              - *(dict) --*
                Contains information about a version of a managed policy.
                This data type is used as a response element in the  CreatePolicyVersion ,  GetPolicyVersion ,  ListPolicyVersions , and  GetAccountAuthorizationDetails operations.
                For more information about managed policies, refer to `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *Using IAM* guide.
                - **Document** *(string) --*
                  The policy document.
                  The policy document is returned in the response to the  GetPolicyVersion and  GetAccountAuthorizationDetails operations. It is not returned in the response to the  CreatePolicyVersion or  ListPolicyVersions operations.
                  The policy document returned in this structure is URL-encoded compliant with `RFC 3986 <https://tools.ietf.org/html/rfc3986>`__ . You can use a URL decoding method to convert the policy back to plain JSON text. For example, if you use Java, you can use the ``decode`` method of the ``java.net.URLDecoder`` utility class in the Java SDK. Other languages and SDKs provide similar functionality.
                - **VersionId** *(string) --*
                  The identifier for the policy version.
                  Policy version identifiers always begin with ``v`` (always lowercase). When a policy is created, the first policy version is ``v1`` .
                - **IsDefaultVersion** *(boolean) --*
                  Specifies whether the policy version is set as the policy's default version.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the policy version was created.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy for which you want the versions.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_role_policies(self, RoleName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the names of the inline policies that are embedded in the specified IAM role.
        An IAM role can also have managed policies attached to it. To list the managed policies that are attached to a role, use  ListAttachedRolePolicies . For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. If there are no inline policies embedded with the specified role, the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListRolePolicies>`_

        **Request Syntax**
        ::
          response = client.list_role_policies(
              RoleName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'PolicyNames': [
                    'string',
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListRolePolicies request.
            - **PolicyNames** *(list) --*
              A list of policy names.
              - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to list policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_role_tags(self, RoleName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the tags that are attached to the specified role. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListRoleTags>`_

        **Request Syntax**
        ::
          response = client.list_role_tags(
              RoleName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            - **Tags** *(list) --*
              The list of tags currently that is attached to the role. Each tag consists of a key name and an associated value. If no tags are attached to the specified role, the response contains an empty list.
              - *(dict) --*
                A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - **Key** *(string) --*
                  The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                - **Value** *(string) --*
                  The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                  .. note::
                    AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can use the ``Marker`` request parameter to make a subsequent pagination request that retrieves more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when more results are available. Check ``IsTruncated`` after every call to ensure that you receive all of your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the IAM role for which you want to see the list of tags.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          (Optional) Use this only when paginating results to indicate the maximum number of items that you want in the response. If additional items exist beyond the maximum that you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, it defaults to 100. Note that IAM might return fewer results, even when more results are available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_roles(self, PathPrefix: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the IAM roles that have the specified path prefix. If there are none, the operation returns an empty list. For more information about roles, go to `Working with Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListRoles>`_

        **Request Syntax**
        ::
          response = client.list_roles(
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Roles': [
                    {
                        'Path': 'string',
                        'RoleName': 'string',
                        'RoleId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'AssumeRolePolicyDocument': 'string',
                        'Description': 'string',
                        'MaxSessionDuration': 123,
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListRoles request.
            - **Roles** *(list) --*
              A list of roles.
              - *(dict) --*
                Contains information about an IAM role. This structure is returned as a response element in several API operations that interact with roles.
                - **Path** *(string) --*
                  The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **RoleName** *(string) --*
                  The friendly name that identifies the role.
                - **RoleId** *(string) --*
                  The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
                - **AssumeRolePolicyDocument** *(string) --*
                  The policy that grants an entity permission to assume the role.
                - **Description** *(string) --*
                  A description of the role that you provide.
                - **MaxSessionDuration** *(integer) --*
                  The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the role.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. For example, the prefix ``/application_abc/component_xyz/`` gets all roles whose path starts with ``/application_abc/component_xyz/`` .
          This parameter is optional. If it is not included, it defaults to a slash (/), listing all roles. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_saml_providers(self) -> Dict:
        """
        Lists the SAML provider resource objects defined in IAM in the account.
        .. note::
          This operation requires `Signature Version 4 <http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListSAMLProviders>`_

        **Request Syntax**
        ::
          response = client.list_saml_providers()

        **Response Syntax**
        ::
            {
                'SAMLProviderList': [
                    {
                        'Arn': 'string',
                        'ValidUntil': datetime(2015, 1, 1),
                        'CreateDate': datetime(2015, 1, 1)
                    },
                ]
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListSAMLProviders request.
            - **SAMLProviderList** *(list) --*
              The list of SAML provider resource objects defined in IAM for this AWS account.
              - *(dict) --*
                Contains the list of SAML providers for this account.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) of the SAML provider.
                - **ValidUntil** *(datetime) --*
                  The expiration date and time for the SAML provider.
                - **CreateDate** *(datetime) --*
                  The date and time when the SAML provider was created.
        :rtype: dict
        :returns:
        """
        pass

    def list_server_certificates(self, PathPrefix: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the server certificates stored in IAM that have the specified path prefix. If none exist, the operation returns an empty list.
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        For more information about working with server certificates, see `Working with Server Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`__ in the *IAM User Guide* . This topic also includes a list of AWS services that can use the server certificates that you manage with IAM.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListServerCertificates>`_

        **Request Syntax**
        ::
          response = client.list_server_certificates(
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'ServerCertificateMetadataList': [
                    {
                        'Path': 'string',
                        'ServerCertificateName': 'string',
                        'ServerCertificateId': 'string',
                        'Arn': 'string',
                        'UploadDate': datetime(2015, 1, 1),
                        'Expiration': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListServerCertificates request.
            - **ServerCertificateMetadataList** *(list) --*
              A list of server certificates.
              - *(dict) --*
                Contains information about a server certificate without its certificate body, certificate chain, and private key.
                This data type is used as a response element in the  UploadServerCertificate and  ListServerCertificates operations.
                - **Path** *(string) --*
                  The path to the server certificate. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **ServerCertificateName** *(string) --*
                  The name that identifies the server certificate.
                - **ServerCertificateId** *(string) --*
                  The stable and unique string identifying the server certificate. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) specifying the server certificate. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UploadDate** *(datetime) --*
                  The date when the server certificate was uploaded.
                - **Expiration** *(datetime) --*
                  The date on which the certificate is set to expire.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. For example: ``/company/servercerts`` would get all server certificates for which the path starts with ``/company/servercerts`` .
          This parameter is optional. If it is not included, it defaults to a slash (/), listing all server certificates. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_service_specific_credentials(self, UserName: str = None, ServiceName: str = None) -> Dict:
        """
        Returns information about the service-specific credentials associated with the specified IAM user. If none exists, the operation returns an empty list. The service-specific credentials returned by this operation are used only for authenticating the IAM user to a specific service. For more information about using service-specific credentials to authenticate to an AWS service, see `Set Up service-specific credentials <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html>`__ in the AWS CodeCommit User Guide.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListServiceSpecificCredentials>`_

        **Request Syntax**
        ::
          response = client.list_service_specific_credentials(
              UserName='string',
              ServiceName='string'
          )

        **Response Syntax**
        ::
            {
                'ServiceSpecificCredentials': [
                    {
                        'UserName': 'string',
                        'Status': 'Active'|'Inactive',
                        'ServiceUserName': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'ServiceSpecificCredentialId': 'string',
                        'ServiceName': 'string'
                    },
                ]
            }

        **Response Structure**
          - *(dict) --*
            - **ServiceSpecificCredentials** *(list) --*
              A list of structures that each contain details about a service-specific credential.
              - *(dict) --*
                Contains additional details about a service-specific credential.
                - **UserName** *(string) --*
                  The name of the IAM user associated with the service-specific credential.
                - **Status** *(string) --*
                  The status of the service-specific credential. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
                - **ServiceUserName** *(string) --*
                  The generated user name for the service-specific credential.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the service-specific credential were created.
                - **ServiceSpecificCredentialId** *(string) --*
                  The unique identifier for the service-specific credential.
                - **ServiceName** *(string) --*
                  The name of the service associated with the service-specific credential.
        :type UserName: string
        :param UserName:
          The name of the user whose service-specific credentials you want information about. If this value is not specified, then the operation assumes the user whose credentials are used to call the operation.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type ServiceName: string
        :param ServiceName:
          Filters the returned results to only those for the specified AWS service. If not specified, then AWS returns service-specific credentials for all services.
        :rtype: dict
        :returns:
        """
        pass

    def list_signing_certificates(self, UserName: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Returns information about the signing certificates associated with the specified IAM user. If there none exists, the operation returns an empty list.
        Although each user is limited to a small number of signing certificates, you can still paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        If the ``UserName`` field is not specified, the user name is determined implicitly based on the AWS access key ID used to sign the request for this API. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListSigningCertificates>`_

        **Request Syntax**
        ::
          response = client.list_signing_certificates(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Certificates': [
                    {
                        'UserName': 'string',
                        'CertificateId': 'string',
                        'CertificateBody': 'string',
                        'Status': 'Active'|'Inactive',
                        'UploadDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListSigningCertificates request.
            - **Certificates** *(list) --*
              A list of the user's signing certificate information.
              - *(dict) --*
                Contains information about an X.509 signing certificate.
                This data type is used as a response element in the  UploadSigningCertificate and  ListSigningCertificates operations.
                - **UserName** *(string) --*
                  The name of the user the signing certificate is associated with.
                - **CertificateId** *(string) --*
                  The ID for the signing certificate.
                - **CertificateBody** *(string) --*
                  The contents of the signing certificate.
                - **Status** *(string) --*
                  The status of the signing certificate. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
                - **UploadDate** *(datetime) --*
                  The date when the signing certificate was uploaded.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName:
          The name of the IAM user whose signing certificates you want to examine.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_ssh_public_keys(self, UserName: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Returns information about the SSH public keys associated with the specified IAM user. If there none exists, the operation returns an empty list.
        The SSH public keys returned by this operation are used only for authenticating the IAM user to an AWS CodeCommit repository. For more information about using SSH keys to authenticate to an AWS CodeCommit repository, see `Set up AWS CodeCommit for SSH Connections <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-credentials-ssh.html>`__ in the *AWS CodeCommit User Guide* .
        Although each user is limited to a small number of keys, you can still paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListSSHPublicKeys>`_

        **Request Syntax**
        ::
          response = client.list_ssh_public_keys(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'SSHPublicKeys': [
                    {
                        'UserName': 'string',
                        'SSHPublicKeyId': 'string',
                        'Status': 'Active'|'Inactive',
                        'UploadDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListSSHPublicKeys request.
            - **SSHPublicKeys** *(list) --*
              A list of the SSH public keys assigned to IAM user.
              - *(dict) --*
                Contains information about an SSH public key, without the key's body or fingerprint.
                This data type is used as a response element in the  ListSSHPublicKeys operation.
                - **UserName** *(string) --*
                  The name of the IAM user associated with the SSH public key.
                - **SSHPublicKeyId** *(string) --*
                  The unique identifier for the SSH public key.
                - **Status** *(string) --*
                  The status of the SSH public key. ``Active`` means that the key can be used for authentication with an AWS CodeCommit repository. ``Inactive`` means that the key cannot be used.
                - **UploadDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the SSH public key was uploaded.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName:
          The name of the IAM user to list SSH public keys for. If none is specified, the ``UserName`` field is determined implicitly based on the AWS access key used to sign the request.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_user_policies(self, UserName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the names of the inline policies embedded in the specified IAM user.
        An IAM user can also have managed policies attached to it. To list the managed policies that are attached to a user, use  ListAttachedUserPolicies . For more information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters. If there are no inline policies embedded with the specified user, the operation returns an empty list.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListUserPolicies>`_

        **Request Syntax**
        ::
          response = client.list_user_policies(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'PolicyNames': [
                    'string',
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListUserPolicies request.
            - **PolicyNames** *(list) --*
              A list of policy names.
              - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to list policies for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_user_tags(self, UserName: str, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the tags that are attached to the specified user. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListUserTags>`_

        **Request Syntax**
        ::
          response = client.list_user_tags(
              UserName='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            - **Tags** *(list) --*
              The list of tags that are currently attached to the user. Each tag consists of a key name and an associated value. If no tags are attached to the specified user, the response contains an empty list.
              - *(dict) --*
                A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - **Key** *(string) --*
                  The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                - **Value** *(string) --*
                  The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                  .. note::
                    AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can use the ``Marker`` request parameter to make a subsequent pagination request that retrieves more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when more results are available. Check ``IsTruncated`` after every call to ensure that you receive all of your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user whose tags you want to see.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@-
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          (Optional) Use this only when paginating results to indicate the maximum number of items that you want in the response. If additional items exist beyond the maximum that you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, it defaults to 100. Note that IAM might return fewer results, even when more results are available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_users(self, PathPrefix: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the IAM users that have the specified path prefix. If no path prefix is specified, the operation returns all users in the AWS account. If there are none, the operation returns an empty list.
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListUsers>`_

        **Request Syntax**
        ::
          response = client.list_users(
              PathPrefix='string',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'Users': [
                    {
                        'Path': 'string',
                        'UserName': 'string',
                        'UserId': 'string',
                        'Arn': 'string',
                        'CreateDate': datetime(2015, 1, 1),
                        'PasswordLastUsed': datetime(2015, 1, 1),
                        'PermissionsBoundary': {
                            'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                            'PermissionsBoundaryArn': 'string'
                        },
                        'Tags': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListUsers request.
            - **Users** *(list) --*
              A list of users.
              - *(dict) --*
                Contains information about an IAM user entity.
                This data type is used as a response element in the following operations:
                *  CreateUser
                *  GetUser
                *  ListUsers
                - **Path** *(string) --*
                  The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **UserName** *(string) --*
                  The friendly name identifying the user.
                - **UserId** *(string) --*
                  The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **Arn** *(string) --*
                  The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                - **CreateDate** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
                - **PasswordLastUsed** *(datetime) --*
                  The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                  * The user never had a password.
                  * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                  A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                  This value is returned only in the  GetUser and  ListUsers operations.
                - **PermissionsBoundary** *(dict) --*
                  The ARN of the policy used to set the permissions boundary for the user.
                  For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                  - **PermissionsBoundaryType** *(string) --*
                    The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                  - **PermissionsBoundaryArn** *(string) --*
                    The ARN of the policy used to set the permissions boundary for the user or role.
                - **Tags** *(list) --*
                  A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - *(dict) --*
                    A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - **Key** *(string) --*
                      The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                    - **Value** *(string) --*
                      The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                      .. note::
                        AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PathPrefix: string
        :param PathPrefix:
          The path prefix for filtering the results. For example: ``/division_abc/subdivision_xyz/`` , which would get all user names whose path starts with ``/division_abc/subdivision_xyz/`` .
          This parameter is optional. If it is not included, it defaults to a slash (/), listing all user names. This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def list_virtual_mfa_devices(self, AssignmentStatus: str = None, Marker: str = None, MaxItems: int = None) -> Dict:
        """
        Lists the virtual MFA devices defined in the AWS account by assignment status. If you do not specify an assignment status, the operation returns a list of all virtual MFA devices. Assignment status can be ``Assigned`` , ``Unassigned`` , or ``Any`` .
        You can paginate the results using the ``MaxItems`` and ``Marker`` parameters.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ListVirtualMFADevices>`_

        **Request Syntax**
        ::
          response = client.list_virtual_mfa_devices(
              AssignmentStatus='Assigned'|'Unassigned'|'Any',
              Marker='string',
              MaxItems=123
          )

        **Response Syntax**
        ::
            {
                'VirtualMFADevices': [
                    {
                        'SerialNumber': 'string',
                        'Base32StringSeed': b'bytes',
                        'QRCodePNG': b'bytes',
                        'User': {
                            'Path': 'string',
                            'UserName': 'string',
                            'UserId': 'string',
                            'Arn': 'string',
                            'CreateDate': datetime(2015, 1, 1),
                            'PasswordLastUsed': datetime(2015, 1, 1),
                            'PermissionsBoundary': {
                                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                                'PermissionsBoundaryArn': 'string'
                            },
                            'Tags': [
                                {
                                    'Key': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                        'EnableDate': datetime(2015, 1, 1)
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  ListVirtualMFADevices request.
            - **VirtualMFADevices** *(list) --*
              The list of virtual MFA devices in the current account that match the ``AssignmentStatus`` value that was passed in the request.
              - *(dict) --*
                Contains information about a virtual MFA device.
                - **SerialNumber** *(string) --*
                  The serial number associated with ``VirtualMFADevice`` .
                - **Base32StringSeed** *(bytes) --*
                  The base32 seed defined as specified in `RFC3548 <https://tools.ietf.org/html/rfc3548.txt>`__ . The ``Base32StringSeed`` is base64-encoded.
                - **QRCodePNG** *(bytes) --*
                  A QR code PNG image that encodes ``otpauth://totp/$virtualMFADeviceName@$AccountName?secret=$Base32String`` where ``$virtualMFADeviceName`` is one of the create call arguments. ``AccountName`` is the user name if set (otherwise, the account ID otherwise), and ``Base32String`` is the seed in base32 format. The ``Base32String`` value is base64-encoded.
                - **User** *(dict) --*
                  The IAM user associated with this virtual MFA device.
                  - **Path** *(string) --*
                    The path to the user. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **UserName** *(string) --*
                    The friendly name identifying the user.
                  - **UserId** *(string) --*
                    The stable and unique string identifying the user. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **Arn** *(string) --*
                    The Amazon Resource Name (ARN) that identifies the user. For more information about ARNs and how to use ARNs in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
                  - **CreateDate** *(datetime) --*
                    The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user was created.
                  - **PasswordLastUsed** *(datetime) --*
                    The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the user's password was last used to sign in to an AWS website. For a list of AWS websites that capture a user's last sign-in time, see the `Credential Reports <http://docs.aws.amazon.com/IAM/latest/UserGuide/credential-reports.html>`__ topic in the *Using IAM* guide. If a password is used more than once in a five-minute span, only the first use is returned in this field. If the field is null (no value), then it indicates that they never signed in with a password. This can be because:
                    * The user never had a password.
                    * A password exists but has not been used since IAM started tracking this information on October 20, 2014.
                    A null valuedoes not mean that the user *never* had a password. Also, if the user does not currently have a password, but had one in the past, then this field contains the date and time the most recent password was used.
                    This value is returned only in the  GetUser and  ListUsers operations.
                  - **PermissionsBoundary** *(dict) --*
                    The ARN of the policy used to set the permissions boundary for the user.
                    For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                    - **PermissionsBoundaryType** *(string) --*
                      The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                    - **PermissionsBoundaryArn** *(string) --*
                      The ARN of the policy used to set the permissions boundary for the user or role.
                  - **Tags** *(list) --*
                    A list of tags that are associated with the specified user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                    - *(dict) --*
                      A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                      - **Key** *(string) --*
                        The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                      - **Value** *(string) --*
                        The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                        .. note::
                          AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
                - **EnableDate** *(datetime) --*
                  The date and time on which the virtual MFA device was enabled.
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type AssignmentStatus: string
        :param AssignmentStatus:
          The status (``Unassigned`` or ``Assigned`` ) of the devices to list. If you do not specify an ``AssignmentStatus`` , the operation defaults to ``Any`` , which lists both assigned and unassigned virtual MFA devices.,
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :rtype: dict
        :returns:
        """
        pass

    def put_group_policy(self, GroupName: str, PolicyName: str, PolicyDocument: str):
        """
        Adds or updates an inline policy document that is embedded in the specified IAM group.
        A user can also have managed policies attached to it. To attach a managed policy to a group, use  AttachGroupPolicy . To create a new managed policy, use  CreatePolicy . For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        .. note::
          Because policy documents can be large, you should use POST rather than GET when calling ``PutGroupPolicy`` . For general information about using the Query API with IAM, go to `Making Query Requests <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_UsingQueryAPI.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/PutGroupPolicy>`_

        **Request Syntax**
        ::
          response = client.put_group_policy(
              GroupName='string',
              PolicyName='string',
              PolicyDocument='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group to associate the policy with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The policy document.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :returns: None
        """
        pass

    def put_role_permissions_boundary(self, RoleName: str, PermissionsBoundary: str):
        """
        Adds or updates the policy that is specified as the IAM role's permissions boundary. You can use an AWS managed policy or a customer managed policy to set the boundary for a role. Use the boundary to control the maximum permissions that the role can have. Setting a permissions boundary is an advanced feature that can affect the permissions for the role.
        You cannot set the boundary for a service-linked role.
        .. warning::
          Policies used as permissions boundaries do not provide permissions. You must also attach a permissions policy to the role. To learn how the effective permissions for a role are evaluated, see `IAM JSON Policy Evaluation Logic <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`__ in the IAM User Guide.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/PutRolePermissionsBoundary>`_

        **Request Syntax**
        ::
          response = client.put_role_permissions_boundary(
              RoleName='string',
              PermissionsBoundary='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM role for which you want to set the permissions boundary.
        :type PermissionsBoundary: string
        :param PermissionsBoundary: **[REQUIRED]**
          The ARN of the policy that is used to set the permissions boundary for the role.
        :returns: None
        """
        pass

    def put_role_policy(self, RoleName: str, PolicyName: str, PolicyDocument: str):
        """
        Adds or updates an inline policy document that is embedded in the specified IAM role.
        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role, using  CreateRole . You can update a role's trust policy using  UpdateAssumeRolePolicy . For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`__ .
        A role can also have a managed policy attached to it. To attach a managed policy to a role, use  AttachRolePolicy . To create a new managed policy, use  CreatePolicy . For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        .. note::
          Because policy documents can be large, you should use POST rather than GET when calling ``PutRolePolicy`` . For general information about using the Query API with IAM, go to `Making Query Requests <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_UsingQueryAPI.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/PutRolePolicy>`_

        **Request Syntax**
        ::
          response = client.put_role_policy(
              RoleName='string',
              PolicyName='string',
              PolicyDocument='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to associate the policy with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The policy document.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :returns: None
        """
        pass

    def put_user_permissions_boundary(self, UserName: str, PermissionsBoundary: str):
        """
        Adds or updates the policy that is specified as the IAM user's permissions boundary. You can use an AWS managed policy or a customer managed policy to set the boundary for a user. Use the boundary to control the maximum permissions that the user can have. Setting a permissions boundary is an advanced feature that can affect the permissions for the user.
        .. warning::
          Policies that are used as permissions boundaries do not provide permissions. You must also attach a permissions policy to the user. To learn how the effective permissions for a user are evaluated, see `IAM JSON Policy Evaluation Logic <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`__ in the IAM User Guide.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/PutUserPermissionsBoundary>`_

        **Request Syntax**
        ::
          response = client.put_user_permissions_boundary(
              UserName='string',
              PermissionsBoundary='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name (friendly name, not ARN) of the IAM user for which you want to set the permissions boundary.
        :type PermissionsBoundary: string
        :param PermissionsBoundary: **[REQUIRED]**
          The ARN of the policy that is used to set the permissions boundary for the user.
        :returns: None
        """
        pass

    def put_user_policy(self, UserName: str, PolicyName: str, PolicyDocument: str):
        """
        Adds or updates an inline policy document that is embedded in the specified IAM user.
        An IAM user can also have a managed policy attached to it. To attach a managed policy to a user, use  AttachUserPolicy . To create a new managed policy, use  CreatePolicy . For information about policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <http://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`__ in the *IAM User Guide* .
        .. note::
          Because policy documents can be large, you should use POST rather than GET when calling ``PutUserPolicy`` . For general information about using the Query API with IAM, go to `Making Query Requests <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_UsingQueryAPI.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/PutUserPolicy>`_

        **Request Syntax**
        ::
          response = client.put_user_policy(
              UserName='string',
              PolicyName='string',
              PolicyDocument='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to associate the policy with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyName: string
        :param PolicyName: **[REQUIRED]**
          The name of the policy document.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The policy document.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :returns: None
        """
        pass

    def remove_client_id_from_open_id_connect_provider(self, OpenIDConnectProviderArn: str, ClientID: str):
        """
        Removes the specified client ID (also known as audience) from the list of client IDs registered for the specified IAM OpenID Connect (OIDC) provider resource object.
        This operation is idempotent; it does not fail or return an error if you try to remove a client ID that does not exist.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/RemoveClientIDFromOpenIDConnectProvider>`_

        **Request Syntax**
        ::
          response = client.remove_client_id_from_open_id_connect_provider(
              OpenIDConnectProviderArn='string',
              ClientID='string'
          )
        :type OpenIDConnectProviderArn: string
        :param OpenIDConnectProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM OIDC provider resource to remove the client ID from. You can get a list of OIDC provider ARNs by using the  ListOpenIDConnectProviders operation.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type ClientID: string
        :param ClientID: **[REQUIRED]**
          The client ID (also known as audience) to remove from the IAM OIDC provider resource. For more information about client IDs, see  CreateOpenIDConnectProvider .
        :returns: None
        """
        pass

    def remove_role_from_instance_profile(self, InstanceProfileName: str, RoleName: str):
        """
        Removes the specified IAM role from the specified EC2 instance profile.
        .. warning::
          Make sure that you do not have any Amazon EC2 instances running with the role you are about to remove from the instance profile. Removing a role from an instance profile that is associated with a running instance might break any applications running on the instance.
        For more information about IAM roles, go to `Working with Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`__ . For more information about instance profiles, go to `About Instance Profiles <http://docs.aws.amazon.com/IAM/latest/UserGuide/AboutInstanceProfiles.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/RemoveRoleFromInstanceProfile>`_

        **Request Syntax**
        ::
          response = client.remove_role_from_instance_profile(
              InstanceProfileName='string',
              RoleName='string'
          )
        :type InstanceProfileName: string
        :param InstanceProfileName: **[REQUIRED]**
          The name of the instance profile to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to remove.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def remove_user_from_group(self, GroupName: str, UserName: str):
        """
        Removes the specified user from the specified group.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/RemoveUserFromGroup>`_

        **Request Syntax**
        ::
          response = client.remove_user_from_group(
              GroupName='string',
              UserName='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          The name of the group to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user to remove.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def reset_service_specific_credential(self, ServiceSpecificCredentialId: str, UserName: str = None) -> Dict:
        """
        Resets the password for a service-specific credential. The new password is AWS generated and cryptographically strong. It cannot be configured by the user. Resetting the password immediately invalidates the previous password associated with this user.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ResetServiceSpecificCredential>`_

        **Request Syntax**
        ::
          response = client.reset_service_specific_credential(
              UserName='string',
              ServiceSpecificCredentialId='string'
          )

        **Response Syntax**
        ::
            {
                'ServiceSpecificCredential': {
                    'CreateDate': datetime(2015, 1, 1),
                    'ServiceName': 'string',
                    'ServiceUserName': 'string',
                    'ServicePassword': 'string',
                    'ServiceSpecificCredentialId': 'string',
                    'UserName': 'string',
                    'Status': 'Active'|'Inactive'
                }
            }

        **Response Structure**
          - *(dict) --*
            - **ServiceSpecificCredential** *(dict) --*
              A structure with details about the updated service-specific credential, including the new password.
              .. warning::
                This is the **only** time that you can access the password. You cannot recover the password later, but you can reset it again.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the service-specific credential were created.
              - **ServiceName** *(string) --*
                The name of the service associated with the service-specific credential.
              - **ServiceUserName** *(string) --*
                The generated user name for the service-specific credential. This value is generated by combining the IAM user's name combined with the ID number of the AWS account, as in ``jane-at-123456789012`` , for example. This value cannot be configured by the user.
              - **ServicePassword** *(string) --*
                The generated password for the service-specific credential.
              - **ServiceSpecificCredentialId** *(string) --*
                The unique identifier for the service-specific credential.
              - **UserName** *(string) --*
                The name of the IAM user associated with the service-specific credential.
              - **Status** *(string) --*
                The status of the service-specific credential. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
        :type UserName: string
        :param UserName:
          The name of the IAM user associated with the service-specific credential. If this value is not specified, then the operation assumes the user whose credentials are used to call the operation.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type ServiceSpecificCredentialId: string
        :param ServiceSpecificCredentialId: **[REQUIRED]**
          The unique identifier of the service-specific credential.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :rtype: dict
        :returns:
        """
        pass

    def resync_mfa_device(self, UserName: str, SerialNumber: str, AuthenticationCode1: str, AuthenticationCode2: str):
        """
        Synchronizes the specified MFA device with its IAM resource object on the AWS servers.
        For more information about creating and working with virtual MFA devices, go to `Using a Virtual MFA Device <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/ResyncMFADevice>`_

        **Request Syntax**
        ::
          response = client.resync_mfa_device(
              UserName='string',
              SerialNumber='string',
              AuthenticationCode1='string',
              AuthenticationCode2='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user whose MFA device you want to resynchronize.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SerialNumber: string
        :param SerialNumber: **[REQUIRED]**
          Serial number that uniquely identifies the MFA device.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type AuthenticationCode1: string
        :param AuthenticationCode1: **[REQUIRED]**
          An authentication code emitted by the device.
          The format for this parameter is a sequence of six digits.
        :type AuthenticationCode2: string
        :param AuthenticationCode2: **[REQUIRED]**
          A subsequent authentication code emitted by the device.
          The format for this parameter is a sequence of six digits.
        :returns: None
        """
        pass

    def set_default_policy_version(self, PolicyArn: str, VersionId: str):
        """
        Sets the specified version of the specified policy as the policy's default (operative) version.
        This operation affects all users, groups, and roles that the policy is attached to. To list the users, groups, and roles that the policy is attached to, use the  ListEntitiesForPolicy API.
        For information about managed policies, see `Managed Policies and Inline Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/SetDefaultPolicyVersion>`_

        **Request Syntax**
        ::
          response = client.set_default_policy_version(
              PolicyArn='string',
              VersionId='string'
          )
        :type PolicyArn: string
        :param PolicyArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM policy whose default version you want to set.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type VersionId: string
        :param VersionId: **[REQUIRED]**
          The version of the policy to set as the default (operative) version.
          For more information about managed policy versions, see `Versioning for Managed Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`__ in the *IAM User Guide* .
        :returns: None
        """
        pass

    def simulate_custom_policy(self, PolicyInputList: List, ActionNames: List, ResourceArns: List = None,
                               ResourcePolicy: str = None, ResourceOwner: str = None, CallerArn: str = None,
                               ContextEntries: List = None, ResourceHandlingOption: str = None, MaxItems: int = None,
                               Marker: str = None) -> Dict:
        """
        Simulate how a set of IAM policies and optionally a resource-based policy works with a list of API operations and AWS resources to determine the policies' effective permissions. The policies are provided as strings.
        The simulation does not perform the API operations; it only checks the authorization to determine if the simulated policies allow or deny the operations.
        If you want to simulate existing policies attached to an IAM user, group, or role, use  SimulatePrincipalPolicy instead.
        Context keys are variables maintained by AWS and its services that provide details about the context of an API query request. You can use the ``Condition`` element of an IAM policy to evaluate context keys. To get the list of context keys that the policies require for correct simulation, use  GetContextKeysForCustomPolicy .
        If the output is long, you can use ``MaxItems`` and ``Marker`` parameters to paginate the results.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/SimulateCustomPolicy>`_

        **Request Syntax**
        ::
          response = client.simulate_custom_policy(
              PolicyInputList=[
                  'string',
              ],
              ActionNames=[
                  'string',
              ],
              ResourceArns=[
                  'string',
              ],
              ResourcePolicy='string',
              ResourceOwner='string',
              CallerArn='string',
              ContextEntries=[
                  {
                      'ContextKeyName': 'string',
                      'ContextKeyValues': [
                          'string',
                      ],
                      'ContextKeyType': 'string'|'stringList'|'numeric'|'numericList'|'boolean'|'booleanList'|'ip'|'ipList'|'binary'|'binaryList'|'date'|'dateList'
                  },
              ],
              ResourceHandlingOption='string',
              MaxItems=123,
              Marker='string'
          )

        **Response Syntax**
        ::
            {
                'EvaluationResults': [
                    {
                        'EvalActionName': 'string',
                        'EvalResourceName': 'string',
                        'EvalDecision': 'allowed'|'explicitDeny'|'implicitDeny',
                        'MatchedStatements': [
                            {
                                'SourcePolicyId': 'string',
                                'SourcePolicyType': 'user'|'group'|'role'|'aws-managed'|'user-managed'|'resource'|'none',
                                'StartPosition': {
                                    'Line': 123,
                                    'Column': 123
                                },
                                'EndPosition': {
                                    'Line': 123,
                                    'Column': 123
                                }
                            },
                        ],
                        'MissingContextValues': [
                            'string',
                        ],
                        'OrganizationsDecisionDetail': {
                            'AllowedByOrganizations': True|False
                        },
                        'EvalDecisionDetails': {
                            'string': 'allowed'|'explicitDeny'|'implicitDeny'
                        },
                        'ResourceSpecificResults': [
                            {
                                'EvalResourceName': 'string',
                                'EvalResourceDecision': 'allowed'|'explicitDeny'|'implicitDeny',
                                'MatchedStatements': [
                                    {
                                        'SourcePolicyId': 'string',
                                        'SourcePolicyType': 'user'|'group'|'role'|'aws-managed'|'user-managed'|'resource'|'none',
                                        'StartPosition': {
                                            'Line': 123,
                                            'Column': 123
                                        },
                                        'EndPosition': {
                                            'Line': 123,
                                            'Column': 123
                                        }
                                    },
                                ],
                                'MissingContextValues': [
                                    'string',
                                ],
                                'EvalDecisionDetails': {
                                    'string': 'allowed'|'explicitDeny'|'implicitDeny'
                                }
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  SimulatePrincipalPolicy or  SimulateCustomPolicy request.
            - **EvaluationResults** *(list) --*
              The results of the simulation.
              - *(dict) --*
                Contains the results of a simulation.
                This data type is used by the return parameter of ``  SimulateCustomPolicy `` and ``  SimulatePrincipalPolicy `` .
                - **EvalActionName** *(string) --*
                  The name of the API operation tested on the indicated resource.
                - **EvalResourceName** *(string) --*
                  The ARN of the resource that the indicated API operation was tested on.
                - **EvalDecision** *(string) --*
                  The result of the simulation.
                - **MatchedStatements** *(list) --*
                  A list of the statements in the input policies that determine the result for this scenario. Remember that even if multiple statements allow the operation on the resource, if only one statement denies that operation, then the explicit deny overrides any allow. Inaddition, the deny statement is the only entry included in the result.
                  - *(dict) --*
                    Contains a reference to a ``Statement`` element in a policy document that determines the result of the simulation.
                    This data type is used by the ``MatchedStatements`` member of the ``  EvaluationResult `` type.
                    - **SourcePolicyId** *(string) --*
                      The identifier of the policy that was provided as an input.
                    - **SourcePolicyType** *(string) --*
                      The type of the policy.
                    - **StartPosition** *(dict) --*
                      The row and column of the beginning of the ``Statement`` in an IAM policy.
                      - **Line** *(integer) --*
                        The line containing the specified position in the document.
                      - **Column** *(integer) --*
                        The column in the line containing the specified position in the document.
                    - **EndPosition** *(dict) --*
                      The row and column of the end of a ``Statement`` in an IAM policy.
                      - **Line** *(integer) --*
                        The line containing the specified position in the document.
                      - **Column** *(integer) --*
                        The column in the line containing the specified position in the document.
                - **MissingContextValues** *(list) --*
                  A list of context keys that are required by the included input policies but that were not provided by one of the input parameters. This list is used when the resource in a simulation is "*", either explicitly, or when the ``ResourceArns`` parameter blank. If you include a list of resources, then any missing context values are instead included under the ``ResourceSpecificResults`` section. To discover the context keys used by a set of policies, you can call  GetContextKeysForCustomPolicy or  GetContextKeysForPrincipalPolicy .
                  - *(string) --*
                - **OrganizationsDecisionDetail** *(dict) --*
                  A structure that details how AWS Organizations and its service control policies affect the results of the simulation. Only applies if the simulated user's account is part of an organization.
                  - **AllowedByOrganizations** *(boolean) --*
                    Specifies whether the simulated operation is allowed by the AWS Organizations service control policies that impact the simulated user's account.
                - **EvalDecisionDetails** *(dict) --*
                  Additional details about the results of the evaluation decision. When there are both IAM policies and resource policies, this parameter explains how each set of policies contributes to the final evaluation decision. When simulating cross-account access to a resource, both the resource-based policy and the caller's IAM policy must grant access. See `How IAM Roles Differ from Resource-based Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html>`__
                  - *(string) --*
                    - *(string) --*
                - **ResourceSpecificResults** *(list) --*
                  The individual results of the simulation of the API operation specified in EvalActionName on each resource.
                  - *(dict) --*
                    Contains the result of the simulation of a single API operation call on a single resource.
                    This data type is used by a member of the  EvaluationResult data type.
                    - **EvalResourceName** *(string) --*
                      The name of the simulated resource, in Amazon Resource Name (ARN) format.
                    - **EvalResourceDecision** *(string) --*
                      The result of the simulation of the simulated API operation on the resource specified in ``EvalResourceName`` .
                    - **MatchedStatements** *(list) --*
                      A list of the statements in the input policies that determine the result for this part of the simulation. Remember that even if multiple statements allow the operation on the resource, if *any* statement denies that operation, then the explicit deny overrides any allow. In addition, the deny statement is the only entry included in the result.
                      - *(dict) --*
                        Contains a reference to a ``Statement`` element in a policy document that determines the result of the simulation.
                        This data type is used by the ``MatchedStatements`` member of the ``  EvaluationResult `` type.
                        - **SourcePolicyId** *(string) --*
                          The identifier of the policy that was provided as an input.
                        - **SourcePolicyType** *(string) --*
                          The type of the policy.
                        - **StartPosition** *(dict) --*
                          The row and column of the beginning of the ``Statement`` in an IAM policy.
                          - **Line** *(integer) --*
                            The line containing the specified position in the document.
                          - **Column** *(integer) --*
                            The column in the line containing the specified position in the document.
                        - **EndPosition** *(dict) --*
                          The row and column of the end of a ``Statement`` in an IAM policy.
                          - **Line** *(integer) --*
                            The line containing the specified position in the document.
                          - **Column** *(integer) --*
                            The column in the line containing the specified position in the document.
                    - **MissingContextValues** *(list) --*
                      A list of context keys that are required by the included input policies but that were not provided by one of the input parameters. This list is used when a list of ARNs is included in the ``ResourceArns`` parameter instead of "*". If you do not specify individual resources, by setting ``ResourceArns`` to "*" or by not including the ``ResourceArns`` parameter, then any missing context values are instead included under the ``EvaluationResults`` section. To discover the context keys used by a set of policies, you can call  GetContextKeysForCustomPolicy or  GetContextKeysForPrincipalPolicy .
                      - *(string) --*
                    - **EvalDecisionDetails** *(dict) --*
                      Additional details about the results of the evaluation decision. When there are both IAM policies and resource policies, this parameter explains how each set of policies contributes to the final evaluation decision. When simulating cross-account access to a resource, both the resource-based policy and the caller's IAM policy must grant access.
                      - *(string) --*
                        - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PolicyInputList: list
        :param PolicyInputList: **[REQUIRED]**
          A list of policy documents to include in the simulation. Each document is specified as a string containing the complete, valid JSON text of an IAM policy. Do not include any resource-based policies in this parameter. Any resource-based policy must be submitted with the ``ResourcePolicy`` parameter. The policies cannot be \"scope-down\" policies, such as you could include in a call to `GetFederationToken <http://docs.aws.amazon.com/IAM/latest/APIReference/API_GetFederationToken.html>`__ or one of the `AssumeRole <http://docs.aws.amazon.com/IAM/latest/APIReference/API_AssumeRole.html>`__ API operations. In other words, do not use policies designed to restrict what a user can do while using the temporary credentials.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
          - *(string) --*
        :type ActionNames: list
        :param ActionNames: **[REQUIRED]**
          A list of names of API operations to evaluate in the simulation. Each operation is evaluated against each resource. Each operation must include the service identifier, such as ``iam:CreateUser`` .
          - *(string) --*
        :type ResourceArns: list
        :param ResourceArns:
          A list of ARNs of AWS resources to include in the simulation. If this parameter is not provided, then the value defaults to ``*`` (all resources). Each API in the ``ActionNames`` parameter is evaluated for each resource in this list. The simulation determines the access result (allowed or denied) of each combination and reports it in the response.
          The simulation does not automatically retrieve policies for the specified resources. If you want to include a resource policy in the simulation, then you must include the policy as a string in the ``ResourcePolicy`` parameter.
          If you include a ``ResourcePolicy`` , then it must be applicable to all of the resources included in the simulation or you receive an invalid input error.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
          - *(string) --*
        :type ResourcePolicy: string
        :param ResourcePolicy:
          A resource-based policy to include in the simulation provided as a string. Each resource in the simulation is treated as if it had this policy attached. You can include only one resource-based policy in a simulation.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type ResourceOwner: string
        :param ResourceOwner:
          An ARN representing the AWS account ID that specifies the owner of any simulated resource that does not identify its owner in the resource ARN, such as an S3 bucket or object. If ``ResourceOwner`` is specified, it is also used as the account owner of any ``ResourcePolicy`` included in the simulation. If the ``ResourceOwner`` parameter is not specified, then the owner of the resources and the resource policy defaults to the account of the identity provided in ``CallerArn`` . This parameter is required only if you specify a resource-based policy and account that owns the resource is different from the account that owns the simulated calling user ``CallerArn`` .
          The ARN for an account uses the following syntax: ``arn:aws:iam::*AWS-account-ID* :root`` . For example, to represent the account with the 112233445566 ID, use the following ARN: ``arn:aws:iam::112233445566-ID:root`` .
        :type CallerArn: string
        :param CallerArn:
          The ARN of the IAM user that you want to use as the simulated caller of the API operations. ``CallerArn`` is required if you include a ``ResourcePolicy`` so that the policy\'s ``Principal`` element has a value to use in evaluating the policy.
          You can specify only the ARN of an IAM user. You cannot specify the ARN of an assumed role, federated user, or a service principal.
        :type ContextEntries: list
        :param ContextEntries:
          A list of context keys and corresponding values for the simulation to use. Whenever a context key is evaluated in one of the simulated IAM permission policies, the corresponding value is supplied.
          - *(dict) --*
            Contains information about a condition context key. It includes the name of the key and specifies the value (or values, if the context key supports multiple values) to use in the simulation. This information is used when evaluating the ``Condition`` elements of the input policies.
            This data type is used as an input parameter to ``  SimulateCustomPolicy `` and ``  SimulateCustomPolicy `` .
            - **ContextKeyName** *(string) --*
              The full name of a condition context key, including the service prefix. For example, ``aws:SourceIp`` or ``s3:VersionId`` .
            - **ContextKeyValues** *(list) --*
              The value (or values, if the condition context key supports multiple values) to provide to the simulation when the key is referenced by a ``Condition`` element in an input policy.
              - *(string) --*
            - **ContextKeyType** *(string) --*
              The data type of the value (or values) specified in the ``ContextKeyValues`` parameter.
        :type ResourceHandlingOption: string
        :param ResourceHandlingOption:
          Specifies the type of simulation to run. Different API operations that support resource-based policies require different combinations of resources. By specifying the type of simulation to run, you enable the policy simulator to enforce the presence of the required resources to ensure reliable simulation results. If your simulation does not match one of the following scenarios, then you can omit this parameter. The following list shows each of the supported scenario values and the resources that you must define to run the simulation.
          Each of the EC2 scenarios requires that you specify instance, image, and security-group resources. If your scenario includes an EBS volume, then you must specify that volume as a resource. If the EC2 scenario includes VPC, then you must supply the network-interface resource. If it includes an IP subnet, then you must specify the subnet resource. For more information on the EC2 scenario options, see `Supported Platforms <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`__ in the *Amazon EC2 User Guide* .
          * **EC2-Classic-InstanceStore**   instance, image, security-group
          * **EC2-Classic-EBS**   instance, image, security-group, volume
          * **EC2-VPC-InstanceStore**   instance, image, security-group, network-interface
          * **EC2-VPC-InstanceStore-Subnet**   instance, image, security-group, network-interface, subnet
          * **EC2-VPC-EBS**   instance, image, security-group, network-interface, volume
          * **EC2-VPC-EBS-Subnet**   instance, image, security-group, network-interface, subnet, volume
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :rtype: dict
        :returns:
        """
        pass

    def simulate_principal_policy(self, PolicySourceArn: str, ActionNames: List, PolicyInputList: List = None,
                                  ResourceArns: List = None, ResourcePolicy: str = None, ResourceOwner: str = None,
                                  CallerArn: str = None, ContextEntries: List = None,
                                  ResourceHandlingOption: str = None, MaxItems: int = None, Marker: str = None) -> Dict:
        """
        Simulate how a set of IAM policies attached to an IAM entity works with a list of API operations and AWS resources to determine the policies' effective permissions. The entity can be an IAM user, group, or role. If you specify a user, then the simulation also includes all of the policies that are attached to groups that the user belongs to.
        You can optionally include a list of one or more additional policies specified as strings to include in the simulation. If you want to simulate only policies specified as strings, use  SimulateCustomPolicy instead.
        You can also optionally include one resource-based policy to be evaluated with each of the resources included in the simulation.
        The simulation does not perform the API operations, it only checks the authorization to determine if the simulated policies allow or deny the operations.
         **Note:** This API discloses information about the permissions granted to other users. If you do not want users to see other user's permissions, then consider allowing them to use  SimulateCustomPolicy instead.
        Context keys are variables maintained by AWS and its services that provide details about the context of an API query request. You can use the ``Condition`` element of an IAM policy to evaluate context keys. To get the list of context keys that the policies require for correct simulation, use  GetContextKeysForPrincipalPolicy .
        If the output is long, you can use the ``MaxItems`` and ``Marker`` parameters to paginate the results.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/SimulatePrincipalPolicy>`_

        **Request Syntax**
        ::
          response = client.simulate_principal_policy(
              PolicySourceArn='string',
              PolicyInputList=[
                  'string',
              ],
              ActionNames=[
                  'string',
              ],
              ResourceArns=[
                  'string',
              ],
              ResourcePolicy='string',
              ResourceOwner='string',
              CallerArn='string',
              ContextEntries=[
                  {
                      'ContextKeyName': 'string',
                      'ContextKeyValues': [
                          'string',
                      ],
                      'ContextKeyType': 'string'|'stringList'|'numeric'|'numericList'|'boolean'|'booleanList'|'ip'|'ipList'|'binary'|'binaryList'|'date'|'dateList'
                  },
              ],
              ResourceHandlingOption='string',
              MaxItems=123,
              Marker='string'
          )

        **Response Syntax**
        ::
            {
                'EvaluationResults': [
                    {
                        'EvalActionName': 'string',
                        'EvalResourceName': 'string',
                        'EvalDecision': 'allowed'|'explicitDeny'|'implicitDeny',
                        'MatchedStatements': [
                            {
                                'SourcePolicyId': 'string',
                                'SourcePolicyType': 'user'|'group'|'role'|'aws-managed'|'user-managed'|'resource'|'none',
                                'StartPosition': {
                                    'Line': 123,
                                    'Column': 123
                                },
                                'EndPosition': {
                                    'Line': 123,
                                    'Column': 123
                                }
                            },
                        ],
                        'MissingContextValues': [
                            'string',
                        ],
                        'OrganizationsDecisionDetail': {
                            'AllowedByOrganizations': True|False
                        },
                        'EvalDecisionDetails': {
                            'string': 'allowed'|'explicitDeny'|'implicitDeny'
                        },
                        'ResourceSpecificResults': [
                            {
                                'EvalResourceName': 'string',
                                'EvalResourceDecision': 'allowed'|'explicitDeny'|'implicitDeny',
                                'MatchedStatements': [
                                    {
                                        'SourcePolicyId': 'string',
                                        'SourcePolicyType': 'user'|'group'|'role'|'aws-managed'|'user-managed'|'resource'|'none',
                                        'StartPosition': {
                                            'Line': 123,
                                            'Column': 123
                                        },
                                        'EndPosition': {
                                            'Line': 123,
                                            'Column': 123
                                        }
                                    },
                                ],
                                'MissingContextValues': [
                                    'string',
                                ],
                                'EvalDecisionDetails': {
                                    'string': 'allowed'|'explicitDeny'|'implicitDeny'
                                }
                            },
                        ]
                    },
                ],
                'IsTruncated': True|False,
                'Marker': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  SimulatePrincipalPolicy or  SimulateCustomPolicy request.
            - **EvaluationResults** *(list) --*
              The results of the simulation.
              - *(dict) --*
                Contains the results of a simulation.
                This data type is used by the return parameter of ``  SimulateCustomPolicy `` and ``  SimulatePrincipalPolicy `` .
                - **EvalActionName** *(string) --*
                  The name of the API operation tested on the indicated resource.
                - **EvalResourceName** *(string) --*
                  The ARN of the resource that the indicated API operation was tested on.
                - **EvalDecision** *(string) --*
                  The result of the simulation.
                - **MatchedStatements** *(list) --*
                  A list of the statements in the input policies that determine the result for this scenario. Remember that even if multiple statements allow the operation on the resource, if only one statement denies that operation, then the explicit deny overrides any allow. Inaddition, the deny statement is the only entry included in the result.
                  - *(dict) --*
                    Contains a reference to a ``Statement`` element in a policy document that determines the result of the simulation.
                    This data type is used by the ``MatchedStatements`` member of the ``  EvaluationResult `` type.
                    - **SourcePolicyId** *(string) --*
                      The identifier of the policy that was provided as an input.
                    - **SourcePolicyType** *(string) --*
                      The type of the policy.
                    - **StartPosition** *(dict) --*
                      The row and column of the beginning of the ``Statement`` in an IAM policy.
                      - **Line** *(integer) --*
                        The line containing the specified position in the document.
                      - **Column** *(integer) --*
                        The column in the line containing the specified position in the document.
                    - **EndPosition** *(dict) --*
                      The row and column of the end of a ``Statement`` in an IAM policy.
                      - **Line** *(integer) --*
                        The line containing the specified position in the document.
                      - **Column** *(integer) --*
                        The column in the line containing the specified position in the document.
                - **MissingContextValues** *(list) --*
                  A list of context keys that are required by the included input policies but that were not provided by one of the input parameters. This list is used when the resource in a simulation is "*", either explicitly, or when the ``ResourceArns`` parameter blank. If you include a list of resources, then any missing context values are instead included under the ``ResourceSpecificResults`` section. To discover the context keys used by a set of policies, you can call  GetContextKeysForCustomPolicy or  GetContextKeysForPrincipalPolicy .
                  - *(string) --*
                - **OrganizationsDecisionDetail** *(dict) --*
                  A structure that details how AWS Organizations and its service control policies affect the results of the simulation. Only applies if the simulated user's account is part of an organization.
                  - **AllowedByOrganizations** *(boolean) --*
                    Specifies whether the simulated operation is allowed by the AWS Organizations service control policies that impact the simulated user's account.
                - **EvalDecisionDetails** *(dict) --*
                  Additional details about the results of the evaluation decision. When there are both IAM policies and resource policies, this parameter explains how each set of policies contributes to the final evaluation decision. When simulating cross-account access to a resource, both the resource-based policy and the caller's IAM policy must grant access. See `How IAM Roles Differ from Resource-based Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_compare-resource-policies.html>`__
                  - *(string) --*
                    - *(string) --*
                - **ResourceSpecificResults** *(list) --*
                  The individual results of the simulation of the API operation specified in EvalActionName on each resource.
                  - *(dict) --*
                    Contains the result of the simulation of a single API operation call on a single resource.
                    This data type is used by a member of the  EvaluationResult data type.
                    - **EvalResourceName** *(string) --*
                      The name of the simulated resource, in Amazon Resource Name (ARN) format.
                    - **EvalResourceDecision** *(string) --*
                      The result of the simulation of the simulated API operation on the resource specified in ``EvalResourceName`` .
                    - **MatchedStatements** *(list) --*
                      A list of the statements in the input policies that determine the result for this part of the simulation. Remember that even if multiple statements allow the operation on the resource, if *any* statement denies that operation, then the explicit deny overrides any allow. In addition, the deny statement is the only entry included in the result.
                      - *(dict) --*
                        Contains a reference to a ``Statement`` element in a policy document that determines the result of the simulation.
                        This data type is used by the ``MatchedStatements`` member of the ``  EvaluationResult `` type.
                        - **SourcePolicyId** *(string) --*
                          The identifier of the policy that was provided as an input.
                        - **SourcePolicyType** *(string) --*
                          The type of the policy.
                        - **StartPosition** *(dict) --*
                          The row and column of the beginning of the ``Statement`` in an IAM policy.
                          - **Line** *(integer) --*
                            The line containing the specified position in the document.
                          - **Column** *(integer) --*
                            The column in the line containing the specified position in the document.
                        - **EndPosition** *(dict) --*
                          The row and column of the end of a ``Statement`` in an IAM policy.
                          - **Line** *(integer) --*
                            The line containing the specified position in the document.
                          - **Column** *(integer) --*
                            The column in the line containing the specified position in the document.
                    - **MissingContextValues** *(list) --*
                      A list of context keys that are required by the included input policies but that were not provided by one of the input parameters. This list is used when a list of ARNs is included in the ``ResourceArns`` parameter instead of "*". If you do not specify individual resources, by setting ``ResourceArns`` to "*" or by not including the ``ResourceArns`` parameter, then any missing context values are instead included under the ``EvaluationResults`` section. To discover the context keys used by a set of policies, you can call  GetContextKeysForCustomPolicy or  GetContextKeysForPrincipalPolicy .
                      - *(string) --*
                    - **EvalDecisionDetails** *(dict) --*
                      Additional details about the results of the evaluation decision. When there are both IAM policies and resource policies, this parameter explains how each set of policies contributes to the final evaluation decision. When simulating cross-account access to a resource, both the resource-based policy and the caller's IAM policy must grant access.
                      - *(string) --*
                        - *(string) --*
            - **IsTruncated** *(boolean) --*
              A flag that indicates whether there are more items to return. If your results were truncated, you can make a subsequent pagination request using the ``Marker`` request parameter to retrieve more items. Note that IAM might return fewer than the ``MaxItems`` number of results even when there are more results available. We recommend that you check ``IsTruncated`` after every call to ensure that you receive all your results.
            - **Marker** *(string) --*
              When ``IsTruncated`` is ``true`` , this element is present and contains the value to use for the ``Marker`` parameter in a subsequent pagination request.
        :type PolicySourceArn: string
        :param PolicySourceArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of a user, group, or role whose policies you want to include in the simulation. If you specify a user, group, or role, the simulation includes all policies that are associated with that entity. If you specify a user, the simulation also includes all policies that are attached to any groups the user belongs to.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type PolicyInputList: list
        :param PolicyInputList:
          An optional list of additional policy documents to include in the simulation. Each document is specified as a string containing the complete, valid JSON text of an IAM policy.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
          - *(string) --*
        :type ActionNames: list
        :param ActionNames: **[REQUIRED]**
          A list of names of API operations to evaluate in the simulation. Each operation is evaluated for each resource. Each operation must include the service identifier, such as ``iam:CreateUser`` .
          - *(string) --*
        :type ResourceArns: list
        :param ResourceArns:
          A list of ARNs of AWS resources to include in the simulation. If this parameter is not provided, then the value defaults to ``*`` (all resources). Each API in the ``ActionNames`` parameter is evaluated for each resource in this list. The simulation determines the access result (allowed or denied) of each combination and reports it in the response.
          The simulation does not automatically retrieve policies for the specified resources. If you want to include a resource policy in the simulation, then you must include the policy as a string in the ``ResourcePolicy`` parameter.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
          - *(string) --*
        :type ResourcePolicy: string
        :param ResourcePolicy:
          A resource-based policy to include in the simulation provided as a string. Each resource in the simulation is treated as if it had this policy attached. You can include only one resource-based policy in a simulation.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type ResourceOwner: string
        :param ResourceOwner:
          An AWS account ID that specifies the owner of any simulated resource that does not identify its owner in the resource ARN, such as an S3 bucket or object. If ``ResourceOwner`` is specified, it is also used as the account owner of any ``ResourcePolicy`` included in the simulation. If the ``ResourceOwner`` parameter is not specified, then the owner of the resources and the resource policy defaults to the account of the identity provided in ``CallerArn`` . This parameter is required only if you specify a resource-based policy and account that owns the resource is different from the account that owns the simulated calling user ``CallerArn`` .
        :type CallerArn: string
        :param CallerArn:
          The ARN of the IAM user that you want to specify as the simulated caller of the API operations. If you do not specify a ``CallerArn`` , it defaults to the ARN of the user that you specify in ``PolicySourceArn`` , if you specified a user. If you include both a ``PolicySourceArn`` (for example, ``arn:aws:iam::123456789012:user/David`` ) and a ``CallerArn`` (for example, ``arn:aws:iam::123456789012:user/Bob`` ), the result is that you simulate calling the API operations as Bob, as if Bob had David\'s policies.
          You can specify only the ARN of an IAM user. You cannot specify the ARN of an assumed role, federated user, or a service principal.
           ``CallerArn`` is required if you include a ``ResourcePolicy`` and the ``PolicySourceArn`` is not the ARN for an IAM user. This is required so that the resource-based policy\'s ``Principal`` element has a value to use in evaluating the policy.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type ContextEntries: list
        :param ContextEntries:
          A list of context keys and corresponding values for the simulation to use. Whenever a context key is evaluated in one of the simulated IAM permission policies, the corresponding value is supplied.
          - *(dict) --*
            Contains information about a condition context key. It includes the name of the key and specifies the value (or values, if the context key supports multiple values) to use in the simulation. This information is used when evaluating the ``Condition`` elements of the input policies.
            This data type is used as an input parameter to ``  SimulateCustomPolicy `` and ``  SimulateCustomPolicy `` .
            - **ContextKeyName** *(string) --*
              The full name of a condition context key, including the service prefix. For example, ``aws:SourceIp`` or ``s3:VersionId`` .
            - **ContextKeyValues** *(list) --*
              The value (or values, if the condition context key supports multiple values) to provide to the simulation when the key is referenced by a ``Condition`` element in an input policy.
              - *(string) --*
            - **ContextKeyType** *(string) --*
              The data type of the value (or values) specified in the ``ContextKeyValues`` parameter.
        :type ResourceHandlingOption: string
        :param ResourceHandlingOption:
          Specifies the type of simulation to run. Different API operations that support resource-based policies require different combinations of resources. By specifying the type of simulation to run, you enable the policy simulator to enforce the presence of the required resources to ensure reliable simulation results. If your simulation does not match one of the following scenarios, then you can omit this parameter. The following list shows each of the supported scenario values and the resources that you must define to run the simulation.
          Each of the EC2 scenarios requires that you specify instance, image, and security group resources. If your scenario includes an EBS volume, then you must specify that volume as a resource. If the EC2 scenario includes VPC, then you must supply the network interface resource. If it includes an IP subnet, then you must specify the subnet resource. For more information on the EC2 scenario options, see `Supported Platforms <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`__ in the *Amazon EC2 User Guide* .
          * **EC2-Classic-InstanceStore**   instance, image, security group
          * **EC2-Classic-EBS**   instance, image, security group, volume
          * **EC2-VPC-InstanceStore**   instance, image, security group, network interface
          * **EC2-VPC-InstanceStore-Subnet**   instance, image, security group, network interface, subnet
          * **EC2-VPC-EBS**   instance, image, security group, network interface, volume
          * **EC2-VPC-EBS-Subnet**   instance, image, security group, network interface, subnet, volume
        :type MaxItems: integer
        :param MaxItems:
          Use this only when paginating results to indicate the maximum number of items you want in the response. If additional items exist beyond the maximum you specify, the ``IsTruncated`` response element is ``true`` .
          If you do not include this parameter, the number of items defaults to 100. Note that IAM might return fewer results, even when there are more results available. In that case, the ``IsTruncated`` response element returns ``true`` , and ``Marker`` contains a value to include in the subsequent call that tells the service where to continue from.
        :type Marker: string
        :param Marker:
          Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the ``Marker`` element in the response that you received to indicate where the next call should start.
        :rtype: dict
        :returns:
        """
        pass

    def tag_role(self, RoleName: str, Tags: List):
        """
        Adds one or more tags to an IAM role. The role can be a regular role or a service-linked role. If a tag with the same key name already exists, then that tag is overwritten with the new value.
        A tag consists of a key name and an associated value. By assigning tags to your resources, you can do the following:
        * **Administrative grouping and discovery** - Attach tags to resources to aid in organization and search. For example, you could search for all resources with the key name *Project* and the value *MyImportantProject* . Or search for all resources with the key name *Cost Center* and the value *41200* .
        * **Access control** - Reference tags in IAM user-based and resource-based policies. You can use tags to restrict access to only an IAM user or role that has a specified tag attached. You can also restrict access to only those resources that have a certain tag attached. For examples of policies that show how to use tags to control access, see `Control Access Using IAM Tags <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_tags.html>`__ in the *IAM User Guide* .
        * **Cost allocation** - Use tags to help track which individuals and teams are using which AWS resources.
        .. note::
          * Make sure that you have no invalid tags and that you do not exceed the allowed number of tags per role. In either case, the entire request fails and *no* tags are added to the role.
          * AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/TagRole>`_

        **Request Syntax**
        ::
          response = client.tag_role(
              RoleName='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role that you want to add tags to.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Tags: list
        :param Tags: **[REQUIRED]**
          The list of tags that you want to attach to the role. Each tag consists of a key name and an associated value. You can specify this with a JSON string.
          - *(dict) --*
            A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
            - **Key** *(string) --* **[REQUIRED]**
              The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
            - **Value** *(string) --* **[REQUIRED]**
              The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
              .. note::
                AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :returns: None
        """
        pass

    def tag_user(self, UserName: str, Tags: List):
        """
        Adds one or more tags to an IAM user. If a tag with the same key name already exists, then that tag is overwritten with the new value.
        A tag consists of a key name and an associated value. By assigning tags to your resources, you can do the following:
        * **Administrative grouping and discovery** - Attach tags to resources to aid in organization and search. For example, you could search for all resources with the key name *Project* and the value *MyImportantProject* . Or search for all resources with the key name *Cost Center* and the value *41200* .
        * **Access control** - Reference tags in IAM user-based and resource-based policies. You can use tags to restrict access to only an IAM requesting user or to a role that has a specified tag attached. You can also restrict access to only those resources that have a certain tag attached. For examples of policies that show how to use tags to control access, see `Control Access Using IAM Tags <http://docs.aws.amazon.com/IAM/latest/UserGuide/access_tags.html>`__ in the *IAM User Guide* .
        * **Cost allocation** - Use tags to help track which individuals and teams are using which AWS resources.
        .. note::
          * Make sure that you have no invalid tags and that you do not exceed the allowed number of tags per role. In either case, the entire request fails and *no* tags are added to the role.
          * AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/TagUser>`_

        **Request Syntax**
        ::
          response = client.tag_user(
              UserName='string',
              Tags=[
                  {
                      'Key': 'string',
                      'Value': 'string'
                  },
              ]
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user that you want to add tags to.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@-
        :type Tags: list
        :param Tags: **[REQUIRED]**
          The list of tags that you want to attach to the user. Each tag consists of a key name and an associated value.
          - *(dict) --*
            A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
            - **Key** *(string) --* **[REQUIRED]**
              The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
            - **Value** *(string) --* **[REQUIRED]**
              The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
              .. note::
                AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :returns: None
        """
        pass

    def untag_role(self, RoleName: str, TagKeys: List):
        """
        Removes the specified tags from the role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UntagRole>`_

        **Request Syntax**
        ::
          response = client.untag_role(
              RoleName='string',
              TagKeys=[
                  'string',
              ]
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the IAM role from which you want to remove tags.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type TagKeys: list
        :param TagKeys: **[REQUIRED]**
          A list of key names as a simple array of strings. The tags with matching keys are removed from the specified role.
          - *(string) --*
        :returns: None
        """
        pass

    def untag_user(self, UserName: str, TagKeys: List):
        """
        Removes the specified tags from the user. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UntagUser>`_

        **Request Syntax**
        ::
          response = client.untag_user(
              UserName='string',
              TagKeys=[
                  'string',
              ]
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user from which you want to remove tags.
          This parameter accepts (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that consist of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: =,.@-
        :type TagKeys: list
        :param TagKeys: **[REQUIRED]**
          A list of key names as a simple array of strings. The tags with matching keys are removed from the specified user.
          - *(string) --*
        :returns: None
        """
        pass

    def update_access_key(self, AccessKeyId: str, Status: str, UserName: str = None):
        """
        Changes the status of the specified access key from Active to Inactive, or vice versa. This operation can be used to disable a user's key as part of a key rotation workflow.
        If the ``UserName`` field is not specified, the user name is determined implicitly based on the AWS access key ID used to sign the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        For information about rotating keys, see `Managing Keys and Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/ManagingCredentials.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateAccessKey>`_

        **Request Syntax**
        ::
          response = client.update_access_key(
              UserName='string',
              AccessKeyId='string',
              Status='Active'|'Inactive'
          )
        :type UserName: string
        :param UserName:
          The name of the user whose key you want to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type AccessKeyId: string
        :param AccessKeyId: **[REQUIRED]**
          The access key ID of the secret access key you want to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :type Status: string
        :param Status: **[REQUIRED]**
          The status you want to assign to the secret access key. ``Active`` means that the key can be used for API calls to AWS, while ``Inactive`` means that the key cannot be used.
        :returns: None
        """
        pass

    def update_account_password_policy(self, MinimumPasswordLength: int = None, RequireSymbols: bool = None,
                                       RequireNumbers: bool = None, RequireUppercaseCharacters: bool = None,
                                       RequireLowercaseCharacters: bool = None, AllowUsersToChangePassword: bool = None,
                                       MaxPasswordAge: int = None, PasswordReusePrevention: int = None,
                                       HardExpiry: bool = None):
        """
        Updates the password policy settings for the AWS account.
        .. note::
          * This operation does not support partial updates. No parameters are required, but if you do not specify a parameter, that parameter's value reverts to its default value. See the **Request Parameters** section for each parameter's default value. Also note that some parameters do not allow the default parameter to be explicitly set. Instead, to invoke the default value, do not include that parameter when you invoke the operation.
        For more information about using a password policy, see `Managing an IAM Password Policy <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingPasswordPolicies.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateAccountPasswordPolicy>`_

        **Request Syntax**
        ::
          response = client.update_account_password_policy(
              MinimumPasswordLength=123,
              RequireSymbols=True|False,
              RequireNumbers=True|False,
              RequireUppercaseCharacters=True|False,
              RequireLowercaseCharacters=True|False,
              AllowUsersToChangePassword=True|False,
              MaxPasswordAge=123,
              PasswordReusePrevention=123,
              HardExpiry=True|False
          )
        :type MinimumPasswordLength: integer
        :param MinimumPasswordLength:
          The minimum number of characters allowed in an IAM user password.
          If you do not specify a value for this parameter, then the operation uses the default value of ``6`` .
        :type RequireSymbols: boolean
        :param RequireSymbols:
          Specifies whether IAM user passwords must contain at least one of the following non-alphanumeric characters:
          ! @ # $ % ^ & * ( ) _ + - = [ ] { } | \'
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that passwords do not require at least one symbol character.
        :type RequireNumbers: boolean
        :param RequireNumbers:
          Specifies whether IAM user passwords must contain at least one numeric character (0 to 9).
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that passwords do not require at least one numeric character.
        :type RequireUppercaseCharacters: boolean
        :param RequireUppercaseCharacters:
          Specifies whether IAM user passwords must contain at least one uppercase character from the ISO basic Latin alphabet (A to Z).
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that passwords do not require at least one uppercase character.
        :type RequireLowercaseCharacters: boolean
        :param RequireLowercaseCharacters:
          Specifies whether IAM user passwords must contain at least one lowercase character from the ISO basic Latin alphabet (a to z).
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that passwords do not require at least one lowercase character.
        :type AllowUsersToChangePassword: boolean
        :param AllowUsersToChangePassword:
          Allows all IAM users in your account to use the AWS Management Console to change their own passwords. For more information, see `Letting IAM Users Change Their Own Passwords <http://docs.aws.amazon.com/IAM/latest/UserGuide/HowToPwdIAMUser.html>`__ in the *IAM User Guide* .
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that IAM users in the account do not automatically have permissions to change their own password.
        :type MaxPasswordAge: integer
        :param MaxPasswordAge:
          The number of days that an IAM user password is valid.
          If you do not specify a value for this parameter, then the operation uses the default value of ``0`` . The result is that IAM user passwords never expire.
        :type PasswordReusePrevention: integer
        :param PasswordReusePrevention:
          Specifies the number of previous passwords that IAM users are prevented from reusing.
          If you do not specify a value for this parameter, then the operation uses the default value of ``0`` . The result is that IAM users are not prevented from reusing previous passwords.
        :type HardExpiry: boolean
        :param HardExpiry:
          Prevents IAM users from setting a new password after their password has expired. The IAM user cannot be accessed until an administrator resets the password.
          If you do not specify a value for this parameter, then the operation uses the default value of ``false`` . The result is that IAM users can change their passwords after they expire and continue to sign in as the user.
        :returns: None
        """
        pass

    def update_assume_role_policy(self, RoleName: str, PolicyDocument: str):
        """
        Updates the policy that grants an IAM entity permission to assume a role. This is typically referred to as the "role trust policy". For more information about roles, go to `Using Roles to Delegate Permissions and Federate Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateAssumeRolePolicy>`_

        **Request Syntax**
        ::
          response = client.update_assume_role_policy(
              RoleName='string',
              PolicyDocument='string'
          )
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role to update with the new policy.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type PolicyDocument: string
        :param PolicyDocument: **[REQUIRED]**
          The policy that grants an entity permission to assume the role.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :returns: None
        """
        pass

    def update_group(self, GroupName: str, NewPath: str = None, NewGroupName: str = None):
        """
        Updates the name and/or the path of the specified IAM group.
        .. warning::
          You should understand the implications of changing a group's path or name. For more information, see `Renaming Users and Groups <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_WorkingWithGroupsAndUsers.html>`__ in the *IAM User Guide* .
        .. note::
          The person making the request (the principal), must have permission to change the role group with the old name and the new name. For example, to change the group named ``Managers`` to ``MGRs`` , the principal must have a policy that allows them to update both groups. If the principal has permission to update the ``Managers`` group, but not the ``MGRs`` group, then the update fails. For more information about permissions, see `Access Management <http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateGroup>`_

        **Request Syntax**
        ::
          response = client.update_group(
              GroupName='string',
              NewPath='string',
              NewGroupName='string'
          )
        :type GroupName: string
        :param GroupName: **[REQUIRED]**
          Name of the IAM group to update. If you\'re changing the name of the group, this is the original name.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type NewPath: string
        :param NewPath:
          New path for the IAM group. Only include this if changing the group\'s path.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type NewGroupName: string
        :param NewGroupName:
          New name for the IAM group. Only include this if changing the group\'s name.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def update_login_profile(self, UserName: str, Password: str = None, PasswordResetRequired: bool = None):
        """
        Changes the password for the specified IAM user.
        IAM users can change their own passwords by calling  ChangePassword . For more information about modifying passwords, see `Managing Passwords <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateLoginProfile>`_

        **Request Syntax**
        ::
          response = client.update_login_profile(
              UserName='string',
              Password='string',
              PasswordResetRequired=True|False
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the user whose password you want to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type Password: string
        :param Password:
          The new password for the specified IAM user.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
          However, the format can be further restricted by the account administrator by setting a password policy on the AWS account. For more information, see  UpdateAccountPasswordPolicy .
        :type PasswordResetRequired: boolean
        :param PasswordResetRequired:
          Allows this new password to be used only once by requiring the specified IAM user to set a new password on next sign-in.
        :returns: None
        """
        pass

    def update_open_id_connect_provider_thumbprint(self, OpenIDConnectProviderArn: str, ThumbprintList: List):
        """
        Replaces the existing list of server certificate thumbprints associated with an OpenID Connect (OIDC) provider resource object with a new list of thumbprints.
        The list that you pass with this operation completely replaces the existing list of thumbprints. (The lists are not merged.)
        Typically, you need to update a thumbprint only when the identity provider's certificate changes, which occurs rarely. However, if the provider's certificate *does* change, any attempt to assume an IAM role that specifies the OIDC provider as a principal fails until the certificate thumbprint is updated.
        .. note::
          Trust for the OIDC provider is derived from the provider's certificate and is validated by the thumbprint. Therefore, it is best to limit access to the ``UpdateOpenIDConnectProviderThumbprint`` operation to highly privileged users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateOpenIDConnectProviderThumbprint>`_

        **Request Syntax**
        ::
          response = client.update_open_id_connect_provider_thumbprint(
              OpenIDConnectProviderArn='string',
              ThumbprintList=[
                  'string',
              ]
          )
        :type OpenIDConnectProviderArn: string
        :param OpenIDConnectProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the IAM OIDC provider resource object for which you want to update the thumbprint. You can get a list of OIDC provider ARNs by using the  ListOpenIDConnectProviders operation.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :type ThumbprintList: list
        :param ThumbprintList: **[REQUIRED]**
          A list of certificate thumbprints that are associated with the specified IAM OpenID Connect provider. For more information, see  CreateOpenIDConnectProvider .
          - *(string) --*
            Contains a thumbprint for an identity provider\'s server certificate.
            The identity provider\'s server certificate thumbprint is the hex-encoded SHA-1 hash value of the self-signed X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string.
        :returns: None
        """
        pass

    def update_role(self, RoleName: str, Description: str = None, MaxSessionDuration: int = None) -> Dict:
        """
        Updates the description or maximum session duration setting of a role.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateRole>`_

        **Request Syntax**
        ::
          response = client.update_role(
              RoleName='string',
              Description='string',
              MaxSessionDuration=123
          )

        **Response Syntax**
        ::
            {}

        **Response Structure**
          - *(dict) --*
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role that you want to modify.
        :type Description: string
        :param Description:
          The new description that you want to apply to the specified role.
        :type MaxSessionDuration: integer
        :param MaxSessionDuration:
          The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default maximum of one hour is applied. This setting can have a value from 1 hour to 12 hours.
          Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don\'t specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM Roles <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`__ in the *IAM User Guide* .
        :rtype: dict
        :returns:
        """
        pass

    def update_role_description(self, RoleName: str, Description: str) -> Dict:
        """
        Use  UpdateRole instead.
        Modifies only the description of a role. This operation performs the same function as the ``Description`` parameter in the ``UpdateRole`` operation.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateRoleDescription>`_

        **Request Syntax**
        ::
          response = client.update_role_description(
              RoleName='string',
              Description='string'
          )

        **Response Syntax**
        ::
            {
                'Role': {
                    'Path': 'string',
                    'RoleName': 'string',
                    'RoleId': 'string',
                    'Arn': 'string',
                    'CreateDate': datetime(2015, 1, 1),
                    'AssumeRolePolicyDocument': 'string',
                    'Description': 'string',
                    'MaxSessionDuration': 123,
                    'PermissionsBoundary': {
                        'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                        'PermissionsBoundaryArn': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ]
                }
            }

        **Response Structure**
          - *(dict) --*
            - **Role** *(dict) --*
              A structure that contains details about the modified role.
              - **Path** *(string) --*
                The path to the role. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **RoleName** *(string) --*
                The friendly name that identifies the role.
              - **RoleId** *(string) --*
                The stable and unique string identifying the role. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the role. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* guide.
              - **CreateDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the role was created.
              - **AssumeRolePolicyDocument** *(string) --*
                The policy that grants an entity permission to assume the role.
              - **Description** *(string) --*
                A description of the role that you provide.
              - **MaxSessionDuration** *(integer) --*
                The maximum session duration (in seconds) for the specified role. Anyone who uses the AWS CLI, or API to assume the role can specify the duration using the optional ``DurationSeconds`` API parameter or ``duration-seconds`` CLI parameter.
              - **PermissionsBoundary** *(dict) --*
                The ARN of the policy used to set the permissions boundary for the role.
                For more information about permissions boundaries, see `Permissions Boundaries for IAM Identities <IAM/latest/UserGuide/access_policies_boundaries.html>`__ in the *IAM User Guide* .
                - **PermissionsBoundaryType** *(string) --*
                  The permissions boundary usage type that indicates what type of IAM resource is used as the permissions boundary for an entity. This data type can only have a value of ``Policy`` .
                - **PermissionsBoundaryArn** *(string) --*
                  The ARN of the policy used to set the permissions boundary for the user or role.
              - **Tags** *(list) --*
                A list of tags that are attached to the specified role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                - *(dict) --*
                  A structure that represents user-provided metadata that can be associated with a resource such as an IAM user or role. For more information about tagging, see `Tagging IAM Identities <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`__ in the *IAM User Guide* .
                  - **Key** *(string) --*
                    The key name that can be used to look up or retrieve the associated value. For example, ``Department`` or ``Cost Center`` are common choices.
                  - **Value** *(string) --*
                    The value associated with this tag. For example, tags with a key name of ``Department`` could have values such as ``Human Resources`` , ``Accounting`` , and ``Support`` . Tags with a key name of ``Cost Center`` might have values that consist of the number associated with the different cost centers in your company. Typically, many resources have tags with the same key name but with different values.
                    .. note::
                      AWS always interprets the tag ``Value`` as a single string. If you need to store an array, you can store comma-separated values in the string. However, you must interpret the value in your code.
        :type RoleName: string
        :param RoleName: **[REQUIRED]**
          The name of the role that you want to modify.
        :type Description: string
        :param Description: **[REQUIRED]**
          The new description that you want to apply to the specified role.
        :rtype: dict
        :returns:
        """
        pass

    def update_saml_provider(self, SAMLMetadataDocument: str, SAMLProviderArn: str) -> Dict:
        """
        Updates the metadata document for an existing SAML provider resource object.
        .. note::
          This operation requires `Signature Version 4 <http://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateSAMLProvider>`_

        **Request Syntax**
        ::
          response = client.update_saml_provider(
              SAMLMetadataDocument='string',
              SAMLProviderArn='string'
          )

        **Response Syntax**
        ::
            {
                'SAMLProviderArn': 'string'
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  UpdateSAMLProvider request.
            - **SAMLProviderArn** *(string) --*
              The Amazon Resource Name (ARN) of the SAML provider that was updated.
        :type SAMLMetadataDocument: string
        :param SAMLMetadataDocument: **[REQUIRED]**
          An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer\'s name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization\'s IdP.
        :type SAMLProviderArn: string
        :param SAMLProviderArn: **[REQUIRED]**
          The Amazon Resource Name (ARN) of the SAML provider to update.
          For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`__ in the *AWS General Reference* .
        :rtype: dict
        :returns:
        """
        pass

    def update_server_certificate(self, ServerCertificateName: str, NewPath: str = None,
                                  NewServerCertificateName: str = None):
        """
        Updates the name and/or the path of the specified server certificate stored in IAM.
        For more information about working with server certificates, see `Working with Server Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`__ in the *IAM User Guide* . This topic also includes a list of AWS services that can use the server certificates that you manage with IAM.
        .. warning::
          You should understand the implications of changing a server certificate's path or name. For more information, see `Renaming a Server Certificate <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs_manage.html#RenamingServerCerts>`__ in the *IAM User Guide* .
        .. note::
          The person making the request (the principal), must have permission to change the server certificate with the old name and the new name. For example, to change the certificate named ``ProductionCert`` to ``ProdCert`` , the principal must have a policy that allows them to update both certificates. If the principal has permission to update the ``ProductionCert`` group, but not the ``ProdCert`` certificate, then the update fails. For more information about permissions, see `Access Management <http://docs.aws.amazon.com/IAM/latest/UserGuide/access.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateServerCertificate>`_

        **Request Syntax**
        ::
          response = client.update_server_certificate(
              ServerCertificateName='string',
              NewPath='string',
              NewServerCertificateName='string'
          )
        :type ServerCertificateName: string
        :param ServerCertificateName: **[REQUIRED]**
          The name of the server certificate that you want to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type NewPath: string
        :param NewPath:
          The new path for the server certificate. Include this only if you are updating the server certificate\'s path.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type NewServerCertificateName: string
        :param NewServerCertificateName:
          The new name for the server certificate. Include this only if you are updating the server certificate\'s name. The name of the certificate cannot contain any spaces.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def update_service_specific_credential(self, ServiceSpecificCredentialId: str, Status: str, UserName: str = None):
        """
        Sets the status of a service-specific credential to ``Active`` or ``Inactive`` . Service-specific credentials that are inactive cannot be used for authentication to the service. This operation can be used to disable a user's service-specific credential as part of a credential rotation work flow.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateServiceSpecificCredential>`_

        **Request Syntax**
        ::
          response = client.update_service_specific_credential(
              UserName='string',
              ServiceSpecificCredentialId='string',
              Status='Active'|'Inactive'
          )
        :type UserName: string
        :param UserName:
          The name of the IAM user associated with the service-specific credential. If you do not specify this value, then the operation assumes the user whose credentials are used to call the operation.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type ServiceSpecificCredentialId: string
        :param ServiceSpecificCredentialId: **[REQUIRED]**
          The unique identifier of the service-specific credential.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :type Status: string
        :param Status: **[REQUIRED]**
          The status to be assigned to the service-specific credential.
        :returns: None
        """
        pass

    def update_signing_certificate(self, CertificateId: str, Status: str, UserName: str = None):
        """
        Changes the status of the specified user signing certificate from active to disabled, or vice versa. This operation can be used to disable an IAM user's signing certificate as part of a certificate rotation work flow.
        If the ``UserName`` field is not specified, the user name is determined implicitly based on the AWS access key ID used to sign the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateSigningCertificate>`_

        **Request Syntax**
        ::
          response = client.update_signing_certificate(
              UserName='string',
              CertificateId='string',
              Status='Active'|'Inactive'
          )
        :type UserName: string
        :param UserName:
          The name of the IAM user the signing certificate belongs to.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type CertificateId: string
        :param CertificateId: **[REQUIRED]**
          The ID of the signing certificate you want to update.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :type Status: string
        :param Status: **[REQUIRED]**
          The status you want to assign to the certificate. ``Active`` means that the certificate can be used for API calls to AWS ``Inactive`` means that the certificate cannot be used.
        :returns: None
        """
        pass

    def update_ssh_public_key(self, UserName: str, SSHPublicKeyId: str, Status: str):
        """
        Sets the status of an IAM user's SSH public key to active or inactive. SSH public keys that are inactive cannot be used for authentication. This operation can be used to disable a user's SSH public key as part of a key rotation work flow.
        The SSH public key affected by this operation is used only for authenticating the associated IAM user to an AWS CodeCommit repository. For more information about using SSH keys to authenticate to an AWS CodeCommit repository, see `Set up AWS CodeCommit for SSH Connections <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-credentials-ssh.html>`__ in the *AWS CodeCommit User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateSSHPublicKey>`_

        **Request Syntax**
        ::
          response = client.update_ssh_public_key(
              UserName='string',
              SSHPublicKeyId='string',
              Status='Active'|'Inactive'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user associated with the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SSHPublicKeyId: string
        :param SSHPublicKeyId: **[REQUIRED]**
          The unique identifier for the SSH public key.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters that can consist of any upper or lowercased letter or digit.
        :type Status: string
        :param Status: **[REQUIRED]**
          The status to assign to the SSH public key. ``Active`` means that the key can be used for authentication with an AWS CodeCommit repository. ``Inactive`` means that the key cannot be used.
        :returns: None
        """
        pass

    def update_user(self, UserName: str, NewPath: str = None, NewUserName: str = None):
        """
        Updates the name and/or the path of the specified IAM user.
        .. warning::
          You should understand the implications of changing an IAM user's path or name. For more information, see `Renaming an IAM User <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_manage.html#id_users_renaming>`__ and `Renaming an IAM Group <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups_manage_rename.html>`__ in the *IAM User Guide* .
        .. note::
          To change a user name, the requester must have appropriate permissions on both the source object and the target object. For example, to change Bob to Robert, the entity making the request must have permission on Bob and Robert, or must have permission on all (*). For more information about permissions, see `Permissions and Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/PermissionsAndPolicies.html>`__ .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UpdateUser>`_

        **Request Syntax**
        ::
          response = client.update_user(
              UserName='string',
              NewPath='string',
              NewUserName='string'
          )
        :type UserName: string
        :param UserName: **[REQUIRED]**
          Name of the user to update. If you\'re changing the name of the user, this is the original user name.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type NewPath: string
        :param NewPath:
          New path for the IAM user. Include this parameter only if you\'re changing the user\'s path.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
        :type NewUserName: string
        :param NewUserName:
          New name for the user. Include this parameter only if you\'re changing the user\'s name.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :returns: None
        """
        pass

    def upload_server_certificate(self, ServerCertificateName: str, CertificateBody: str, PrivateKey: str,
                                  Path: str = None, CertificateChain: str = None) -> Dict:
        """
        Uploads a server certificate entity for the AWS account. The server certificate entity includes a public key certificate, a private key, and an optional certificate chain, which should all be PEM-encoded.
        We recommend that you use `AWS Certificate Manager <http://docs.aws.amazon.com/certificate-manager/>`__ to provision, manage, and deploy your server certificates. With ACM you can request a certificate, deploy it to AWS resources, and let ACM handle certificate renewals for you. Certificates provided by ACM are free. For more information about using ACM, see the `AWS Certificate Manager User Guide <http://docs.aws.amazon.com/acm/latest/userguide/>`__ .
        For more information about working with server certificates, see `Working with Server Certificates <http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`__ in the *IAM User Guide* . This topic includes a list of AWS services that can use the server certificates that you manage with IAM.
        For information about the number of server certificates you can upload, see `Limitations on IAM Entities and Objects <http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-limits.html>`__ in the *IAM User Guide* .
        .. note::
          Because the body of the public key certificate, private key, and the certificate chain can be large, you should use POST rather than GET when calling ``UploadServerCertificate`` . For information about setting up signatures and authorization through the API, go to `Signing AWS API Requests <http://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html>`__ in the *AWS General Reference* . For general information about using the Query API with IAM, go to `Calling the API by Making HTTP Query Requests <http://docs.aws.amazon.com/IAM/latest/UserGuide/programming.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UploadServerCertificate>`_

        **Request Syntax**
        ::
          response = client.upload_server_certificate(
              Path='string',
              ServerCertificateName='string',
              CertificateBody='string',
              PrivateKey='string',
              CertificateChain='string'
          )

        **Response Syntax**
        ::
            {
                'ServerCertificateMetadata': {
                    'Path': 'string',
                    'ServerCertificateName': 'string',
                    'ServerCertificateId': 'string',
                    'Arn': 'string',
                    'UploadDate': datetime(2015, 1, 1),
                    'Expiration': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  UploadServerCertificate request.
            - **ServerCertificateMetadata** *(dict) --*
              The meta information of the uploaded server certificate without its certificate body, certificate chain, and private key.
              - **Path** *(string) --*
                The path to the server certificate. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **ServerCertificateName** *(string) --*
                The name that identifies the server certificate.
              - **ServerCertificateId** *(string) --*
                The stable and unique string identifying the server certificate. For more information about IDs, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **Arn** *(string) --*
                The Amazon Resource Name (ARN) specifying the server certificate. For more information about ARNs and how to use them in policies, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *Using IAM* guide.
              - **UploadDate** *(datetime) --*
                The date when the server certificate was uploaded.
              - **Expiration** *(datetime) --*
                The date on which the certificate is set to expire.
        :type Path: string
        :param Path:
          The path for the server certificate. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`__ in the *IAM User Guide* .
          This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\u0021) through the DEL character (\u007F), including most punctuation characters, digits, and upper and lowercased letters.
          .. note::
            If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :type ServerCertificateName: string
        :param ServerCertificateName: **[REQUIRED]**
          The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type CertificateBody: string
        :param CertificateBody: **[REQUIRED]**
          The contents of the public key certificate in PEM-encoded format.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type PrivateKey: string
        :param PrivateKey: **[REQUIRED]**
          The contents of the private key in PEM-encoded format.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :type CertificateChain: string
        :param CertificateChain:
          The contents of the certificate chain. This is typically a concatenation of the PEM-encoded public key certificates of the chain.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :rtype: dict
        :returns:
        """
        pass

    def upload_signing_certificate(self, CertificateBody: str, UserName: str = None) -> Dict:
        """
        Uploads an X.509 signing certificate and associates it with the specified IAM user. Some AWS services use X.509 signing certificates to validate requests that are signed with a corresponding private key. When you upload the certificate, its default status is ``Active`` .
        If the ``UserName`` field is not specified, the IAM user name is determined implicitly based on the AWS access key ID used to sign the request. This operation works for access keys under the AWS account. Consequently, you can use this operation to manage AWS account root user credentials even if the AWS account has no associated users.
        .. note::
          Because the body of an X.509 certificate can be large, you should use POST rather than GET when calling ``UploadSigningCertificate`` . For information about setting up signatures and authorization through the API, go to `Signing AWS API Requests <http://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html>`__ in the *AWS General Reference* . For general information about using the Query API with IAM, go to `Making Query Requests <http://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_UsingQueryAPI.html>`__ in the *IAM User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UploadSigningCertificate>`_

        **Request Syntax**
        ::
          response = client.upload_signing_certificate(
              UserName='string',
              CertificateBody='string'
          )

        **Response Syntax**
        ::
            {
                'Certificate': {
                    'UserName': 'string',
                    'CertificateId': 'string',
                    'CertificateBody': 'string',
                    'Status': 'Active'|'Inactive',
                    'UploadDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  UploadSigningCertificate request.
            - **Certificate** *(dict) --*
              Information about the certificate.
              - **UserName** *(string) --*
                The name of the user the signing certificate is associated with.
              - **CertificateId** *(string) --*
                The ID for the signing certificate.
              - **CertificateBody** *(string) --*
                The contents of the signing certificate.
              - **Status** *(string) --*
                The status of the signing certificate. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
              - **UploadDate** *(datetime) --*
                The date when the signing certificate was uploaded.
        :type UserName: string
        :param UserName:
          The name of the user the signing certificate is for.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type CertificateBody: string
        :param CertificateBody: **[REQUIRED]**
          The contents of the signing certificate.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :rtype: dict
        :returns:
        """
        pass

    def upload_ssh_public_key(self, UserName: str, SSHPublicKeyBody: str) -> Dict:
        """
        Uploads an SSH public key and associates it with the specified IAM user.
        The SSH public key uploaded by this operation can be used only for authenticating the associated IAM user to an AWS CodeCommit repository. For more information about using SSH keys to authenticate to an AWS CodeCommit repository, see `Set up AWS CodeCommit for SSH Connections <http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-credentials-ssh.html>`__ in the *AWS CodeCommit User Guide* .
        See also: `AWS API Documentation <https://docs.aws.amazon.com/goto/WebAPI/iam-2010-05-08/UploadSSHPublicKey>`_

        **Request Syntax**
        ::
          response = client.upload_ssh_public_key(
              UserName='string',
              SSHPublicKeyBody='string'
          )

        **Response Syntax**
        ::
            {
                'SSHPublicKey': {
                    'UserName': 'string',
                    'SSHPublicKeyId': 'string',
                    'Fingerprint': 'string',
                    'SSHPublicKeyBody': 'string',
                    'Status': 'Active'|'Inactive',
                    'UploadDate': datetime(2015, 1, 1)
                }
            }

        **Response Structure**
          - *(dict) --*
            Contains the response to a successful  UploadSSHPublicKey request.
            - **SSHPublicKey** *(dict) --*
              Contains information about the SSH public key.
              - **UserName** *(string) --*
                The name of the IAM user associated with the SSH public key.
              - **SSHPublicKeyId** *(string) --*
                The unique identifier for the SSH public key.
              - **Fingerprint** *(string) --*
                The MD5 message digest of the SSH public key.
              - **SSHPublicKeyBody** *(string) --*
                The SSH public key.
              - **Status** *(string) --*
                The status of the SSH public key. ``Active`` means that the key can be used for authentication with an AWS CodeCommit repository. ``Inactive`` means that the key cannot be used.
              - **UploadDate** *(datetime) --*
                The date and time, in `ISO 8601 date-time format <http://www.iso.org/iso/iso8601>`__ , when the SSH public key was uploaded.
        :type UserName: string
        :param UserName: **[REQUIRED]**
          The name of the IAM user to associate the SSH public key with.
          This parameter allows (through its `regex pattern <http://wikipedia.org/wiki/regex>`__ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :type SSHPublicKeyBody: string
        :param SSHPublicKeyBody: **[REQUIRED]**
          The SSH public key. The public key must be encoded in ssh-rsa format or PEM format. The minimum bit-length of the public key is 2048 bits. For example, you can generate a 2048-bit key, and the resulting PEM file is 1679 bytes long.
          The `regex pattern <http://wikipedia.org/wiki/regex>`__ used to validate this parameter is a string of characters consisting of the following:
          * Any printable ASCII character ranging from the space character (\u0020) through the end of the ASCII character range
          * The printable characters in the Basic Latin and Latin-1 Supplement character set (through \u00FF)
          * The special characters tab (\u0009), line feed (\u000A), and carriage return (\u000D)
        :rtype: dict
        :returns:
        """
        pass
