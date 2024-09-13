
# Audit S3 Bucket Permissions and Notify for Public Buckets


## Objective
Automatically audit S3 bucket permissions and send notifications if any buckets have public read or write permissions.

## Task
Set up a Lambda function to regularly audit S3 bucket permissions and send SNS notifications for any buckets that are publicly accessible.


---

## Tools required
- AWS portal access
- AWS Lambda function
- AWS S3 buckets
- Boto3
- SNS

---

## Deployment Steps

### 1. Creation of AWS S3 bucket and upload of random garbage image files into it.
- Opened AWS portal using my credentials
- Navigated to AWS S3
- Clicked on **"Create bucket"**
- Bucket Type as **"General Purpose"**
- Gave a bucket name
- Under **Object ownership** selected **"ACLs enabled"** 
    - Objects in this bucket can be owned by other AWS accounts. Access to this bucket and its objects can be specified using ACLs.
- Under **object ownership** selected **"Bucket owner preferred"**
- Click on **"block all public access"**
- Kept **Bucket Versioning** as disabled
- Kept rest of the settings as default 
- Clicked on **"Create Bucket"**

After the bucket was provisioned, either upload anything or keep it empty.

Create multiple such buckets and set some of them to public state.

---

### 2. Creation IAM role for our Lambda function
- In the **IAM dashboard**, a new role specifically for Lambda was created.  
- The trusted entity type was set to **Lambda**, allowing the role to be used by AWS Lambda functions.

After the role was created, the **AmazonS3FullAccess** policy was attached to it, giving the Lambda function full access to interact with S3 buckets.  
*(Note: In a real-world scenario, more restrictive permissions would be advisable to follow the principle of least privilege, ensuring tighter security.)*

- Could not attach the AmazonSNSFullAccess policy to the role as there were no IAM roles with 2 policy attached to them, so for this case we would require S3FullAccess and AmazonSNSFullAccess
- If done properly then this policy will allow your Lambda function to publish messages to SNS if any public buckets detected.

---

### 3. Lambda function creation and deployment 

- Navigated to the **Lambda dashboard** and clicked on **"Create function"**.
- Selected **"Author from Scratch"**.
- Gave function name as **"Aditya-s3-bucket-permission"**.
- Chose **Python 3.10** as the runtime for the function to ensure compatibility with Boto3 library.
- The IAM role from the previous step was assigned to the Lambda function, giving it the necessary permissions to interact with S3.
- Kept **Architecture as "arm64"**.
- Rest of the configurations were left as default.
- Clicked on **"Create function"**.

No need to create any Trigger for this function as this case study is to determine and perofrm audit on all existing buckets.

![Alt Text](/4-Audit-S3-Bucket-Permissions-and-Notify-for-Public-Buckets/images/PER-lambda-flow.JPG)


- Made a Git repository called **"Serverless-Architecture"**.
    - Opened Git Bash on local:
      ```bash
      touch lambda_function.py
      code .
      ```
    - Opened VS Code and wrote a Boto3 Python script

    - This Lambda function automatically audits the permissions of all S3 buckets in your AWS account and identifies any buckets with public read or write access.

- **Initialized S3 Client**:
  - Used `Boto3` to interact with AWS S3 for listing and checking permissions of S3 buckets.

- **Checked Bucket Permissions**:
  - The `check_bucket_permissions(bucket_name)` function retrieved the **ACL (Access Control List)** for a given bucket.
  - It checked if the bucket had public access by looking for the `AllUsers` group in the ACL.
  - If public access with **READ** or **WRITE** permission was found, the function returned `True`; otherwise, it returned `False`.

- **Listed All Buckets**:
  - Retrieved a list of all S3 buckets in the account using `list_buckets()`.
  - Logged the name of each bucket in **CloudWatch Logs** for auditing purposes.

- **Audited Permissions**:
  - Checked each bucket for public read/write permissions using the `check_bucket_permissions()` function.
  - If a bucket was public, its name was added to the `public_buckets` list.

- **Logged Public Buckets**:
  - If public buckets were detected, logged their names to **CloudWatch Logs** and returned them in the Lambda function's response.
  - If no public buckets were found, logged a message indicating that no public buckets were detected.

    
    - Pushed the script to Git:
      ```bash
      git add .
      git commit -m "WIP"
      git push origin main
      ```

    - The code was copied and pasted under the **Code** section of our AWS Lambda function.
      
![Alt Text](/4-Audit-S3-Bucket-Permissions-and-Notify-for-Public-Buckets/images/per-code.JPG)



- Clicked on **"Deploy"** at the top.
- Went to the **Test** section, created a sample Test event, and then clicked on **Test**.
- Test executed successfully.

![Alt Text](/4-Audit-S3-Bucket-Permissions-and-Notify-for-Public-Buckets/images/per-first-test-success.JPG)

- Checked **Cloudflare logs** and saw that audit for all the S3 buckets was done, also specifying which bcukets were public.

![Alt Text](/4-Audit-S3-Bucket-Permissions-and-Notify-for-Public-Buckets/images/PER-CLOUDFARE-log-SS1.JPG)
---

![Alt Text](/4-Audit-S3-Bucket-Permissions-and-Notify-for-Public-Buckets/images/PER-CLOUDFARE-log-SS2.JPG)


- **Challenges faced**:

- While executing the lambda code in TEST section, a timeout error was encountered after 3 secs. Went to configuration -> General Configs -> Edit -> Set the Timeout to 1min 1 sec
- After doing this the lambda function took 43 secs to audit all the buckets... :)

## 4. Testing
- Note : Cloud watch access was not there to perform this
- The CloudWatch functionality can be achieved this way.
- You can manually trigger the Lambda function or set up a periodic trigger (e.g., using CloudWatch Events) to run it on a schedule.
- Review the CloudWatch Logs to ensure that the files were successfully archived.

- CloudWatch Logs Setup:

- CloudWatch is automatically enabled for Lambda functions.
- Logs of your Lambda execution (such as bucket names) will be sent to CloudWatch.
- You can view these logs by:
- Going to CloudWatch.
- Clicking on Log groups.
- Finding your Lambda function's log group (e.g., /aws/lambda/S3-Audit-Function).
- View the log stream to see the names of all buckets audited.

## 5. Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear messages.
4. Submit a pull request for review.

Make sure to follow the code style guidelines and include proper documentation for any new features.


## 6. Contact

For any queries, feel free to contact me:

- **Email:** adityavakharia@gmail.com
- **GitHub:** [Aditya-rgb](https://github.com/Aditya-rgb/Serverless-Architecture)

You can also open an issue in the repository for questions or suggestions.
