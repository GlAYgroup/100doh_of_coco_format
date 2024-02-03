import json
import collections as cl
import os

def get_info():
    tmp = cl.OrderedDict()
    tmp["description"] = "100doh dataset of coco format"
    tmp["url"] = ""
    tmp["version"] = "1"
    tmp["year"] = 2024
    tmp["contributor"] = ""
    tmp["data_created"] = "2024/01/01"
    return tmp

def get_licenses():
    tmp = cl.OrderedDict()
    tmp["id"] = 0
    tmp["url"] = ""
    tmp["name"] = ""
    return tmp

def get_image_data(id, annotation, image_file):
    tmp = cl.OrderedDict()
    tmp["license"] = 0
    tmp["file_name"] = image_file
    tmp["coco_url"] = ""
    tmp["height"] = annotation["height"] 
    tmp["width"] = annotation["width"]
    tmp["date_captured"] = ""
    tmp["flickr_url"] = ""
    tmp["id"] = id
    return tmp

def get_categories():
    tmps = []
    sup = ["N/A", "hand", "object"]
    categories = ["N/A", "hand", "object"]
    for i in range(len(categories)):
        tmp = cl.OrderedDict()
        tmp["id"] = i
        tmp["supercategory"] = sup[i]
        tmp["name"] = categories[i]
        tmps.append(tmp)
    return tmps

def main(annotation_dir, json_path):
   
    with open(annotation_dir) as f:
        annotations_origin = json.load(f)

    image_list = annotations_origin.keys()
    print(type(image_list))
    print(len(image_list))

    info = get_info()
    licenses = get_licenses()
    categories = get_categories()
    images = []
    annotations = []

    # get image data and annotations
    count_ano_id = 0
    for i, image_file in enumerate(image_list):    
        annotation_origin = annotations_origin[image_file]
        image_data = get_image_data(i, annotation_origin[0], image_file)

        # get annotation per image
        old_obj_bbox = None # 同一画像内の1つ前のobj_bboxを保存しておく
        for side_annotation in annotation_origin:
            side_annotation_dict = cl.OrderedDict()

            new_hand_bbox = [side_annotation["x1"] * side_annotation["width"],
                side_annotation["y1"] * side_annotation["height"],
                side_annotation["x2"] * side_annotation["width"] - side_annotation["x1"] * side_annotation["width"],
                side_annotation["y2"] * side_annotation["height"] - side_annotation["y1"] * side_annotation["height"]]
            
            side_annotation_dict["segmentation"] = []
            side_annotation_dict["id"] = count_ano_id
            count_ano_id += 1
            side_annotation_dict["image_id"] = i
            side_annotation_dict["category_id"] = 1
            side_annotation_dict["area"] = new_hand_bbox[2] * new_hand_bbox[3]
            side_annotation_dict["iscrowd"] = 0
            side_annotation_dict["bbox"] = new_hand_bbox

            annotations.append(side_annotation_dict)

                
            if side_annotation["obj_bbox"] is not None:
                side_obj_annotation_dict = cl.OrderedDict()

                new_obj_bbox = [side_annotation["obj_bbox"]["x1"] * side_annotation["width"],
                                side_annotation["obj_bbox"]["y1"] * side_annotation["height"],
                                side_annotation["obj_bbox"]["x2"] * side_annotation["width"] - side_annotation["obj_bbox"]["x1"] * side_annotation["width"],
                                side_annotation["obj_bbox"]["y2"] * side_annotation["height"] - side_annotation["obj_bbox"]["y1"] * side_annotation["height"]]
                
                side_obj_annotation_dict["segmentation"] = []
                side_obj_annotation_dict["id"] = count_ano_id
                count_ano_id += 1
                side_obj_annotation_dict["image_id"] = i
                side_obj_annotation_dict["category_id"] = 2
                side_obj_annotation_dict["area"] = new_obj_bbox[2] * new_obj_bbox[3]
                side_obj_annotation_dict["iscrowd"] = 0
                side_obj_annotation_dict["bbox"] = new_obj_bbox

                if new_obj_bbox != old_obj_bbox:
                    annotations.append(side_obj_annotation_dict)
                old_obj_bbox = new_obj_bbox

        images.append(image_data)
    print("Made file")

    json_data = {
        'info': info,
        'images': images,
        'licenses': licenses,
        'annotations': annotations,
        'categories': categories,
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


annotation_dir_list = ["check_trainval.json", "trainval.json", "check_test.json", "test.json"]
json_path_list = ["check_trainval_cocof.json", "trainval_cocof.json", "check_test_cocof.json", "test_cocof.json"]
for a, j in zip(annotation_dir_list, json_path_list):
    print(a, j)
    main(a, j)
