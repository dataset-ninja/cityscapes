from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Cityscapes"
PROJECT_NAME_FULL: Optional[str] = "Cityscapes"

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="https://www.cityscapes-dataset.com/license/")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Domain.General()]
CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.SemanticSegmentation(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_YEAR: int = 2016
HOMEPAGE_URL: str = "https://www.cityscapes-dataset.com/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 1673790
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/cityscapes"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = None
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "unlabeled": [0, 0, 0],
    "ego vehicle": [98, 15, 138],
    "rectification border": [15, 120, 55],
    "out of roi": [125, 138, 15],
    "static": [63, 15, 138],
    "dynamic": [111, 74, 0],
    "ground": [81, 0, 81],
    "road": [128, 64, 128],
    "sidewalk": [244, 35, 232],
    "parking": [250, 170, 160],
    "rail track": [230, 150, 140],
    "building": [70, 70, 70],
    "wall": [102, 102, 156],
    "fence": [190, 153, 153],
    "guard rail": [180, 165, 180],
    "bridge": [150, 100, 100],
    "tunnel": [150, 120, 90],
    "pole": [153, 153, 153],
    "polegroup": [153, 153, 153],
    "traffic light": [250, 170, 30],
    "traffic sign": [220, 220, 0],
    "vegetation": [107, 142, 35],
    "terrain": [152, 251, 152],
    "sky": [70, 130, 180],
    "person": [220, 20, 60],
    "rider": [255, 0, 0],
    "car": [0, 0, 142],
    "truck": [0, 0, 70],
    "bus": [0, 60, 100],
    "caravan": [0, 0, 90],
    "trailer": [0, 0, 110],
    "train": [0, 80, 100],
    "motorcycle": [0, 0, 230],
    "bicycle": [119, 11, 32],
    "license plate": [0, 0, 142],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = "https://arxiv.org/pdf/1604.01685v2.pdf"
CITATION_URL: Optional[str] = "https://www.cityscapes-dataset.com/citation/"
ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "Daimler AG R&D, Germany",
    "Max Planck Institute for Informatics, Germany",
    "TU Darmstadt Visual Inference Group, Germany",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "http://www.mercedes-benz.com/en/mercedes-benz/innovation/autonomous-driving/",
    "http://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/",
    "http://www.visinf.tu-darmstadt.de/",
]

SLYTAGSPLIT: Dict[str, List[str]] = {
    "city": [
        "aachen",
        "berlin",
        "bielefeld",
        "bochum",
        "bonn",
        "bremen",
        "cologne",
        "darmstadt",
        "dusseldorf",
        "erfurt",
        "frankfurt",
        "hamburg",
        "hanover",
        "jena",
        "krefeld",
        "leverkusen",
        "lindau",
        "mainz",
        "monchengladbach",
        "munich",
        "munster",
        "strasbourg",
        "stuttgart",
        "tubingen",
        "ulm",
        "weimar",
        "zurich",
    ]
}
TAGS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }
    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["project_name_full"] = PROJECT_NAME_FULL
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    return settings
