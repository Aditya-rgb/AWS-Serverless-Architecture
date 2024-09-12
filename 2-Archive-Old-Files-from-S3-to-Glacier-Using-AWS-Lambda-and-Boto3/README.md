# Archive Old Files from S3 to Glacier Using AWS Lambda and Boto3


## Objective
Automate the archival of files older than a certain age from an S3 bucket to Amazon Glacier for cost-effective storage.

## Task
Automatically move files in an S3 bucket older than 6 months to Glacier storage class.

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

After the bucket was provisioned, uploaded 4 image files into it.

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
- Gave function name as **"Aditya-Glacier-Function"**.
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

![Alt Text](/2-Archive-Old-Files-from-S3-to-Glacier-Using-AWS-Lambda-and-Boto3/images/GL-Function-flow.JPG)


- Made a Git repository called **"Serverless-Architecture"**.
    - Opened Git Bash on local:
      ```bash
      touch lambda_function.py
      code .
      ```
    - Opened VS Code and wrote a Boto3 Python script:
    
      - A Boto3 S3 client was initialized to connect and interact with S3 resources.
      - The script listed the objects in the specified S3 bucket and identified files older than 6 months residing in the S3 bucket.
      - The script then changed the storage class of the identified files to Glacier and logged the names of the archived files for monitoring purposes.
    
    - Pushed the script to Git:
      ```bash
      git add .
      git commit -m "WIP"
      git push origin main
      ```

    - The code was copied and pasted under the **Code** section of our AWS Lambda function.
 
- Clicked on **"Deploy"** at the top.
- Went to the **Test** section, created a sample Test event, and then clicked on **Test**.
- Test executed successfully.

![Alt Text](/2-Archive-Old-Files-from-S3-to-Glacier-Using-AWS-Lambda-and-Boto3/images/GA-TEST-Success.JPG)

- Checked **Cloudflare logs** and saw that the 4 images's storage class changed to Glacier

![Alt Text](/2-Archive-Old-Files-from-S3-to-Glacier-Using-AWS-Lambda-and-Boto3/images/GA-cloudwatch-log.JPG)

- Went to the AWS S3 bucket and captured the results...


![Alt Text](/2-Archive-Old-Files-from-S3-to-Glacier-Using-AWS-Lambda-and-Boto3/images/GA-Bucket-class.JPG)


- For faster testing executed the code for any file older than more than 5 mins residing in the S3 bucket.


## Testing

- You can manually trigger the Lambda function or set up a periodic trigger (e.g., using CloudWatch Events) to run it on a schedule.
- Check the S3 bucket after running the Lambda function to verify that files older than 1 year have been moved to the Glacier storage class.
- Review the CloudWatch Logs to ensure that the files were successfully archived.


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
