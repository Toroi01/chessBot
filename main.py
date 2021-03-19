'''
Important variables:
  time_to_think = Amount of time for the engine to compute the best move
  certainty = Certainty of the obtained fens according to the model
  num_obs = Numbers of screenshots samples to decide the actual fen of the position

Note:
  Put stockfish.exe inside stockfish folder

Controls:
  -Hold A to reshape the board position inside the screen.
  Click in the top left corner of the screen
  Then, move the cursor to the top left corner of the chess board and press Z.
  Then, move the cursor to the bottom right corner of the chess board and press Z again.

  -Hold Q to pause the bot

  -Hold W to unpause the bot

  -Hold E to close the bot

  -Hold T to change the time_to_think (Amount of time for the engine to compute the best move)

  -Hold Y to change the num_obs (Numbers of screenshots samples to decide the actual fen of the position)
'''
from screen import *
from tensorflow_chessbot import *
import asyncio
import chess
import chess.engine
import pyautogui
import time
import keyboard
from collections import Counter
import operator

def update_screen_cords():
  '''
  Updates where is the board in the screen and compute two dictionary between chess moves and screen coordinates
  moves_to_cords_white
  moves_to_cords_black
  '''
  global board_cords
  global moves_to_cords_white
  global moves_to_cords_black
  board_cords = get_board_cords_in_screen()
  
  letters = ['a','b','c','d','e','f','g','h']
  origin = (board_cords[0],board_cords[1]+board_cords[3])
  sqsize = int((board_cords[2]/8))
  keys_white = []
  cords_white = []

  keys_black = []
  cords_black = []
  
  #White
  for l in letters:
    for x in range (1,9):        
         keys_white.append(l+str(x))

  for x in range(0,8):
    for y in range(0,8):
      cords_white.append((origin[0]+x*(sqsize)+sqsize/2,origin[1]-y*sqsize-sqsize/2))

  #Black   
  for l in letters[::-1]:
    for x in range (8,0,-1):         
         keys_black.append(l+str(x))

  for x in range(0,8):
    for y in range(0,8):
      cords_black.append((origin[0]+x*(sqsize)+sqsize/2,origin[1]-y*sqsize-sqsize/2))

  moves_to_cords_white = dict(zip(keys_white, cords_white))
  moves_to_cords_black = dict(zip(keys_black, cords_black))

def make_move(move):
  '''
  Executes a chess move according to board location into the screen
  '''
  print(move)
  if(player_color == 'w'):    
    pyautogui.click(moves_to_cords_white[str(move[0:2])])
    pyautogui.click(moves_to_cords_white[str(move[2:4])])
    #Two more because of promotion
    pyautogui.click(moves_to_cords_white[str(move[2:4])])
    pyautogui.click(moves_to_cords_white[str(move[2:4])])
  else:
    if(player_color == 'b'):
      pyautogui.click(moves_to_cords_black[str(move[0:2])])
      pyautogui.click(moves_to_cords_black[str(move[2:4])])
      #Two more because of promotion
      pyautogui.click(moves_to_cords_black[str(move[2:4])])
      pyautogui.click(moves_to_cords_black[str(move[2:4])])
    
