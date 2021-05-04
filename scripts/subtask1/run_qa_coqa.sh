python run_qa.py \
 --dataset_name '../datasets/coqa/coqa.py' \
 --dataset_config_name coqa_rc \
 --model_name_or_path bert-large-uncased-whole-word-masking \
 --do_train \
 --do_eval \
 --logging_steps 2000 \
 --save_steps 2000 \
 --learning_rate 3e-5  \
 --num_train_epochs 5 \
 --max_seq_length 512  \
 --max_answer_length 80 \
 --doc_stride 64 \
 --cache_dir /root/sharedtask-dialdoc2021/coqa-cache \
 --output_dir /root/sharedtask-dialdoc2021/coqa-output \
 --overwrite_output_dir  \
 --per_device_train_batch_size 8 \
 --gradient_accumulation_steps 2  \
 --warmup_steps 1000 \
 --weight_decay 0.01  \
 --fp16 
