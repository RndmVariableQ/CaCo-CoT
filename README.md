# CaCo-CoT
Towards CausalGPT: A Multi-Agent Approach for Faithful Knowledge Reasoning via Promoting Causal Consistency in LLMs


## Requirements

Before you proceed, make sure to install the necessary packages by running the following command:

```
pip install -r requirements.txt
```

Then, follow the steps below to download and set up the datasets:

1. **Download the ScienceQA dataset**:
   - Visit [Dataset Link](https://www.your_dataset_link_here.com) (replace this with the actual link to the dataset).
   - Download the dataset files.

2. **Directory Structure**:
   After downloading, ensure your directory structure looks like this:

```
📂 [Your_Project_Root_Directory]
│
├─📂 datasets
│ ├─📂 ScienceQA
│ │ ├─📂 train
│ │ ├─📂 test
│ │ └─📂 [Other dataset directories, if any]
│
├─📄 run_scienceqa.py
├─📄 requirements.txt
└─📄 [other project files]
```

Make sure to place all downloaded ScienceQA data into the `datasets/ScienceQA/` directory accordingly.



## Running CaCo-CoT on ScienceQA

To run text-only ScienceQA, use the command below. Remember to replace `YOUR-API-KEY` with your OpenAI API key.

```
python run_scienceqa.py \
	--data_root ./datasets/ScienceQA \
    	--label sciqa_ours_gpt_0 \
    	--test_split test \
	--txt_only \
	--num_workers 48 \
	--test_number -1 \
	--shot_number 0 \
	--top_p 0.4 \
	--temperature 0.5 \
	--seed 0 \
	--save_every 1 \
	--model gpt \
	--api_key YOUR-API-KEY \
	--api_url https://api.openai.com/v1/chat/completions \
	--method ours \
	--seed 0 \
```
