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

- Snake Sprite Sheet downloaded from [OpenGameArt](https://opengameart.org/content/snake-sprite-sheet)
- Apple Sprite downloaded from [Vecteezy Apple PNGS](https://www.vecteezy.com/free-png/apple)
- Speedup Shoes and Snail Sprites downloaded from [Freepik](https://www.freepik.com/)
- Button Icons and Particles downloaded from [Freepik](https://www.freepik.com/)
- All fonts used are free license from [Dafont](https://www.dafont.com)

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
  - Added snake auto random movement Menu Panel.
- April 17, 2024
  - Implementation of Start Button and game panel slide animation.
- April 18, 2024
  - Implementation of the Snake Sprite with the correct turn covers.
  - Added snake head animation and updated stretch computation.
- April 20, 2024
  - Added snake shadow in sprite and fixed turn cover outside the screen.
  - Implemented the Game Over Screen. Added checker for collision with head 
    and body parts to trigger the game over state.
  - Implementation of Restart button event to reset the game after GAMEOVER.
- April 22, 2024
  - Added DeathCam and Quit Button in the Game Over Screen.
  - Added Icons to Buttons in Main Menu and Game Over Screen.
- April 23, 2024
  - Added Results Panel in the Game Over Screen with new font and icons.
  - Implemented Quit Button to go back to main menu screen and reset values.
- April 24, 2024
  - Added a snake dead sprite on the head part.
- April 26, 2024
  - Added FoodBuff class that spawns golden apple with random delayed timer.
  - Implemented Particle System and Particle Classes to emulate particle effects.
  - Added a sparkle particle system in the food buff class.
- April 27, 2024
  - Implemented lifetime of food buff to dissapear after a certain time.
  - Added Score points floater after eating any kind of food.
- April 29, 2024
  - Fixed spawn of food and food buff to prevent very close area spawns to each other.
  - Transferred particle system to the main Food class and added health effect on basic apple.
- April 30, 2024
  - Implementation of SpeedUp Class that spawns a speedup item with arrow up effects.
  - Updated particles effect to include a floating type of animation.
- May 1, 2024
  - Added Collision to snake head and items. Implemented Buff Icon on the Snake Head to show the current buff effect.
- May 2, 2024
  - Added Code to apply speed buff effect to snake parts. And to reset the speed after buff duration.
  - Removed the looping of snake body parts on window boundaries. It will die instead when bumped window bounds.
- May 3, 2024
  - Added wall sprites and fixed wall bounderies. Fixed auto path code of snake in main menu screen.
  - Fixed Last moments image capture. And bug fix on transparent speedup floater.
- May 7, 2024
  - Fixed bug on snake grow which the tail appears disconnected on certain turns.
  - Fixed bug on turn covers to include wall bounds image.
- May 8, 2024
  - Added a slowdown debuff class that spawns a slowdown item with arrow down effects.
- May 9, 2024
  - Fixed particle animation on food buffs. Fixed Bug on change sprite of snake head when dead after buff wears off.
  - Fixed snake head sprite detached on died state. Fixed item adding of score and balancing of spawn times.
- May 10, 2024
  - Added partial UI Design for the Top 3 Leaderboard in the menu screen.
- May 14, 2024
  - Finished UI Design codes for the Top 3 Leaderboard in menu screen. Updated Designed by label.
- May 15, 2024
  - Updated Slowdown Debuff to spawn near the snake head within a specified range on current direction.

<br>
<b>This project is currently under development.</b>