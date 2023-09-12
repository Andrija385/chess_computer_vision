from tensorflow_neural_net import *
import numpy as np
import cv2 as cv
def get_fig():
    fig={}
    fig[0] = 'K'
    fig[1] = 'Q'
    fig[2] = 'R'
    fig[3] = 'B'
    fig[4] = 'N'
    fig[5] = 'P'
    fig[6] = 'k'
    fig[7] = 'q'
    fig[8] = 'r'
    fig[9] = 'b'
    fig[10] = 'n'
    fig[11] = 'p'
    return fig
def generate_fen(table,model_number):
    model = create_model100(True)
    tabla=table.reshape((-1,32,32,3))
    tabla = np.array([cv.cvtColor(img,cv.COLOR_BGR2GRAY) for img in tabla])
    predictions = model.predict(tabla,verbose=False)
    predictions = np.argmax(predictions,axis=1)
    predictions = np.transpose(predictions.reshape((8,8)))
    ans = ''
    fig=get_fig()
    for i in range(8):
        cnt = 0
        for j in range(8):
            if predictions[i,j] == 12:
                cnt += 1
            else:
                if cnt > 0:
                    ans += str(cnt)
                ans += fig[predictions[i, j]]
                cnt = 0
        if cnt > 0:
            ans += str(cnt)
        ans += '/'
    return ans[:-1]
def flipped(fen):
    return '/'.join(reversed([row[::-1] for row in fen.split('/')]))