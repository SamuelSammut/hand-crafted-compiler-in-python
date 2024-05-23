# Class to wrap the different tokens we'll be using
import string
from enum import Enum


class TokenType(Enum):
    VOID = 1
    END = 2
    WS = 3
    TYPE = 4
    BOOLEAN_LITERAL = 5
    COLOUR_LITERAL = 6
    INTEGER_LITERAL = 7
    FLOAT_LITERAL = 8
    MULTIPLICATIVE_OPERAND = 9
    ADDITIVE_OPERAND = 10
    RELATIONAL_OPERAND = 11
    IDENTIFIER = 12
    EQUALS = 13
    PAD_WIDTH = 14
    PAD_HEIGHT = 15
    PAD_READ = 16
    RANDOM_INT = 17
    PRINT = 18
    DELAY = 19
    WRITE_BOX = 20
    WRITE = 21
    RETURN = 22
    IF = 23
    FOR = 24
    WHILE = 25
    FUN = 26
    LET = 27
    ELSE = 28
    AS = 29
    NOT = 30
    COMMA = 31
    LEFT_SQUARE_BRACKET = 32
    RIGHT_SQUARE_BRACKET = 33
    LEFT_ROUND_BRACKET = 34
    RIGHT_ROUND_BRACKET = 35
    COLON = 36
    SEMI_COLON = 37
    ARROW = 38
    RIGHT_CURLY_BRACKET = 39
    LEFT_CURLY_BRACKET = 40


class Token:
    def __init__(self, t, l):
        self.type = t
        self.lexeme = l


def GetTokenTypeByFinalState(state, lexeme):
    if state == 1:
        return Token(TokenType.WS, lexeme)
    elif state == 2:
        return Token(TokenType.INTEGER_LITERAL, lexeme)
    elif state == 4:
        return Token(TokenType.FLOAT_LITERAL, lexeme)
    elif state == 11:
        return Token(TokenType.COLOUR_LITERAL, lexeme)
    elif state in [16, 19, 23, 29]:
        return Token(TokenType.TYPE, lexeme)
    elif state in [33, 38]:
        return Token(TokenType.BOOLEAN_LITERAL, lexeme)
    elif state in [39, 40, 52]:
        return Token(TokenType.MULTIPLICATIVE_OPERAND, lexeme)
    elif state in [41, 42, 49]:
        return Token(TokenType.ADDITIVE_OPERAND, lexeme)
    elif state in [43, 44, 47]:
        return Token(TokenType.RELATIONAL_OPERAND, lexeme)
    elif state == 45:
        return Token(TokenType.EQUALS, lexeme)
    elif state in [12, 13, 14, 15, 17, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 31, 32, 34, 35, 36, 37, 48, 50, 51, 53,
                   119, 120, 121, 122, 123, 125, 127, 128, 130, 131, 132, 133, 135, 136, 138, 139, 141, 142, 143, 157,
                   158, 160]:
        return Token(TokenType.IDENTIFIER, lexeme)
    elif state == 60:
        return Token(TokenType.PAD_WIDTH, lexeme)
    elif state == 68:
        return Token(TokenType.PAD_HEIGHT, lexeme)
    elif state == 74:
        return Token(TokenType.PAD_READ, lexeme)
    elif state == 86:
        return Token(TokenType.RANDOM_INT, lexeme)
    elif state == 93:
        return Token(TokenType.PRINT, lexeme)
    elif state == 100:
        return Token(TokenType.DELAY, lexeme)
    elif state == 111:
        return Token(TokenType.WRITE_BOX, lexeme)
    elif state == 118:
        return Token(TokenType.WRITE, lexeme)
    elif state == 124:
        return Token(TokenType.RETURN, lexeme)
    elif state == 126:
        return Token(TokenType.IF, lexeme)
    elif state == 129:
        return Token(TokenType.FOR, lexeme)
    elif state == 134:
        return Token(TokenType.WHILE, lexeme)
    elif state == 137:
        return Token(TokenType.FUN, lexeme)
    elif state == 140:
        return Token(TokenType.LET, lexeme)
    elif state == 145:
        return Token(TokenType.ELSE, lexeme)
    elif state == 146:
        return Token(TokenType.COMMA, lexeme)
    elif state == 147:
        return Token(TokenType.LEFT_SQUARE_BRACKET, lexeme)
    elif state == 148:
        return Token(TokenType.RIGHT_SQUARE_BRACKET, lexeme)
    elif state == 149:
        return Token(TokenType.LEFT_ROUND_BRACKET, lexeme)
    elif state == 150:
        return Token(TokenType.RIGHT_ROUND_BRACKET, lexeme)
    elif state == 151:
        return Token(TokenType.COLON, lexeme)
    elif state == 152:
        return Token(TokenType.SEMI_COLON, lexeme)
    elif state == 155:
        return Token(TokenType.LEFT_CURLY_BRACKET, lexeme)
    elif state == 156:
        return Token(TokenType.RIGHT_CURLY_BRACKET, lexeme)
    elif state == 154:
        return Token(TokenType.ARROW, lexeme)
    elif state == 159:
        return Token(TokenType.NOT, lexeme)
    elif state == 161:
        return Token(TokenType.AS, lexeme)


    else:
        return 'default result'


