### 脚本设置无效，已在py中写好
# eval_path='F:/train_bird/train.json'
# 我想要dev的数据
eval_path='F:/Mercury-SQL/Datasets/BIRD_dev/dev.json'
dev_path='./output/'
#db_root_path='F:/train_bird/train_databases'
db_root_path='F:/Mercury-SQL/Datasets/BIRD_dev/dev_databases'
use_knowledge='True'
not_use_knowledge='False'
mode='train' # choose dev or dev
cot='True'
no_cot='False'

YOUR_API_KEY='?'

engine1='code-davinci-002'
engine2='text-davinci-003'
engine3='gpt-3.5-turbo'

# data_output_path='./exp_result/gpt_output/'
# data_kg_output_path='./exp_result/gpt_output_kg/'

data_output_path='./exp_result/turbo_output/'
data_kg_output_path='./exp_result/turbo_output_kg/'


echo 'generate GPT3.5 batch with knowledge'
python -u ./src/gpt_request.py --db_root_path ${db_root_path} --api_key ${YOUR_API_KEY} --mode ${mode} \
--engine ${engine3} --eval_path ${eval_path} --data_output_path ${data_kg_output_path} --use_knowledge ${use_knowledge} \
--chain_of_thought ${no_cot}

# 先跳过不要外部知识的
#echo 'generate GPT3.5 batch without knowledge'
#python3 -u ./src/gpt_request.py --db_root_path ${db_root_path} --api_key ${YOUR_API_KEY} --mode ${mode} \
#--engine ${engine3} --eval_path ${eval_path} --data_output_path ${data_output_path} --use_knowledge ${not_use_knowledge} \
#--chain_of_thought ${no_cot}
