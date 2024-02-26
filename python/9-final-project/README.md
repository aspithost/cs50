# Football stats
Video Demo:  https://youtu.be/b-_S-TS2F0c
## Summary:
Football stats is a command-line tool built with Python to query and filter football (or "soccer") data from a .csv file. Users can look for player statistics from a given season in a given competition, provided they supply a .csv file with that data, and will have that player data output to them in the command-line.
## How to use
### Instructions
Users can check all the command-line options and filters by typing the help command.
CS50:
```
python project.py
```
Mac:
```
python3 project.py -h
```

Windows:
```
py project.py -h
```

If you would like to use the default .csv file with player stats from the 2018-2019 English Premier League season that comes with this demo version, you can use the following command:
```
python project.py ./csv/20182019-pl-player-stats.csv [--command value]
```

### Prerequisites
Besides having Python and the modules specified in `requirements.txt` installed, users should supply a valid .csv file with player statistics. When you use a different .csv file than the one provided in the `./stats` folder in this demo version, you may need to "normalize" the names of columns (see the "ARGPARSE_MAPPINGS" constants in `project.py`).
## Modules used:
### Argparse
This command-line tool uses Python's argparse module to define what data users can query and how users can format that data. With the `-h` or `--help` command, users can view all the required and optional arguments that the command-line tool comes with.

This program uses argparse argument groups to logically group the command-line arguments that a user can enter. Users can query the .csv file with any number of command-line arguments, and can combine arguments to narrow down the results even further.
### Tabulate
This command-line tool uses Tabulate to structure the output of a user's query. When a user's search returns a long list of players, formatting the results with Tabulate helps users comprehend this data and allows them to easily compare player statistics to one another row-by-row/player-by-player
## Functionality
To output the stats of football players to users of this command-line tool, this program comes with the following functionality
### Validate command-line input
Prior to processing any of the user's input, the program checks whether the user has specified valid command-line arguments. Users should provide a valid .csv file and filter or sort the data by at least one filter or formatting argument. Users can always use the help command.
### Parsing command-line arguments
In the `parse_arguments()` step, this program uses argparse to create some easy to use flags or commands for the user to filter and format player data. I did not want users to enter the often long and technical names of columns of .csv files, so I created mappings so that user can simply enter `--goals` instead of `goals_overall`. It requires the user to supply a .csv file, and adds argument groups for both filtering data and formatting data.

Users are allowed to filter player data with as many command-line arguments as they like, and can even use the same argument several times to check for multiple values of the same argument. For example, if a user wants to look for defenders who have scored 2 or 3 goals in a given season, you can use the following command-line arguments:
```
-p defender -g 2 -g 3
```
Which will return all defenders who have scored 2 or 3 goals.
### Format a user's supplied filters
Further on in this program, we want to apply the user's filters to query the .csv file with. The `format_filters()` function takes all arguments parsed by argparse, and filters out any arguments that are not filters specified by the user. It returns a dictionary in the following structure
```
{'goals': [0, 1, 2], 'position': ['defender']}
```
Where keys are the arguments as specified by argparse, and the values are lists of the values specified by the user.
### Filter players
The program then filters out any players who do not match the filters specified by the user with the `filter_players()` function. This function in turn uses numerous nested functions before returning a list of filtered players. It uses csv.DictReader to read the .csv file, and then checks line-by-line (or player-by-player) if that player fulfills all criteria specified in the filters, and does so recursively. In the example mentioned in the previous paragraph, it would return defenders who have scored 0, 1, or 2 times.

As soon as a player does not match one of the filters, the function returns `None` and does not proceed to check for any further filters. Only players who match all filters (or at least one value of a filter with multiple values) will be appended to a list of filtered players. After completing this process for every player, the function returns a list of players that match all filters.
### Formatting options
By default, the program does not sort any player data. In this case, that means it will return the data in the order it is defined in your .csv file. In this demo version, for example, it sorts players alphabetically.

If the user provides a sort attribute, it will sort players by that attribute instead. By default, it will sort "descending" by that attribute, but a user can specify a sort order of "ascending" as well.

After sorting players by attribute (either alphabetically or numerically), the progam then limits the output to a certain number of players specified. For example, the following command-line arguments will sort players by goals scored and return the top 10 goal-scorers:
```
-sa goals -lm 10
```
### Output player statistics in command-line
After the program completes all filtering and formatting operations, it will output the results to the user using Tabulate. The program returns some (but not all) relevant player statistics, and does not allow the user to specify which player stats to output or to omit. I decided not to include such functionality in this version of the application, as I prioritized the filtering and formatting functionality.

## On a personal note
My name is Abel Spithost, I'm 31 years old, and I live in Groningen, the Netherlands. I only got started with coding and web development about three and a half years ago, and although I now have a job as a developer, I had never had taken any actual computer science courses like this one. I had a lot of fun with this course, and am hoping to complete the "regular" CS50 course in the near future as well. Thank you so much for making these courses available for free, as I couldn't have hoped for better introductions to some of these concepts and languages that I had never worked with before. Least I can do is recommend these courses to those around me!