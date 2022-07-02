import os
import shutil
from datetime import datetime
from pathlib import Path
import threading
from collections import OrderedDict
from teplakokkaBot import get_settings

image_list = []
list_detect = []
result_list = []
tmp = get_settings.get_dir_tmp()
dirs = get_settings.get_dir_dirs()


def check_new_image():
    # проверяет появились ли новые файлы во времненной директории
    global image_list
    global isDetect

    for files in os.listdir(tmp):
        image_list.append(tmp+'/'+files)

    if len(image_list):
        isDetect = True
        print("found image in directory! Thread name is ***{}*** \n".format(threading.current_thread().name))
        result_list.clear()
        result_list.append(OrderedDict.fromkeys(image_list))
        result_list.append(isDetect)
        return result_list
    else:
        isDetect = False
        result_list.append([])
        result_list.append(isDetect)
        return result_list


def move_image_to_dir(list_paths):
    # перемещает файлы из временной директории в постоянное хранилище
    global isDetect
    global result_list
    day, month, year = datetime.today().strftime('%d.%B.%Y').split('.')
    hours = datetime.now().strftime('%H%M%S')
    for paths in list_paths:
        #
        try:
            if not os.path.exists(paths):
                shutil.move(paths, dirs)
            else:
                suffix = Path(paths).suffix
                p = shutil.copy(paths, os.path.dirname(paths) + '/' + day + hours + suffix)
                os.remove(paths)
                shutil.move(p, dirs)

        except shutil.Error as e:
            print('пока хз придумаем потом {}\n'.format(e))

    print("move_image_to_dir - is done!\n")
    result_list.clear()
    isDetect = False
    image_list.clear()



