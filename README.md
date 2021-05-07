# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- simulate games for AI vs AI (apart of `Game` class)
  - file containing matrix where cell I,j = player I wins vs player j
  - scoreboard class has an attribute players= Players()
  - players.add(), player in players, players.add_game(player1, player2, winner), players.get_score(player), players
Get_scoreboard(), players.get_score(player1, player2)
- Set up cnn/RNN/RNN,CNN/Greedy/Greedy+exploit
  - implement `train`, store result in `models/{model}/weights.txt
  - storing these games should be same type as raw_dat_to_board
- Map datapoints to our coordinates
  - `raw_data_to_board` function in `data_extractor.py` -store data in file(`data/` directory)
- implement `trained` by checking for valid `weights.txt` file and initializing `self.predictor`
- implement `predict_move`
- #### MILESTONE 1.5 base smart AI done
- Move w.r.t. various reward functions
- Set up qlearning (links game to models>)
- Train/Test
- IReinfLearn to learn reward
#### MILESTONE 2: **Smart AI done**
- Write monitoring scripts
- Try other networks
- Tweak qlearning rewards

### **Ali**
- unit tests for board and game
- Write actual integration tests (one for why moves needs to be updated after each move)
  - i think it only needs tobe updated before a king moves
- Implement king movement
- enpassant/castle/promote
- check/checkmate
- Something wrong:
  - with the square 0,0
  - pawn capture pawn 2,5 -> 1,6
- write 2 system tests
- implement scoreboard + visualization
- type documentation
- optimizations
  - change coordinate system to 2-digit int
  - remove `if x.is_white: ... else: ...` by inverting board at start/end of code

#### MILESTONE 1: **Done backend**
- Start frontend
- Write Controller to interact Model and View
- Write Buttons for View
#### MILESTONE 2: **Frontend done**
- Optimize backend
- User-friendly Frontend

### **Zuraze**
- Lose to AI

### Project Complete
