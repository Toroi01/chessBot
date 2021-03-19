# chessBot
A bot that plays chess using an engine to compute the best move and a [convolutional neural network](https://github.com/Elucidation/tensorflow_chessbot) which predicts the chessboard position from online chessboard screenshots.

The bot needs a starting chess position to start executing moves.

### Controls:
  * Hold A to reshape the board position inside the screen.
  Click in the top left corner of the screen
  Then, move the cursor to the top left corner of the chess board and press Z.
  Then, move the cursor to the bottom right corner of the chess board and press Z again.

  * Hold Q to pause the bot

  * Hold W to unpause the bot

  * Hold E to close the bot

  * Hold T to change the time_to_think (Amount of time for the engine to compute the best move)

  * Hold Y to change the num_obs (Numbers of screenshots samples to decide the actual fen of the position)
