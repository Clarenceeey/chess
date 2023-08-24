global game_state
global curr_turn
global kings

#to convert letters in chess notation into coordinates
letter_to_coords = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

#to convert coordinates into letters in chess notation
coords_to_letters = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
}

#coords are given by (row, column) in integers


def main():
    global game_state
    global curr_turn
    global kings

    game_log = []

    black_king = King("black", [(0, 4)])
    white_king = King("white", [(7, 4)])

    #Game_state is a list of pieces currently in play 
    #string representation of pieces: (pawn, P) (knight, N) (bishop, B) (rook, R) (queen, Q) (king, K)
    game_state = [Rook("black", [(0, 0)], False), Knight("black", [(0, 1)]), Bishop("black", [(0, 2)]), Queen("black", [(0, 3)]), black_king, Bishop("black", [(0, 5)]), Knight("black", [(0, 6)]), Rook("black", [(0, 7)], False),\
        Pawn("black", [(1, 0)]), Pawn("black", [(1, 1)]), Pawn("black", [(1, 2)]), Pawn("black", [(1, 3)]), Pawn("black", [(1, 4)]), Pawn("black", [(1, 5)]), Pawn("black", [(1, 6)]), Pawn("black", [(1, 7)]),\
        Pawn("white", [(6, 0)]), Pawn("white", [(6, 1)]), Pawn("white", [(6, 2)]), Pawn("white", [(6, 3)]), Pawn("white", [(6, 4)]), Pawn("white", [(6, 5)]), Pawn("white", [(6, 6)]), Pawn("white", [(6, 7)]),\
        Rook("white", [(7, 0)], False), Knight("white", [(7, 1)]), Bishop("white", [(7, 2)]), Queen("white", [(7, 3)]), white_king, Bishop("white", [(7, 5)]), Knight("white", [(7, 6)]), Rook("white", [(7, 7)], False)]

    #dictionary containing the kings of both players so they can be easily accessed
    kings = {
        "white": white_king,
        "black": black_king
    }

    
    #white starts first
    white_turn = True
    curr_turn = "white"

    #print game state at the start
    print_game_state()

    #while game has yet to end
    while is_finished()[0] == False:
        

        output = (False,)
        while output[0] == False:
            user_input = input('What is your next move? (Format: <pieceName><currentPosition>-<destination>)\nType \\help for help or \\resign to resign\n')

            #if output[0] is true, the move has been made. Go to the next player's turn. If output[0] is False, ask the user for input again
            output =  input_is_valid(user_input)

            #print the success/error message before breaking/continuing
            print(output[1])

        #if player resigns, end the game
        if "resigned" in output[1]:
            return
        else:

            #record the move made
            game_log.append(output[1])
        
        #print game state for user to see the board
        print_game_state()

        #swap to next player
        white_turn = not white_turn
        if white_turn:
            curr_turn = "white"
        else:
            curr_turn = "black"
    
    #game has ended, print result
    result_of_game = is_finished()
    print(result_of_game[1])
    return


