Our code is adpated from the following repo - https://github.com/ithemal/Ithemal

We modified the code to support python3 and recent torch versions


## Setup

Follow these instructions in addition to the main README.md


First step is to generate the dataset for training - for that follow the instructions in the `bhive` folder `bhive/README.md`


## Training

To train the model use `run_train.sh`
- input `ITHEMAL_HOME`: the path to the Ithemal folder
- input `DATA_PATH`: the path to the data .pt file

The data files can be downloaded from here - https://drive.google.com/drive/folders/1yGKZ-cU_YWCP2I4Dl0GC6EMCU_xy5EnU?usp=sharing

All runs model weights saved here - https://drive.google.com/drive/folders/1yGKZ-cU_YWCP2I4Dl0GC6EMCU_xy5EnU?usp=sharing

upsample_data.py is used to upsampled the weakest category based on the error distribution

get_category_errors.py can be used to reproduce the Figure 1 in the report
