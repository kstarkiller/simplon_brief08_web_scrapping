# Book Scraper and Dashboard Project

## Overview

This project is a Python-based web scraping and data visualization project using the Scrapy, pymongo, and Dash libraries. The goal is to scrape data from [books.toscrape.com](http://books.toscrape.com), store it in a MongoDB database, and create a dashboard to search and visualize the scraped book data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Scraping](#scraping)
- [Dashboard](#dashboard)
- [Automatic execution with anacron](#anacron)
- [Contributing](#contributing)

## Installation

1. **Clone the repository:**

    ```bash
    git clone git@github.com:kstarkiller/simplon_brief08_web_scrapping.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd simplon_brief08_web_scraping (or whatever you named this project)
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r dash/requirements.txt
    ```

## Usage
### Scraping
To scrape data from books.toscrape.com, you first have to install MongoDB and create your user (if not already done): without this step you won't be able to run scraping process.
[See instructions to install MongoDB and create an user below](#MongoDB)

In spider.py and main.py, replace MONGO_USR and MONGO_PWD variables by your MongoDB username and password (see lines 14 and 15 of the spider.py file and line 23 of the main.py)

Then you can run the following command:
    scrapy crawl myspider

This command will initiate the scraping process and save the scraped data in 'books' collection of 'scraped_books' database.

### Dashboard
To launch the dashboard, run the following command:
    python dash/main.py

Visit http://localhost:8050/ in your web browser to interact with the dashboard. You can search for books and visualize some data points.

### Anacron
### Automatic execution
To crawling books.toscrape.com website every day (monday to friday) automatically go the ~/etc/anacrontab and write this line and the end of the file :

    1       15      spider       [1-5] "~/path/to/your/file"
    
What means this line ?
- 1: Specifies that the command should be executed every day.
- 15: Represents the delay in minutes.
- spider: Is the identifier for the job.
- [1-5]: This specifies the range of days from Monday (1) to Friday (5). So, the command will only be executed on days 1 through 5 (Monday to Friday).
- /path/to/your/file: Is the path to the program or script that will be executed.

## Project Structure
    simplon_brief08_web_scraping/
    ├── scraping/
    │   ├── myproject/
    │   │   ├── spiders/
    │   │   │   ├── _init_.py
    │   │   │   └── spider.py
    │   │   ├── _init_.py
    │   │   ├── items.py
    │   │   ├── middlewares.py
    │   │   ├── pipelines.py
    │   │   └── settings.py
    │   └── scrapy.cgf
    ├── dash/
    │   ├── assets
    │   │   ├── icons/
    │   │   │   ├── logo.svg
    │   │   │   └── search_icon.svg
    │   │   └── style.css
    │   ├── main.py
    │   └── requirements.txt
    ├── api/
    │   └── traduction_api.py
    ├── .gitignore
    └── README.md

- scraping/ : Contains the Scrapy spider for scraping book data.
- spider.py: Script to scrape data and store them in a MongoDB database.
- main.py: Script to create and launch the Dash dashboard.
- requirements.txt: Lists the required Python libraries and versions.
- README.md: Project documentation.

## Contributing
Feel free to contribute to this project by opening issues or submitting pull requests. Your input is highly appreciated.

-----------------------------------------------------------------
-----------------------------------------------------------------

## MongoDB
## Installation and User Creation Guide

This guide will walk you through the process of installing MongoDB on Ubuntu and creating a user with read and write permissions.

## 1. Install MongoDB

### 1.1 Update Package List
    sudo apt update

### 1.2 Install MongoDB
    sudo apt install -y mongodb

### 1.3 Start MongoDB
    sudo systemctl start mongod

### 1.4 Enable MongoDB to Start on Boot
    sudo systemctl enable mongod

## 2. Access MongoDB Shell
    mongosh

## 3. Create a Database and User
### 3.1 Switch to Admin Database
    use admin

### 3.2 Create a User with Read and Write Permissions
Replace username and password with your desired values.

    db.createUser({
            user: "username",
            pwd: "password",
            roles: [
                { role: "readWrite", db: "your_database" }
            ]
        })
        
Make sure to replace your_database with the name of the database you want to grant read and write permissions to.

### 3.3 Exit MongoDB Shell
    exit

## 4. Test the New User
### 4.1 Open MongoDB Shell with the New User
    mongo -u username -p password --authenticationDatabase your_database
Replace username, password, and your_database with your specified values.

### 4.2 Verify User Permissions
    use your_database
    db.getCollectionNames()
This should display the collections in your database, confirming that the user has read and write permissions.
