# Football DB
[Video demo URL](https://youtu.be/QVTieepkTTM)

I like to play football, or what you in the United States would call "soccer". I can use scores of apps to track my favorite teams' games, and I would like to do the same for my own team that plays at an amateur level. For the final project of CS50's Introduction to Computer Science, I have built (the start of) a REST API with Flask and Sqlite3 to do just that! I can create club, add teams to that clubs, create players, add players to a team, and so on!
## Design choices & constraints
For this project, I focused "just" on creating a REST API with Flask. I could have added some frontend display with Flask, but I thought just building the API would be more than enough work already (and it was!).

Similarly, I would love to add more routes to this API so that I can actually start tracking useful data such as match scores, player statistics, standings, and so on. As it stands, this first version of my API already includes 19 routes.

I chose to use Sqlite3 as my database for this project. I found all sorts of useful Python frameworks that would abstract away some SQL logic for me, but I chose to create a "as-bare-bones-as-possible" application so that I could learn proper SQL first.

I use a controllers/services folder structure for this Flask API. In my controllers files, I handle all logic of the network calls, such as parsing a JSON request and a route's query parameters, verifying user input, and returning a JSON response. In my services files, I perform all database actions. The project also includes some other folders (constants, db, helpers, tests) which support the main interactions in the controllers and services

## Features
### Player routes
Users of the API can find, create, update and delete a player. Users can specify some basic information about their player, such as their date of birth and their preferred foot.
### Club routes
Users of the API can find, create, update and delete a club. Additionally, users can also add or update a club's details (such as address, year founded, etc.). Similarly, users can add or edit a club's kit colors, such as the the color and pattern of the shirts a club plays in.
### Team routes
Users of the API can find, create, update and delete a team. Teams are linked to a parent club with a foreign key. Users can also find a team's players and add to or remove players from a team. Users can specify query parameters to find a team's players for one or multiple seasons.