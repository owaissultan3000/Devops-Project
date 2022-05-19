# Sprint 3 CI/CD implementation of webhealth lambda

This project is created for the integration of CI/CD pipeline with my repository which will pull, build, run test, and deploy the code, which will speed up development by performing steps necessary for production.
## Technologies used
-AWS_codepipeline is used to implement pipelines

-Github is used for version control

# Installing and Runing the Project 
## Requirments
-python version 3




Note: following steps are for linux system only
## Step 1
*checking for python version

`python --version`

 if version is python 3 don't porform the following steps

 `where python3`

copy the location

`vim ~/.bashrc`

copy the below code at the last line

`alias python = <loaction of python3>`

and press esc once or twice

`:wq`

to write to the bashrc file and quit the vim editor

verify for python3 version 

`python --version`

## Step 2

*checking for aws cli version 2

`aws --version`

If cli version is 2 don't perform following steps

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

`unzip awscliv2.zip`

`sudo ./aws/install`

copy and paste above commands in terminal

for further assistence refer to the following document

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

## Step 3
now you need to fork and clone this git repository

`git clone <add git url>`

## Step 4
step into sprint3/ drirectory

initialize cdk app

`cdk init --language python`

activate virtual environment

`source ./venv/bin/activate`

install Requirments

`pip install -r requirments.txt`

`npm install -g aws_cdk`

and run `cdk synth && cdk deploy` command in the terminal

Once you have deployed your app now whenever you push code into the repo the pipeline will build itself 

### Git commands 

`git add .`

`git commit -m "<msg>"`

`git push`






