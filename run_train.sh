export CUDA_VISIBLE_DEVICES=6
export ITHEMAL_HOME="Ithemal"
export EXPERIMENT_NAME="hsw"
export EXPERIMENT_TIME="lstm_upsampled"
export DATA_PATH="Ithemal/hsw_bhive_ithemal_dataset_v3_upsampled.pt"

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

