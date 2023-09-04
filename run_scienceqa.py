import os
import re
import json
import argparse
import random
from tqdm import tqdm
# from prompts.scienceqa_base_prompt import *
from retry import retry
import openai
import requests
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import concurrent
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from prompts.prompts_scienceqa_ours_os_claude import *



def load_data(args):
    problems = json.load(open(os.path.join(args.data_root, 'problems.json')))
    pid_splits = json.load(open(os.path.join(args.data_root, 'pid_splits.json')))

    qids = pid_splits['%s' % (args.test_split)]
    qids = qids[:args.test_number] if args.test_number > 0 else qids
    print(f"number of test problems: {len(qids)}\n")

    if args.txt_only:
        txt_qids = []
        for qid in qids:
            if problems[qid]['image'] == None:
                txt_qids.append(qid) 
        print('Number of text-only questions: ', len(txt_qids))

    # pick up shot examples from the training set
    shot_qids = args.shot_qids
    train_qids = pid_splits['train']
    if shot_qids == None:
        assert args.shot_number >= 0 and args.shot_number <= 32
        shot_qids = random.sample(train_qids, args.shot_number)  # random sample
    else:
        shot_qids = [str(qid) for qid in shot_qids]

    print("training question ids for prompting: ", shot_qids, "\n")

    return problems, txt_qids, shot_qids


@retry(delay=5, tries=10, backoff=2, max_delay=120)
def get_single_run_claude(cot_prompt, prompt, args): 

    anthropic = Anthropic(api_key=args.key)
    response = anthropic.completions.create(
        model="claude-1",
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens_to_sample=3000,
        prompt=f"{HUMAN_PROMPT} {prompt+cot_prompt} {AI_PROMPT}",
    )

    return response.completion


@retry(delay=5, tries=15, backoff=2, max_delay=120)
def get_single_run_gpt(cot_prompt, prompt, args): 
    headers = {
            'Authorization': f'Bearer ' + args.api_key, 
            'Content-Type': 'application/json'
            }

    response = requests.post(args.api_url, 
                            headers=headers, 
                            json={
                                "model": 'gpt-3.5-turbo',
                                "messages": [
                                    {'role': 'user', 'content': prompt}, 
                                    ],
                                "temperature": args.temperature,
                                "top_p": args.top_p,
                                }).json()
    
    return response['choices'][0]['message']['content']



# @retry(delay=10, tries=5, backoff=2, max_delay=120)
def get_single_result(qid, prompt, choice, args): 
    if args.model == 'claude':
        get_single_run = get_single_run_claude
    elif args.model == 'gpt':
        get_single_run = get_single_run_gpt
    else:
        raise NotImplementedError('undefined model')

    if 'self-consistent' in args.method or 'complexity' in args.method:
        answers = []
        outputs = ''
        n_chains = []
        for i in range(10): 
            cot_prompt = 'Let\'s think step by step. '
            response = get_single_run(cot_prompt, prompt, args)
            output = response

            n_chain = output.count('\n') - output.count('\n\n') + 1
            n_chains.append(n_chain) # \n or \n\n + 1 as number of chains
            outputs += '\n' + '-'*50 + f'\n\nRound {i+1} #Chain {n_chain} \n Output: {output}'
            answer = filter_output(output, choice)
            answers.append(answer)

            # print(answer)

            
        if 'complexity' in args.method: # filter out those with a shorter reasoning chain
            longchain_indices = np.argsort(n_chains)[-int(0.6*len(n_chains)):] # indices of those with more chains
            answers = np.array(answers)[longchain_indices]

        answer = max(set(answers), key=list(answers).count)
        output = outputs
        # print(answer, output)

    elif args.method in ['zeroshot-cot']:
        output = get_single_run('Let\'s think step by step. ', prompt, args)
        answer = filter_output(output, choice)

    elif args.method in ['base', 'oneshot-cot', 'zeroshot-cot']:
        output = get_single_run('', prompt, args)
        answer = filter_output(output, choice)

    elif args.method == 'least-to-most':
        # PROBLEM DECOMPOSITION
        response = get_single_run('', prompt, args)
        output = response
        
        subquestion_list = re.findall(r'<subquestion>(.*?)</subquestion>', output)

        original_question = prompt.split('Judge whether the sentense is true or false: ')[-1]
        messages = f"{least_to_most_subq_solver_prompt}Now, the context is: \n{original_question}"
        # PROBLEM SOLVING {original_question } {AI_PROMPT}
        for subq in subquestion_list: 
            messages += '\nQ: ' + subq
            
            ans = get_single_run('', messages, args)
            if 'A:' not in ans:
                messages += '\nA: ' + ans + '\n\n'
            else:
                messages += '\nA:' + ans.split('A:')[1] + '\n\n'
        
        messages += f"\nQ: Is the sentense true or false, \"{original_question}\"? Your reply MUST include '<Answer>True</Answer>' or '<Answer>False</Answer>' at the end."
        ans = get_single_run('', messages, args)
        messages += '\nA: ' + ans + '\n\n'
        answer = filter_output(ans, choice)
        output = messages.split(f'Now, the context is: \n{original_question}')[1]
                  
    elif args.method == 'ours':
        answer, output = answer_review(question=prompt, choice=choice, depth=1, history='', args=args)
        
    return qid, answer, output



