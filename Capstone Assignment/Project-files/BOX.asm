(LOOP)
    // color = -1 (black) if a key is pressed, otherwise 0 (white)
    @color
    M=0
    @KBD
    D=M
    @DRAW
    D;JEQ
    @color
    M=-1

(DRAW)
    // addr = first word of row 1 = SCREEN + 32*1
    @SCREEN
    D=A
    @32
    D=D+A
    @addr
    M=D
    // rows = 20
    @20
    D=A
    @rows
    M=D

(ROW)
    // cols = 2 words per row
    @2
    D=A
    @cols
    M=D

(COL)
    // RAM[addr] = color, then move to the next word
    @color
    D=M
    @addr
    A=M
    M=D
    @addr
    M=M+1
    // more words in this row?
    @cols
    MD=M-1
    @COL
    D;JGT

    // go to the start of the next row: skip the other 32 - 2 = 30 words
    @30
    D=A
    @addr
    M=D+M
    // more rows?
    @rows
    MD=M-1
    @ROW
    D;JGT

    @LOOP
    0;JMP
