Minesweeper-Clone
=================

A little Pygame project

Minesweeper is a well-known computer game famously available for the Microsoft Windows operating system. Many variations exist on many platforms. 

The objective of the game is to click on all of the non-mine blocks. Clicking on a mine block should lead to a game-over screen.

This game was inspired by the programarcadegames.com tutorial.

Here, I aim to create a simple clone of Minesweeper to introduce myself to basic Pygame modules. 

NOTE: This game was created for Python3. It requires the pygame library for Python3.

<h3>TODO:</h3>

<h4>High priority</h4>
<ul>
  <li><s>Add a game-over state (victory and defeat)</s></li>
  <li><s>Have an option to restart the game after the game has ended</s></li>
  <li><s>Find a faster way to generate mine-less neighbors (recursion?)</s></li>
  <li><s>Initialize mines after the player has clicked once, and not where the player has already clicked</s></li>
  <li><s>Find a better way to initialize mines</s></li>
  <li>Update appropriate grids to use boolean values rather than 0s and 1s</li>
</ul>

<h4>Low priority</h4>
<ul>
  <li><s>Add flags</s></li>
  <li>Time the player</li>
  <li>Keep a record of best times</li>
  <li><s>Add numbers to blocks to signify the number of mine-neighbors (currently using colors)</s></li>
  <li>Refactor code</li>
  <li>Move grids to their own class</li>
  <li>Add option to have custom number of rows and columns</li>
  <li>Add option to have custom number of mines in play</li>
  <li>Improve game over screen</li>
</ul>