from time import sleep
@retry(delay=3, tries=10, backoff=2, max_delay=120)
def answer_review(question=None, choice=None, depth=1, history='', args=None):
    if args.model == 'claude':
        get_single_run = get_single_run_claude
    elif args.model == 'gpt':
        get_single_run = get_single_run_gpt
    else:
        raise NotImplementedError('undefined model')

    output_1 = get_single_run(None, our_reasoner1_prompt + question, args)
    answer_1 = filter_output(output_1, choice=choice)

    sleep(0.1)
    output_2 = get_single_run(None, our_reasoner2_prompt + question, args)
    answer_2 = filter_output(output_2, choice=choice)

    history += f" ########## Round {depth} ########## \n" + str(output_1 + '\n\n' + '-'*30 + '\n\n' + output_2 + '\n\n')

    answers = []

    if answer_1 == answer_2: 

        lst = ['A', 'B', 'C', 'D', 'E']
        lst = lst[:len(choice)]
        lst.pop(lst.index(answer_1))

        answer_cf = np.random.choice(lst)
        reviewer_prompt1 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\" \n\n\nA possible solution is: \n\"\"\"\n{np.random.choice([output_1, output_2])}\n\"\"\"\n\nPlease provide your evaluation, while looking out for option ({answer_cf}). Remember, if the answer cannot be determined, make an educated guess at the end. "

        reviewer_output_3 = get_single_run(None, reviewer_prompt1, args)
        answer_3 = filter_output(reviewer_output_3, choice)

        history += f" ######## Round {depth} Review ######## \n\n" + str(reviewer_output_3 + '\n\n' + '='*30 + '\n\n')

        answers = [answer_1, answer_2, answer_3]
        max_answer = max(set(answers), key=answers.count)

        if answer_3 == answer_1: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} CF: {answer_cf}  >>> all consensus \n\n'
            return answer_3, history
        elif depth >= 4: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} CF: {answer_cf} >>> reach max depth\n\n'
            return np.random.choice([answer_1, answer_2,]), history
        else: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} CF: {answer_cf} >>> go deeper\n\n'
            return answer_review(question=question, choice=choice, depth=depth+1, history=history, args=args)

    elif answer_1 != answer_2: 

        reviewer_prompt1 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\" \n\n\nA possible solution is: \n\"\"\"\n{output_1}\n\"\"\"\n\nPlease provide your evaluation, while looking out for option ({answer_2}). Remember, if the answer cannot be determined, make an educated guess at the end. "
        reviewer_prompt2 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\" \n\n\nA possible solution is: \n\"\"\"\n{output_2}\n\"\"\"\n\nPlease provide your evaluation, while looking out for option ({answer_1}). Remember, if the answer cannot be determined, make an educated guess at the end. "

        reviewer_output_3 = get_single_run(None, reviewer_prompt1, args)
        reviewer_output_4 = get_single_run(None, reviewer_prompt2, args)
        
        answer_3 = filter_output(reviewer_output_3, choice)
        answer_4 = filter_output(reviewer_output_4, choice)

        history += f" ######## Round {depth} Review ######## \n\n" + str(reviewer_output_3 + '\n\n' + '-'*30 + '\n\n' + reviewer_output_4 + '\n\n' + '='*30 + '\n\n')

        answers = [answer_1, answer_2, answer_3, answer_4]
        max_answer = max(set(answers), key=answers.count)

        if answer_3 == answer_4: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> evaluators\' consensus \n\n'
            return answer_3, history
        elif depth >= 4: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> reach the max depth\n\n'
            return np.random.choice([answer_1, answer_2]), history
        else: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> go deeper\n\n'
            return answer_review(question=question, choice=choice, depth=depth+1, history=history, args=args)




