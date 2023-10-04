# PRGX Test

A basic test to apply foa a Python/SQL position

## Installation

I recommend install the project in a linux distro in order to use all
bash scripts developed to facilitate the installation.
You need to have previously installed python 3.7+ (with pip) and Postgres13+

Clone the repository:
    
    sds

Go to root directory:
    
    cd /my/previous/directories/prgx_test

Give execution's permission to up.sh, run.sh and stop.sh
    
    chmod +x up.sh run.sh stop.sh

Create Main DataBase (it is used to resolve the client's requests).
It is necessary that you use a user whit CREATE_DB's permission
available:

    psql -U YOUR_USER -d template1 -f up_main_db.sql -W

And, in the same way, up Test DataBase (It is used to resolve test's request):

    psql -U YOUR_USER -d template1 -f up_test_db.sql -W

Next, go to inner_server and create a file **.env** using the next structure:
    
    cd inner_server
    touch .env

(Copy this structure into **.env** file and modify the fields **POSTGRES_USER** and
**POSTGRES_PASSWORD** with your postgres' user and password )

    POSTGRES_USER=YOUR_USER
    POSTGRES_PASSWORD=YOUR_PASSWORD
    POSTGRES_SERVER=localhost
    POSTGRES_PORT=5432
    POSTGRES_MAIN_DB=pgrx
    POSTGRES_TEST_DB=pgrx_test

Return to root and after that, run **up.sh**:

    ./up.sh

When process finished, execute **run.sh**:

    ./run.sh

Open other terminal and go to inner_service:

    cd /my/previous/directories/prgx_test/inner_service

Is that directory up its virtual environmental:

    source venv/bin/activate

Execute its tests:

    pytest -v

If everything went well, go to the browser at the following
address:

    http://localhost:8000/docs

In that address you can see all the operation that are supported
by the system.

To end the process press CTRL + C in the terminal where you execute
**run.sh** and after run:
    
    ./stop.sh

Finally, press again CTRL + C to quit of the information server console
of uvicorn.

It is very important that you finish the process in this way because this
way ensure that all processes ended.

## SQL Test

My answer of SQLTEST are in the root directory in the file: 
**prueba_tecnica_sql.md** 
    