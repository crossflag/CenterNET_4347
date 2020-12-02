import numpy as np
import cv2
import os

COLORS_10 =[(144,238,144),(178, 34, 34),(221,160,221),(  0,255,  0),(  0,128,  0),(210,105, 30),(220, 20, 60),
            (192,192,192),(255,228,196),( 50,205, 50),(139,  0,139),(100,149,237),(138, 43,226),(238,130,238),
            (255,  0,255),(  0,100,  0),(127,255,  0),(255,  0,255),(  0,  0,205),(255,140,  0),(255,239,213),
            (199, 21,133),(124,252,  0),(147,112,219),(106, 90,205),(176,196,222),( 65,105,225),(173,255, 47),
            (255, 20,147),(219,112,147),(186, 85,211),(199, 21,133),(148,  0,211),(255, 99, 71),(144,238,144),
            (255,255,  0),(230,230,250),(  0,  0,255),(128,128,  0),(189,183,107),(255,255,224),(128,128,128),
            (105,105,105),( 64,224,208),(205,133, 63),(  0,128,128),( 72,209,204),(139, 69, 19),(255,245,238),
            (250,240,230),(152,251,152),(  0,255,255),(135,206,235),(  0,191,255),(176,224,230),(  0,250,154),
            (245,255,250),(240,230,140),(245,222,179),(  0,139,139),(143,188,143),(255,  0,  0),(240,128,128),
            (102,205,170),( 60,179,113),( 46,139, 87),(165, 42, 42),(178, 34, 34),(175,238,238),(255,248,220),
            (218,165, 32),(255,250,240),(253,245,230),(244,164, 96),(210,105, 30)]
waiting = []
seen = []
global fcount
fcount = 0
def draw_bbox(img, box, cls_name, identity=None, offset=(0,0)):
    '''
        draw box of an id
    '''
    x1,y1,x2,y2 = [int(i+offset[idx%2]) for idx,i in enumerate(box)]
    # set color and label text
    color = COLORS_10[identity%len(COLORS_10)] if identity is not None else COLORS_10[0]
    label = '{} {}'.format(cls_name, identity)
    # box text and bar
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    cv2.rectangle(img,(x1, y1),(x2,y2),color,2)
    cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
    cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255], 1)
    #
    return img


def draw_bboxes(img, bbox, dists, identities=None, offset=(0,0)):
    myoffset = -50
    do_stuff(img,bbox,identities)
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    

        #print("id: " + str(identities[i]) + " | " + "dist = " + str(dists[i]))
        color = COLORS_10[id%len(COLORS_10)]
        label = '{} {}'.format("Vehicle", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        #cv2.rectangle(img, (420, 480), (421, 479), color, 3)
        cv2.rectangle(img,(x1, y1 + myoffset),(x1+t_size[0]+3,y1+t_size[1]+4 + myoffset), color,-1)
        #cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
        cv2.putText(img,label,(x1,y1+t_size[1]+4 + myoffset), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    return img

def get_avg_color(imge, one_box):
    a,b,c,d = [x for x in one_box]
    new_img = imge[b:d, a:c]
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    # plt.imshow(new_img)
    # plt.show()
    new_img = cv2.resize(new_img, (1,1))
    return tuple(x for x in new_img[0,0])

# def write_to_file(fname, data_lst):
#     with open(fname, 'a') as f:
#         for dp in data_lst:
#             col_str_tup = tuple(str(x) for x in dp[2])
#             col = ' '.join(col_str_tup)
#             line = f'{dp[0]},{dp[1]},{col}\n'
#             f.write(line)

def write_to_file_HR(fname, data_lst):
    speed_const = 20
    if not os.path.isfile(fname):
        with open(fname, 'a') as f:
            f.write('ID,speed,color\n')
    with open(fname, 'a') as f:
        for dp in data_lst:
            color_str = get_color_str(dp[2])
            speed = dp[1]
            line = '{}, {:.2f},{}\n'.format(dp[0], speed, color_str)
            f.write(line)

def get_color_str(rbg_tup):
    white_const = 30
    if sum(rbg_tup) < 255:
        return 'black/gray'
    elif (abs(rbg_tup[0]-rbg_tup[1]) < white_const) and (abs(rbg_tup[0] - rbg_tup[2]) < white_const) and (abs(rbg_tup[1] - rbg_tup[2]) < white_const):
        return 'white'
    elif rbg_tup[0] > any([rbg_tup[1], rbg_tup[2]]):
        return 'red'
    elif rbg_tup[1] > any([rbg_tup[0], rbg_tup[2]]):
        return 'green'
    else:
        return 'blue'
            
def do_stuff(img, boxes, ids):
    global fcount
    fcount += 1
    n_wait_frames = 4 
    quick_ids = [x[0] for x in waiting]
    to_write = []
    for i, id_ in enumerate(ids):
        if id_ not in seen:
            current_pos = (boxes[i][0], boxes[i][1])
            if id_ in quick_ids:
                index = quick_ids.index(id_)
                if waiting[index][2] == n_wait_frames:
                    a = waiting[index][1]
                    vec = (current_pos[0] - a[0], current_pos[1] - a[1])
                    dist = ((vec[0]**2 + vec[1]**2)**.5)/(fcount - waiting[index][3])
                    color = get_avg_color(np.copy(img), boxes[i])
                    to_write.append((id_, dist, color))
                    seen.append(id_)
                else:
                    waiting[index][2]+=1
            else: 
                waiting.append([id_, current_pos, 1, fcount])
    write_to_file_HR('data_new.csv', to_write)

def softmax(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(x*5)
    return x_exp/x_exp.sum()

def softmin(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(-x)
    return x_exp/x_exp.sum()



if __name__ == '__main__':
    x = np.arange(10)/10.
    x = np.array([0.5,0.5,0.5,0.6,1.])
    y = softmax(x)
    z = softmin(x)
    import ipdb; ipdb.set_trace()