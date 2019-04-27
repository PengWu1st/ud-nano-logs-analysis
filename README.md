# Project Name: News Website Log Analysis Statistics
## Overview
This project sets up a **PostgreSQL** database for a **news** website
The provided Python script **report_tool.py** uses the **psycopg2** library to query
the database and produce a report that answers the following questions
- Question 1: What are the most popular three articles of all time?
- Question 2: Who are the most popular article authors of all time?
- Question 3: On which days did more than 1% of requests lead to errors?

## Requirements
- Vagrant
- VirtualBox

### Step1: install VirtualBox
Follow [this instruction](https://www.virtualbox.org/wiki/Downloads) to download and setup VirtualBox
### Step2: install Vagrant
Follow [this instruction](https://www.vagrantup.com/downloads.html) to download and setup Vagrant
### Step3: setup project enviroment
1. Create a new folder on your computer where you’ll store your work for this project, then open that folder within your terminal.
2. Download this [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) to your project folder. This Vagrantfile already include the commands to download and install **PostgreSQL**
3. Type `vagrant up` to download and start running the virtual machine
### Step4: download the data
1. Download [the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.
2. To load the data, cd into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.
### Step5: run the report

## Database and tables

### List of tables in the news dababase
| Schema |   Name   |  Type  |  Owner  |
| ------ | -------- | ------ | ------- |
| public | articles | table  | vagrant |
| public | authors  | table  | vagrant |
| public | log      | table  | vagrant |

### table structures

Table `log`
| Column |           Type          |             Description                 |
| ------ | ----------------------- | --------------------------------------- | 
 path   | text                     | value like `/article/candidate-is-jerk` |
 ip     | inet                     |                                         |
 method | text                     |                                         |
 status | text                     | value like `200 OK`,`404 NOT FOUND`     |
 time   | timestamp with time zone | value like `2016-07-01 07:00:47+00`     |
 id     | integer                  |                                         |

Table `articles`
| Column |           Type          |                   Description         |
| ------ | ----------------------- | ------------------------------------- |
 author | integer                  | author id
 title  | text                     | value like `Candidate is jerk, alleges rival`
 slug   | text                     | value like `candidate-is-jerk`
 lead   | text                     | 
 body   | text                     | 
 time   | timestamp with time zone |
 id     | integer                  | 

Table `authors`
 Column |  Type   |                      Description                       
------- | ------- | -----------------------------------------------------
 name   | text    | value like `Ursula La Multa`
 bio    | text    | 
 id     | integer | author id

## how to run
Put `report_tool.py` into the `vagrant` directory and run
```shell
python report_tool.py
```