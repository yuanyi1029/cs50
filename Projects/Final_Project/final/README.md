# CS50W Finance Tracker
#### Video Demo: xxxxxxx

This is my capstone project for CS50W. Finance Tracker is a simple web application built for users to document their financial activity as well as further understand their own spending habits and financial activity.


## Distinctiveness and Complexity
The idea for this project stemmed from receiving red envelopes from my relatives during the Lunar New Year because it would be much easier to document my earnings `:money_mouth_face:`. 

## What’s contained in each file you created.

## How to run your application.

## Any other additional information the staff should know about your project.



## Introduction
This is my final project for cs50x. Movie Reviewer is a simple barebones web based application made with Flask, HTML, CSS and SQL used to rate movies. Users are allowed to create an account and write reviews for movies they have seen or just browse through movies and check out the reviews and ratings that have been made by other people. This web applications aims to become a credible source for moviegoers as well as a platform to freely share one's opinion and thoughts about a movie.

## Frontend UI Implementation
This web application first prompts user to register or login into an account in register.html and login.html pages respectively. Once entered into an account, users are defaulted at the My Reviews page written in reviews.html. By default there are no reviews in a new account. Users are also abled to search for a specific movie at the website header written in search.html and searched.html. If a specific movie is found, users can choose to view all reviews by other users (in view.html) as well as choose to write a review for that specific movie. Lastly, users can choose to write a review from scratch by clicking on "Write Review" at the header which will redirect them to write.html. An extra feature which allows users to change their passwords are also included in which they will be redirected to change.html. An extra stylesheet CSS file (style.css) and a favicon icon is also included in the static folder for the web application.

## Backend Server Implementation
The implementation for the webserver is written in app.py. <u>To test the code out and run a development server, it is required to change directory into the project folder and type out "flask run" into the command line.</u> This app.py file is configured as a Flask application, and also creates 3 database tables (users, movies, reviews) if it does not already exist. Each webpage route is also configured and handled to perform database query tasks, simple calculations and render html templates.

Each route are implemented as follows:
1) "/" route

    the "/" route is tasked to run the reviews() function which brings users to the "/reviews" route

2) "/write" route

    the "/write" route will render write.html when using the GET method but will get the form inputs from write.html and update the movies and reviews table when using the POST method. Once the tables are updated, the users are redirected back to the default route

3) "/reviews" route

    the "/reviews" route only utilises the GET method because a HTML form is not used. The reviews() simply gets all the reviews from the user in that session as well as creates an id_to_movie dictionary. These 2 variables are passed into reviews.html and rendered. The id_to_movie dictionary is important as it will be used to translate each movie_id in the table into each movie title.

4) "/login" route

    the "/login" route will render login.html when using the GET method but will get the form inputs from login.html and perform some validations  when using the POST method. If all the validations are true, a session will be recorded and the user will be redirected to the default route

5) "/logout" route

    the "/logout" route simply clears a session and redirects the user to the default route. Since the sessions are now empty, the user will be prompted to login first.

6) "/search" route

    the "/search" route will render search.html when using the GET method but will get the form inputs from search.html and query the database table for a similar movie name as the input when using the POST method. searched.html will then be rendered for the users for their search results

7) "/searched" route

    the "/searched" route will render search.html when using the GET method but will get the form inputs from searched.html and determine either "View reviews" or "Write reviews" button has been pressed. It will then redirect users to either view.html or write.html depending on which button is pressed.

8) "/register" route

    the "/register" route renders register.html when using the GET method but will get the form inputs from register.html and perform some validations when using the POST method. If all the validations turn out to be true, a new row (representing an account) will be added into the users database

9) "/change" route

    the "/change" route renders change.html which allows users to change their password when using the GET method but will get the form inputs from change.html and perform some validations when using the POST method. If all the validations are true, the user's password will be updated in the users database table.




