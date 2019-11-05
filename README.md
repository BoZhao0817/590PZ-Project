# 590PZ-Project-Circle the cat
Forks of this are student projects for IS 590PZ

## Original Game Introduction
Group: Yuan Gao, Bo Zhao

you can play the original game here: https://www.crazygames.com/game/circle-the-cat
### rules
* cat is at the center of the board when game start
* human should play first
* cat can't move to the obstacles
* cat win condition: escape from the board(move to the blue point)
![alt text](https://github.com/BoZhao0817/590PZ-Project/blob/master/catwin.png)

## Our Game Setting
we add some additional rules to the game

### rules
* add mice to the game, number of mice can be changed, cat must eat one mouse before escape from the board
* add cat food to the game, numebr of cat food can be changed, if cat eat cat food, it can move twice the next turn
* add dog to the game, number of dogs can be changed, not decided whether the dog can randomly move, but prefer a fixed postion now(may change later), if the cat meet the dog, the cat lose immediately
* cat is at the center of the board when the game start
* human should play first(note: human in the program means player),human put obstacles to trap the cat
* cat can't move to the obstacles
* cat win condition: escape from the board + eat a mouse
* human(player) win condition: cat encounter dog/ cat is trapped by obstacles / cat can't eat mouse(mouse is surrounded by obstcles)

### algorithm
Minimax
