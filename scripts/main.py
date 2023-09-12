from tiles_detection import *
from generate_fen import *
from stockfish import Stockfish
import webbrowser
tf.get_logger().setLevel('ERROR')

path = "C:\\Users\\Andrija\\Downloads\\375764444_1666809590397089_3973586229311863932_n.png"
data_path = '../../superset/database'
model_number=100


tabla = extract_table_box(path,20,show=False)

fen = generate_fen(tabla,model_number)
is_flipped = input('is the board flipped?')
if is_flipped.lower()=="yes":
    fen = flipped(fen)
move = input('whose move it is?(w/b)')
if move == 'w':
    fen+=' w'
elif move=='b':
    fen+=' b'
else:
    print('unvalid input')
    exit(0)
#fen += ' KQkq - 0 1'
print(fen)
sf = Stockfish('C:/Users/Andrija/Downloads/stockfish/stockfish-windows-x86-64-avx2.exe',depth=25)
ok = True
open_web = input('do you want to open lichess.org analysis?(yes/no)')
if not ok:
    print('fen is not valid')
    if open_web == 'yes':
        webbrowser.open('https://lichess.org/editor/' + fen)
    exit(0)

sf.set_fen_position(fen)
move = sf.get_best_move()
eval = sf.get_evaluation()
print(eval)
print(move)

if open_web == 'yes':
    webbrowser.open('https://lichess.org/editor/'+fen)