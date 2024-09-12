# Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective
To gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.

## Task
Automate the deletion of files older than 30 days in a specific S3 bucket.

---

## Tools required
- AWS portal access
- AWS Lambda function
- AWS S3 bucket
- Sample files
- Boto3

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

After the bucket was provisioned, uploaded 2 image files into it.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-S3-INITAL.JPG)

---

### 2. Creation IAM role for our Lambda function
- In the **IAM dashboard**, a new role specifically for Lambda was created.  
- The trusted entity type was set to **Lambda**, allowing the role to be used by AWS Lambda functions.

After the role was created, the **AmazonS3FullAccess** policy was attached to it, giving the Lambda function full access to interact with S3 buckets.  
*(Note: In a real-world scenario, more restrictive permissions would be advisable to follow the principle of least privilege, ensuring tighter security.)*

---

### 3. Lambda function creation and deployment 

- Navigated to the **Lambda dashboard** and clicked on **"Create function"**.
- Selected **"Author from Scratch"**.
- Gave function name as **"s3-bucket-cleanup-aditya"**.
- Chose **Python 3.10** as the runtime for the function to ensure compatibility with Boto3 library.
- The IAM role from the previous step was assigned to the Lambda function, giving it the necessary permissions to interact with S3.
- Kept **Architecture as "arm64"**.
- Rest of the configurations were left as default.
- Clicked on **"Create function"**.



- Clicked on **"Create Triggers"**
    - AWS S3 was selected as the source.
    - Bucket name was given as **"aditya-serverless-bucket"**.
    - **"All object create events"** was selected.
    - Prefix and Suffix were kept empty.
    - Acknowledged the condition given.
    - Finally clicked on **ADD**.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-Lambda-flow.JPG)

- Made a Git repository called **"Serverless-Architecture"**.
    - Opened Git Bash on local:
      ```bash
      touch lambda_s3_cleanup.py
      code .
      ```
    - Opened VS Code and wrote a Boto3 Python script:
    
      - A Boto3 S3 client was initialized to connect and interact with S3 resources.
      - The script listed the objects in the specified S3 bucket.
      - The script then deleted objects older than 30 days by comparing their last modified dates with the current date.
    
    - Pushed the script to Git:
      ```bash
      git add .
      git commit -m "WIP"
      git push origin main
      ```

    - The code was copied and pasted under the **Code** section of our AWS Lambda function.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-code.JPG/)

- Clicked on **"Deploy"** at the top.
- Went to the **Test** section, created a sample Test event, and then clicked on **Test**.
- Test executed successfully.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-Test-event-success.JPG)

- Checked **Cloudflare logs** and saw that the 2 images got deleted successfully.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-Cloudfare-logs-images-deleted.JPG)

- Handled the above error of lambda handeler.

![Alt Text](/1-Automated-S3-Bucket-Cleanup-Using-AWS-Lambda-and-Boto3/images/SA-cloudfare-log-images-deleted-again.JPG)
---

### 4. Testing the Lambda function

- Went to AWS S3 dashboard of the bucket.  
- The files were no longer present as they were successfully deleted by the AWS Lambda function.

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
