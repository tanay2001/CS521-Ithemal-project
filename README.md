Our code is adpated from the following repo - https://github.com/ithemal/Ithemal

**We modified the code to support python3 and recent torch versions**


## Setup

Follow these instructions in addition to the [README_ithemal.md](https://github.com/tanay2001/CS521-Ithemal-project/blob/main/README_ithemal.md)


First step is to generate the dataset for training - for that follow the instructions in the `bhive` folder `bhive/README.md`


## Training

To train the model use `run_train.sh`

```
export ITHEMAL_HOME=""
export EXPERIMENT_NAME=""
export EXPERIMENT_TIME=""
export DATA_PATH=""

python3 learning/pytorch/ithemal/run_ithemal.py \
        --data $DATA_PATH --use-rnn \
        --rnn-lstm \
        train \
        --experiment-name $EXPERIMENT_NAME \
        --experiment-time $EXPERIMENT_TIME \
        --sgd \
        --threads 4 \
        --trainers 6 \
        --weird-lr \
        --decay-lr  \
        --epochs 100 \

```


- `ITHEMAL_HOME`: the path to the Ithemal folder
- `EXPERIMENT_NAME` is the folder name to checkpoints the runs and model weights
- `EXPERIMENT_TIME` this acts like the subfolder in `EXPERIMENT_NAME`
- `DATA_PATH`: the path to the data .pt file, this should be generated following the instructions in the [bhive](https://github.com/tanay2001/CS521-Ithemal-project/blob/main/bhive/README.md) readme

## Dowloading Options

The data files (.pt files) can be downloaded from here - https://drive.google.com/drive/folders/1yGKZ-cU_YWCP2I4Dl0GC6EMCU_xy5EnU?usp=sharing

All our runs model weights saved here - https://drive.google.com/drive/folders/1yGKZ-cU_YWCP2I4Dl0GC6EMCU_xy5EnU?usp=sharing

## Extra
upsample_data.py is used to upsampled the weakest category based on the error distribution

get_category_errors.py can be used to reproduce the Figure 1 in the report
