### This is the procedure to set up the s3 bucket for the Heroku app:


1. navigate to aws.amazon.com
1. click on crate aws account
1. crate password and username and select continue
1. select 'personal' and fill the required information and click continue
1. go back to aws.amazon.com and sign in into the aws management control
1. on the find services search enter s3
1. open s3 and create new bucket
1. name the bucket, allow public access and confirm your choice
1. click create bucket
1. select properties
1. on the site website hosting select 'use this bucket to host a website'
1. select the permission tab
1. add a CORS configuration to set up the required access between our app and the bucket
1. click on the bucket policy tab and select a policy generator to create a security policy for our bucket
1. select s3 bucket policy for the policy type
1. allow all principals with '*'
1. select get-object as action
1. enter the ARN(amazon resource name)
1. click add statement
1. click generate policy
1. copy and paste the policy into the bucket policy editor
1. to allow all resources add /* at the end of the resources key line
1. click save to save the policy 
1. go to the access control list tab and select allow public access to everyone
1. go back to the services menu and select IAM
1. click on groups
1. create a new group and give it a name
1. click create group
1. click policies to create a policy to attach to the newly crated group
1. select the JSON tab and click on 'import managed policy'
1. select s3 full access policy and import it from the list
1. in the policy switch the * in resources with our bucket ARN and ARN/* to allow only our bucket
1. click review policy
1. add name and description
1. click create policy
1. attach the newly creted policy to the group by clicking on groups
1. select group
1. click attach policy
1. select the new policy created
1. click attach policy
1. to create a user to put in the group click on users
1. click add user
1. give the new user a name
1. give the user programmatic access
1. cilck next
1. add user to our group with the policy attached
1. click on create user
1. download the csv file that contains user access key and secret access key

our s3 bucket it is ready to be connected to our Heroku app