#Check whether the game has finished, returns a tuple with 2 elements. tpl[0] is a boolean representing if the game is over. If tpl[0] is false, game is not over and tpl[1] is empty.
#If tpl[0] is true, game has ended in either a checkmate or a stalemate. tpl[1] contains the message informing user of the end of the game.
def is_finished():

    #get the king
    king = kings[curr_turn]

    #get the possible tiles the king can move to
    possible_moves = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if king.location[-1][0]+i <0 or king.location[-1][0]+i > 7 or king.location[-1][1]+j < 0 or king.location[-1][1]+j > 7:
                continue
            possible_moves.append((king.location[-1][0]+i, king.location[-1][1]+j))

    
    #see if king can move to a tile. If king can move, it is neither a stalemate nor checkmate
    for i in range(len(possible_moves)):
        if king.is_valid_move(possible_moves[i])[0] == True:
            if king.is_check(king, possible_moves[i])[0] == False:
                return (False,)

    #Save is_check as a variable. under_check[0] is a bool on whether the king is under check. under_check[1] shows the list of pieces checking the king
    under_check, checking_king = king.is_check()

    #if king is under check
    if under_check == True:

        #king has no possible moves, check how many pieces are checking the king
        #if more than 1 piece is checking the king, the game is over
        if len(checking_king) > 1:
            return (True, f"{curr_turn} has been checkmated!")
        
        #if only one piece is checking the king, the player can either take the piece or block
        else:

            #check if piece can be taken
            for piece in game_state:

                #if piece is player's piece and if piece can take the piece checking the king
                if piece.colour == king.colour and piece.is_valid_move(checking_king[0].location[0])[0] == True and type(piece) != King:
                    return (False,)
            
            #piece checking the king cannot be captured, check if any of your pieces can block
            #tiles that your pieces can move to to prevent a check
            tiles_to_block = checking_king[0].in_btw(king.location[0])

            for piece in game_state:
                if piece.colour == king.colour and type(piece) != King:
                    for tile in tiles_to_block:
                        if piece.is_valid_move(tile)[0] == True:
                            return (False,)
            
            #Piece can neither be blocked nor taken. Game is over

            return (True, f"{curr_turn} has been checkmated!")
    
    #king is not under check
    else:

        #Check if there are only 2 pieces left in the game. If rest of game logic is correct, if there are only 2 pieces left, they must be the two kings.
        if len(game_state) == 2:
            return (True, "A stalemate has been reached!")
        
        #if there are more pieces left in the game, check if they can move. Dont need to check for king
        else:
            for piece in game_state:
                if piece.colour == curr_turn and type(piece) != King:

                    #check tiles the piece can move to. if piece can move, it is not a stalemate. Movement returns a list of the tiles the piece can move to if the whole board is empty.
                    #king does not need this method as his movement has been checked already
                    possible_moves = piece.movement()
                    for move in possible_moves:
                        if piece.is_valid_move(move)[0] == True:
                            return (False,)
            
            return (True, "A stalemate has been reached!")

    

#check which piece is at the given tile
def at_des(destination):
    for piece in game_state:
        if piece.location[-1] == destination:
            return piece
    return False



#takes in the user input, outputs a tpl. tpl[0] is validity of input. If valid, tpl[1] shows which piece moves to what tile and what piece (if any) is captured. If invalid, tpl[1] contains error message
def input_is_valid(user_input): 

    #if user_input is not empty
    if user_input == "":
        return (False, "Cannot input an empty string")

    #if user asks for help
    if user_input == "\\help":
        print("To move pawn from e2 to e4, type 'e2-e4'. Each move should have either 5 or 6 characters; 5 characters for moving pawns, 6 characters for moving other pieces. \n\
The letters for the pieces are: \nK for king \nQ for queen \nR for rook \nN for knight \nB for bishop \nNo letters are required for pawns. \n\
Here are the commands for some moves you may make: \nc7-c6 (Caro-Kann defense) \nKe1-g1 (king side castling)\ne7-e8 (White pawn promoting. You will be prompted to indicate what you want your pawn to promote to.)")
        
        #return False so that the while loop will continue instead of going to move the piece
        return (False, "Please input a move")
    
    #if user resigns
    if user_input == "\\resign":
        return (True, f"{curr_turn} has resigned")
    
    #if user is trying to move a piece that is not a pawn
    if 65<=ord(user_input[0])<= 90:

        #user input should have 6 characters if moving non-pawn pieces, if not it is not a valid move
        if len(user_input) == 6:
            moving_piece = user_input[0]

            #check whether tiles given are within a chess board
            if ord(user_input[1]) < 97 or ord(user_input[1])> 104 or ord(user_input[-2]) < 97 or ord(user_input[-2])> 104:
                return (False, "Move given is outside a chessboard.")
            
            if int(user_input[2]) < 1 or int(user_input[2]) > 8 or int(user_input[-1]) < 1 or int(user_input[-1]) > 8:
                return (False, "Move given is outside a chessboard.")

            #tiles user gave are valid
            from_tile = (8-int(user_input[2]), letter_to_coords[user_input[1]])
            
        else:
            return (False, "Invalid move")
    else:
        #if moving pawn, the first character should be between a and h and length of user_input should be 5 characters
        #set the moving_piece variable as "P", the string representation of pawn
        #check if tiles user gave are within a chessboard
        if (97<=ord(user_input[0])<= 104 and 97<=ord(user_input[3])<= 104) and (1<= int(user_input[1]) <= 8 and 1<= int(user_input[4]) <= 8) and len(user_input) == 5:
            moving_piece = "P"
            from_tile = (8-int(user_input[1]), letter_to_coords[user_input[0]])
        else:
            return (False, "Invalid move")
    
    #check if piece on from tile is piece that user wants to move
    from_piece = at_des(from_tile)

    #if there is nothing at the from_tile, return False
    if from_piece == False:
        return (False, "There is nothing on that tile")
    else:

        #if the piece at the from_tile is not current player's piece, return False
        if curr_turn != from_piece.colour:
             return (False, "Piece that you want to move is not your piece")
        
        #if piece at from tile is current player's piece
        else:
            
            #if piece at from_tile is not the piece the player wants to move, return False
            if moving_piece not in from_piece.getPiece():
                return (False, f"You want to move a {moving_piece}, but piece on tile is {from_piece.getPiece}.")
            
    #now can safely use from_piece as the object of the piece the user wants to move


    #tile that piece will move to
    destination_tile = (8-int(user_input[-1]), letter_to_coords[user_input[-2]])


    #method return (True,) if move is valid, or (False, string on why move is invalid)
    valid_move = from_piece.is_valid_move(destination_tile)
    
    

    #check if the destination is a valid move and whether the current player's king will be under check after the move is made
    if valid_move[0] == True:
        destination_coord = user_input[-2] + user_input[-1]

        try:
            if "Castling succcessful" == valid_move[1]:
                from_piece.move(destination_tile)
                rook_piece = at_des(valid_move[2])
                rook_piece.move(valid_move[3])
                return (True, "O-O")
        except:
            pass

        under_check = kings[curr_turn].is_check(from_piece, destination_tile)
        if under_check[0] == False:
            try:
                if valid_move[1] == "promotion":
                    while True:
                        promoting_to = input("What do you want to promote your pawn to? \n")
                        if promoting_to == "Q":
                            game_state.append(Queen(curr_turn, [destination_tile]))
                            break
                        elif promoting_to == "R":
                            game_state.append(Rook(curr_turn, [destination_tile], True))
                            break
                        elif promoting_to == "N":
                            game_state.append(Knight(curr_turn, [destination_tile]))
                            break
                        elif promoting_to == "B":
                            game_state.append(Bishop(curr_turn, [destination_tile]))
                            break
                    
                    #piece has been promoted. Remove the pawn and return
                    game_state.remove(from_piece)
                    return (True, destination_coord + promoting_to)
            except:
                pass

            captured_piece = at_des(destination_tile)
            from_piece.move(destination_tile)
            if captured_piece == False:
                if moving_piece != "P":
                    return (True, moving_piece + destination_coord)
                else:
                    return (True, destination_coord)
            else:
                if moving_piece != "P":
                    return (True, moving_piece + 'x' + destination_coord)
                else:
                    return (True, user_input[0] + 'x' + destination_coord)
        else:
            return (False, f"King is still under check if move {user_input} is made.")
    
    #if move is invalid, return False and error message
    else:
        return valid_move
                    


