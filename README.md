# Obsidian fitness tracker
This program will enable you to automatically track your fitness progress using Obsidian. It will read from a markdown table in your vault and write your noted exercises to a history file. It will then sort this table containing all workouts based on a score. This means the workout you should do next is always at the top. The score will increase based on 3 factors:
- The category hasn't been trained as much
- The subcategory hasn't been trained as much
- Days since you last did this exercise

Category can be a full exercise like push/pull, back/chest/arms, etc. Subcategory can be a muscle group.
## Requirements
- Somewhere to run (I used a Raspi)
- Obsidian
- Obsidian Sync or equivalent
## Setup
### Obsidian
- Setup Obsidian Sync to automatically sync with your smartphone
- Add Obsidian to autostart
### Markdown
In your Obsidian vault create 2 .md files with the following tables
#### Dashboard
In this .md file you keep track of the workouts you want to do. Everytime you do a workout you enter the weight into the 'value' column. The 'unit' and 'note' columns are optional. The workouts here are just examples.
| value | name           | variant  | last | max  | unit | category  | subcategory | note     |
| ----- | -------------- | -------- | ---- | ---- | ---- | --------- | ----------- | -------- |
|       | Curls          | pole     | 7.5  | 7.5  | kg   | arms      | bizeps      | preacher |
|       | Curls          | machine  | 30   | 30   | kg   | arms      | bizeps      | preacher |
|       | Curls          | hammer   | 16   | 16   | kg   | arms      | bizeps      | dumbells |
|       | Curls          | dumbells | 16   | 16   | kg   | arms      | bizeps      |          |
|       | Curls          | cable    | 30   | 30   | kg   | arms      | bizeps      | preacher |
|       | Curls          | cable    | 30   | 30   | kg   | arms      | bizeps      | normal   |
|       | Abdominals     | free     | 15   | 15   |      | legs      | abdominals  |          |
|       | Military press | dumbells | 16   | 16   | kg   | shoulders | upper       |          |
|       | Quadriceps     | machine  | 65   | 65   | kg   | legs      | quadriceps  |          |
|       | Hamstrings     | machine  | 55   | 55   | kg   | legs      | hamstrings  |          |
|       | Calves         | standing | 100  | 100  | kg   | legs      | calves      |          |
|       | Bench press    | negative | 30   | 30   | kg   | chest     | lower       | machine  |
|       | Fly            | dumbells | 12   | 12   | kg   | chest     | inner       |          |
|       | Bench press    | pushups  | 15   | 15   |      | chest     | central     |          |
|       | Squads         | free     | 60   | 60   | kg   | legs      | full        |          |
|       | Leg press      | machine  | 160  | 160  | kg   | legs      | full        |          |
|       | Back raises    | pole     | 70   | 70   | kg   | back      | lower       |          |
|       | Back raises    | plate    | 15   | 15   | kg   | back      | lower       |          |
|       | Single row     | machine  | 35   | 35   | kg   | back      | inner       |          |
|       | Reverse fly    | machine  | 35   | 35   | kg   | back      | inner       |          |
|       | Lat pulldown   | close    | 55   | 55   | kg   | back      | outer       | machine  |
|       | Rowing         | pole     | 40   | 40   | kg   | back      | upper       |          |
|       | Rowing         | machine  | 50   | 50   | kg   | back      | upper       |          |
|       | Military press | pole     | 40   | 40   | kg   | shoulders | upper       |          |
|       | Side lifting   | cable    | 12.5 | 12.5 | kg   | shoulders | side        |          |
|       | Front lifting  | cable    | 10   | 10   | kg   | shoulders | front       |          |
|       | Bench press    | incline  | 18   | 18   |      | chest     | upper       | dumbells |
|       | Bench press    | incline  |      |      |      | chest     | upper       | pole     |
|       | Bench press    | incline  |      |      |      | chest     | upper       | machine  |
|       | Dips           | machine  | 20   | 20   | kg   | chest     | lower       |          |
|       | Fly            | machine  | 55   | 55   | kg   | chest     | inner       |          |
|       | Bench press    | vertical | 60   | 60   | kg   | chest     | central     |          |
|       | Triceps press  | overhead | 45   | 45   | kg   | arms      | triceps     |          |
|       | Triceps press  | cable    | 45   | 45   | kg   | arms      | triceps     | rope     |
|       | Triceps press  | cable    | 45   | 45   | kg   | arms      | triceps     | pole     |
|       | Treadmill      | running  | 20   | 30   | min  | cardio    | cardio      | machine  |
|       | Lat pulldown   | wide     | 50   | 55   | kg   | back      | outer       | machine  |
|       | Shruggs        | dumbells | 30   | 30   | kg   | shoulders | neck        |          |

#### Goals
In this .md file you set targets for your workout, e.g. on a weekly basis. The timeframe can be arbitrary, important is the ratio between the categories and subcategories
| category  | subcategory | goal |
| --------- | ----------- | ---- |
| back      | upper       | 1    |
| back      | outer       | 2    |
| back      | lower       | 1    |
| back      | inner       | 2    |
| arms      | bizeps      | 3    |
| arms      | triceps     | 2    |
| cardio    | cardio      | 1    |
| chest     | central     | 1    |
| chest     | upper       | 1    |
| chest     | lower       | 1    |
| shoulders | upper       | 1    |
| shoulders | side        | 1    |
| shoulders | front       | 1    |
| chest     | inner       | 1    |
| legs      | full        | 2    |
| legs      | quadriceps  | 1    |
| legs      | hamstrings  | 1    |
| legs      | calves      | 1    |
| legs      | abdominals  | 1    |

### Create environment
Create an environment 
```
python -m venv /.venv/
```
Install packages
```
pip install -r requirements.txt
```
### Setup environment variables
Create a file called .env with these values
```
DASHBOARD = 'path/to/dashboard.md'
HISTORY = 'history.csv'
GOALS = 'path/to/goals.md' 
```
### Add cronjob
Edit line 2 in fitness_tracker.bash to point to this directory.
Add a cronjob to run fitness_tracker.bash on a daily basis. Enjoy :)