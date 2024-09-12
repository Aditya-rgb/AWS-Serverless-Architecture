# Implement a Log Cleaner for S3


## Objective
Create a Lambda function that automatically deletes logs in a specified S3 bucket that are older than 90 days.


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

After the bucket was provisioned, uploaded 3 log files into it.

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

![Alt Text](/3-Implement-a-Log-Cleaner-for-AWS-S3/images/LOG-FUNCTION-flow.JPG)


- Made a Git repository called **"Serverless-Architecture"**.
    - Opened Git Bash on local:
      ```bash
      touch lambda_function.py
      code .
      ```
    - Opened VS Code and wrote a Boto3 Python script:
    
      -The script listed all objects in the specified S3 bucket and identified files with the .log extension.
      -The script then checked the age of each .log file and deleted those older than 5 minutes.
      -It logged the names of the deleted .log files for monitoring and verification purposes.
    
    - Pushed the script to Git:
      ```bash
      git add .
      git commit -m "WIP"
      git push origin main
      ```

    - The code was copied and pasted under the **Code** section of our AWS Lambda function.
    - 
 ![Alt Text](/3-Implement-a-Log-Cleaner-for-AWS-S3/images/LOG-CODE-COPIED.JPG)



- Clicked on **"Deploy"** at the top.
- Went to the **Test** section, created a sample Test event, and then clicked on **Test**.
- Test executed successfully.

![Alt Text](/3-Implement-a-Log-Cleaner-for-AWS-S3/images/LOG-TEST-PASS.JPG)

- Checked **Cloudflare logs** and saw that the 4 images's storage class changed to Glacier

![Alt Text](/3-Implement-a-Log-Cleaner-for-AWS-S3/images/LOG-CLOUDFARE-LOGS.JPG)

- Went to the AWS S3 bucket and captured the results... and saw 2 log files a.log and b.log got deleted and c.log which was freshly uploaded still resided.


![Alt Text](/3-Implement-a-Log-Cleaner-for-AWS-S3/images/LOG-BUCKET-SS.JPG)


- For faster testing executed the code for any log file older than more than 5 mins were deleted instaed of 90 days. The code for both scenarios have been uploaded inside this git repository.


## Testing

- You can manually trigger the Lambda function or set up a periodic trigger (e.g., using CloudWatch Events) to run it on a schedule.
- Check the S3 bucket after running the Lambda function to verify that log files older than 90 days have been deleted.
- Review the CloudWatch Logs to ensure that the files were successfully archived.


### 4. Testing the Lambda function

- Went to AWS S3 dashboard of the bucket.  
- The log files a.log and b.log files were no longer present as they were successfully deleted by the AWS Lambda function.

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