#it is finally time to create the classes for each piece

class Piece(object):

    def __init__(self, colour, location):

        #colour of piece
        self.colour = colour

        #location of piece as a list of coordinates. This is because when implementing the is_valid_move, I advance the game state by appending the new location of the tile(s) and seeing if the user is under check. 
        # If yes, revert back and return invalid move. If not, update the game_state by removing previous location and returning valid move
        self.location = location

    #updates the game state
    def move(self, destination):
        
        #if there is a piece at the destination, it will be captured
        for piece in game_state:
            if piece.location[0] == destination:
                game_state.remove(piece)

        #move current piece to the destination
        self.location[0] = destination



class King(Piece):

    #king has extra attribute has_moved. It is used to determine whether the king can undergo castling
    def __init__(self, colour, location):
        super().__init__(colour, location)
        self.has_moved = False

    #has_moved becomes true once the king has made a move
    def move(self, destination):
        super().move(destination)
        self.has_moved = True



    def is_valid_move(self, destination):

        #king can only move one tile. If the max drow or dcolumn is more than 1, the king cannot move there UNLESS castling is taking place
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]
        chess_notation = coords_to_letters[destination[1]] + str(8-destination[0])
        if max(abs(drow), abs(dcolumn)) != 1:
            if self.has_moved == True:
                return (False, f"The king cannot move to tile {chess_notation}.")
            
            #King has not moved. Check all the possible cases for castling (only 4 cases) 
            else:

                
                #castling can only happen on the row the king is on 
                castle_row = destination[0]

                #If white, castling only occurs at the bottom. If black, it occurs at the top
                if self.colour == "white":
                    if castle_row != 7:
                        return (False, f"King cannot move to tile {chess_notation}.")
                else:
                    if castle_row != 0:
                        return (False, f"King cannot move to tile {chess_notation}")

                
                
                #If king is moving to column 6, it is king side castling. If king is moving to column 2, it is queen side.
                #Tuple[:-1] contains columns to check for opponent pieces threatening. tuple[-1] is the tile of the rook
                if destination[1] == 6:
                    castle_columns = (5, 6, 7)
                elif destination[1] == 2:
                    castle_columns = (3, 2, 1, 0)
                else:
                    return (False, f"King cannot move to tile {chess_notation}")

                #confirmed that the tile is a valid castle tile. Check for conditions for castling
                #king is under check, castling cannnot happen
                if self.is_check()[0] == True:
                    return (False, "Castling cannot occur as king is under check.")

                #check for rook
                rook_piece = at_des((castle_row, castle_columns[-1]))
                if type(rook_piece) != Rook:
                    return (False, f"The king cannot move to tile {destination}.")
                
                #if there is a rook, check if it has moved
                else:
                    if rook_piece.has_moved == True:
                        return (False, "Castling cannot occur as rook has moved.")
                    #else, check if any pieces are between king and rook
                    else:
                        #castle_columns[:-1] are the column coordinates between the king and the rook
                        for column_coord in castle_columns[:-1]:
                            if at_des((castle_row, column_coord)) != False:
                                return (False, "Castling cannot occur as there are pieces between king and rook.")
                        
                        #there are no tiles between king and rook. check if tiles are under opponent influence
                        for piece in game_state:
                            if piece.colour != self.colour:
                                for column_coord in castle_columns[:-1]:
                                    if piece.is_valid_move([castle_row, column_coord])[0] == True:
                                        return (False, "Castling cannot occur as king crosses over tiles that are being attacked.")
                        
                        #king not crossing tiles under threat. Castling can take place. Second last tuple returns tile that rook is on. Last tuple returns the tile the rook moves to
                        return (True, "Castling succcessful", (castle_row, castle_columns[-1]), (castle_row, castle_columns[0]))



        else:
            #king can move to that tile. Check if there is a piece on that tile. If there is, ensure that it is not the current player's tile.

            
            for piece in game_state:
                if piece.location[-1] == destination:
                    if piece.colour == self.colour:
                        return  (False, f"The piece on the destination tile, {piece.getPiece()}, is your own piece")
                    else:
                        captured_piece = piece
            

            #check if a opponent king is adjacent to destination (not checked for under is_check)
            for colour in kings:
                if colour != self.colour:
                    opponent_king = kings[colour]
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if opponent_king.location[-1] == (destination[0] + i, destination[1] + j):
                        return (False, f"The king will be adjacent to the opponent king if it goes to {chess_notation}")
                    



            #confirmed that king can move to that tile
            return (True,)
    
    #there can be no tile in between the king and a destination because the king can only move 1 tile
    def in_btw():
        return []
    
    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wK"
        else:
            return "bK"
        

    #An important function, checks whether the king is under check. If no arguments are given, it will check whether the king is under check in the current game state.
    #If arguments are given, they will be in the order of (piece that is going to move, destination). This function temporarily updates the game state and checks if the king will be under check.
    def is_check(self, *args):

        pieces_checking_king = []
        piece_to_move = None
        piece_captured = None
        #checking for check in updated game state. Update the game state temporarily
        if args != ():
            piece_to_move = args[0]
            destination = args[1]
            piece_to_move.location.append(destination)
            for piece in game_state:
                if piece.location[0] == destination:
                    piece_captured = piece
                    piece.location.append(None)
                    break
        
        #now we can check if king is under check. Omit if piece is king because it will cause infinite recursion. Please sos
        for piece in game_state:
            if piece.colour != self.colour and piece.location[-1] != None and type(piece) != King:
                if piece.is_valid_move(self.location[-1])[0]:
                    pieces_checking_king.append(piece)
        
        if args != ():
            piece_to_move.location.pop()
            if piece_captured != None:
                piece_captured.location.pop()

        if pieces_checking_king == []:
            return (False, pieces_checking_king)
        else:
            return (True, pieces_checking_king)
        


