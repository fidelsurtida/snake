# SNAKE GAME

A simple project of a snake game based on the 1997 Nokia phone game 
with improvised graphics and gameplay.


## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Development Updates](#development-updates)

## About

A snake game replicated from the famous Nokia phone game application. 
Unlike other implementations that uses grid system which appends
and pops the snake parts, this snake showcases smooth movement by moving
the parts per frame based on speed.
<br><br>
This will be my first ever game project in python as a software engineer.
This showcases my knowledge about object-oriented design, and basic uses of 
the fundamentals of python language.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

## Usage

Provide examples or instructions on how to use your project. Include screenshots or gifs if applicable.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- Apple Sprite downloaded from [Vecteezy Apple PNGS](https://www.vecteezy.com/free-png/apple)

## Support

If you have any questions or issues, please feel free to [open an issue](https://github.com/fidelsurtida/snake/issues/new) on GitHub.

## Authors

- [Fidel Jesus O. Surtida I](https://github.com/fidelsurtida) - *Game Developer*

## Development Updates

- March 27, 2024 
  - Initial commit of the project
- March 28, 2024 
  - Refactored the project structure
- March 29, 2024
  - Added the snake class which the player can control.
  - Restricted movement of snake to opposite direction.
- April 1, 2024
  - Implementation of rectangular snake cover for each turning parts.
- April 2, 2024
  - Refactored code for direction using properties
  - Implemented snake bounderies to move to the opposite side of the screen.
- April 3, 2024
  - Added starting food class with simple spawn at random locations.
  - Added snake head collision to destroy food. The food also respawns 
    at a specified delay and random location after being eaten.
- April 5, 2024
  - Implemented snake body grow logic after eating food.
- April 7, 2024
  - Created initial Interface Manager that updates and displays score.
- April 8, 2024
  - Reimplemented GUI Manager to use the library pygame_gui. Now displays
    the score inside a white panel at the top.
  - Added lifetime mechanic and label that decreases per second 
    and replenishes on eating the food. 
  - Added the Stretch label that shows the added length of snake in meters.
- April 10, 2024
  - Fixed snake loop boundary (y-axis) which includes the game panel at top.
- April 11, 2024
  - Added a regen label with fade and move up animation after eating food.
  - Fixed food respawn bounderies and added checker to prevent overlap with snake.
  - Fixed bug of snake movement going back when pressing 2 simultaneous directions.
  - Added an apple sprite to the food class.
- April 12, 2024
  - Added config class to store all game configurations. Refactored all current config codes.
  - Added game background and adjusted regen label readability and apple shadow.
- April 15, 2024
  - Added Panel Background and added starting game fonts for the panel labels.
  - Added Icons for the game panel and added game regen heart icon.
- April 16, 2024
  - Added the Floater Class to encapsulate the UILabel and Icon for status
    text that floats after an action by the player.
  - Implementation of the Menu Panel with title and start button.

<br>
<b>This project is currently under development.</b>