def filter_output(output, choice):

    tags = re.findall(r'<Answer>(.*?)</Answer>', output)
    if len(tags) == 0:
        answer = output
    else:
        answer = tags[-1]
    
    num_choice = len(choice)
    # print(choice)
    if len(answer) == 1 and answer in ['A', 'B', 'C', 'D', 'E'][:num_choice]:
        return answer[0]
    
    elif answer in choice:
        return ['A', 'B', 'C', 'D', 'E'][choice.index(answer)]
    
    elif 'cannot' in answer.lower():
        return ['A', 'B', 'C', 'D', 'E'][random.choice(range(num_choice))]
    
    else: 
        answer = [a for a in ['A', 'B', 'C', 'D', 'E'][:num_choice] if a in answer]
        # print(answer)
        if len(answer) == 1: 
            return answer[-1]
        elif len(answer) > 1:
            return answer[random.choice(range(len(answer)))]
        else:
            return ['A', 'B', 'C', 'D', 'E'][random.choice(range(num_choice))]



def get_pred_idx(prediction, choices, options):
    """
    Get the index (e.g. 2) from the prediction (e.g. 'C')
    """
    if prediction in options[:len(choices)]:
        return options.index(prediction)
    else:
        return random.choice(range(len(choices)))


from prompts.scienceqa_base_prompt import *
def build_prompt_sciqa(problems, qid, args):
    question = get_question_text(problems[qid])
    context = get_context_text(problems[qid], args.use_caption)
    choice = get_choice_text(problems[qid], args.options)
    answer = get_answer(problems[qid], args.options)
    lecture = get_lecture_text(problems[qid])
    solution = get_solution_text(problems[qid])
    test_example = create_one_example(args.prompt_format,
                                      question,
                                      context,
                                      choice,
                                      answer,
                                      lecture,
                                      solution,
                                      test_example=True)
    # print(test_example)
    # exit(0)

    if args.method == 'base':
        prompt = base_prompt + test_example
    elif args.method in ['zeroshot-cot', 'zs-self-consistent', 'zs-complexity']:
        prompt = zeroshot_cot_prompt + test_example
    elif args.method in ['oneshot-cot', 'os-self-consistent', 'os-complexity']:
        prompt = one_shot_cot_prompt + test_example # cot_prompt + 
    elif args.method == 'ours':
        prompt = f"\"\"\"\n{test_example}\n\"\"\""
    elif args.method == 'least-to-most':
        prompt = least_to_most_decomposer_prompt + \
f"""
Now, provide the sub-questions for the question: 
Q: 
    Judge whether the sentense is true or false: {test_example}"""

    else:
        raise NotImplementedError('Method not implemented')
    return prompt



def get_result_file(args):
    result_file = "{}/{}/{}_{}_{}_{}_seed_{}.json".format(args.output_root, args.model, args.label, args.test_split,
                                                          args.prompt_format, args.shot_number, args.seed)

    return result_file