class Queen(Piece):

    #accepts a destination, returns (True,) if move is valid, or (False, string on why move is invalid)
    def is_valid_move(self, destination):

        #if destination is right next to the piece or is inaccesible by queen, tiles_inbetween will be empty 
        tiles_inbetween = self.in_btw(destination)
        if tiles_inbetween == []:
            drow = self.location[-1][0] - destination[0]
            dcolumn = self.location[-1][1] - destination[1]
            #if destination is also not right next to queen, destination tile can not be moved to by the queen.
            if max(abs(drow), abs(dcolumn)) != 1:
                return (False, f"The queen cannot move to tile {destination}.")
            
        #Confirmed that destination tile can be moved to by the queen. Now check if there are any pieces in between queen and destination.
        for tile in tiles_inbetween:
            for piece in game_state:
                if piece.location[-1] == tile:
                    chess_notation = coords_to_letters[tile[1]] + str(8-tile[0])
                    return (False, f"There is a tile at {chess_notation} that is blocking the queen.")
        
        #Confirmed that there are no tiles between the queen and the destination.


        #captured_piece = None

        #Check if piece at destination belongs to the current player or the opponent. If it belongs to the current player, return False. Else, remember that tile. 
        #Assuming rest of game logic is correct, there should only be one piece on each tile.
        for piece in game_state:
            if piece.location[-1] == destination:
                if piece.colour == self.colour:
                    return (False, f"The piece on the destination tile, {piece.getPiece()}, is your own piece")
                else:
                    captured_piece = piece
        
        #Now, it is confirmed that the queen can indeed move to the destination. Return True
        
        return (True,)


        # 
        # Update the game state and check if the king is under check after this move is made.

        # self.location.append(destination)
        # if captured_piece != None:
        #     captured_piece.location.append(None)
        
        # #get the current player's king
        # king = kings[curr_turn]

        # #checker is a tuple. tpl[0] is a boolean on whether the king is under check. tpl[1] contains the pieces checking the king.
        # checker = king.is_check()

        # #After checking if the king is under check after this move, delete the new game state to prevent making any changes, regardless of the result. Only the move method should update the game_state.
        # self.location.pop(-1)
        # if captured_piece != None:
        #     captured_piece.location.pop(-1)

        # #if king is not under check, return True. 
        # if checker[0] == False:
        #     return (True,)
        
        # #king is under check after this move is made. This means the move is invalid
        # else:
        #     return (False, f"The king will be under check if this move is made. Please make another move.")


    def movement(self):
        
        res = []
        row = self.location[-1][0]
        column = self.location[-1][1]
        #queen can at most move 7 tiles
        for i in range(1, 8):


            if 0<= row + i <= 7:
                #queen goes downwards
                res.append((row+i, column))
                if 0 <= column + i <= 7:
                    #queen goes down right
                    res.append((row+i, column+i))
                if 0 <= column - i <= 7:
                    #queen goes down left
                    res.append((row+i, column-i))
            if 0 <= row - i <= 7:
                #queen goes upwards
                res.append((row-i, column))
                if 0 <= column + i <= 7:
                    #queen goes up right
                    res.append((row-i, column+i))
                if 0 <= column - i <= 7:
                    #queen goes up left
                    res.append((row-i, column-i))

            if 0 <= column - i <= 7:
                #queen goes leftwards
                res.append((row, column-1))
            if 0 <= column + i <= 7:
                #queen goes rightwards
                res.append((row, column+i))
        
        return res





    #check for tiles in between the queen and the destination. Checks for horizontal, vertical and diagonal movement
    def in_btw(self, destination):
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]
        res = []

        #this piece and destination are side by side
        if max(abs(drow), abs(dcolumn)) == 1:
            return res
        
        #moving vertically
        if drow != 0:
            
            #moving horizontally
            if dcolumn != 0:
                
                #not diagonal movement
                if abs(drow) != abs(dcolumn):
                    #not horizontal, veritcal or diagonal movement
                    return res
        
        #not moving vertically, means only horizontal movement
        if drow == 0:
            if dcolumn > 0:
                for i in range(1, dcolumn):
                    res.append((destination[0], destination[1]+i))
            else:
                for i in range(1, abs(dcolumn)):
                    res.append((destination[0], destination[1]-i))
            return res
        
        #not moving horizontally, means only vertical movement 
        elif dcolumn == 0:
            if drow > 0:
                for i in range(1, drow):
                    res.append((destination[0]+i, destination[1]))
            else:
                for i in range(1, abs(drow)):
                    res.append((destination[0]-i, destination[1]))
            return res
        
        #diagonal movement
        else:

            #if drow and dcolumn have the same sign, we can start from the top left and proceed to the bottom right
            if (drow<0 and dcolumn<0) or (drow>0 and dcolumn>0):
                if drow<0 and dcolumn<0:
                    start_coord = (self.location[-1][0], self.location[-1][1])
                if drow>0 and dcolumn>0:
                    start_coord = (destination[0], destination[1])
                
                for i in range(1, abs(drow)):
                    res.append((start_coord[0] + i, start_coord[1] + i))
            
            #if drow and dcolumn have different signs, start from the bottom left and proceed to the top right
            else:
                if drow < 0:
                    start_coord = (destination[0], destination[1])
                else:
                    start_coord = (self.location[-1][0], self.location[-1][1])
                for i in range(1, abs(drow)):
                    res.append((start_coord[0] - i, start_coord[1] + i))
            
            return res
        

    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wQ"
        else:
            return "bQ"



