import os
import re
import json
import argparse
import random
from tqdm import tqdm
# from base_prompt import *
from retry import retry
import openai
import requests
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import concurrent
# from prompts.prompts_boolq_ours_os import *
from prompts.prompts_boolq_ours_os import *

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT





def load_data(args):
    data = open(args.data_root, 'r')
    questions = {}
    passages = {}
    labels = {}
    qids = []
    
    mapping = {'True': 'yes', 'False': 'no'}

    for i, line in enumerate(data):
        line = json.loads(line)
        questions.update({str(i): line["question"]})
        passages.update({str(i): line["passage"]})
        labels.update({str(i): mapping[str(line["answer"])]})
        qids.append(str(i))
    
    # print(labels, type(labels['3260']))
    print(f"number of test problems: {len(qids)}\n")
    return questions, passages, labels, qids


def build_prompt(questions, passages, qid, args):
    # closed-book setting
    if args.method == 'base_oneshot':
        prompt = base_prompt_oneshot + f"\nQ: {questions[qid]}?"
    elif args.method == 'base_zeroshot':
        prompt = base_prompt_zeroshot + f"\nQ: {questions[qid]}?"
    elif args.method == 'zeroshot-cot':
        prompt = cot_zeroshot_prompt + f"\nQuestion: {questions[qid]}?" # \nPassage: \"{passages[qid]}\" 
    elif args.method in ['os-cot', 'os-fewshot-cot', 'os-self-consistent', 'os-complexity']:
        prompt = cot_oneshot_prompt + f"\nQ: {questions[qid]}?" #\nPassage: \"{passages[qid]}\" 
    elif args.method == 'ours':
        prompt = f"\nQuestion: \n{questions[qid]}? "
    elif args.method == 'least-to-most':
        prompt = least_to_most_decomposer_prompt + \
f"""
Now, provide the sub-questions for the question: 
Q: 
    Judge whether the sentense is true or false: {questions[qid]}"""

    # elif args.method == 'fewshot-cot':
    #     prompt = few_shot_cot_prompt + \
    # f"Your reply MUST include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\' at the end. \n\nQ: Judge whether the sentense is true or false: \"{sents[qid]}\". "
    # print(args.method) Remember, if the answer cannot be determined, make an educated guess, and y
    # print(prompt)
    return prompt
    


def filter_output(output):
    tags = re.findall(r'<Answer>(.*?)</Answer>', output)
    if len(tags) == 0:
        answer = output
    else:
        answer = tags[-1]

    if answer in ['yes', 'no']:
        return answer
    elif ('yes' not in answer.lower() and 'no' not in answer.lower()) or 'cannot' in answer.lower():
        answer = np.random.choice(['yes', 'no'])
    elif 'yes' in answer.lower():
        answer = 'yes'
    elif 'no' in answer.lower():
        answer = 'no'
    else:
        answer = np.random.choice(['yes', 'no'])
    return answer

from time import sleep

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

    # print(response)
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
    
    # print(response)
    if 'error' in response.keys():
        print(response['error'])
    
    return response['choices'][0]['message']['content']


@retry(delay=5, tries=10, backoff=2, max_delay=120)
def answer_review(question=None, depth=1, history='', args=None):
    if args.model == 'claude':
        get_single_run = get_single_run_claude
    elif args.model == 'gpt':
        get_single_run = get_single_run_gpt
    else:
        raise NotImplementedError('undefined model')

    output_1 = get_single_run('', our_reasoner1_prompt + question, args)
    answer_1 = filter_output(output_1)
    sleep(0.1)
    # return answer_1, output_1
    
    output_2 = get_single_run('', our_reasoner2_prompt + question, args)
    answer_2 = filter_output(output_2)
    # return answer_2, output_2
    
    
    history += f" ########## Round {depth} ########## \n" + str(output_1 + '\n\n' + '-'*30 + '\n\n' + output_2 + '\n\n')

    if answer_1 == answer_2: 
        # history += f'\n\n{answer_1} {answer_2} >>> output\n\n'

        #####
        lst = ['yes', 'no']
        lst.pop(lst.index(answer_1))

        answer_cf = np.random.choice(lst)
        reviewer_prompt1 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\" \n\n\nA possible solution is: \n\"\"\"\n{np.random.choice([output_1, output_2])}\n\"\"\"\n\nPlease provide your evaluation, while looking out for answer \'{answer_cf}\'. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. " # 

        reviewer_output_3 = get_single_run('', reviewer_prompt1, args)

        answer_3 = filter_output(reviewer_output_3)

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
            return answer_review(question=question, depth=depth+1, history=history, args=args)
        
    elif answer_1 != answer_2:
        reviewer_prompt1 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\"\n\n\nA possible solution is: \n\"\"\"\n{output_1}\n\"\"\"\n\nPlease provide your review following the review outline, while looking out for answer \'{answer_2}\'. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. " # , while looking out for answer \'{answer_2}\'
        reviewer_prompt2 = our_reviewer_prompt + f"Now, For the question: \n\"\"\"\n{question}\n\"\"\"\n\n\nA possible solution is: \n\"\"\"\n{output_2}\n\"\"\"\n\nPlease provide your review following the review outline, while looking out for answer \'{answer_1}\'. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. " # , while looking out for answer \'{answer_1}\'

        reviewer_output_3 = get_single_run('', reviewer_prompt1, args)
        reviewer_output_4 = get_single_run('', reviewer_prompt2, args)
        
        answer_3 = filter_output(reviewer_output_3)
        answer_4 = filter_output(reviewer_output_4)

        history += f" ######## Round {depth} Review ######## \n\n" + str(reviewer_output_3 + '\n\n' + '-'*30 + '\n\n' + reviewer_output_4 + '\n\n' + '='*30 + '\n\n')

        answers = [answer_1, answer_2, answer_3, answer_4]
        max_answer = max(set(answers), key=answers.count)

        if answers.count(max_answer) > 2:
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> # evaluators consensus {max_answer} >= 3\n\n'
            return max_answer, history
        elif depth > 3:
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> reach max depth\n\n'
            return np.random.choice(answers), history
        else: 
            history += f'\n\n{answer_1} {answer_2} {answer_3} {answer_4} >>> go deeper\n\n'
            return answer_review(question=question, depth=depth+1, history=history, args=args)



