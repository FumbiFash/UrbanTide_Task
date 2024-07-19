# UrbanTide_Task
Technical Test


## Setup

### Need to have the following
- Docker
- Docker Compose
- Python 3

# Instruction

 Clone the repository:
   ```sh
   git clone https://github.com/FumbiFash/UrbanTide_Task.git
   cd UrbanTide_Task



### Approach to the problem

Note
 I would typically create a virtual environment but I have chosen not to use a one for this project to keep the setup simpler.
Although using a virtual environment would help in managing dependencies and avoiding conflicts, it was omitted here for simplicity. The correct versions for the dependencies are in the requirements.txt file. 

1. Tools 
- I Had initially attempted building the application with Django in order to make use of Django REST Framework and its validation tools/api interface, but task description specified Flask so accomplished it following instructions instead

2. Flask app setup
   - set up flask app with endpoint for file upload handling
   - configured sqlalchemy to connect to postgresql env using docker environment variables

3. csv upload
 - used pandas to read the uploaded csv into dataframes and created sql table from the csv schema

4. outlier detection
 - performed simple outlier detection using interquartile range to check outliers in the data

5 . Containerization

 - i wrote a dockerfile to containerize flask app, and then i used docker compose to run the flask app and postgresql together

 6. I accessed the API using Postman and used the test csv files to check which one passed and failed




### Some problems I had


1. Table already defined error
  - error when i attemped to upload a new csv file for testing because table already existed in database. Error was from sqlalchemy which was thrown when multiple csv files were uploaded.

Solution
   - Modified the 'create_table_from_df' function to chech if table already existed before attempting to create it. Accomplished this by using 'inspect' module to query database for existing tables. If table alsready exists, then the function uses existing table for data insertion. 

2. General error handling
   Some errors suchas as the one above where the table was already defined were not so easy to find at first in my code so i used imported and used 'logging' for this. 

   Solution 
    - Implemented logging to the application to capture and log error messages to help in troubleshooting 
 
3.  Port conflict
  There was a port conflict on my host machine because the default PostgreSQL port 5432 and Flask port 5000 were being used already by other instances of postgresql and other web servers on my machine
  Solution
  -  changed the postgresql port to 5433 and flask port to 5001 in the docker-compose file 

4.  compatibility issue with pandas and numpy causing error with the flask application. 

 compatibility issues between Flask, Werkzeug, Pandas, and Numpy also caused some headaches.

Solution 
 - Updated the requirements.txt file to include compatible versions
