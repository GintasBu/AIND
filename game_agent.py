"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2*opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    booster=0
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    if game.move_count>(game.width)*(game.height)/2:
        pref_moves=list(set(own_moves) & set(opp_moves))
        if len(pref_moves):
            booster=1
    return float(len(own_moves) - 2*len(opp_moves)+8*booster)    # favors moves that limit opponent's choice


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    occupied_neighbors_amount=0
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if game.move_count<(game.width-4)*(game.height-4)*2:  #len(list(not_empty))<game.width*game.height/2:
        #for move in own_moves:
        x,y=game.get_player_location(player)
        if x==0: xx=[0,1]
        elif x==game.width-1: xx=[game.width-2, game.width-1]
        else: xx=[x-1,x,x+1]
        if y==0: yy=[0,1]
        elif y==game.height-1: yy=[game.height-2, game.height-1]
        else: yy=[y-1,y,y+1]
        non_empty=[(i, j) for i in xx for j in yy if game._board_state[i + j * game.height] != 0]
        non_empty.remove((x,y))#print((x,y), game._board_state)
        occupied_neighbors_amount=len(non_empty) # non-empty spaces
        #neighbors=set([(i,j) for i in xx for j in yy ])
        #occupied_neighbors_amount=len(list(set(not_empty) & set(neighbors)))
    else:
        if len(opp_moves)==1 and opp_moves[0] in own_moves: occupied_neighbors_amount=float('inf')
        
    return float(len(own_moves) - len(opp_moves)+6*occupied_neighbors_amount)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves=game.get_legal_moves(self)


        if len(legal_moves):
            _, move=max([(self.score(game.forecast_move(m), self),m) for m in legal_moves])#argmax for scores at last depth
            best_move= move
        else: best_move=(-1,-1)
            #best_move=(-1,-1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move=self.minimax(game, self.search_depth)
            return best_move
        except SearchTimeout:
            print('minimax timeout') #pass #return best_move #return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        #return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
    #def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth<1: raise Exception('Too small depth')
        legal_moves=game.get_legal_moves(self) 
        if len(legal_moves)==0:
            return (-1,-1)
        if depth==1:   # at depth=1
            _, move=max([(self.score(game.forecast_move(m), self),m) for m in legal_moves])#argmax for scores at last depth
            return move
        else:
            _, move=max([(self.min_value(game.forecast_move(m), depth-1),m) for m in legal_moves]) # argmax for recursive calls 
            return move
                
    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()	
        if len(game.get_legal_moves(self))==0:
            return self.score(game, self)
        if depth:
            v=float('-inf')
            for a in game.get_legal_moves(self):
                v=max(v, self.min_value(game.forecast_move(a), depth-1))
            return v
        else: return self.score(game, self)

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if len(game.get_legal_moves(game.get_opponent(self)))==0:
            return self.score(game, game.get_opponent(self))
        if depth:
            v=float('inf')
            for a in game.get_legal_moves(game.get_opponent(self)):
                v=min(v, self.max_value(game.forecast_move(a), depth-1))
            return v
        else: return self.score(game, self)

class AlphaBetaPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        legal_moves=game.get_legal_moves(self)
        if len(legal_moves):
            _, move=max([(self.score(game.forecast_move(m), self),m) for m in legal_moves])#argmax for scores at last depth
            best_move= move
        else: 
            best_move=(-1,-1)
            return best_move

        try:
            for self.search_depth in range(1, game.height*game.width+1):
                #print(self.search_depth , '1')                
                best_move=self.alphabeta(game, self.search_depth)

                #return result
        except SearchTimeout:
            pass 
        #print (result, depth)
        return best_move



		#try:
        #    for self.search_depth in range(1, game.height*game.width+1):
        #        best_move=self.alphabeta(game, self.search_depth)
        #        print(best_move, self.search_depth)
        #        return best_move				
        #except SearchTimeout:
        #    pass 





    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        #print(depth, alpha, beta, 'abin')
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth==1:   
            scor, move=max([(self.score(game.forecast_move(m), self),m) for m in game.get_legal_moves(self)])#argmax for scores at last depth
            return move
        else:
            max_v=float('-inf')
            for m in game.get_legal_moves(self):
                v=self.min_value(game.forecast_move(m), depth-1, alpha, beta)
                if v>=max_v:
                    max_v=v
                    best_move=m
                    #return best_move
                alpha=max(alpha, v)
            return best_move

                
    def max_value(self, game, depth, alpha, beta):
        #print(depth, 'max', alpha, beta)
        v=float('-inf')
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()	
        if len(game.get_legal_moves(self))==0:
            return self.score(game, self)
        if depth:
            for a in game.get_legal_moves(self):
                v=max(v, self.min_value(game.forecast_move(a), depth-1, alpha, beta))
                if v>= beta: 
                    #beta=v
                    return v
                alpha=max(alpha, v)
            return v
        else: 
            #scor, move=max([(self.score(game.forecast_move(m), self),m) for m in game.get_legal_moves()])#argmax for scores at last depth
            return self.score(game, self)      

    def min_value(self, game, depth, alpha, beta):
        #print(depth, 'min', alpha, beta)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        v=float('inf')
        if len(game.get_legal_moves(game.get_opponent(self)))==0:
            return self.score(game, self)
        if depth:
            for a in game.get_legal_moves(game.get_opponent(self)):
                v=min(v, self.max_value(game.forecast_move(a), depth-1, alpha, beta))
                if v<=alpha: return v
                beta=min(beta, v)
            return v
        else: 
            return self.score(game, self)