@retry(delay=5, tries=5, backoff=2, max_delay=120)
def get_single_result(qid, prompt, args): 
    if args.model == 'claude':
        get_single_run = get_single_run_claude
    elif args.model == 'gpt':
        get_single_run = get_single_run_gpt
    else:
        raise NotImplementedError('undefined model')



    if args.method in ['self-consistent', 'complexity']:
        answers = []
        outputs = ''
        n_chains = []
        for i in range(10): 
            cot_prompt = 'Let\'s think step by step. '
            response = get_single_run_gpt(cot_prompt, prompt, args)
            output = response

            n_chain = output.count('\n') - output.count('\n\n') + 1
            n_chains.append(n_chain) # \n or \n\n + 1 as number of chains
            outputs += '\n' + '-'*50 + f'\n\nRound {i+1} #Chain {n_chain} \n Output: {output}'
            answer = filter_output(output)
            answers.append(answer)

            
        if args.method == 'complexity': # filter out those with a shorter reasoning chain
            longchain_indices = np.argsort(n_chains)[-int(0.6*len(n_chains)):] # indices of those with more chains
            cplx_answers = np.array(answers)[longchain_indices]

        # answer = max(set(answers), key=list(answers).count)
        answer = [answers[0], max(set(answers), key=list(answers).count), max(set(cplx_answers), key=list(cplx_answers).count)]
        output = outputs
        # print(answer, output)

    elif args.method in ['base_zeroshot', 'base_oneshot', 'oneshot-cot', 'zeroshot-cot']:
        output = get_single_run('', prompt, args)
        answer = filter_output(output)

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

        answer = filter_output(ans)
        output = messages.split(f'Now, the context is: \n{original_question}')[1]

        
        # print("dialogue: \n\n", output)
                  
    elif args.method == 'ours':
        answer, output = answer_review(question=prompt, depth=0, history='', args=args)
        
    return qid, answer, output



def get_pred_idx(prediction, choices, options):
    """
    Get the index (e.g. 2) from the prediction (e.g. 'C')
    """
    if prediction in options[:len(choices)]:
        return options.index(prediction)
    else:
        return random.choice(range(len(choices)))


def get_result_file(args):
    result_file = "{}/{}/{}_{}_seed_{}.json".format(args.output_root, args.model, args.label, args.test_split, args.seed)

    return result_file


def save_results(result_file, acc, correct, count, args, results, outputs):
    data = {}
    data['acc'] = acc
    data['correct'] = correct
    data['count'] = count
    data['args'] = vars(args)
    data['results'] = results
    data['outputs'] = outputs

    with open(result_file, 'w') as f:
        json.dump(data, f, indent=2, separators=(',', ': '))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default='./datasets/com2sense.json')
    parser.add_argument('--output_root', type=str, default='./results')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo-0613')
    parser.add_argument('--num_workers', type=int, default=16)
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

    questions, passages, labels, qids = load_data(args)  # probelms, test question ids, shot example ids

    if args.subset:
        qids = qids[::20]

    result_file = get_result_file(args)
    print(result_file)


    if args.method == 'ours':
        print("="*25, "  PROMPT  ", '='*25)
        print(our_reasoner1_prompt)
        print(our_reasoner2_prompt)
        print(our_reviewer_prompt)
        print("="*60)
    # exit(0)

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

    # print('# Example for prompting: \n', build_prompt(sents, '1', args).split('\n\n')[0])

    executor = ThreadPoolExecutor(max_workers=args.num_workers)

    futures = [
        executor.submit(get_single_result, qid, build_prompt(questions, passages, qid, args), args)
        for i, qid in enumerate(qids) if qid not in results
    ]

    n = 0
    for future in concurrent.futures.as_completed(futures):
        qid, prediction, output = future.result()
        if qid in results:
            continue
        n += 1

        label = labels[qid]

        results[qid] = prediction
        outputs[qid] = output
        if prediction == label:
            correct += 1

        acc = correct / len(results) * 100

        if True: # args.debug or i < 50:
            print('\n\n\n', "###"*15, 'START', "###"*15)
            print('# Num: ', qid)
            print('# Prompt: ', build_prompt(questions, passages, qid, args))
            print("# full output:", output)
            print("# labeled answer:", label)
            print("# predicted answer:", prediction)
            print("# Correct:", prediction == label)
            print(f"{len(results)}/{len(qids)}, correct: {correct}, acc: {round(acc, 2)}%")
            print("###"*15, 'END', "###"*15, '\n\n\n')

        if (n + 1) % args.save_every == 0 or (n + 1) == len(qids):
            print(f"{len(results)}/{len(qids)}, correct: {correct}, acc: {round(acc, 2)}%, saving to {result_file}")
            save_results(result_file, acc, correct, n + 1, args, results, outputs)
