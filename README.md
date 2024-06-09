# GameBase
<p align="center">
    <img src ="src/static/images/GameBaseLogo_Transparent.png" width="300" >
</p>
Created on Windows 11 and 1920x1080 monitor. Works on other setups, but might appear slightly different.

# RUNNING THE CODE:

1) Install the dependencies
>$ pip install -r requirements.txt

2) Start up your database

3) In the config.py-file, input your database information

4) run setup.py from the GameReview or src folder, this will initialize the database (If it does not work go into the setup file and replace line 15)
>$ python src/setup.py  

5) Run Web-App:
>$ python src/app.py

# Using the application:

1) Create account / Press the 'Create Account' button, you then get to page where you choose your username, mail and password.

2) Login / Now you can login to your account by typing in your username and password.

3) Home / On the Home tab you will see some random games and you have access some different filter options.

4) Searching / You can search with a combination of Genre, Platform, Developer, Release Year and Title

5) Games / When you click on a game you get taken the their detail page, here you can see information about the game, see the reviews of other accounts or submit your own review

6) Profile / On your profile you can see all of the reviews you have made, and you can easily access the game you made them on

7) Logout / Log out of your account and return to Login



Test-reviews have been created for the 3 pokemon games to show a proof of concept.