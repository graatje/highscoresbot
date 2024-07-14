This is the github repository of highscores bot for the game pokemon planet. 

# Getting started
1. Make the .env file, see .env.example for the format.
2. Run the docker-compose.yaml. This will run `python manage.py runserver`.
3. In the highscoresbot container, run `python manage.py migrate`
4. To seed the database, run `python manage.py seed`
5. To run the command part of the discord bot itself, run `python main.py`
6. To run the sending of events, run `python manage.py eventsender`


If you have any questions, feel free to pm kevin123456 on discord.