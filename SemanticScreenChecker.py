'''
0) run uied to get ui hierarchy json;
   taks output of JSONParser
1) compare two trees and calculate tree similarity scores
2) compare two text strings and calculate string similarity scores
3) return true means two images refer to the same screen
'''
from AugBres.JSONParser import *
from scipy import spatial
import time

class Screen:
    def __init__(self, tree=None, content=None, foundModal=False):
        self.tree = tree
        self.content = content
        self.foundModal = foundModal


    def is_content_same(self,another_content):
        same_ratio = 0.7
        same_count = 0
        i = 0
        for i in range(0,len(self.content)):
            try:
                if self.content[i] == another_content[i]:
                    same_count += 1
                elif self.content[i] == another_content[i+1]:
                    same_count += 1
                elif self.content[i] == another_content[i+2]:
                    same_count += 1
                elif self.content[i] == another_content[i-1]:
                    same_count += 1
                elif self.content[1] == another_content[i-2]:
                    same_count += 1
            except:
                break
        print(f'same_count{same_count} / length{len(self.content)} is {same_count/len(self.content)}!')
        if same_count/len(self.content) > same_ratio:
            return True
        #if self.content == another_content:
            #return True
        return False

    def is_shape_same(self,another_tree):
        global shape_similarity
        threshold = 0.955 #changed from 0.96 to 0.955
        shape_similarity = 1 - spatial.distance.cosine(self.tree.to_vec(), another_tree.to_vec())
        print(f'tree shape similarity is {shape_similarity}')
        if shape_similarity >= threshold:
            return True
        return False


    def is_tree_same(self, another_tree):
        matched_node_count = 0
        match_threshold = 0.7
        tree_similarity_threshold = 0.84
        weight = 0.7

        if self.is_shape_same(another_tree):
            org_relTree = self.tree.to_relTree()  # org_relTree: original relTree
            contr_relTree = another_tree.to_relTree()
            for org_node in org_relTree:
                if found_node_in_tree(org_node, contr_relTree):
                    matched_node_count += 1

            matched_ratio = matched_node_count / len(org_relTree)
            print(f'Matched ratio is {matched_ratio}')

            if matched_ratio > match_threshold:
                tree_similarity = weight * shape_similarity + (1 - weight) * matched_ratio
                print(f'tree shape similarity is {shape_similarity}')
                print(f'tree similarity is {tree_similarity}')
                if tree_similarity > tree_similarity_threshold:
                    return True

        return False


    def is_screen_semantic(self,another_screen):
        if self.foundModal:
            if self.is_content_same(another_screen.content):
                return True
        else:
            try:
                if self.is_tree_same(another_screen.tree):
                    return True
            except:
                print('contra or org screen has no modal!')
                return False


        return False


def is_node_correspond(orgNode, contrNode):
    xlt_threashold = 0.055
    xrd_threashold = 0.28
    y_threadhold = 0.07
    if abs(orgNode['x_lt'] - contrNode['x_lt']) < xlt_threashold and abs(orgNode['y_lt'] - contrNode['y_lt']) < y_threadhold and \
            abs(orgNode['x_rd']-contrNode['x_rd']) < xrd_threashold and abs(orgNode['y_rd']-contrNode['y_rd']) < y_threadhold:
        return True
    return False

def found_node_in_tree(rel_node, rel_tree):
    '''
    find a given node with relative coordinates in another relative node list
    '''
    for contr_node in rel_tree: #contr_node: contrast node
        print(f"Start finding node{rel_node['id']} in tree:")
        if is_node_correspond(rel_node, contr_node):
            rel_tree.remove(contr_node)
            print(f"Found orgNode{rel_node['id']} is same with contrNode{contr_node['id']}")
            return True
        #else:
            #print(
                #f"\ntop x dif between org{rel_node['id']} and contr{contr_node['id']} is {rel_node['x_lt'] - contr_node['x_lt']}; top y dif between org{rel_node['id']} and contr{contr_node['id']} is {rel_node['y_lt'] - contr_node['y_lt']}")
            #print(
                #f"down x dif is {rel_node['x_rd'] - contr_node['x_rd']}; down y dif is {rel_node['y_rd'] - contr_node['y_rd']}")
    return False


def semantic_screen_checker(br_ui, br_img, br_outputpath, rt_ui,rt_img,rt_outputpath):
    br_parResult = json_parser(
        br_ui,
        br_img,
        br_outputpath
    )
    rt_parResult = json_parser(
        rt_ui,
        rt_img,
        rt_outputpath
    )
    if isinstance(br_parResult, str):
        org_screen = Screen(content=br_parResult, foundModal=True)
        contr_screen = Screen(content=rt_parResult, foundModal=True)
    else:
        org_screen = Screen(tree=br_parResult)
        contr_screen = Screen(tree=rt_parResult)

    if org_screen.is_screen_semantic(contr_screen):
        print("Found buggy screen rt0!")
        return True
    else:
        print("The two screens are not the same!")
        return False


def test_screen_checker():
    import os

    #DIR = "/Users/yanrankou/Documents/data/3.LibreNews-21-android8-Galaxy"
    # DIR = "/Users/yanrankou/Documents/data/5.openHAB-937-android9"
    #DIR = "/Users/yanrankou/Documents/data/4.openHAB-652-android9"
    #DIR = "/Users/yanrankou/Documents/data/6.openHAB-2074-android9"
    #DIR = "/Users/yanrankou/Documents/data/7.paylist-52-android9"
    #DIR = "/Users/yanrankou/Documents/data/8.skyTube-652-android9"
    #DIR = "/Users/yanrankou/Documents/data/9.SMSSync-360-android8-Nexus6"
    #DIR = "/Users/yanrankou/Documents/data/10.SMSSync-389-android8-Nexus6"
    # DIR = "/Users/yanrankou/Documents/data/12.transistor-254-android8-Nexus6"
    DIR = "/Users/yanrankou/Documents/data/13.LibreNews-33-android8"
    test_DIR = "/Users/yanrankou/Documents/data/test_img"


    br_parResult = json_parser(
        DIR + "/br.json",
        DIR + "/processedbr.png",
        test_DIR + "/br_tree.json"
    )
    rt_parResult = json_parser(
        DIR + "/rt4.json",
        DIR + "/processedrt4.png",
        test_DIR + "/rt4_tree.json"
    )

    if isinstance(br_parResult, str):
        org_screen = Screen(content=br_parResult, foundModal=True)
        contr_screen = Screen(content=rt_parResult,foundModal=True)
    else:
        org_screen = Screen(tree=br_parResult)
        contr_screen = Screen(tree=rt_parResult)

    if org_screen.is_screen_semantic(contr_screen):
        print("Found buggy screen rt0!")
    else:
        print("The two screens are not the same!")























