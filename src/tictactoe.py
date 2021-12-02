import re, random;

class TicTacToe:
    humanSign: str = 'X';
    aiSign: str = 'O';
    gameboard: list[int | str] = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    difficulty: str;

    def __init__(self, difficulty: str) -> None:
        self.difficulty = difficulty;

    #Method used to start the game
    def newGame(self, human: bool) -> None:
        if human: 
            self.humanMove(input('Starting New Game...\nYou will be going first. Your sign is "X"!\n\nPlacement: '));
        else:
            print('Starting New Game...\nThe AI will be going first!');
            self.aiMove();

    #Method used to render the tic-tac-toe board in a string
    def drawboard(self) -> str:
        board = '';
        for y in range(3):
            for x in range(3):
                index = str(self.gameboard[y * 3 + x]);
                board += f"| {(re.sub('^[0-9]+$', ' ', index) or index)} ";
            board += '|\n';
        return board;

    #Get the human move
    def humanMove(self, inputPlacement: str) -> None:
        #Check if they gave a valid position
        if not re.match('^[1-9]+$', inputPlacement): 
            self.humanMove(input('Please type a valid number between 1-9, which will be the placement for your next move!\nPlacement: '));
        else:
            #Check if the position is taken 
            if type(self.gameboard[int(inputPlacement) - 1]) == str:
                return self.humanMove(input('That position is already taken!\nPlacement: '));

            #Place at the position
            self.gameboard[int(inputPlacement) - 1] = self.humanSign;
            #Check if the player won or its a draw
            if self.winCheck(self.gameboard, self.humanSign): return self.gameOver('win');
            elif self.drawCheck(self.gameboard): return self.gameOver('draw');

            #Ai's turn now
            self.aiMove();

    def aiMove(self):
        aiPos: int;
        #Ai's turn depending on the difficulty
        if self.difficulty == 'e':
            aiPos = self.emptySpot(self.gameboard, True);
        elif self.difficulty == 'h':
            aiPos = self.miniMax(self.gameboard, self.aiSign)['index'];
        self.gameboard[aiPos] = self.aiSign;

        #Check if the Ai won or its a draw
        if self.winCheck(self.gameboard, self.aiSign): return self.gameOver('lost');
        elif self.drawCheck(self.gameboard): return self.gameOver('draw');

        print(f"\nThe AI has placed at position {aiPos + 1}...\n\n{self.drawboard()}");
        #Users turn if it came this far
        self.humanMove(input('Placement: '));

    #Method to get all the empty spot
    def emptySpot(self, board: list, randomElement: bool) -> list[int]:
        filtered = [num for num in board if isinstance(num, (int, float))];
        if(randomElement): return random.choice(filtered);
        return filtered;

    #Method to check for win
    def winCheck(self, board: list, sign: str) -> bool:
        combos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
        for index in combos:
            [pos1, pos2, pos3] = index;
            spot1 = str(board[pos1]);
            spot2 = str(board[pos2]);
            spot3 = str(board[pos3]);
            if spot1 == sign and spot1 and spot1 == spot2 and spot1 == spot3:
                return True;
        return False;

    #Method to check for draw
    def drawCheck(self, board: list) -> bool:
        return not any(isinstance(item, int) for item in board);

    #Method to broadcast depending on the game result
    def gameOver(self, option: str) -> None:
        print('\n');
        if option == 'win':
            print('You have WON the match against the AI!');
        elif option == 'lost':
            print('You have LOST the match against the AI!');
        elif option == 'draw':
            print('This match has ended in a draw...');

        print(f"{self.drawboard()}\nNew Game?");
        newGame()

    #Tic-Tac-Toe AI method
    def miniMax(self, board: list, sign: str):
        emptySpots = self.emptySpot(board, False);

        if self.winCheck(board, self.humanSign): return { "score": -1 };
        elif self.winCheck(board, self.aiSign): return { "score": 1 };
        elif len(emptySpots) == 0: return { "score": 0 };

        collectedMoves = [];
        for i in range(len(emptySpots)):
            move = {};
            move['index'] = board[emptySpots[i]];
            board[emptySpots[i]] = sign;

            if(sign == self.aiSign):
                if(self.winCheck(board, self.aiSign)):
                    move['score'] = 1;
                    board[emptySpots[i]] = move['index'];
                    return move;
                result = self.miniMax(board, self.humanSign);
                move['score'] = result['score'];
            else:
                result = self.miniMax(board, self.aiSign);
                move['score'] = result['score'];

            board[emptySpots[i]] = move['index'];
            collectedMoves.append(move);

        bestMove = None;
        if(sign == self.aiSign):
            bestScore = float('-inf');
            for i in range(len(emptySpots)):
                if collectedMoves[i]['score'] > bestScore:
                    bestScore = collectedMoves[i]['score'];
                    bestMove = i;
        else:
            bestScore = float('inf');
            for i in range(len(emptySpots)):
                if collectedMoves[i]['score'] < bestScore:
                    bestScore = collectedMoves[i]['score'];
                    bestMove = i;

        return collectedMoves[bestMove];

difficultyList = ['easy', 'e', 'hard', 'h'];

def getDifficulty() -> str:
    difficulty = input('Choose between the difficulties "easy", and "hard": ').lower();
    if difficulty not in difficultyList: return getDifficulty()
    else: return difficulty[0];

def newGame() -> None:
    TicTacToe(getDifficulty()).newGame(random.random() <= 0.5);
#Just starting the game
newGame();