def save_results(result_file, acc, correct, count, shot_qids, args, results, outputs):
    data = {}
    data['acc'] = acc
    data['correct'] = correct
    data['count'] = len(results)
    data['shot_qids'] = shot_qids
    data['args'] = vars(args)
    data['results'] = results
    data['outputs'] = outputs

    with open(result_file, 'w') as f:
        json.dump(data, f, indent=2, separators=(',', ': '))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default='./datasets/ScienceQA')
    parser.add_argument('--output_root', type=str, default='./results')
    parser.add_argument('--caption_file', type=str, default='../datasets/ScienceQA/captions.json')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo-0613')
    parser.add_argument('--num_workers', type=int, default=32)
    parser.add_argument('--options', type=list, default=["A", "B", "C", "D", "E"])
    # user options
    parser.add_argument('--label', type=str, default='exp0')
    parser.add_argument('--test_split', type=str, default='val', choices=['test', 'val', 'minival', 'train'])
    parser.add_argument('--txt_only', default=False, action='store_true')
    parser.add_argument('--subset', default=False, action='store_true')
    parser.add_argument('--test_number', type=int, default=10, help='GPT-3 is expensive. -1 for whole val/test set')
    parser.add_argument('--use_caption', action='store_true', help='use image captions or not')
    parser.add_argument('--save_every', type=int, default=10, help='Save the result with every n examples.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--prompt_format',
                        type=str,
                        default='CQM-A',
                        choices=[
                            'CQM-A', 'CQM-LA', 'CQM-EA', 'CQM-LEA', 'CQM-ELA', 'CQM-AL', 'CQM-AE', 'CQM-ALE', 'QCM-A',
                            'QCM-LA', 'QCM-EA', 'QCM-LEA', 'QCM-ELA', 'QCM-AL', 'QCM-AE', 'QCM-ALE', 'QCML-A', 'QCME-A',
                            'QCMLE-A', 'QCLM-A', 'QCEM-A', 'QCLEM-A', 'QCLM-AE'
                        ],
                        help='prompt format template')
    parser.add_argument('--shot_number', type=int, default=3, help='Number of n-shot training examples.')
    parser.add_argument('--shot_qids', nargs='+', type=int, help='Question indexes of shot examples')
    parser.add_argument('--seed', type=int, default=10, help='random seed')
    # GPT-3 settings
    parser.add_argument('--api_key', type=str, help='OpenAI API key')
    parser.add_argument('--api_url', type=str, help='OpenAI API URL')
    parser.add_argument('--engine', type=str, default='text-davinci-002')
    parser.add_argument('--temperature', type=float, default=0.5)
    parser.add_argument('--max_tokens',
                        type=int,
                        default=2000,
                        help='The maximum number of tokens allowed for the generated answer.')
    parser.add_argument('--top_p', type=float, default=0.5)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)
    parser.add_argument('--method', type=str, default='reviewer')

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    print('====Input Arguments====')
    print(json.dumps(vars(args), indent=2, sort_keys=False))

    random.seed(args.seed)
    np.random.seed(args.seed)

    problems, qids, shot_qids = load_data(args)  # probelms, test question ids, shot example ids

    if args.subset:
        qids = qids[::20]

    result_file = get_result_file(args)
    # exit(0)

    if args.method == 'ours':
        print("="*25, "  PROMPT  ", '='*25)
        print(our_reasoner1_prompt, '\n' + '- '*30)
        print(our_reasoner2_prompt, '\n' + '- '*30)
        print(our_reviewer_prompt, )
        print("="*60)

    # load the check point
    if os.path.exists(result_file):
        print("# The result file exists! We will load the check point!!!")
        check_point = json.load(open(result_file))
        acc = check_point['acc']
        correct = check_point['correct']
        results = check_point['results']
        outputs = check_point['outputs']
        print(f"{len(results)}/{len(qids)}, correct: {correct}, acc: {round(acc, 2)}%")
    else:
        correct = 0
        results = {}
        outputs = {}

    executor = ThreadPoolExecutor(max_workers=args.num_workers)

    futures = [
        executor.submit(get_single_result, qid, build_prompt_sciqa(problems, qid, args), problems[qid]["choices"], args)
        for i, qid in enumerate(qids) if qid not in results # ['19723', '19913', '19638', '19601', '19500']
    ]


    n = 0
    for future in concurrent.futures.as_completed(futures):
        qid, prediction, output = future.result()
        # for i, qid in enumerate(qids):
        if qid in results:
            continue
        n += 1

        choices = problems[qid]["choices"]
        answer = problems[qid]["answer"]  # 0, 1, ..., 4
        label = args.options[answer]  # 'A', ..., 'E'
        
        # prediction, output = get_single_result(qid, prompt, choices, args)  # 'A', ..., 'E'
        pred_idx = get_pred_idx(prediction, choices, args.options)  # 0, 1, ..., 4

        results[qid] = pred_idx
        outputs[qid] = output
        if pred_idx == answer:
            correct += 1

        acc = correct / len(results) * 100

        if True: # args.debug or i < 50:
            print('\n\n\n', "###"*15, 'START', "###"*15)
            print('# Num: ', qid)
            print('# ', build_prompt_sciqa(problems, qid, args))
            print("# Full output: \n", output)
            print("# labeled answer:", label)
            print("# predicted answer:", prediction)
            print("# predicted index:", pred_idx)
            print("# Correct:", pred_idx == answer)
            print(f"{len(results)}/{len(qids)}, correct: {correct}, acc: {round(acc, 2)}%")
            print("###"*15, 'END', "###"*15, '\n\n\n')

        if (n + 1) % args.save_every == 0 or (n + 1) == len(qids):
            print(f"{len(results)}/{len(qids)}, correct: {correct}, acc: {round(acc, 2)}%, saving to {result_file}")
            save_results(result_file, acc, correct, n + 1, shot_qids, args, results, outputs)