class Rook(Piece):
    #rook has extra attribute has_moved. It is used to determine whether the rook can undergo castling
    def __init__(self, colour, location, has_moved):
        super().__init__(colour, location)
        self.has_moved = has_moved

    #has_moved becomes true once the rook has made a move
    def move(self, destination):
        super().move(destination)
        self.has_moved = True

    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wR"
        else:
            return "bR"
        
    #check for tiles in between the rook and the destination. Checks for horizontal and vertical movement
    def in_btw(self, destination):
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]
        res = []

        #this piece and destination are side by side
        if max(abs(drow), abs(dcolumn)) == 1:
            return res
        
        #not moving in cross
        if drow != 0 and dcolumn != 0:
            return res
        
        #not moving vertically, means only horizontal movement
        if drow == 0:
            if dcolumn > 0:
                for i in range(1, dcolumn):
                    res.append((destination[0], destination[1]+i))
            else:
                for i in range(1, abs(dcolumn)):
                    res.append((destination[0], destination[1]-i))
            return res
        
        #not moving horizontally, means only vertical movement 
        else:
            if drow > 0:
                for i in range(1, drow):
                    res.append((destination[0]+i, destination[1]))
            else:
                for i in range(1, abs(drow)):
                    res.append((destination[0]-i, destination[1]))
            return res
        


    def movement(self):
        
        res = []
        row = self.location[-1][0]
        column = self.location[-1][1]
        #rook can at most move 7 tiles
        for i in range(1, 8):
            if 0<= row + i <= 7:
                #rook goes downwards
                res.append((row+i, column))
            if 0 <= row - i <= 7:
                #rook goes upwards
                res.append((row-i, column))
            if 0 <= column - i <= 7:
                #rook goes leftwards
                res.append((row, column-1))
            if 0 <= column + i <= 7:
                #rook goes rightwards
                res.append((row, column+i))
        
        return res

    #accepts a destination, returns (True,) if move is valid, or (False, string on why move is invalid)
    def is_valid_move(self, destination):

        destination_chess_notation = coords_to_letters[destination[1]] + str(8-destination[0])

        #if destination is right next to the piece or is inaccesible by rook, tiles_inbetween will be empty 
        tiles_inbetween = self.in_btw(destination)
        if tiles_inbetween == []:
            drow = self.location[-1][0] - destination[0]
            dcolumn = self.location[-1][1] - destination[1]
            #if destination is neither on the same row or column as rook, that tile is inaccesible to the rook.
            if drow != 0 and dcolumn != 0:
                return (False, f"The rook cannot move to tile {destination_chess_notation}.")
            
        #Confirmed that destination tile can be moved to by the rook. Now check if there are any pieces in between rook and destination.
        for tile in tiles_inbetween:
            for piece in game_state:
                if piece.location[-1] == tile:
                    chess_notation = coords_to_letters[tile[1]] + str(8-tile[0])
                    return (False, f"There is a tile at {chess_notation} that is blocking the rook.")
        
        #Confirmed that there are no tiles between the rook and the destination.


        #captured_piece = None

        #Check if piece at destination belongs to the current player or the opponent. If it belongs to the current player, return False. Else, remember that tile. 
        #Assuming rest of game logic is correct, there should only be one piece on each tile.
        for piece in game_state:
            if piece.location[-1] == destination:
                if piece.colour == self.colour:
                    return (False, f"The piece on the destination tile, {piece.getPiece()}, is your own piece")
                else:
                    captured_piece = piece
        
        #Now, it is confirmed that the rook can indeed move to the destination. Return True
        
        return (True,)
        


