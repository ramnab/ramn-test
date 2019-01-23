import boto3
import string
import random


def gen():
    lc = string.ascii_lowercase
    pw = random.sample(lc, 8)
    rand_upper = random.randint(0, 7)
    pw[rand_upper] = pw[rand_upper].upper()
    rand_punc = random.randint(0, 7)
    pw[rand_punc] = random.choice(list(string.punctuation))
    rand_num_pos = random.randint(0, 7)
    rand_num = random.randint(1, 100)
    pw[rand_num_pos] = str(rand_num)
    return "".join(pw)


print(f"Create a new user\n-----------\n")
print("Uses email address for log-in")

region = input("Region (default=eu-central-1)? ")
if not region:
    region = 'eu-central-1'

pool = input("Pool ID? ")

if not pool:
    print("A pool ID is required")
    exit(1)

client = boto3.client('cognito-idp', region_name=region)

user = True
while user:
    user = input("To quit just press RETURN\nUsername? ")

    if user:
        email = input("Email? ")
        pw_default = gen()
        print(f"""
Password is '{pw_default}'. To accept, press RETURN or type new

Passwords need to
    - be at least 8 characters
    - contain upper and lower case letters
    - include punctuation
    - include a number

""")
        pw = input("Password? ")
        if not pw:
            pw = pw_default

        response = client.admin_create_user(
            UserPoolId=pool,
            Username=user,
            TemporaryPassword=pw,
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": email
                },
                {
                    "Name": "email_verified",
                    "Value": "True"
                }
            ]
        )
        if response and response.get('User'):
            username = response.get('User').get('Username')
            print(f"{username} successfully created")
            print(f"Temporary password: {pw}")
        else:
            print(response)
