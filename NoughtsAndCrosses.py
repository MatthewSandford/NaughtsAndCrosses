from random import randint
import math
import copy

class tree_node:

    def __init__(self,board,ai_char,turn_char):
                
        self.turn_char = turn_char
        self.ai_char = ai_char
        self.board = board
        self.children = {}

    def generate_children(self):

        #Check for victory on board and give a score to the outcome of the game

        if check_winner(self.ai_char,self.board):
            return 10
        elif check_winner(1-self.ai_char,self.board):
            return -10
        else:
            
            #Loop through possilbe moves 
            for i in range(0,len(self.board)):

                if self.board[i] == 2:

                    #Add a new move
                    new_board = copy.deepcopy(self.board)
                    new_board[i] = self.turn_char

                    #Create a new node and add it to the tree whilst also constructing it children
                    #Get a score for the baord
                    node = tree_node(new_board,self.ai_char,1-self.turn_char)                 
                    self.children[node] = node.generate_children()

            #Access the score of current node             
            if len(self.children) != 0:
                
                if self.ai_char == self.turn_char:                   
                    #Our move so pick the best
                    return max(self.children.itervalues())*0.9
                else:                 
                    #Their move so pick the worst  
                    return min(self.children.itervalues())*0.9
            else:
                
                #Draw case so return 0  
                return 0

#Used to update our position in the tree after a player move
def find_move(current_node,board):

    #Loop through children of last board state and find new board state
    for node in current_node.children:
        if node.board == board:
            return node

#Choose the best move                  
def choose_move(node,ai_char):

    #Depending on our character (X,O) find the best score of our children nodes
    if ai_char == 0:      
        maximum = max(list(node.children.values()))
    else:
        maximum = min(list(node.children.values()))
        
    boards = []
    
    #Loop through the child nodes with the "best" score and add them to a "bucket" to choose from
    if ai_char == 0:
        for nodes in node.children:
            if node.children[nodes] == maximum :
                boards.append(nodes.board)

    #Choose on of the best nodes
    return boards[randint(0,len(boards)-1)]

def print_board(board):

    print "-----"

    #Loop through the board and print out relevant characters to screen
    for row in range(0,int(math.sqrt(len(board)))):
        for column in range(0,int(math.sqrt(len(board)))):
            if column == int(math.sqrt(len(board))-1):
                if board[column + 3*row] == 2:
                    print " "
                elif board[column + 3*row] == 1:
                    print "O"
                else:
                    print "X"
            else:
                if board[column + 3*row] == 2:
                    print " ",
                elif board[column + 3*row] == 1:
                    print "O",
                else:
                    print "X",

    print "-----\n"

def check_winner(char,board):

    #Check board for a victory for team using char variable
    if board[0] == char:
        if board[1] == char and board[2] == char:
            return 1
        if board[4] == char and board[8] == char:
            return 1
        if board[3] == char and board[6] == char:
            return 1

    if board[6] == char:
        if board[7] == char and board[8] == char:
            return 1
        if board[4] == char and board[2] == char:
            return 1

    if board[3] == char and board[4] == char and board[5] == char:
         return 1
        
    if board[1] == char and board[4] == char and board[7] == char:
         return 1

    if board[2] == char and board[5] == char and board[8] == char:
         return 1

    return 0

def player_turn(board,player_char):

    move = False

    #Loop until a valid move is input
    while move == False:

        #Get column from user
        column = 3
        while(column > 2 or column < 0):

            column = raw_input("Enter the column you would like to select: ")
            column = int(ord(column[0])-48)

        #Get row from user
        row = 3
        while(row > 2 or row < 0):

            row = raw_input("Enter the row you would like to select: ")
            row = int(ord(row[0])-48)

        #Check for valid move
        if board[column + 3*row] == 2:
        
            board[column + 3*row] = player_char
            move = True

        else:

            print "\nInvalid Move\n"

    print "\nPlayer Turn:"

    return board

def game_finished(board):

    #Check for draw or victory for either team 
    return (2 not in board) or check_winner(1,board) or check_winner(0,board)

def main():

    wins = 0
    losses = 0
    draws = 0

    print "AI warming up..."

    #Generate the board tree 
    board = [2,2,2,2,2,2,2,2,2]
    root = tree_node(board,0,0)
    root.generate_children()

    #Get the number of games the user wishes to play 
    games = 0
    while(games <= 0):

        games = raw_input("How many Games would you like to play? ")
        games = int(games)
        
    #Loop through the number of games to play
    for i in range(0,games):

        print "\n--NEW GAME--"

        #Reset board at start of game and start from the root of our tree
        board = [2,2,2,2,2,2,2,2,2]
        current_node = root

        #Random who starts first
        turn = randint(0,1)

        #Set the players and AIs team character, required for traversal of board tree
        if turn == 0:
            player_char = 0
        else:
            player_char = 1

        #Check the games is not over
        while not game_finished(board):

            #Player turn
            if turn == 0:

                #Call for user input and update board and tree position 
                board = player_turn(board,player_char)
                current_node = find_move(current_node,board)
                
            else:

                print "\nAI Turn:"
                
                #Choose next best move, update current node in tree 
                board = copy.deepcopy(choose_move(current_node,1-player_char))
                current_node = find_move(current_node,board)

            #Toggle turn
            turn = 1 - turn

            print_board(board)    

        #Check the outcome of the game
        if check_winner(player_char,board):
            print "You Win!"
            wins += 1
        elif check_winner(1-player_char,board):
            print "AI Wins!"
            losses += 1
        else:
            print "Draw!"
            draws += 1

    print "Wins:", wins
    print "Draws:", draws
    print "Losses:", losses

if __name__ == '__main__':

    main()

