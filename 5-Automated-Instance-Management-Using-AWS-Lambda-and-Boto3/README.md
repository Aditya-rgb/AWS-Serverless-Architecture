
# Automated Instance Management Using AWS Lambda and Boto3


## Objective
In this case study, we will gain hands-on experience with AWS Lambda and Boto3, Amazon's SDK for Python. I will create a Lambda function that will automatically manage EC2 instances based on their tags.

## Task
To automate the stopping and starting of EC2 instances based on tags.


---

## Tools required
- AWS portal access
- AWS Lambda function
- AWS EC2FullAccess IAM Role
- Boto3

---

## Deployment Steps

### 1. Creation of 2 EC2 instances

- **Step 1**: Sign in to the AWS Console.
  - Navigated to the [AWS Management Console](https://aws.amazon.com/console/), and logged in to my AWS account.
  
- **Step 2**: Navigate to EC2.
  - From the services menu, searcedh for **EC2** and selected **Launch Instance**.
  - Clicked on Add Additional Tags
  - Created two tags one key-value as "name" and "Aditya-Serverless" and another key-value as "Action and "Aditya-Serverless"

- **Step 3**: Choose an Operating System.
  - Opted for **Ubuntu** as the OS.

- **Step 4**: Choose Architecture.
  - Selected **64-bit (arm)** architecture.

- **Step 5**: Choose Instance Type.
  - Chose **t4g.micro** for this case.

- **Step 6**: Configure Key Pair.
  - Set up key-pair login for the EC2 instance (download the `.pem` file for future access).

- **Step 7**: Configure Security Groups.
  - Allowed the following traffic:
    - SSH traffic
    - HTTPS traffic
    - HTTP traffic
  - Selected "Anywhere 0.0.0.0/0" for all.

- **Step 8**: Kept Storage as Default.

- **Step 9**: Review the Instance Summary.
  - Verified the summary on the right side of the screen before creating the instance.

- **Step 10**: Launch the Instance.
  - Launched the instance using **EC2 Instance Connect** instead of using the `.pem` file.

- **Note**: Downloaded the key pair (`.pem` file) for future access.
After the bucket was provisioned, either upload anything or keep it empty.

Create multiple such buckets and set some of them to public state.

---

### 2. Creation IAM role for our Lambda function
- In the **IAM dashboard**, a new role specifically for Lambda was created.  
- The trusted entity type was set to **Lambda**, allowing the role to be used by AWS Lambda functions.

After the role was created, the **EC2FullAccess** policy was attached to it, giving the Lambda function full access to interact with S3 buckets.  
*(Note: In a real-world scenario, more restrictive permissions would be advisable to follow the principle of least privilege, ensuring tighter security.)*

- Could not attach the AmazonSNSFullAccess policy to the role as there were no IAM roles with 2 policy attached to them, so for this case we would require S3FullAccess and AmazonSNSFullAccess
- If done properly then this policy will allow your Lambda function to publish messages to SNS if any public buckets detected.

---

### 3. Lambda function creation and deployment 

- Navigated to the **Lambda dashboard** and clicked on **"Create function"**.
- Selected **"Author from Scratch"**.
- Gave function name as **"Aditya-EC2-Auto"**.
- Chose **Python 3.10** as the runtime for the function to ensure compatibility with Boto3 library.
- The IAM role from the previous step was assigned to the Lambda function, giving it the necessary permissions to interact with EC2 instances.
- Kept **Architecture as "arm64"**.
- Rest of the configurations were left as default.
- Clicked on **"Create function"**.

No need to create any Trigger for this function as this case study is to determine and perofrm audit on all existing EC2 instances.

![Alt Text](/5-Automated-Instance-Management-Using-AWS-Lambda-and-Boto3/images/auto-lambda-flow.JPG)


- Made a Git repository called **"Serverless-Architecture"**.
    - Opened Git Bash on local:
      ```bash
      touch lambda_function.py
      code .
      ```
    - Opened VS Code and wrote a Boto3 Python script

    - This Lambda function automatically audits all the EC2 instances in your AWS account and identifies any EC2 with tags as Auto-Start and Auto-Stop.


## Functionality

### 1. **Initialized EC2 Client**
- Used `Boto3` to interact with AWS EC2 services for listing, starting, and stopping EC2 instances based on specific tags.

### 2. **Stopped EC2 Instances**
- The `stop_instances()` function retrieves instances that have the `Action` tag set to **Auto-Stop** and are currently in a **running** state.
- For each instance, the function:
  - Prints the **Instance ID**.
  - Fetches and prints the value of the **Name** tag (or labels it as "Unnamed Instance" if no `Name` tag is present).
  - Stops the instances by invoking `stop_instances()`.

### 3. **Started EC2 Instances**
- The `start_instances()` function retrieves instances that have the `Action` tag set to **Auto-Start** and are currently in a **stopped** state.
- For each instance, the function:
  - Prints the **Instance ID**.
  - Fetches and prints the value of the **Name** tag (or labels it as "Unnamed Instance" if no `Name` tag is present).
  - Starts the instances by invoking `start_instances()`.

### 4. **Handled Errors**
- Used `try-except` blocks to catch and log any exceptions encountered during instance start or stop operations.
- Printed exception details for troubleshooting.

### 5. **Utility: Fetched EC2 Instance Name**
- The `get_instance_name()` function:
  - Extracts the value of the **Name** tag for a given EC2 instance.
  - Returns `"Unnamed Instance"` if the instance does not have a **Name** tag.

---

## Example Output

- **Stopping Instances:**
  ```text
  Stopping instance: i-0123456789abcdef0, Name: MyEC2Server


    
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

![Alt Text](/5-Automated-Instance-Management-Using-AWS-Lambda-and-Boto3/images/auto-test-success.JPG)

- Checked **Cloudwatch logs** and saw that audit for all the concerend EC2 instances.

![Alt Text](/5-Automated-Instance-Management-Using-AWS-Lambda-and-Boto3/images/auto-logs-success.JPG)

-EC2 status afetr Lambda function execution

![Alt Text](/5-Automated-Instance-Management-Using-AWS-Lambda-and-Boto3/images/auto-ec2-status-after-lambda.JPG)



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

