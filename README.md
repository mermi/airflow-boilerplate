# airflow-boilerplate

This is an example of running airflow in docker locally. 

## Requirements:

- Docker
- Python 3.8

## How to setup
---
- You only need to run the following:

<pre>
docker build -t airflow-local .
</pre>

> For some reasons I had to run the build command above as with `docker-compose up --build` was still looking for the build image and failing


## to run airflow:
---
You can spin up airflow image locally by running:

<pre>
make airflow-up
</pre>
One, you see the `init` part created and `usr admin created` you can reach airflow on localhost:8080.
You will be able to login with the `username` and `password` set in the `init` block in `docker-compose` file

<pre>
username: admin
password: admin
</pre>

> Airflow instance is based on LocalExecutor, this means that the tasks will run inside the scheduler container.

**to shut it down airflow instance**

<pre>
make airflow-down
</pre>

## How to setup local env
---

When you are interactong and using the codebase in your editor, is very helpful to have airflow installed locally. how? is easy, you need to setup a virtual environment and install all the libraries needed for your code. Simply run

<pre>
make init-local
</pre>

This command will do the following:

* clean local files: configuration files
* setup local python environement by running all the libraries in `requirements_*` files
* Source to the virtual environement
* Initialize the airflow home to your current `pwd`

## Linting
---
I decided to use `flake8` for python linting. to make sure you python files are aligned simply run:

<pre>
make lint
</pre>

To sort my import properly, decided to use `isort` by running

<pre>
make fix-imports
</pre>