class Bishop(Piece):

    #check for tiles in between the bishop and the destination. Checks for diagonal movement
    def in_btw(self, destination):
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]
        res = []

        #this piece and destination are side by side
        if max(abs(drow), abs(dcolumn)) == 1:
            return res
        
        #if not diagonal movement, return nothing
        if abs(drow) != abs(dcolumn):
            return res

        #if drow and dcolumn have the same sign, we can start from the top left and proceed to the bottom right
        if (drow<0 and dcolumn<0) or (drow>0 and dcolumn>0):
            if drow<0 and dcolumn<0:
                start_coord = (self.location[-1][0], self.location[-1][1])
            if drow>0 and dcolumn>0:
                start_coord = (destination[0], destination[1])
            
            for i in range(1, abs(drow)):
                res.append((start_coord[0] + i, start_coord[1] + i))
        
        #if drow and dcolumn have different signs, start from the bottom left and proceed to the top right
        else:
            if drow < 0:
                start_coord = (destination[0], destination[1])
            else:
                start_coord = (self.location[-1][0], self.location[-1][1])
            for i in range(1, abs(drow)):
                res.append((start_coord[0] - i, start_coord[1] + i))
        
        return res
            
    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wB"
        else:
            return "bB"
        

    def movement(self):
        
        res = []
        row = self.location[-1][0]
        column = self.location[-1][1]
        #bishop can at most move 7 tiles
        for i in range(1, 8):


            if 0<= row + i <= 7:
                if 0 <= column + i <= 7:
                    #bishop goes down right
                    res.append((row+i, column+i))
                if 0 <= column - i <= 7:
                    #bishop goes down left
                    res.append((row+i, column-i))
            if 0 <= row - i <= 7:
                if 0 <= column + i <= 7:
                    #bishop goes up right
                    res.append((row-i, column+i))
                if 0 <= column - i <= 7:
                    #bishop goes up left
                    res.append((row-i, column-i))

            
        return res


    #accepts a destination, returns (True,) if move is valid, or (False, string on why move is invalid)
    def is_valid_move(self, destination):

        #if destination is right next to the piece or is inaccesible by bishop, tiles_inbetween will be empty 
        tiles_inbetween = self.in_btw(destination)
        

        if tiles_inbetween == []:
            drow = self.location[-1][0] - destination[0]
            dcolumn = self.location[-1][1] - destination[1]

            #if tile is not diagonal to bishop, it is invalid
            if abs(drow) != abs(dcolumn):
                return (False, f"The bishop cannot move to tile {destination}.")
            
        #Confirmed that destination tile can be moved to by the bishop. Now check if there are any pieces in between bishop and destination.
        for tile in tiles_inbetween:
            for piece in game_state:
                if piece.location[-1] == tile:
                    chess_notation = coords_to_letters[tile[1]] + str(8-tile[0])
                    return (False, f"There is a tile at {chess_notation} that is blocking the bishop.")
        
        #Confirmed that there are no tiles between the bishop and the destination.


        #captured_piece = None

        #Check if piece at destination belongs to the current player or the opponent. If it belongs to the current player, return False. Else, remember that tile. 
        #Assuming rest of game logic is correct, there should only be one piece on each tile.
        for piece in game_state:
            if piece.location[-1] == destination:
                if piece.colour == self.colour:
                    return (False, f"The piece on the destination tile, {piece.getPiece()}, is your own piece")
                else:
                    captured_piece = piece
        
        #Now, it is confirmed that the bishop can indeed move to the destination. Return True
        
        return (True,)



