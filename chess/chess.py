from chess_const import *

class Chess:
    def __init__(self):
        self.board = []
        self.create_board()
 
    def create_board(self):             #8x8 체스판 생성
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            row = []
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                row.append(EMPTY)
            self.board.append(row)

    def print_board(self):              # 현재 체스보드판을 프린트 출력.
        for N in reversed(range(CHESS_BOARD_TOTAL_CELLS)):
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                print(self.board[N][M], end=" ")
            print()
    
    def erase_board(self):              # 8x8 체스판을 EMPTY로 초기화
        for N in range(CHESS_BOARD_TOTAL_CELLS):
            for M in range(CHESS_BOARD_TOTAL_CELLS):
                self.board[N][M] = EMPTY

    def is_valid_posstr(self, pos_str): # a1~h8 유효범위 확인 
        if len(pos_str) != 2:
            return False
        
        if ord(pos_str[0]) >= ord('a') and ord(pos_str[0]) <= ord('h'):
            if int(pos_str[1]) >= 1 and int(pos_str[1]) <= 8:
                return True        
        return False 
    
    def posstr_TO_num(self, pos_str):  # 'a1' => 00  보드판 인덱스를 위한 숫자로 반환 
        j = ord(pos_str[0]) - ord('a') 
        i = int(pos_str[1]) - 1 
        return i, j
    
    def cell_value(self, pos_str):      #해당 칸에 무엇이 있는지 반환
        i, j = self.posstr_TO_num(pos_str)
        return self.board[i][j]

    def set_cell(self, pos_str, piece_type_str):
        if self.is_valid_posstr(pos_str)==True:
            i, j = self.posstr_TO_num(pos_str)
            self.board[i][j] = piece_type_str      
        else: print("is not valid pos_str")  

    def del_cell(self, pos_str):
        i, j = self.posstr_TO_num(pos_str)
        self.board[i][j] = EMPTY
        
    

    def set_pieces(self):         #체스말 세팅 
        color = [BLACK, WHITE]
        posstr1 = ['7', '2']  # 7(블랙 폰행),2(화이트 폰행) 
        for i in range(2):  #블랙폰 -> 화이트폰 순으로 세팅
            for n in range(CHESS_BOARD_TOTAL_CELLS):
                char = chr(ord('a') + n)
                self.set_cell(char + posstr1[i], color[i]+PAWN) 
        self.set_cell('a8', BLACK+ROOK)
        self.set_cell('b8', BLACK+KNIGHT)
        self.set_cell('c8', BLACK+BISHOP)
        self.set_cell('d8', BLACK+KING)
        self.set_cell('e8', BLACK+QUEEN)
        self.set_cell('f8', BLACK+BISHOP)
        self.set_cell('g8', BLACK+KNIGHT)
        self.set_cell('h8', BLACK+ROOK)

        self.set_cell('a1', WHITE+ROOK)
        self.set_cell('b1', WHITE+KNIGHT)
        self.set_cell('c1', WHITE+BISHOP)
        self.set_cell('d1', WHITE+QUEEN)
        self.set_cell('e1', WHITE+KING)
        self.set_cell('f1', WHITE+BISHOP)
        self.set_cell('g1', WHITE+KNIGHT)
        self.set_cell('h1', WHITE+ROOK)

    def piece_moves(self, pos_str, move_pos):
        piece_type_str = self.cell_value(pos_str)   #pos_str 밸류값 불러오기. 
        piece_type = {'W' : self.pawn_moves,
                      'R' : self.rook_moves, 
                      'N' : self.knight_moves,
                      'B' : self.bishop_moves,
                      'Q' : self.queen_moves,
                      'K' : self.king_moves}
        
        moves = piece_type[piece_type_str[1]]       # 피스 종류
 
        valid_moves_pos = moves(pos_str, piece_type_str[0])    # [piece_type]_moves(pos_str, color)

        if move_pos in valid_moves_pos:
            self.del_cell(pos_str)
            self.set_cell(move_pos, piece_type_str)
            #return print("piece_type_str = "+piece_type_str)
            print('이동성공!')
            return move_pos, piece_type_str 
        else : print("failed the moves")
        return print("failed the moves")


   
    def pawn_moves(self, pos_str, color):
        moves = []
        row = pos_str[1]
        column = pos_str[0]
    
        row = str(int(row)+1)
        if self.is_valid_posstr(column+row) == True:    #폰 1칸 전진 가능여부 확인
            if self.cell_value(column+row) == EMPTY:
                moves.append(column+row)
                
                init_pos = ""                               #폰 2칸 전진 가능여부 확인
                if color == BLACK:
                    init_pos = '7'
                else: 
                    init_pos = '2'

                if init_pos == pos_str[1]:
                    if self.cell_value(column+str(int(row)+1)) == EMPTY:
                        moves.append(column+str(int(row)+1))


        column = chr(ord(column) - 1)
        piece_type = self.cell_value(column+row)
        if self.is_valid_posstr(column+row) == True:    #폰 좌측 대각선 전진 가능여부 확인
            if not(color in piece_type) and piece_type != EMPTY:
                moves.append(column+row)

        column = chr(ord(column) + 2)
        piece_type = self.cell_value(column+row)
        if self.is_valid_posstr(column+row) == True:    #폰 우측 대각선  전진 가능여부 확인
            if not(color in piece_type) and piece_type != EMPTY:
                moves.append(column+row) 
        #print("moves =" , moves)
        return moves
    

    def rook_moves(self,str_pos, color):
        moves = []
        row = str_pos[1]
        column = str_pos[0]

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #좌측 직선 경로 
            cnt_column = chr(ord(column)-i)
            if self.is_valid_posstr(cnt_column+row) == True:
                if self.cell_value(cnt_column+row) == EMPTY:
                    moves.append(cnt_column+row)
                    continue
                elif not(color in self.cell_value(cnt_column+row)):
                    moves.append(cnt_column+row)
                    break
            else : break
        
        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #우측 직선 경로 
            cnt_column = chr(ord(column)+i)
            if self.is_valid_posstr(cnt_column+row) == True:
                if self.cell_value(cnt_column+row) == EMPTY:
                    moves.append(cnt_column+row)
                    continue
                elif not(color in self.cell_value(cnt_column+row)):
                    moves.append(cnt_column+row)
                    break
            else : break

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #하측 직선 경로 
            cnt_row = str(int(row) - i) 
            if self.is_valid_posstr(column+cnt_row) == True:
                if self.cell_value(column+cnt_row) == EMPTY:
                    moves.append(column+cnt_row)
                    continue
                elif not(color in self.cell_value(column+cnt_row)):
                    moves.append(column+cnt_row)
                    break
            else : break

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #상측 직선 경로 
            cnt_row = str(int(row) + i)
            if self.is_valid_posstr(column+cnt_row) == True:
                if self.cell_value(column+cnt_row) == EMPTY:
                    moves.append(column+cnt_row)
                    continue
                elif not(color in self.cell_value(column+cnt_row)):
                    moves.append(column+cnt_row)
                    break
            else : break        
    
        return moves


    def knight_moves(self,str_pos, color):

        pass
    def bishop_moves(self,str_pos, color):
        moves = []
        row = str_pos[1]
        column = str_pos[0]

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #좌측하단 대각선 경로
            cnt_row = str(int(row) - i)
            cnt_column = chr(ord(column) - i)
            if self.is_valid_posstr(cnt_column+cnt_row) == True:
                if self.cell_value(cnt_column+cnt_row) == EMPTY:
                    moves.append(cnt_column+cnt_row)
                    continue
                elif not(color in self.cell_value(cnt_column+cnt_row)):
                    moves.append(cnt_column+cnt_row)
                    break
            else : break
            
        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #우측하단 대각선 경로
            cnt_row = str(int(row) - i)
            cnt_column = chr(ord(column) + i)
            if self.is_valid_posstr(cnt_column+cnt_row) == True:
                if self.cell_value(cnt_column+cnt_row) == EMPTY:
                    moves.append(cnt_column+cnt_row)
                    continue
                elif not(color in self.cell_value(cnt_column+cnt_row)):
                    moves.append(cnt_column+cnt_row)
                    break
            else : break

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #좌측상단 대각선 경로 
            cnt_row = str(int(row) + i)
            cnt_column = chr(ord(column) - i)
            if self.is_valid_posstr(cnt_column+cnt_row) == True:
                if self.cell_value(cnt_column+cnt_row) == EMPTY:
                    moves.append(cnt_column+cnt_row)
                    continue
                elif not(color in self.cell_value(cnt_column+cnt_row)):
                    moves.append(cnt_column+cnt_row)
                    break
            else : break

        for i in range(1, CHESS_BOARD_TOTAL_CELLS):             #우측상단 대각선 경로
            cnt_row = str(int(row) + i)
            cnt_column = chr(ord(column) + i)
            if self.is_valid_posstr(cnt_column+cnt_row) == True:
                if self.cell_value(cnt_column+cnt_row) == EMPTY:
                    moves.append(cnt_column+cnt_row)
                    continue
                elif not(color in self.cell_value(cnt_column+cnt_row)):
                    moves.append(cnt_column+cnt_row)
                    break
            else : break


        print(moves)
        return moves





        pass
    def queen_moves(self,str_pos, color):
        moves = []
        moves.extend(self.rook_moves(str_pos, color))
        moves.extend(self.bishop_moves(str_pos, color))    
        print(moves)
        return moves
    
    def king_moves(self,str_pos, color):
        pass
        
            

                

        
        
   
# 위치를 선택하면 해당 기물 이동범위를 배열에 담아서 리턴  
        
               
                    
            
                




chess = Chess()      

chess.set_pieces()

chess.set_cell('d4', BLACK+QUEEN)
chess.piece_moves('d4', 'b2')
print()
print()
chess.print_board()


print('\n not error complete')