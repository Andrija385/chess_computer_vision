import numpy as np
import cv2 as cv
import os
path = '../../superset/pieces_png'
code = {}
code['wk.png']=0
code['wq.png']=1
code['wr.png']=2
code['wb.png']=3
code['wn.png']=4
code['wp.png']=5

code['bk.png']=6
code['bq.png']=7
code['br.png']=8
code['bb.png']=9
code['bn.png']=10
code['bp.png']=11
code['ti.png']=12

code['wk']=0
code['wq']=1
code['wr']=2
code['wb']=3
code['wn']=4
code['wp']=5

code['bk']=6
code['bq']=7
code['br']=8
code['bb']=9
code['bn']=10
code['bp']=11
code['ti']=12
def extract_database(path):
    x=[]
    y=[]
    for example in os.listdir(path):
        img = cv.imread(os.path.join(path,example))
        x.append(img)
        y.append(code[example[:2].lower()])
    x=np.array(x)
    y=np.array(y)
    return x,y

def listaj(path):
    x=[]
    y=[]
    for filename in os.listdir(path):
        for pic in os.listdir(os.path.join(path,filename)):
            img = cv.imread(os.path.join(os.path.join(path,filename),pic))
            img = cv.resize(img,dsize=(32,32))
            label = code[pic.lower()]
            x.append(img)
            y.append(label)
    return np.array(x),np.array(y)
def extract_piece(piece):
    piece_canny = cv.Canny(cv.cvtColor(piece, cv.COLOR_BGR2GRAY), 20, 20, apertureSize=5)
    contours, hierarchy = cv.findContours(piece_canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cont_areas = np.array([cv.contourArea(cont) for cont in contours])
    prazno = np.zeros((32, 32, 3),dtype=np.uint8)
    # tabla_canny = cv.morphologyEx(tabla_canny,cv.MORPH_CLOSE,kernel=np.ones((2,2)))
    # for cont in contours:
    # if cv.contourArea(cont)<100.0:
    # tabla_canny = cv.drawContours(tabla_canny,[cont],-1,(0,0,0),cv.FILLED)
    if cont_areas.shape[0] > 0 and np.max(cont_areas) / (32 * 32) > 0.2:
        cv.drawContours(prazno, contours, np.argmax(cont_areas), (255, 255, 255), cv.FILLED)
    print(piece.shape)
    print(prazno.shape)
    print(piece.dtype)
    print(prazno.dtype)
    return cv.bitwise_and(piece,prazno)
def extract_piece2(piece):
        prazno = cv.Sobel(cv.cvtColor(piece, cv.COLOR_BGR2GRAY),-1,2,2)
        return prazno
def extract_pieces(tabla):
    tablica=[[],[],[],[],[],[],[],[]]
    for i in range(8):
        for j in range(8):
            tablica[i].append(extract_piece2(tabla[i,j]))
        tablica[i]=np.array(tablica[i])
    tablica=np.array(tablica)
    return tablica
def extract_tiles(path):
    chesscom = os.path.join(path,'chess.com')
    lichess = os.path.join(path,'lichess.org')
    sve = os.path.join(path,'sve')
    for theme in os.listdir(chesscom):
        tile = cv.imread(os.path.join(chesscom,theme))
        tile_white = tile[:tile.shape[1]//2,:tile.shape[0]//2,:]
        tile_black = tile[:tile.shape[1]//2,tile.shape[0]//2:tile.shape[0],:]
        tile_white = cv.resize(tile_white,dsize=(32,32))
        tile_black = cv.resize(tile_black,dsize=(32,32))
        cv.imwrite(os.path.join(sve,'white_chesscom_'+theme),tile_white)
        cv.imwrite(os.path.join(sve,'black_chesscom_'+theme),tile_black)
    for theme in os.listdir(lichess):
        tile = cv.imread(os.path.join(lichess,theme))
        tile_white = tile[:tile.shape[1],:tile.shape[0]//2,:]
        tile_black = tile[:tile.shape[1],tile.shape[0]//2:tile.shape[0],:]
        tile_white = cv.resize(tile_white,dsize=(32,32))
        tile_black = cv.resize(tile_black,dsize=(32,32))
        cv.imwrite(os.path.join(sve,'white_lichess_'+theme),tile_white)
        cv.imwrite(os.path.join(sve,'black_lichess_'+theme),tile_black)
def create_database(path):
    pieces = os.path.join(path,'pieces_png')
    tiles = os.path.join(path,'tiles','sve')
    for tile_name in os.listdir(tiles):
        tile = cv.imread(os.path.join(tiles,tile_name))
        for theme in os.listdir(pieces):
            for piece_name in os.listdir(os.path.join(pieces,theme)):
                ime = piece_name[:2].lower()
                type = piece_name[-4:]
                new_name = ime+'_'+theme+'_'+tile_name+'_'+type
                piece = cv.imread(os.path.join(pieces,theme,piece_name),cv.IMREAD_UNCHANGED)
                piece_mask = piece[:,:,3].astype(np.uint8)
                piece = piece[:,:,:3]
                piece = cv.resize(piece,dsize=(32,32))
                piece_mask = cv.resize(piece_mask,dsize=(32,32))
                piece_mask_inv = cv.bitwise_not(piece_mask)
                tile_mod = cv.bitwise_and(tile,tile,mask=piece_mask_inv)
                tile_mod = cv.add(tile_mod,piece)
                cv.imwrite(os.path.join(path,'database',new_name),tile_mod)
def make_database(path):
    pieces = os.path.join(path,'pieces_png')
    tiles = os.path.join(path,'tiles')
    x = []
    y = []
    for tile_name in os.listdir(tiles):
        tile = cv.imread(os.path.join(tiles,tile_name))
        tile = cv.resize(tile,dsize=(32,32))
        x.append(tile)
        y.append(12)
        for theme in os.listdir(pieces):
            for piece_name in os.listdir(os.path.join(pieces,theme)):
                ime = piece_name[:2].lower()
                label = code[ime]
                piece = cv.imread(os.path.join(pieces,theme,piece_name),cv.IMREAD_UNCHANGED)
                piece_mask = piece[:,:,3].astype(np.uint8)
                piece = piece[:,:,:3]
                piece = cv.resize(piece,dsize=(32,32))
                piece_mask = cv.resize(piece_mask,dsize=(32,32))
                piece_mask_inv = cv.bitwise_not(piece_mask)
                tile_mod = cv.bitwise_and(tile,tile,mask=piece_mask_inv)
                tile_mod = cv.add(tile_mod,piece)
                x.append(tile_mod)
                y.append(label)
    return np.array(x),np.array(y)
