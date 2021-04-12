'''
the main class of AugBres
1) control the main flow of AugBres
2) steps:
    2-1 gets runtime screenshot path and runs uied with it
    2-2 gets ui hierarchy json and sends to JSONParser
'''
import os
from AugBres.SemanticScreenChecker import *

DIR = '/home/joy/apps/crash21'


class AugBres():
    def __init__(self):

        pass

    def uied_run(self,img_path):
        import subprocess

        python_file = '/home/joy/UIED/run_single.py'  # uied execution python file
        os.makedirs(f"/home/joy/apps/crash21/output/{os.path.splitext(img_path)[0]}")
        output_dir = f"/home/joy/apps/crash21/output/{os.path.splitext(img_path)[0]}"  # uied output dir
        python_exe = '/home/joy/miniconda3/envs/UIED/bin/python'  # python compiler for UIED
        cmd = '%s %s %s %s' % (python_exe, python_file, img_path, output_dir)
        p = subprocess.run(cmd.split(),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        print(p.stdout.decode())
        print(p.stderr.decode())
        return output_dir

    def semantic_screen_checker_run(self,rt_img_path,rt_ui_dir):
        br_ui_path = os.path.join(DIR, 'output/home/joy/apps/crash21/input/br_processed/compo.json')
        br_img_path = os.path.join(DIR, 'input/br_processed.png')
        br_tree_path = os.path.join(DIR, 'output/trees/br_tree.json')
        rt_ui_path = os.path.join(rt_ui_dir, 'compo.json')
        state_string = os.path.splitext(os.path.basename(rt_img_path))[0]
        rt_tree_path = os.path.join(DIR,f'output/trees/{state_string}_tree.json')
        is_screen_same = semantic_screen_checker(
            br_ui_path,br_img_path,br_tree_path,
            rt_ui_path,rt_img_path,rt_tree_path
        )
        return is_screen_same

    def uied_run_test(self,img_path):
        import subprocess

        python_file = '/home/joy/UIED/run_single.py'  # uied execution python file
        os.makedirs(f"/home/joy/Documents/imgset/67F/uied_rt")
        output_dir = f"/home/joy/Documents/imgset/67F/uied_rt"  # uied output dir
        python_exe = '/home/joy/miniconda3/envs/UIED/bin/python'  # python compiler for UIED
        cmd = '%s %s %s %s' % (python_exe, python_file, img_path, output_dir)
        p = subprocess.run(cmd.split(),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        print(p.stdout.decode())
        print(p.stderr.decode())
        return output_dir

    def semantic_screen_test(self):
        br_ui_path = '/home/joy/Documents/imgset/67F/uied_br/compo.json'
        br_img_path = '/home/joy/Documents/imgset/67F/br_processed.png'
        br_tree_path = '/home/joy/Documents/imgset/67F/br_tree.json'
        rt_ui_path = '/home/joy/Documents/imgset/67F/uied_rt/compo.json'
        rt_img_path = '/home/joy/Documents/imgset/67F/rt.png'
        rt_tree_path = '/home/joy/Documents/imgset/67F/rt_tree.json'
        is_screen_same = semantic_screen_checker(
            br_ui_path, br_img_path, br_tree_path,
            rt_ui_path, rt_img_path, rt_tree_path
        )
        return is_screen_same

    def debugging(self):
        semantic_screen_checker(
            "/home/joy/8.skyTube-652-android9/output/home/joy/50.wordpress-11745-android10/input/br_processed/compo.json",
            "/home/joy/8.skyTube-652-android9/input/br_processed.jpg",
            "/home/joy/output/br_tree.json",
            "/home/joy/8.skyTube-652-android9/output/8.skyTube-652-android9/output/droidbot/states/screen_2021-01-26_160157_processed/compo.json",
            "/home/joy/8.skyTube-652-android9/output/droidbot/states/screen_2021-01-26_160157_processed.jpg",
            "/home/joy/output/rt_tree.json",
        )

if __name__ == '__main__':
    aug = AugBres()
    #aug.debugging()
    aug.semantic_screen_test()