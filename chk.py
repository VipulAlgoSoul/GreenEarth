import cv2
import os

for i in os.listdir("data"):
    im = cv2.imread(os.path.join("data",i))
    imn = os.path.splitext(i)[0]+".jpg"
    cv2.imwrite(os.path.join("data",imn), im)