class Lexer:
    def __init__(self):
        self.needed_letters_list = ["a_letter", "b_letter", "c_letter", "d_letter", "e_letter", "f_letter", "g_letter",
                                    "h_letter", "i_letter", "l_letter", "m_letter", "n_letter", "o_letter", "p_letter", "r_letter",
                                    "s_letter", "t_letter",
                                    "u_letter", "w_letter", "x_letter", "y_letter"]
        self.operand_list = ["*", "/", "+", "-", "or", "and", "<", ">", "=", "!"]
        self.symbol_list = ["#", ".", "_", "[", "]", ":", ",", "(", ")", ";", "{", "}"]
        self.lexeme_list = ["letter", "digit", "ws", "type",
                            "other", "as"] + self.needed_letters_list + self.operand_list + self.symbol_list
        self.states_list = [i for i in range(161 + 1)]
        self.states_accp = [1, 2, 4, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60,
                            68, 74, 86, 93, 100, 111, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130,
                            131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 143, 144, 145, 146, 147, 148,
                            149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161]
        self.except_list = self.needed_letters_list + ["_"]
        # All excepts
        self.all_except_a = [letter for letter in self.except_list if letter != 'a_letter']
        self.all_except_l = [letter for letter in self.except_list if letter != 'l_letter']
        self.all_except_n = [letter for letter in self.except_list if letter != 'n_letter']
        self.all_except_o = [letter for letter in self.except_list if letter != 'o_letter']
        self.all_except_r = [letter for letter in self.except_list if letter != 'r_letter']
        self.all_except_t = [letter for letter in self.except_list if letter != 't_letter']
        self.all_except_u = [letter for letter in self.except_list if letter != 'u_letter']
        self.all_except_e = [letter for letter in self.except_list if letter != 'e_letter']
        self.all_except_s = [letter for letter in self.except_list if letter != 's_letter']
        self.all_except_d = [letter for letter in self.except_list if letter != 'd_letter']
        self.all_except_f = [letter for letter in self.except_list if letter != 'f_letter']
        self.all_except_h = [letter for letter in self.except_list if letter != 'h_letter']
        self.all_except_i = [letter for letter in self.except_list if letter != 'i_letter']

        self.rows = len(self.states_list)
        self.cols = len(self.lexeme_list)

        # Let's take integer -1 to represent the error state for this DFA
        self.Tx = [[-1 for j in range(self.cols)] for i in range(self.rows)]
        self.InitialiseTxTable()

    def InitialiseTxTable(self):
        # Update Tx to represent the state transition function of the DFA

        # WS
        self.Tx[0][self.lexeme_list.index("ws")] = 1
        self.Tx[1][self.lexeme_list.index("ws")] = 1

        # Integer and Float Literal
        self.Tx[0][self.lexeme_list.index("digit")] = 2
        self.Tx[2][self.lexeme_list.index("digit")] = 2
        self.Tx[2][self.lexeme_list.index(".")] = 3
        self.Tx[3][self.lexeme_list.index("digit")] = 4
        self.Tx[4][self.lexeme_list.index("digit")] = 4

        # Colour Literal
        self.Tx[0][self.lexeme_list.index("#")] = 5

        # For hexletters
        for hexletter in self.needed_letters_list[0:6]:
            self.Tx[5][self.lexeme_list.index(hexletter)] = 6
            self.Tx[6][self.lexeme_list.index(hexletter)] = 7
            self.Tx[7][self.lexeme_list.index(hexletter)] = 8
            self.Tx[8][self.lexeme_list.index(hexletter)] = 9
            self.Tx[9][self.lexeme_list.index(hexletter)] = 10
            self.Tx[10][self.lexeme_list.index(hexletter)] = 11

        self.Tx[5][self.lexeme_list.index("digit")] = 6
        self.Tx[6][self.lexeme_list.index("digit")] = 7
        self.Tx[7][self.lexeme_list.index("digit")] = 8
        self.Tx[8][self.lexeme_list.index("digit")] = 9
        self.Tx[9][self.lexeme_list.index("digit")] = 10
        self.Tx[10][self.lexeme_list.index("digit")] = 11

        # Types

        # float
        self.Tx[0][self.lexeme_list.index("f_letter")] = 12

        for letter in self.all_except_l:
            self.Tx[12][self.lexeme_list.index(letter)] = 53
        self.Tx[12][self.lexeme_list.index("letter")] = 53
        self.Tx[12][self.lexeme_list.index("digit")] = 53
        self.Tx[12][self.lexeme_list.index("_")] = 53
        self.Tx[12][self.lexeme_list.index("l_letter")] = 13

        for letter in self.all_except_o:
            self.Tx[13][self.lexeme_list.index(letter)] = 53
        self.Tx[13][self.lexeme_list.index("letter")] = 53
        self.Tx[13][self.lexeme_list.index("digit")] = 53
        self.Tx[13][self.lexeme_list.index("_")] = 53
        self.Tx[13][self.lexeme_list.index("o_letter")] = 14

        for letter in self.all_except_a:
            self.Tx[14][self.lexeme_list.index(letter)] = 53
        self.Tx[14][self.lexeme_list.index("letter")] = 53
        self.Tx[14][self.lexeme_list.index("digit")] = 53
        self.Tx[14][self.lexeme_list.index("_")] = 53
        self.Tx[14][self.lexeme_list.index("a_letter")] = 15

        for letter in self.all_except_t:
            self.Tx[15][self.lexeme_list.index(letter)] = 53
        self.Tx[15][self.lexeme_list.index("letter")] = 53
        self.Tx[15][self.lexeme_list.index("digit")] = 53
        self.Tx[15][self.lexeme_list.index("_")] = 53
        self.Tx[15][self.lexeme_list.index("t_letter")] = 16

        for letter in self.needed_letters_list:
            self.Tx[16][self.lexeme_list.index(letter)] = 53
        self.Tx[16][self.lexeme_list.index("letter")] = 53
        self.Tx[16][self.lexeme_list.index("digit")] = 53
        self.Tx[16][self.lexeme_list.index("_")] = 53

        # int
        self.Tx[0][self.lexeme_list.index("i_letter")] = 17

        for letter in self.all_except_n:
            self.Tx[17][self.lexeme_list.index(letter)] = 53
        self.Tx[17][self.lexeme_list.index("letter")] = 53
        self.Tx[17][self.lexeme_list.index("digit")] = 53
        self.Tx[17][self.lexeme_list.index("_")] = 53
        self.Tx[17][self.lexeme_list.index("n_letter")] = 18

        for letter in self.all_except_t:
            self.Tx[18][self.lexeme_list.index(letter)] = 53
        self.Tx[18][self.lexeme_list.index("letter")] = 53
        self.Tx[18][self.lexeme_list.index("digit")] = 53
        self.Tx[18][self.lexeme_list.index("_")] = 53
        self.Tx[18][self.lexeme_list.index("t_letter")] = 19

        for letter in self.needed_letters_list:
            self.Tx[19][self.lexeme_list.index(letter)] = 53
        self.Tx[19][self.lexeme_list.index("letter")] = 53
        self.Tx[19][self.lexeme_list.index("digit")] = 53
        self.Tx[19][self.lexeme_list.index("_")] = 53

        # bool
        self.Tx[0][self.lexeme_list.index("b_letter")] = 20

        for letter in self.all_except_o:
            self.Tx[20][self.lexeme_list.index(letter)] = 53
        self.Tx[20][self.lexeme_list.index("letter")] = 53
        self.Tx[20][self.lexeme_list.index("digit")] = 53
        self.Tx[20][self.lexeme_list.index("_")] = 53
        self.Tx[20][self.lexeme_list.index("o_letter")] = 21

        for letter in self.all_except_o:
            self.Tx[21][self.lexeme_list.index(letter)] = 53
        self.Tx[21][self.lexeme_list.index("letter")] = 53
        self.Tx[21][self.lexeme_list.index("digit")] = 53
        self.Tx[21][self.lexeme_list.index("_")] = 53
        self.Tx[21][self.lexeme_list.index("o_letter")] = 22

        for letter in self.all_except_l:
            self.Tx[22][self.lexeme_list.index(letter)] = 53
        self.Tx[22][self.lexeme_list.index("letter")] = 53
        self.Tx[22][self.lexeme_list.index("digit")] = 53
        self.Tx[22][self.lexeme_list.index("_")] = 53
        self.Tx[22][self.lexeme_list.index("l_letter")] = 23

        for letter in self.needed_letters_list:
            self.Tx[23][self.lexeme_list.index(letter)] = 53
        self.Tx[23][self.lexeme_list.index("letter")] = 53
        self.Tx[23][self.lexeme_list.index("digit")] = 53
        self.Tx[23][self.lexeme_list.index("_")] = 53

        # colour
        self.Tx[0][self.lexeme_list.index("c_letter")] = 24

        for letter in self.all_except_o:
            self.Tx[24][self.lexeme_list.index(letter)] = 53
        self.Tx[24][self.lexeme_list.index("letter")] = 53
        self.Tx[24][self.lexeme_list.index("digit")] = 53
        self.Tx[24][self.lexeme_list.index("_")] = 53
        self.Tx[24][self.lexeme_list.index("o_letter")] = 25

        for letter in self.all_except_l:
            self.Tx[25][self.lexeme_list.index(letter)] = 53
        self.Tx[25][self.lexeme_list.index("letter")] = 53
        self.Tx[25][self.lexeme_list.index("digit")] = 53
        self.Tx[25][self.lexeme_list.index("_")] = 53
        self.Tx[25][self.lexeme_list.index("l_letter")] = 26

        for letter in self.all_except_o:
            self.Tx[26][self.lexeme_list.index(letter)] = 53
        self.Tx[26][self.lexeme_list.index("letter")] = 53
        self.Tx[26][self.lexeme_list.index("digit")] = 53
        self.Tx[26][self.lexeme_list.index("_")] = 53
        self.Tx[26][self.lexeme_list.index("o_letter")] = 27

        for letter in self.all_except_u:
            self.Tx[27][self.lexeme_list.index(letter)] = 53
        self.Tx[27][self.lexeme_list.index("letter")] = 53
        self.Tx[27][self.lexeme_list.index("digit")] = 53
        self.Tx[27][self.lexeme_list.index("_")] = 53
        self.Tx[27][self.lexeme_list.index("u_letter")] = 28

        for letter in self.all_except_r:
            self.Tx[28][self.lexeme_list.index(letter)] = 53
        self.Tx[28][self.lexeme_list.index("letter")] = 53
        self.Tx[28][self.lexeme_list.index("digit")] = 53
        self.Tx[28][self.lexeme_list.index("_")] = 53
        self.Tx[28][self.lexeme_list.index("r_letter")] = 29

        for letter in self.needed_letters_list:
            self.Tx[29][self.lexeme_list.index(letter)] = 53
        self.Tx[29][self.lexeme_list.index("letter")] = 53
        self.Tx[29][self.lexeme_list.index("digit")] = 53
        self.Tx[29][self.lexeme_list.index("_")] = 53

        # Boolean Literal

        # True
        self.Tx[0][self.lexeme_list.index("t_letter")] = 30

        for letter in self.all_except_r:
            self.Tx[30][self.lexeme_list.index(letter)] = 53
        self.Tx[30][self.lexeme_list.index("letter")] = 53
        self.Tx[30][self.lexeme_list.index("digit")] = 53
        self.Tx[30][self.lexeme_list.index("_")] = 53
        self.Tx[30][self.lexeme_list.index("r_letter")] = 31

        for letter in self.all_except_u:
            self.Tx[31][self.lexeme_list.index(letter)] = 53
        self.Tx[31][self.lexeme_list.index("letter")] = 53
        self.Tx[31][self.lexeme_list.index("digit")] = 53
        self.Tx[31][self.lexeme_list.index("_")] = 53
        self.Tx[31][self.lexeme_list.index("u_letter")] = 32

        for letter in self.all_except_e:
            self.Tx[32][self.lexeme_list.index(letter)] = 53
        self.Tx[32][self.lexeme_list.index("letter")] = 53
        self.Tx[32][self.lexeme_list.index("digit")] = 53
        self.Tx[32][self.lexeme_list.index("_")] = 53
        self.Tx[32][self.lexeme_list.index("e_letter")] = 33

        for letter in self.needed_letters_list:
            self.Tx[33][self.lexeme_list.index(letter)] = 53
        self.Tx[33][self.lexeme_list.index("letter")] = 53
        self.Tx[33][self.lexeme_list.index("digit")] = 53
        self.Tx[33][self.lexeme_list.index("_")] = 53

        # False

        self.Tx[0][self.lexeme_list.index("f_letter")] = 34

        self.Tx[34][self.lexeme_list.index("l_letter")] = 13

        for letter in self.all_except_a:
            if letter != "l_letter":
                self.Tx[34][self.lexeme_list.index(letter)] = 53
        self.Tx[34][self.lexeme_list.index("letter")] = 53
        self.Tx[34][self.lexeme_list.index("digit")] = 53
        self.Tx[34][self.lexeme_list.index("_")] = 53
        self.Tx[34][self.lexeme_list.index("a_letter")] = 35

        for letter in self.all_except_l:
            self.Tx[35][self.lexeme_list.index(letter)] = 53
        self.Tx[35][self.lexeme_list.index("letter")] = 53
        self.Tx[35][self.lexeme_list.index("digit")] = 53
        self.Tx[35][self.lexeme_list.index("_")] = 53
        self.Tx[35][self.lexeme_list.index("l_letter")] = 36

        for letter in self.all_except_s:
            self.Tx[36][self.lexeme_list.index(letter)] = 53
        self.Tx[36][self.lexeme_list.index("letter")] = 53
        self.Tx[36][self.lexeme_list.index("digit")] = 53
        self.Tx[36][self.lexeme_list.index("_")] = 53
        self.Tx[36][self.lexeme_list.index("s_letter")] = 37

        for letter in self.all_except_e:
            self.Tx[37][self.lexeme_list.index(letter)] = 53
        self.Tx[37][self.lexeme_list.index("letter")] = 53
        self.Tx[37][self.lexeme_list.index("digit")] = 53
        self.Tx[37][self.lexeme_list.index("_")] = 53
        self.Tx[37][self.lexeme_list.index("e_letter")] = 38

        for letter in self.needed_letters_list:
            self.Tx[38][self.lexeme_list.index(letter)] = 53
        self.Tx[38][self.lexeme_list.index("letter")] = 53
        self.Tx[38][self.lexeme_list.index("digit")] = 53
        self.Tx[38][self.lexeme_list.index("_")] = 53

        # Operands

        # Multiplicative Operands
        self.Tx[0][self.lexeme_list.index("*")] = 39
        self.Tx[0][self.lexeme_list.index("/")] = 40
        self.Tx[0][self.lexeme_list.index("a_letter")] = 50

        for letter in self.all_except_n:
            self.Tx[50][self.lexeme_list.index(letter)] = 53
        self.Tx[50][self.lexeme_list.index("letter")] = 53
        self.Tx[50][self.lexeme_list.index("digit")] = 53
        self.Tx[50][self.lexeme_list.index("_")] = 53
        self.Tx[50][self.lexeme_list.index("n_letter")] = 51

        for letter in self.all_except_d:
            self.Tx[51][self.lexeme_list.index(letter)] = 53
        self.Tx[51][self.lexeme_list.index("letter")] = 53
        self.Tx[51][self.lexeme_list.index("digit")] = 53
        self.Tx[51][self.lexeme_list.index("_")] = 53
        self.Tx[51][self.lexeme_list.index("d_letter")] = 52

        for letter in self.needed_letters_list:
            self.Tx[52][self.lexeme_list.index(letter)] = 53
        self.Tx[52][self.lexeme_list.index("letter")] = 53
        self.Tx[52][self.lexeme_list.index("digit")] = 53
        self.Tx[52][self.lexeme_list.index("_")] = 53

        # Additive Operands
        self.Tx[0][self.lexeme_list.index("+")] = 41
        self.Tx[0][self.lexeme_list.index("-")] = 42
        self.Tx[42][self.lexeme_list.index(">")] = 154
        self.Tx[0][self.lexeme_list.index("o_letter")] = 48

        for letter in self.all_except_r:
            self.Tx[48][self.lexeme_list.index(letter)] = 53
        self.Tx[48][self.lexeme_list.index("letter")] = 53
        self.Tx[48][self.lexeme_list.index("digit")] = 53
        self.Tx[48][self.lexeme_list.index("_")] = 53
        self.Tx[48][self.lexeme_list.index("r_letter")] = 49

        for letter in self.needed_letters_list:
            self.Tx[49][self.lexeme_list.index(letter)] = 53
        self.Tx[49][self.lexeme_list.index("letter")] = 53
        self.Tx[49][self.lexeme_list.index("digit")] = 53
        self.Tx[49][self.lexeme_list.index("_")] = 53

        # Relational Operands
        self.Tx[0][self.lexeme_list.index("<")] = 43
        self.Tx[43][self.lexeme_list.index("=")] = 47
        self.Tx[0][self.lexeme_list.index(">")] = 44
        self.Tx[44][self.lexeme_list.index("=")] = 47
        self.Tx[0][self.lexeme_list.index("=")] = 45
        self.Tx[45][self.lexeme_list.index("=")] = 47
        self.Tx[0][self.lexeme_list.index("!")] = 46
        self.Tx[46][self.lexeme_list.index("=")] = 47

        # Identifier
        for letter in self.needed_letters_list:
            self.Tx[53][self.lexeme_list.index(letter)] = 53
        self.Tx[53][self.lexeme_list.index("letter")] = 53
        self.Tx[0][self.lexeme_list.index("letter")] = 53
        self.Tx[53][self.lexeme_list.index("letter")] = 53
        self.Tx[53][self.lexeme_list.index("digit")] = 53
        self.Tx[53][self.lexeme_list.index("_")] = 53

        # PAD Keywords:
        self.Tx[0][self.lexeme_list.index("_")] = 54
        self.Tx[54][self.lexeme_list.index("_")] = 55
        self.Tx[55][self.lexeme_list.index("w_letter")] = 56
        self.Tx[56][self.lexeme_list.index("i_letter")] = 57
        self.Tx[57][self.lexeme_list.index("d_letter")] = 58
        self.Tx[58][self.lexeme_list.index("t_letter")] = 59
        self.Tx[59][self.lexeme_list.index("h_letter")] = 60

        self.Tx[0][self.lexeme_list.index("_")] = 61
        self.Tx[61][self.lexeme_list.index("_")] = 62
        self.Tx[62][self.lexeme_list.index("h_letter")] = 63
        self.Tx[63][self.lexeme_list.index("e_letter")] = 64
        self.Tx[64][self.lexeme_list.index("i_letter")] = 65
        self.Tx[65][self.lexeme_list.index("g_letter")] = 66
        self.Tx[66][self.lexeme_list.index("h_letter")] = 67
        self.Tx[67][self.lexeme_list.index("t_letter")] = 68

        self.Tx[0][self.lexeme_list.index("_")] = 69
        self.Tx[69][self.lexeme_list.index("_")] = 70
        self.Tx[70][self.lexeme_list.index("r_letter")] = 71

        self.Tx[71][self.lexeme_list.index("a_letter")] = 78

        self.Tx[71][self.lexeme_list.index("e_letter")] = 72
        self.Tx[72][self.lexeme_list.index("a_letter")] = 73
        self.Tx[73][self.lexeme_list.index("d_letter")] = 74

        self.Tx[0][self.lexeme_list.index("_")] = 75
        self.Tx[75][self.lexeme_list.index("_")] = 76
        self.Tx[76][self.lexeme_list.index("r_letter")] = 77
        self.Tx[77][self.lexeme_list.index("a_letter")] = 78
        self.Tx[78][self.lexeme_list.index("n_letter")] = 79
        self.Tx[79][self.lexeme_list.index("d_letter")] = 80
        self.Tx[80][self.lexeme_list.index("o_letter")] = 81
        self.Tx[81][self.lexeme_list.index("m_letter")] = 82
        self.Tx[82][self.lexeme_list.index("_")] = 83
        self.Tx[83][self.lexeme_list.index("i_letter")] = 84
        self.Tx[84][self.lexeme_list.index("n_letter")] = 85
        self.Tx[85][self.lexeme_list.index("t_letter")] = 86

        # __ Keywords

        self.Tx[0][self.lexeme_list.index("_")] = 87
        self.Tx[87][self.lexeme_list.index("_")] = 88
        self.Tx[88][self.lexeme_list.index("d_letter")] = 96
        self.Tx[88][self.lexeme_list.index("w_letter")] = 103

        self.Tx[88][self.lexeme_list.index("p_letter")] = 89
        self.Tx[89][self.lexeme_list.index("r_letter")] = 90
        self.Tx[90][self.lexeme_list.index("i_letter")] = 91
        self.Tx[91][self.lexeme_list.index("n_letter")] = 92
        self.Tx[92][self.lexeme_list.index("t_letter")] = 93

        self.Tx[0][self.lexeme_list.index("_")] = 94
        self.Tx[94][self.lexeme_list.index("_")] = 95
        self.Tx[95][self.lexeme_list.index("d_letter")] = 96
        self.Tx[96][self.lexeme_list.index("e_letter")] = 97
        self.Tx[97][self.lexeme_list.index("l_letter")] = 98
        self.Tx[98][self.lexeme_list.index("a_letter")] = 99
        self.Tx[99][self.lexeme_list.index("y_letter")] = 100

        self.Tx[0][self.lexeme_list.index("_")] = 101
        self.Tx[101][self.lexeme_list.index("_")] = 102
        self.Tx[102][self.lexeme_list.index("w_letter")] = 103
        self.Tx[103][self.lexeme_list.index("r_letter")] = 104
        self.Tx[104][self.lexeme_list.index("i_letter")] = 105
        self.Tx[105][self.lexeme_list.index("t_letter")] = 106
        self.Tx[106][self.lexeme_list.index("e_letter")] = 107
        self.Tx[107][self.lexeme_list.index("_")] = 108
        self.Tx[108][self.lexeme_list.index("b_letter")] = 109
        self.Tx[109][self.lexeme_list.index("o_letter")] = 110
        self.Tx[110][self.lexeme_list.index("x_letter")] = 111

        self.Tx[0][self.lexeme_list.index("_")] = 112
        self.Tx[112][self.lexeme_list.index("_")] = 113

        self.Tx[113][self.lexeme_list.index("h_letter")] = 63
        self.Tx[113][self.lexeme_list.index("r_letter")] = 71
        self.Tx[113][self.lexeme_list.index("p_letter")] = 89
        self.Tx[113][self.lexeme_list.index("d_letter")] = 96

        self.Tx[113][self.lexeme_list.index("w_letter")] = 114
        self.Tx[114][self.lexeme_list.index("i_letter")] = 57

        self.Tx[114][self.lexeme_list.index("r_letter")] = 115
        self.Tx[115][self.lexeme_list.index("i_letter")] = 116
        self.Tx[116][self.lexeme_list.index("t_letter")] = 117
        self.Tx[117][self.lexeme_list.index("e_letter")] = 118
        self.Tx[118][self.lexeme_list.index("_")] = 108


        # Other keywords

        # Return

        self.Tx[0][self.lexeme_list.index("r_letter")] = 119

        for letter in self.all_except_e:
            self.Tx[119][self.lexeme_list.index(letter)] = 53
        self.Tx[119][self.lexeme_list.index("letter")] = 53
        self.Tx[119][self.lexeme_list.index("digit")] = 53
        self.Tx[119][self.lexeme_list.index("_")] = 53
        self.Tx[119][self.lexeme_list.index("e_letter")] = 120

        for letter in self.all_except_t:
            self.Tx[120][self.lexeme_list.index(letter)] = 53
        self.Tx[120][self.lexeme_list.index("letter")] = 53
        self.Tx[120][self.lexeme_list.index("digit")] = 53
        self.Tx[120][self.lexeme_list.index("_")] = 53
        self.Tx[120][self.lexeme_list.index("t_letter")] = 121

        for letter in self.all_except_u:
            self.Tx[121][self.lexeme_list.index(letter)] = 53
        self.Tx[121][self.lexeme_list.index("letter")] = 53
        self.Tx[121][self.lexeme_list.index("digit")] = 53
        self.Tx[121][self.lexeme_list.index("_")] = 53
        self.Tx[121][self.lexeme_list.index("u_letter")] = 122

        for letter in self.all_except_r:
            self.Tx[122][self.lexeme_list.index(letter)] = 53
        self.Tx[122][self.lexeme_list.index("letter")] = 53
        self.Tx[122][self.lexeme_list.index("digit")] = 53
        self.Tx[122][self.lexeme_list.index("_")] = 53
        self.Tx[122][self.lexeme_list.index("r_letter")] = 123

        for letter in self.all_except_n:
            self.Tx[123][self.lexeme_list.index(letter)] = 53
        self.Tx[123][self.lexeme_list.index("letter")] = 53
        self.Tx[123][self.lexeme_list.index("digit")] = 53
        self.Tx[123][self.lexeme_list.index("_")] = 53
        self.Tx[123][self.lexeme_list.index("n_letter")] = 124

        self.Tx[124][self.lexeme_list.index("letter")] = 53
        self.Tx[124][self.lexeme_list.index("digit")] = 53
        self.Tx[124][self.lexeme_list.index("_")] = 53

        # if

        self.Tx[0][self.lexeme_list.index("i_letter")] = 125
        self.Tx[125][self.lexeme_list.index("n_letter")] = 18

        for letter in self.all_except_f:
            if letter != "n_letter":
                self.Tx[125][self.lexeme_list.index(letter)] = 53
        self.Tx[125][self.lexeme_list.index("letter")] = 53
        self.Tx[125][self.lexeme_list.index("digit")] = 53
        self.Tx[125][self.lexeme_list.index("_")] = 53

        self.Tx[125][self.lexeme_list.index("f_letter")] = 126

        self.Tx[126][self.lexeme_list.index("letter")] = 53
        self.Tx[126][self.lexeme_list.index("digit")] = 53
        self.Tx[126][self.lexeme_list.index("_")] = 53

        # for

        self.Tx[0][self.lexeme_list.index("f_letter")] = 127

        for letter in self.all_except_o:
            self.Tx[127][self.lexeme_list.index(letter)] = 53
        self.Tx[127][self.lexeme_list.index("letter")] = 53
        self.Tx[127][self.lexeme_list.index("digit")] = 53
        self.Tx[127][self.lexeme_list.index("_")] = 53
        self.Tx[127][self.lexeme_list.index("o_letter")] = 128

        for letter in self.all_except_r:
            self.Tx[128][self.lexeme_list.index(letter)] = 53
        self.Tx[128][self.lexeme_list.index("letter")] = 53
        self.Tx[128][self.lexeme_list.index("digit")] = 53
        self.Tx[128][self.lexeme_list.index("_")] = 53
        self.Tx[128][self.lexeme_list.index("r_letter")] = 129

        for letter in self.needed_letters_list:
            self.Tx[129][self.lexeme_list.index(letter)] = 53
        self.Tx[129][self.lexeme_list.index("letter")] = 53
        self.Tx[129][self.lexeme_list.index("letter")] = 53
        self.Tx[129][self.lexeme_list.index("digit")] = 53
        self.Tx[129][self.lexeme_list.index("_")] = 53

        # while

        self.Tx[0][self.lexeme_list.index("w_letter")] = 130

        for letter in self.all_except_h:
            self.Tx[130][self.lexeme_list.index(letter)] = 53
        self.Tx[130][self.lexeme_list.index("letter")] = 53
        self.Tx[130][self.lexeme_list.index("digit")] = 53
        self.Tx[130][self.lexeme_list.index("_")] = 53
        self.Tx[130][self.lexeme_list.index("h_letter")] = 131

        for letter in self.all_except_i:
            self.Tx[131][self.lexeme_list.index(letter)] = 53
        self.Tx[131][self.lexeme_list.index("letter")] = 53
        self.Tx[131][self.lexeme_list.index("digit")] = 53
        self.Tx[131][self.lexeme_list.index("_")] = 53
        self.Tx[131][self.lexeme_list.index("i_letter")] = 132

        for letter in self.all_except_l:
            self.Tx[132][self.lexeme_list.index(letter)] = 53
        self.Tx[132][self.lexeme_list.index("letter")] = 53
        self.Tx[132][self.lexeme_list.index("digit")] = 53
        self.Tx[132][self.lexeme_list.index("_")] = 53
        self.Tx[132][self.lexeme_list.index("l_letter")] = 133

        for letter in self.all_except_e:
            self.Tx[133][self.lexeme_list.index(letter)] = 53
        self.Tx[133][self.lexeme_list.index("letter")] = 53
        self.Tx[133][self.lexeme_list.index("digit")] = 53
        self.Tx[133][self.lexeme_list.index("_")] = 53
        self.Tx[133][self.lexeme_list.index("e_letter")] = 134

        for letter in self.needed_letters_list:
            self.Tx[134][self.lexeme_list.index(letter)] = 53
        self.Tx[134][self.lexeme_list.index("letter")] = 53
        self.Tx[134][self.lexeme_list.index("digit")] = 53
        self.Tx[134][self.lexeme_list.index("_")] = 53

        # fun
        self.Tx[0][self.lexeme_list.index("f_letter")] = 135
        self.Tx[135][self.lexeme_list.index("a_letter")] = 35
        self.Tx[135][self.lexeme_list.index("o_letter")] = 128
        self.Tx[135][self.lexeme_list.index("l_letter")] = 13

        for letter in self.all_except_u:
            if letter != "o_letter" and letter != "l_letter" and letter != "a_letter":
                self.Tx[135][self.lexeme_list.index(letter)] = 53

        self.Tx[135][self.lexeme_list.index("letter")] = 53
        self.Tx[135][self.lexeme_list.index("digit")] = 53
        self.Tx[135][self.lexeme_list.index("_")] = 53
        self.Tx[135][self.lexeme_list.index("letter")] = 53
        self.Tx[135][self.lexeme_list.index("u_letter")] = 136

        for letter in self.all_except_n:
            self.Tx[136][self.lexeme_list.index(letter)] = 53
        self.Tx[136][self.lexeme_list.index("letter")] = 53
        self.Tx[136][self.lexeme_list.index("digit")] = 53
        self.Tx[136][self.lexeme_list.index("_")] = 53
        self.Tx[136][self.lexeme_list.index("n_letter")] = 137

        for letter in self.needed_letters_list:
            self.Tx[137][self.lexeme_list.index(letter)] = 53

        self.Tx[137][self.lexeme_list.index("letter")] = 53
        self.Tx[137][self.lexeme_list.index("digit")] = 53
        self.Tx[137][self.lexeme_list.index("_")] = 53

        # let
        self.Tx[0][self.lexeme_list.index("l_letter")] = 138

        for letter in self.all_except_e:
            self.Tx[138][self.lexeme_list.index(letter)] = 53
        self.Tx[138][self.lexeme_list.index("letter")] = 53
        self.Tx[138][self.lexeme_list.index("digit")] = 53
        self.Tx[138][self.lexeme_list.index("_")] = 53
        self.Tx[138][self.lexeme_list.index("e_letter")] = 139

        for letter in self.all_except_t:
            self.Tx[139][self.lexeme_list.index(letter)] = 53
        self.Tx[139][self.lexeme_list.index("letter")] = 53
        self.Tx[139][self.lexeme_list.index("digit")] = 53
        self.Tx[139][self.lexeme_list.index("_")] = 53
        self.Tx[139][self.lexeme_list.index("t_letter")] = 140

        for letter in self.needed_letters_list:
            self.Tx[140][self.lexeme_list.index(letter)] = 53
        self.Tx[140][self.lexeme_list.index("letter")] = 53
        self.Tx[140][self.lexeme_list.index("digit")] = 53
        self.Tx[140][self.lexeme_list.index("_")] = 53

        # not

        self.Tx[0][self.lexeme_list.index("n_letter")] = 157

        for letter in self.all_except_o:
            self.Tx[157][self.lexeme_list.index(letter)] = 53
        self.Tx[157][self.lexeme_list.index("letter")] = 53
        self.Tx[157][self.lexeme_list.index("digit")] = 53
        self.Tx[157][self.lexeme_list.index("_")] = 53
        self.Tx[157][self.lexeme_list.index("o_letter")] = 158

        for letter in self.all_except_t:
            self.Tx[158][self.lexeme_list.index(letter)] = 53
        self.Tx[158][self.lexeme_list.index("letter")] = 53
        self.Tx[158][self.lexeme_list.index("digit")] = 53
        self.Tx[158][self.lexeme_list.index("_")] = 53
        self.Tx[158][self.lexeme_list.index("t_letter")] = 159

        for letter in self.needed_letters_list:
            self.Tx[159][self.lexeme_list.index(letter)] = 53
        self.Tx[159][self.lexeme_list.index("letter")] = 53
        self.Tx[159][self.lexeme_list.index("digit")] = 53
        self.Tx[159][self.lexeme_list.index("_")] = 53

        # as

        self.Tx[0][self.lexeme_list.index("a_letter")] = 160

        for letter in self.all_except_n:
            self.Tx[160][self.lexeme_list.index(letter)] = 53
        self.Tx[160][self.lexeme_list.index("letter")] = 53
        self.Tx[160][self.lexeme_list.index("digit")] = 53
        self.Tx[160][self.lexeme_list.index("_")] = 53
        self.Tx[160][self.lexeme_list.index("n_letter")] = 51

        for letter in self.all_except_s:
            if letter != "n_letter":
             self.Tx[160][self.lexeme_list.index(letter)] = 53
        self.Tx[160][self.lexeme_list.index("letter")] = 53
        self.Tx[160][self.lexeme_list.index("digit")] = 53
        self.Tx[160][self.lexeme_list.index("_")] = 53
        self.Tx[160][self.lexeme_list.index("s_letter")] = 161

        # else
        self.Tx[0][self.lexeme_list.index("e_letter")] = 141

        for letter in self.all_except_e:
             self.Tx[141][self.lexeme_list.index(letter)] = 53
        self.Tx[141][self.lexeme_list.index("letter")] = 53
        self.Tx[141][self.lexeme_list.index("digit")] = 53
        self.Tx[141][self.lexeme_list.index("_")] = 53
        self.Tx[141][self.lexeme_list.index("l_letter")] = 142
        for letter in self.all_except_s:
             self.Tx[142][self.lexeme_list.index(letter)] = 53
        self.Tx[142][self.lexeme_list.index("letter")] = 53
        self.Tx[142][self.lexeme_list.index("digit")] = 53
        self.Tx[142][self.lexeme_list.index("_")] = 53
        self.Tx[142][self.lexeme_list.index("s_letter")] = 143
        for letter in self.all_except_e:
             self.Tx[143][self.lexeme_list.index(letter)] = 53
        self.Tx[143][self.lexeme_list.index("letter")] = 53
        self.Tx[143][self.lexeme_list.index("digit")] = 53
        self.Tx[143][self.lexeme_list.index("_")] = 53
        self.Tx[143][self.lexeme_list.index("e_letter")] = 145
        for letter in self.needed_letters_list:
            self.Tx[145][self.lexeme_list.index(letter)] = 53
        self.Tx[145][self.lexeme_list.index("letter")] = 53
        self.Tx[145][self.lexeme_list.index("digit")] = 53
        self.Tx[145][self.lexeme_list.index("_")] = 53

        # Symbols
        self.Tx[0][self.lexeme_list.index(",")] = 146
        self.Tx[0][self.lexeme_list.index("[")] = 147
        self.Tx[0][self.lexeme_list.index("]")] = 148
        self.Tx[0][self.lexeme_list.index("(")] = 149
        self.Tx[0][self.lexeme_list.index(")")] = 150
        self.Tx[0][self.lexeme_list.index(":")] = 151
        self.Tx[0][self.lexeme_list.index(";")] = 152
        self.Tx[0][self.lexeme_list.index("{")] = 155
        self.Tx[0][self.lexeme_list.index("}")] = 156

        # Catch needed letters in starting state
        catch_letters = ["d", "g", "h", "m", "p", "s", "u", "x", "y"]
        for letter in catch_letters:
            self.Tx[0][self.lexeme_list.index(letter + "_letter")] = 53


    def AcceptingStates(self, state):
        try:
            self.states_accp.index(state)
            return True
        except ValueError:
            return False

    def CatChar(self, character):
        cat = "other"
        if character.lower() in self.symbol_list:
            cat = character.lower()
        elif character.lower() + "_letter" in self.needed_letters_list:
            cat = character.lower() + "_letter"
        elif character.lower() in self.operand_list:
            cat = character.lower()
        elif character.isalpha():
            cat = "letter"
        elif character.isdigit():
            cat = "digit"
        elif character.lower() == " ":
            cat = "ws"

        return cat

    def EndOfInput(self, src_program_str, src_program_idx):
        if src_program_idx > len(src_program_str) - 1:
            return True;
        else:
            return False;

    def NextChar(self, src_program_str, src_program_idx):
        if not self.EndOfInput(src_program_str, src_program_idx):
            return True, src_program_str[src_program_idx]
        else:
            return False, "."

    def NextToken(self, src_program_str, src_program_idx):
        state = 0  # initial state is 0 - check Tx
        stack = []
        lexeme = ""
        stack.append(-2)  # insert the error state at the bottom of the stack.

        while (state != -1):
            if self.AcceptingStates(state):
                stack.clear()
            stack.append(state)

            exists, character = self.NextChar(src_program_str, src_program_idx)
            lexeme += character
            if not exists:
                # print("LAST LEXEME: ", lexeme)
                break  # Break out of loop if we're at the end of the string
            src_program_idx = src_program_idx + 1

            cat = self.CatChar(character)
            state = self.Tx[state][self.lexeme_list.index(cat)]
            print("Lexeme: ", lexeme, " => NEXT STATE: ", state, "  => CAT: ", cat, "  => CHAR:", character,
                  "  => STACK: ", stack)

        lexeme = lexeme[:-1]  # remove the last character added which sent the lexer to state -1

        syntax_error = False
        # rollback
        while len(stack) > 0:
            if stack[-1] == -2:  # report a syntax error
                syntax_error = True
                break

                # Pop this state if not an accepting state.
            if not self.AcceptingStates(stack[-1]):
                stack.pop()
                lexeme = lexeme[:-1]

            else:
                state = stack.pop()
                break


        if syntax_error:
            return Token(TokenType.VOID, "error"), "error"

        if self.AcceptingStates(state):
            return GetTokenTypeByFinalState(state, lexeme), lexeme
        else:
            return Token(TokenType.VOID, "error"), "error"

    def GenerateTokens(self, src_program_str):
        tokens_list = []
        src_program_idx = 0
        token, lexeme = self.NextToken(src_program_str, src_program_idx)
        tokens_list.append(token)

        while token.type != TokenType.END:  # this loop is simulating the Parser asking for the next Token
            src_program_idx = src_program_idx + len(lexeme)
            if not self.EndOfInput(src_program_str, src_program_idx):
                token, lexeme = self.NextToken(src_program_str, src_program_idx)
                tokens_list.append(token)
                if token.type == TokenType.VOID:
                    break
            else:
                token, lexeme = Token(TokenType.END, "END"), "END"


        return tokens_list