class Knight(Piece):

    #no pieces can come between knight and a tile
    def in_btw(self, destination):
        return []
    
    #accepts a destination, returns (True,) if move is valid, or (False, string on why move is invalid)
    def is_valid_move(self, destination):
        
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]

        #check if knight is moving in an L shape
        if max(abs(drow), abs(dcolumn)) != 2 or min(abs(drow), abs(dcolumn)) != 1:
            return (False, f"The knight cannot move to tile {destination}.")
        
        #knight is indeed moving in an L shape

        #captured_piece = None

        #Check if piece at destination belongs to the current player or the opponent. If it belongs to the current player, return False. Else, remember that tile. 
        #Assuming rest of game logic is correct, there should only be one piece on each tile.
        for piece in game_state:
            if piece.location[-1] == destination:
                if piece.colour == self.colour:
                    return (False, f"The piece on the destination tile, {piece.getPiece()}, is your own piece")
                else:
                    captured_piece = piece
        
        #Now, it is confirmed that the bishop can indeed move to the destination. Return True
        
        return (True,)
    
    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wN"
        else:
            return "bN"

    def movement(self):
        
        res = []
        row = self.location[-1][0]
        column = self.location[-1][1]
        #knight can at most move to 8 tiles

        #row can change from -2, -1, 1, 2
        for drow in range(-2, 3):

            #if the knight cannot go upwards, continue as i increases
            if row + drow < 0 or drow == 0:
                continue

            #if knight cannot go downwards, break as i increases
            if row + drow > 7:
                break

            #if knight moves vertically by 2, it can only move horizontally by 1
            if abs(drow) == 2:
                if 0 <= column -1:
                    res.append((row + drow, column -1))
                if column + 1 <= 7:
                    res.append((row + drow, column +1))

            #if knight moves vertically by 1, it can move horizontally by 2
            else:
                if 0 <= column -2:
                    res.append((row + drow, column -2))
                if column + 2 <= 7:
                    res.append((row + drow, column +2))
        
        return res

