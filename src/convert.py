import glob
import json
import os
import random
import tarfile
import zipfile
from pathlib import Path

import numpy as np
import supervisely_lib as sly

from supervisely.imaging.color import generate_rgb
from supervisely.io.fs import (
    download,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
)

# my_app = sly.AppService()
# TEAM_ID = int(os.environ['context.teamId'])
# WORKSPACE_ID = int(os.environ['context.workspaceId'])
# INPUT_DIR = os.environ.get("modal.state.slyFolder")
# INPUT_FILE = os.environ.get("modal.state.slyFile")
# PROJECT_NAME = 'cityscapes'
IMAGE_EXT = ".png"
logger = sly.logger
samplePercent = int(100) / 100

# city_tags = [
#     "munster",
#     "berlin",
#     "bielefeld",
#     "leverkusen",
#     "mainz",
#     "munich",
#     "bochum",
#     "dusseldorf",
#     "cologne",
#     "erfurt",
#     "monchengladbach",
#     "hanover",
#     "jena",
#     "ulm",
#     "tubingen",
#     "stuttgart",
#     "weimar",
#     "frankfurt",
#     "lindau",
#     "bonn",
#     "aachen",
#     "krefeld",
#     "bremen",
#     "darmstadt",
#     "hamburg",
#     "strasbourg",
#     "zurich",
# ]
# train_tag = "train"
# trainval_tag = "trainval"
# val_tag = "val"

city_classes_to_colors = {
    "unlabeled": (0, 0, 0),
    "ego vehicle": (98, 15, 138),
    "rectification border": (15, 120, 55),
    "out of roi": (125, 138, 15),
    "static": (63, 15, 138),
    "dynamic": (111, 74, 0),
    "ground": (81, 0, 81),
    "road": (128, 64, 128),
    "sidewalk": (244, 35, 232),
    "parking": (250, 170, 160),
    "rail track": (230, 150, 140),
    "building": (70, 70, 70),
    "wall": (102, 102, 156),
    "fence": (190, 153, 153),
    "guard rail": (180, 165, 180),
    "bridge": (150, 100, 100),
    "tunnel": (150, 120, 90),
    "pole": (153, 153, 153),
    "polegroup": (153, 153, 153),
    "traffic light": (250, 170, 30),
    "traffic sign": (220, 220, 0),
    "vegetation": (107, 142, 35),
    "terrain": (152, 251, 152),
    "sky": (70, 130, 180),
    "person": (220, 20, 60),
    "rider": (255, 0, 0),
    "car": (0, 0, 142),
    "truck": (0, 0, 70),
    "bus": (0, 60, 100),
    "caravan": (0, 0, 90),
    "trailer": (0, 0, 110),
    "train": (0, 80, 100),
    "motorcycle": (0, 0, 230),
    "bicycle": (119, 11, 32),
    "license plate": (0, 0, 142),
}

city_colors = list(city_classes_to_colors.values())


def json_path_to_image_path(json_path):
    img_path = json_path.replace("/gtFine/", "/leftImg8bit/")
    img_path = img_path.replace("_gtFine_polygons.json", "_leftImg8bit" + IMAGE_EXT)
    return img_path


def convert_points(simple_points):
    return [sly.PointLocation(int(p[1]), int(p[0])) for p in simple_points]


