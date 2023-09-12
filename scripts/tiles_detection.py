import cv2 as cv
import numpy as np

def contour_is_square(cont):
    x,y,w,h = cv.boundingRect(cont)
    area = cv.contourArea(cont)
    scale = area/(w*h)
    sq_scale = w/h
    return scale>0.8 and scale<1.2 and sq_scale<1.1 and sq_scale>0.9

def extract_table_box(img_path,padding=20,show = False):
    img = cv.imread(img_path)
    val = (int(img[0,0,0]),int(img[0,0,1]),int(img[0,0,2]))
    if padding>0:
        img = cv.copyMakeBorder(img,padding,padding,padding,padding,cv.BORDER_CONSTANT,value=val)
    if show:
        cv.imshow('img',img)
    img_gray0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_gray = cv.bilateralFilter(img_gray0,9,150,150)
    img_gray = img_gray0
    img_canny = cv.Canny(img_gray, 250, 250, apertureSize=3)
    img_canny = cv.dilate(img_canny,kernel=np.ones((3,3)))
    if show:
        cv.imshow('img_canny', img_canny)
    contours, hierarchy = cv.findContours(img_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    hierarchy=hierarchy[0]
    rects = np.array([[id,cont] for id,cont in enumerate(contours) if contour_is_square(cont)],dtype = np.ndarray)
    cont_areas = np.array([cv.contourArea(cont) for cont in contours],dtype = np.ndarray)
    rect_areas = np.array([cv.contourArea(rect[1]) for rect in rects])
    boxes = np.array([cv.boundingRect(cont[1]) for cont in rects])
    id = np.argmax(rect_areas)
    id = rects[id][0]
    while hierarchy[id][2]!=-1:
        child_id = hierarchy[id][2]
        if contour_is_square(contours[child_id]) and cv.contourArea(contours[child_id]) / cv.contourArea(
                contours[id]) > 1. / 10:
            id = child_id
        else:
            break

    tabla_cont = contours[id]
    tabla_box = cv.boundingRect(tabla_cont)
    x, y, w, h = tabla_box
    tabla = img[y:y+h, x:x+w, :]
    if show:
        cv.imshow('tabla1',tabla)
        cv.waitKey(0)
    tabla = cv.resize(tabla, dsize=(256, 256), fx=0, fy=0)
    polje_d = 32
    tabla = np.array([[tabla[j*polje_d:(j+1)*polje_d,i*polje_d:(i+1)*polje_d,:] for j in range(8)] for i in range(8)])
    return tabla