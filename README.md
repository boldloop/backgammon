# GB-gammon

This repository holds my backgammon-playing AI, which uses TD-lambda learning and a neural net, following Gerald Tesauro's TD-Gammon papers. I worked on this largely in May of 2020 as a quarantine self-edification project. To that end, I tried to do everything myself, instead of relying on external packages. That means everything is written more or less in stock python (with a little bit of NumPy), so it's not super fast—my five-year-old laptop can run about 4,000 games in an hour, or slightly more than one game a second.

If you'd like to try to play the trained net, you can run `game.py`. I'll warn that this interface is extremely rough, because I built it for debugging, not enjoyment. The rolls are given as tuples with each die. To enter your moves, type `<point>-<num>, <point>-<num>`. So, if I rolled a `(3, 1)` to open, I would type `8-3, 3-1` to make my 5-point. For doubles, you can type four sequences, and if you have no valid move you need to type something like `6-0`. To enter off the bar, type `25-<number entering>`. (Like I said, the user experience is, uh, unpleasant.)

Hope you have a great day!