class Pawn(Piece):

    #pawn has extra attribute has_moved. It is used to determine whether the pawn can move up 2 tiles
    def __init__(self, colour, location):
        super().__init__(colour, location)
        self.has_moved = False

    #has_moved becomes true once the pawn has made a move
    def move(self, destination):
        super().move(destination)
        self.has_moved = True


    #string representation of this piece
    def getPiece(self):
        if self.colour == "white":
            return "wP"
        else:
            return "bP"
    
    #no pieces can come between pawn and a tile as a pawn can only move one tile
    def in_btw(self, destination):
        return []
    


    def movement(self):
        
        res = []
        row = self.location[-1][0]
        column = self.location[-1][1]

        #white parn moves upwards
        if self.colour == "white":
            if row != 0:
            #moves up by 1, horizontally by either -1, 0 or 1
                for i in range(-1, 2):
                    if 0<= column + i <= 7:
                        res.append((row + 1, column + i)) 
        
        #black pawn moves downwards
        else:
            if row != 7:
                #moves down by 1, horizontally by either -1, 0 or 1
                for i in range(-1, 2):
                    if 0<= column + i <= 7:
                        res.append((row - 1, column + i)) 
        
        return res



    


    def is_valid_move(self, destination):
        drow = self.location[-1][0] - destination[0]
        dcolumn = self.location[-1][1] - destination[1]


        #if pawn is moving, not capturing
        if dcolumn == 0:
            #if pawn has not moved, it can move up 2 tiles
            if self.has_moved == False:
                threshold = 2
            else:
                threshold = 1
            
            #check if pawn can move to destination tile 
            if self.colour == "white":
                in_range = 0<drow<=threshold
            else:
                in_range = -threshold<=drow<0
            
            #if in_range, check if there are any pieces on the destination 
            if in_range:
                for piece in game_state:
                    if piece.location[-1] == destination:
                        return (False, f"The pawn cannot move to tile {destination}.")
                

                #check for promotion
                if self.colour == "white":
                    end_row = 0
                else:
                    end_row = 7
                
                #if promotion available, return message so that if after the move the king is not under check, the promotion can occur
                if destination[0] == end_row:
                    return (True, "promotion")
                else:
                    return (True,)
            
            else:
                return (False, f"The pawn cannot move to tile {destination}.")
        
        #pawn is capturing, can only go one tile diagonally upwards/downwards (can be both left or right)
        else:
            if abs(dcolumn) != 1:
                return (False, f"The pawn cannot move to tile {destination}.")
            else:
                if self.colour == "white":
                    in_range = 0<drow<=1
                else:
                    in_range = -1<=drow<0
                
                #if going only 1 tile diagonally up/down, check that there is a piece on the destination for the pawn to capture 
                if in_range:
                    for piece in game_state:
                        if piece.location[-1] == destination:
                            if piece.colour != self.colour:
                                return (True,)
                            else:
                                break
                    return (False, f"There is no piece at {destination} that can be captured.")

                else:
                    return (False, f"The pawn cannot move to tile {destination}.")

       


def print_game_state():

    #create an 8x8 matrix
    row = ["  "] * 8
    game_state_lst = []
    for i in range(8):
        game_state_lst.append(row.copy())
    
    #add the pieces in
    for piece in game_state:
        coords = piece.location[-1]
        game_state_lst[coords[0]][coords[1]] = piece.getPiece()
    
    #print the rows one by one
    for i in range(8):
        print(game_state_lst[i])
    

main()