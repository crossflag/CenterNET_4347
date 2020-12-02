# CenterNET_4347
Testing for Machine Learning project. 

# CenterNet Deep SORT

-This contains the basic instructions for installation of centernet deepsort. After this has been installed change the filepaths on the centernet_deepsort2PROJ.py
 file to meet the requirements to produce a bounded boxed video. A demo video is included with the direct submission.

-the necessary MODEL.pth file and video test file unboxed will be included in the final deliverable.

## Requirements / Installation
```bash
git clone https://github.com/kimyoon-young/centerNet-deep-sort.git
cd centerNet-deep-sort
conda env create -f CenterNet.yml
pip install -r requirments.txt
```

## Training CenterNet
- Follow installation [instructions](https://github.com/kimyoon-young/centerNet-deep-sort/blob/master/CenterNet/readme/INSTALL.md#installation)
- [Basic training command](https://github.com/kimyoon-young/centerNet-deep-sort/blob/master/CenterNet/readme/GETTING_STARTED.md#training) 
- To re-train an existing model (e.g. COCO-DLA), use the option --load_model [path_to_model]
- CUDAoutofmemory exceptions may occur; start with batch size of 16x(numGPUs) and adjust accordingly. 

Example command for training on the RedBarn workstation in M12
```bash 
python main.py ctdet --exp_id coco_dla --batch_size 16 --master_batch 15 --lr 1.25e-4  --load_model /centerNet-deep-sort/CenterNet/models/ctdet_coco_dla_2x.pth --gpus 0
```
For a COCO model that has already been retrained on IPATCH, visit https://webfiles.txstate.edu/ -> DepartmentShare/AA/COSE/CS/CS-Shares/BigDataM12/NAVAIR/CenterNetDeepSORT/model_best.pth (TXState Credentials Required)

## Evaluating Model
Follow the [benchmark evaluation instructions](https://github.com/kimyoon-young/centerNet-deep-sort/blob/master/CenterNet/readme/GETTING_STARTED.md#benchmark-evaluation), but use the model you want to evaluate rather than one from their model zoo. 

## [CNDS Tools](https://git.txstate.edu/M12/MCMT-TOP/tree/master/Tracking/CNDS%20Tools)
Used for extracting tracking data from a directory of videos and annotation files.