def update_fens_list():
  '''
  Try to get the chess board position from multiples screenshot.It takes multiples screenshots and gets the position of each one, then, choose the most likely (to avoid confusions if it takes the screenshot while a move is being executed).
  Track the game status by storing the different board positions into fens_list
  '''
  global fens_list
  global player_color
  global turn
  global fens_list
  global tmp_obs
  global num_obs
  #Take an screenshot of the board
  screenshot(board_cords)
  #Get the fen_observation
  fen_observation,certainty = get_fen_from_board(0)
  #print(fen_observation,certainty)


  limit = 0.98
  if certainty>limit:
    if(fen_observation=='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
      print('New game as White')
      player_color = 'w'
      turn = 'w'
      fens_list = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR']
      tmp_obs = []
      
    if(fen_observation=='RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr'):
      print('New game as Black')
      player_color = 'b'
      turn = 'w'
      fens_list = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR']
      tmp_obs = []

    if(player_color=='b'):
        fen_observation = fen_observation[::-1]

    tmp_obs.append(fen_observation)

    #Takes num_obs screenshots, gets the fen of each one, and choose the most likely 
    if(len(tmp_obs)>=num_obs):
      count = Counter(tmp_obs)
      fen = max(count.items(), key=operator.itemgetter(1))[0]
      if(fens_list != [] and fen_observation != fens_list[-1] and turn!=player_color):
        fens_list.append(fen_observation)
      tmp_obs = []

#A list which will contains fens in order to decide the real board position 
tmp_obs = []
#The fens that has occurred along the game
fens_list = []
#The actual fen in the board
final_fen = ''
#A dictionary between chess moves and screen coordinates
moves_to_cords_white = None
moves_to_cords_black = None
#Left top corner of the board and right bottom corner of the board
board_cords = None
#Bot's color
player_color = None
#Player's turn
turn = None

engine = chess.engine.SimpleEngine.popen_uci(r'stockfish\stockfish')
#Time to spend thinking about the best move
time_to_think = 0.2
#Numbers of screenshots samples to decide the actual fen of the position
num_obs = 4

def main() -> None:
  global final_fen
  global player_color
  global turn
  global fens_list
  global time_to_think
  global num_obs
  
  #update_screen_cords()
  while True:    
    #To update the board position at screen
    if keyboard.is_pressed('a'):
      print('Set new coordinates for the screenshot')
      update_screen_cords()

    #Pause
    if keyboard.is_pressed('q'):
      print('Pause')
      while True:
        time.sleep(0.1)
        if keyboard.is_pressed('w'):
          print('Continue')
          break
        
    #Exit
    if keyboard.is_pressed('e'):
      print('Exit')
      engine.quit()
      raise SystemExit

    #Change time_to_think
    if keyboard.is_pressed('t'):
      print('Update time_to_think')
      print('Prev time_to_think was: ',time_to_think)
      is_valid = False
      while(is_valid == False):
        try:
          time_to_think = float(input('Introduce new time_to_think: '))
          is_valid = True
        except Exception as e:
          print('Invalid time_to_think value')
        
    #Change num_obs
    if keyboard.is_pressed('y'):
      print('Update num_obs')
      print('Prev num_obs was: ',num_obs)
      is_valid = False
      while(is_valid == False):
        try:
          num_obs = int(input('Introduce new num_obs: '))
          is_valid = True
        except Exception as e:
          print('Invalid num_obs value')        

    #Try to get the board position    
    update_fens_list()

    if(len(fens_list)%2==1):
      turn = 'w'
    else:
      turn = 'b'
      
    #Add to final_fen the castling rights acording to the last fen (fens_list[-1])
    if(turn == player_color):
      castling = ''
      test = fens_list[-1] +' '+'w'+' KQkq - 0 0'
      test_castling_board = chess.Board(test)
      if(test_castling_board.has_kingside_castling_rights(1)):
        castling+='K'
      if(test_castling_board.has_queenside_castling_rights(1)):
        castling+='Q'    
      if(test_castling_board.has_kingside_castling_rights(0)):
        castling+='k'
      if(test_castling_board.has_queenside_castling_rights(0)):
        castling+='q'
      if(castling==''):
        castling='-'
        
      final_fen = fens_list[-1] +' '+turn+' '+castling+' - 0 0'
      board = chess.Board(final_fen)
      
      if(board.is_valid()):
        info = engine.analyse(board, chess.engine.Limit(time=time_to_think))
        move = info['pv'][0].uci()
        board.push(chess.Move.from_uci(move))
        board_fen = board.fen().split(' ')[0]
        fens_list.append(board_fen)
        make_move(move)
      else:
        fens_list.pop()
        print("DEBUG: Invalid FEN")
        print(final_fen)

while True:
  try:
    main()
  except Exception as e:
    print('Board not found')


