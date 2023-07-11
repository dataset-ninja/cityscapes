**Cityscapes** is a dataset for instance segmentation, object detection, and semantic segmentation tasks. It is applicable or relevant across various domains. 

The dataset consists of 5000 images with 287540 labeled objects belonging to 40 different classes including *ego vehicle*, *out of roi*, *static*, and other: *pole*, *building*, *road*, *vegetation*, *car*, *sidewalk*, *traffic sign*, *sky*, *person*, *license plate*, *terrain*, *traffic light*, *bicycle*, *rectification border*, *dynamic*, *fence*, *ground*, *rider*, *wall*, *cargroup*, *parking*, *bicyclegroup*, *motorcycle*, *persongroup*, *truck*, *bus*, *polegroup*, *bridge*, *train*, *rail track*, *trailer*, *caravan*, *tunnel*, *guard rail*, *ridergroup*, *motorcyclegroup*, and *truckgroup*.

Images in the Cityscapes dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. All images are labeled (i.e. with annotations). There are 3 splits in the dataset: *test* (1525 images), *train* (2975 images), and *val* (500 images). The dataset was released in 2016 by the [Daimler AG R&D, Germany](http://www.mercedes-benz.com/en/mercedes-benz/innovation/autonomous-driving/), [Max Planck Institute for Informatics, Germany](http://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/), and [TU Darmstadt Visual Inference Group, Germany](http://www.visinf.tu-darmstadt.de/).

Here is a visualized example for 25 randomly selected sample classes:

[Dataset classes](https://github.com/dataset-ninja/cityscapes/raw/main/visualizations/classes_preview.webm)
