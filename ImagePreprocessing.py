'''
crop an image (remove header and footer) and
resize it to 464*800 before feeding to UIED
'''

from PIL import Image
import os
from AugBres.AugBresRun import AugBres

DIR = "/home/joy/apps/crash21/input"


class ImageProcessor:
    def __init__(self):

        pass

    def runtime_img_preprocess(self, img_path):
        img = Image.open(img_path)
        width, height = img.size
        img_cropped = img.crop((0, 100, width, height - 150))
        cropped_path = f"{os.path.splitext(img_path)[0]}_processed.jpg"
        print('cropped_path', cropped_path)
        img_cropped.save(cropped_path)

        aug = AugBres()
        hirhy_dir = aug.uied_run(cropped_path)
        return cropped_path, hirhy_dir

    def bug_img_preprocess(self, img_path):
        img = Image.open(img_path)
        width, height = img.size
        if height > width:  # 图片是竖直的
            h2 = height / 2
            h4 = height / 4
        #new_size = (464, 800)
        left = 0
        top = 80
        right = width
        bottom = height - 150

        #wordpress: top 50, bottom height -50
        #wordpress23: top50, bottom height-130

        img_croped = img.crop((left, top, right, bottom))
        # new_img = img_croped.resize(new_size)
        # return new_img
        # img = cv2.resize(img, None, fx=0.5, fy=0.5)
        # gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        br_img_path = os.path.join(DIR, "br_processed.png")
        img_croped.save(br_img_path)

        aug = AugBres()
        aug.uied_run(br_img_path)
        return

    def test_img_preprocess(self):
        img = Image.open(os.path.join(DIR, "/home/joy/output/states/screen_2021-01-18_162541.jpg"))
        width, height = img.size
        new_size = (464, 800)
        img_croped = img.crop((0, 100, width, height - 150))
        new_img = img_croped.resize(new_size)
        new_img.show()
        new_img.save(os.path.join(DIR, "state1.jpg"))


def main(img_path):
    p = ImageProcessor()
    p.bug_img_preprocess(img_path)



if __name__ == '__main__':
    '''
    call main function when bug report image needs preprocessing
    '''
    #main("/home/joy/apps/crash15/input/br.png")

    '''
    execute following two statements when bug report image doesn't need preprocessing
    '''
    #augbress = AugBres()
    #augbress.uied_run(os.path.join(DIR,"br_processed.png"))
    '''
    execute for img processing experiment
    '''
    augbres = AugBres()
    augbres.uied_run_test('/home/joy/Documents/imgset/67F/rt.png')
    #augbres.uied_run_test('/home/joy/Documents/imgset/8F/screen_2021-02-15_145551_processed.jpg')