def get_split_idxs(num_imgs, percentage):
    train_sample_idxs = int(np.floor(num_imgs * percentage))
    random_idxs = random.sample(population=range(num_imgs), k=train_sample_idxs)
    return random_idxs


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    tag_metas = sly.TagMetaCollection()
    obj_classes = sly.ObjClassCollection()
    dataset_names = []

    input_dir = "./APP_DATA/cityscapes"

    new_project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    # tags_template = os.path.join(input_dir, "gtFine", "*", "*")
    # tags_paths = glob.glob(tags_template)
    # tags = [os.path.basename(tag_path) for tag_path in tags_paths]
    # if train_tag in tags and val_tag not in tags:
    #     split_train = True
    # elif trainval_tag in tags and val_tag not in tags:
    #     split_train = True
    # else:
    #     split_train = False
    search_fine = os.path.join(input_dir, "gtFine", "*", "*", "*_gt*_polygons.json")
    files_fine = glob.glob(search_fine)
    files_fine.sort()
    search_imgs = os.path.join(input_dir, "leftImg8bit", "*", "*", "*_leftImg8bit" + IMAGE_EXT)
    files_imgs = glob.glob(search_imgs)
    files_imgs.sort()
    if len(files_fine) == 0 or len(files_imgs) == 0:
        raise Exception("Input cityscapes format not correct")
    samples_count = len(files_fine)
    progress = sly.Progress("Importing images", samples_count)
    images_pathes_for_compare = []
    images_pathes = {}
    images_names = {}
    anns_data = {}
    ds_name_to_id = {}

    if samples_count > 2:
        random_train_indexes = get_split_idxs(samples_count, samplePercent)

    for idx, orig_ann_path in enumerate(files_fine):
        parent_dir, json_filename = os.path.split(os.path.abspath(orig_ann_path))
        dataset_name = os.path.basename(os.path.dirname(parent_dir))
        if dataset_name not in dataset_names:
            dataset_names.append(dataset_name)
            logger.info(f"Creating {dataset_name} dataset...")
            ds = api.dataset.create(new_project.id, dataset_name, change_name_if_conflict=True)
            ds_name_to_id[dataset_name] = ds.id
            images_pathes[dataset_name] = []
            images_names[dataset_name] = []
            anns_data[dataset_name] = []
        orig_img_path = json_path_to_image_path(orig_ann_path)
        images_pathes_for_compare.append(orig_img_path)
        if not file_exists(orig_img_path):
            logger.warn(
                "Image for annotation {} not found is dataset {}".format(
                    orig_ann_path.split("/")[-1], dataset_name
                )
            )
            continue
        images_pathes[dataset_name].append(orig_img_path)
        images_names[dataset_name].append(sly.io.fs.get_file_name_with_ext(orig_img_path))
        # tag_path = os.path.split(parent_dir)[0]
        tag_path = parent_dir
        city_tag = os.path.basename(tag_path)
        # if split_train is True and samples_count > 2:
        #     if (city_tag == train_tag) or (city_tag == trainval_tag):
        #         if idx in random_train_indexes:
        #             city_tag = train_tag
        #         else:
        #             city_tag = val_tag

        # tag_meta = sly.TagMeta(train_val_tag, sly.TagValueType.NONE)
        tag_meta = sly.TagMeta("city", sly.TagValueType.ANY_STRING)
        if not tag_metas.has_key(tag_meta.name):
            tag_metas = tag_metas.add(tag_meta)
        # tag = sly.Tag(tag_meta)
        tag = sly.Tag(meta=tag_meta, value=city_tag)
        json_data = json.load(open(orig_ann_path))
        ann = sly.Annotation.from_img_path(orig_img_path)
        for obj in json_data["objects"]:
            class_name = obj["label"]
            if class_name == "out of roi":
                polygon = obj["polygon"][:5]
                interiors = [obj["polygon"][5:]]
            else:
                polygon = obj["polygon"]
                if len(polygon) < 3:
                    logger.warn(
                        "Polygon must contain at least 3 points in ann {}, obj_class {}".format(
                            orig_ann_path, class_name
                        )
                    )
                    continue
                interiors = []
            interiors = [convert_points(interior) for interior in interiors]
            polygon = sly.Polygon(convert_points(polygon), interiors)
            if city_classes_to_colors.get(class_name, None):
                obj_class = sly.ObjClass(
                    name=class_name,
                    geometry_type=sly.Polygon,
                    color=city_classes_to_colors[class_name],
                )
            else:
                new_color = generate_rgb(city_colors)
                city_colors.append(new_color)
                obj_class = sly.ObjClass(
                    name=class_name, geometry_type=sly.Polygon, color=new_color
                )
            ann = ann.add_label(sly.Label(polygon, obj_class))
            if not obj_classes.has_key(class_name):
                obj_classes = obj_classes.add(obj_class)
        ann = ann.add_tag(tag)
        anns_data[dataset_name].append(ann)
        progress.iter_done_report()
    out_meta = sly.ProjectMeta(obj_classes=obj_classes, tag_metas=tag_metas)
    api.project.update_meta(new_project.id, out_meta.to_json())

    for ds_name, ds_id in ds_name_to_id.items():
        dst_image_infos = api.image.upload_paths(
            ds_id, images_names[ds_name], images_pathes[ds_name]
        )
        dst_image_ids = [img_info.id for img_info in dst_image_infos]
        api.annotation.upload_anns(dst_image_ids, anns_data[ds_name])

    stat_dct = {
        "samples": samples_count,
        "src_ann_cnt": len(files_fine),
        "src_img_cnt": len(files_imgs),
    }
    logger.info("Found img/ann pairs.", extra=stat_dct)
    images_without_anns = set(files_imgs) - set(images_pathes_for_compare)
    if len(images_without_anns) > 0:
        logger.warn("Found source images without corresponding annotations:")
        for im_path in images_without_anns:
            logger.warn("Annotation not found {}".format(im_path))

    logger.info(
        "Found classes.",
        extra={
            "cnt": len(obj_classes),
            "classes": sorted([obj_class.name for obj_class in obj_classes]),
        },
    )
    logger.info(
        "Created tags.",
        extra={
            "cnt": len(out_meta.tag_metas),
            "tags": sorted([tag_meta.name for tag_meta in out_meta.tag_metas]),
        },
    )
    # my_app.stop()

    return new_project
