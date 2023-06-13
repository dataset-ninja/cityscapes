from typing import Dict, List, Optional, Union

from dataset_tools.templates import AnnotationType, CVTask, Industry, License

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Cityscapes"
PROJECT_NAME_FULL: Optional[str] = None

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="https://www.cityscapes-dataset.com/license/")
INDUSTRIES: List[Industry] = [Industry.GeneralDomain()]
CV_TASKS: List[CVTask] = [CVTask.InstanceSegmentation(), CVTask.ObjectDetection(), CVTask.SemanticSegmentation()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_YEAR: int = 2016
HOMEPAGE_URL: str = "https://www.cityscapes-dataset.com/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 370882
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/cityscapes"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = None
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = "https://arxiv.org/pdf/1604.01685v2.pdf"
CITATION_URL: Optional[str] = "https://www.cityscapes-dataset.com/citation/"
ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["Daimler AG R&D", "Max Planck Institute for Informatics", "TU Darmstadt Visual Inference Group"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["http://www.mercedes-benz.com/en/mercedes-benz/innovation/autonomous-driving/", "http://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/", "http://www.visinf.tu-darmstadt.de/"]
TAGS: List[str] = None

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
        "industries": INDUSTRIES,
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
    settings["tags"] = TAGS if TAGS is not None else []

    return settings