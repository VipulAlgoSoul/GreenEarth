from ultralytics import YOLO
import cv2
import numpy as np
import os
# load the model
model = YOLO('yolov9e.pt')

remap_dict={"waste":[27,33,32,34,35,39,29,40,41,42,43,44,45,64,65,75,74,76,77,78,79],
            "locator_waste":[61,62,63,67,68,69,70,71,72],
            "missing_waste":[67,73,24,26,38],
            "human":[0],
            "living_things":[14,15,16,17,18,19,20],
            "bio_waste":[46,47,48,49,50,51,52,53,54,55]}



for im in os.listdir("data"):
    img = cv2.imread(os.path.join("data",im))

    # make the prediction
    results = model(img)

    # get the first result (we only have one image)
    result = results[0]

    # convert the results to numpy arrays
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype=int)
    classes = np.array(result.boxes.cls.cpu(), dtype=int)

    box_color = (0, 255, 0)
    center_color = (0, 0, 255)
    thickness = 2
    font_scale = 2

    # draw the bounding boxes and the class names
    for cls, bbox in zip(classes, bboxes):
        x1, y1, x2, y2 = bbox

        cv2.rectangle(img, (x1, y1), (x2, y2), box_color, thickness)

        try:
            result_name = [i for i in remap_dict.keys() if cls in remap_dict[i]][0]
        except:
            result_name = result.names[cls]
        cv2.putText(img, result_name, (x1, y1 - 5), cv2.FONT_HERSHEY_PLAIN, font_scale, box_color, thickness)

    # # opens the preview window
    # cv2.imshow('preview', img)
    # # waits for user to press any key
    # # (this is necessary to avoid Python kernel form crashing)
    # cv2.waitKey(0)
    # # closing all open windows
    # cv2.destroyAllWindows()
    cv2.imwrite(os.path.join("results",im),img)