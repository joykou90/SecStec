'''
takes the output of UIED
1) check is modal or not
2) to_tree if not modal
3) to_text if modal
'''

import os
import json
from AugBres.UITree import *


class Hierarchy():
    def __init__(self,jfile):
        with open (jfile) as f:
            data = json.load(f)
        self.hierarchy = data['compos']


    def found_modal(self):
        '''
        modal:
          120 < height < 400
          310< width < 480
          x_center = width/2 + col_min
          y_center = height/2 + row_min
          190 < x < 350
          370< y < 460
          type == 'compos' or 'block

        '''
        for node in self.hierarchy[1:]:
            if node['class'] != 'Text':
                height = node['height']
                width = node['width']
                if 120 < height < 400 and 310 < width < 480:
                    row_min = node['row_min']
                    col_min = node['column_min']
                    x = width / 2 + col_min
                    y = height / 2 + row_min
                    if 190 < x < 350 and 370 < y < 460:
                        print("Found Modal!")
                        return True
        return False


    def to_tree(self, output_path):
        tree = UITree(self.hierarchy)
        tree.build_ui_tree()
        tree.output_ui_tree(output_path)
        return tree

    def to_text(self,img_path):
        import numpy as np
        import pytesseract
        from PIL import Image
        import string

        pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # r"installation path of tesseract"

        img = Image.open(img_path)
        width, height = img.size

        if height > width:
            h2 = height / 2
            h4 = height / 4
        left = 0
        top = h4
        right = width
        bottom = 3 * h4
        img_croped = img.crop((left, top, right, bottom)) #crop the modal window area
        img_croped.show()

        config = "--psm 3"  # pagesegmode values; 3 is the default value
        text = pytesseract.image_to_string(img_croped, config=config)
        new_text = text.translate({ord(c): None for c in string.whitespace})

        print(new_text)
        return new_text


def json_parser(uifile, img, output_path):
    new_hierarchy = Hierarchy(uifile)
    if new_hierarchy.found_modal():
        text = new_hierarchy.to_text(img)
        return text
    else:
        tree = new_hierarchy.to_tree(output_path)
        return tree



def test_json_parser():
    # DIR = "/Users/yanrankou/Documents/data/3.LibreNews-21-android8-Galaxy"
    # DIR = "/Users/yanrankou/Documents/data/5.openHAB-937-android9"
    DIR = "/Users/yanrankou/Documents/data/4.openHAB-652-android9"
    # DIR = "/Users/yanrankou/Documents/data/6.openHAB-2074-android9"
    # DIR = "/Users/yanrankou/Documents/data/7.paylist-52-android9"
    # DIR = "/Users/yanrankou/Documents/data/8.skyTube-652-android9"
    # DIR = "/Users/yanrankou/Documents/data/9.SMSSync-360-android8-Nexus6"
    # DIR = "10.SMSSync-389-android8-Nexus6"
    # DIR = "/Users/yanrankou/Documents/data/12.transistor-254-android8-Nexus6"

    file_name = "br.json"
    img_name = "br.png"
    ui_path = os.path.join(DIR, file_name)
    img_path = os.path.join(DIR, img_name)
    output_dir = "/Users/yanrankou/Documents/data/test_img"
    output_file_name = "tree.json"
    output_path = os.path.join(output_dir, output_file_name)

    br_hierarchy = Hierarchy(ui_path)
    if br_hierarchy.found_modal():
        content = br_hierarchy.to_text(img_path)
        print(content)
        return content
    else:
        br_tree = br_hierarchy.to_tree(output_path)
        return br_tree



#if __name__ == '__main__':
    #test_json_parser()


