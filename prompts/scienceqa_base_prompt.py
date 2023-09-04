def get_question_text(problem):
    question = problem['question']
    return question


def get_context_text(problem, use_caption):
    txt_context = problem['hint']
    img_context = problem['caption'] if use_caption else ""
    context = " ".join([txt_context, img_context]).strip()
    if context == "":
        context = "N/A"
    return context


def get_choice_text(probelm, options):
    choices = probelm['choices']
    choice_list = []
    for i, c in enumerate(choices):
        choice_list.append("({}) {}".format(options[i], c))
    choice_txt = " ".join(choice_list)
    #print(choice_txt)
    return choice_txt


def get_answer(problem, options):
    return options[problem['answer']]


def get_lecture_text(problem):
    # \\n: GPT-3 can generate the lecture with more tokens.
    lecture = problem['lecture'].replace("\n", "\\n")
    return lecture


def get_solution_text(problem):
    # \\n: GPT-3 can generate the solution with more tokens
    solution = problem['solution'].replace("\n", "\\n")
    return solution


def create_one_example(format, question, context, choice, answer, lecture, solution, test_example=True):

    input_format, output_format = format.split("-")

    ## Inputs
    if input_format == "CQM":
        input = f"Context: {context}\nQuestion: {question}\nOptions: {choice}\n"
    elif input_format == "QCM":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\n"
    # upper bound experiment
    elif input_format == "QCML":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture}\n"
    elif input_format == "QCME":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {solution}\n"
    elif input_format == "QCMLE":
        input = f"Question: {question}\nContext: {context}\nOptions: {choice}\nBECAUSE: {lecture} {solution}\n"

    elif input_format == "QCLM":
        input = f"Question: {question}\n\nContext: \"{context}\"\n\nLecture: \"{lecture}\"\n\nOptions: {choice}\n"
    elif input_format == "QCEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {solution}\nOptions: {choice}\n"
    elif input_format == "QCLEM":
        input = f"Question: {question}\nContext: {context}\nBECAUSE: {lecture} {solution}\nOptions: {choice}\n"

    # Outputs
    if test_example:
        output = "" # Answer: (Provide your answer with tags, e.g., <Answer>A/B/C</Answer>.)
    elif output_format == 'A':
        output = f"Answer: The answer is <Answer>{answer}</Answer>."

    elif output_format == 'AL':
        output = f"Answer: The answer is <Answer>{answer}</Answer>. BECAUSE: {solution}"
    elif output_format == 'AE':
        output = f"Answer: The answer is <Answer>{answer}</Answer>. BECAUSE: {lecture}"
    elif output_format == 'ALE':
        output = f"Answer: The answer is <Answer>{answer}</Answer>. BECAUSE: {lecture} {solution}"
    elif output_format == 'AEL':
        output = f"Answer: The answer is <Answer>{answer}</Answer>. BECAUSE: {solution} {lecture}"

    elif output_format == 'LA':
        output = f"Answer: {lecture} The answer is <Answer>{answer}</Answer>."
    elif output_format == 'EA':
        output = f"Answer: {solution} Therefore, the answer is <Answer>{answer}</Answer>."
    elif output_format == 'LEA':
        output = f"Answer: {lecture} {solution} The answer is <Answer>{answer}</Answer>."
    elif output_format == 'ELA':
        output = f"Answer: {solution} {lecture} The answer is <Answer>{answer}</Answer>."
    elif output_format == 'CoTEA':
        output = f"Answer: Let's think step by step. {solution} The answer is <Answer>{answer}</Answer>."

    text = input + output
    text = text.replace("  ", " ").strip()
    if text.endswith("BECAUSE:"):
        text = text.replace("BECAUSE:", "").strip()
    return text


def build_prompt(problems, shot_qids, test_qid, args):

    examples = []
    

    # n-shot training examples
    for qid in shot_qids:
        # print(problems[qid]['caption'])
        # ['question', 'choices', 'answer', 'hint', 'image', 'task', 'grade', 'subject', 'topic', 'category', 'skill', 'lecture', 'solution', 'split', 'caption']
        question = get_question_text(problems[qid])
        context = get_context_text(problems[qid], args.use_caption)
        choice = get_choice_text(problems[qid], args.options)
        answer = get_answer(problems[qid], args.options)
        lecture = get_lecture_text(problems[qid])
        solution = get_solution_text(problems[qid])

        train_example = create_one_example(args.prompt_format,
                                           question,
                                           context,
                                           choice,
                                           answer,
                                           lecture,
                                           solution,
                                           test_example=False)
        examples.append(train_example)

    # test example
    question = get_question_text(problems[test_qid])
    context = get_context_text(problems[test_qid], args.use_caption)
    choice = get_choice_text(problems[test_qid], args.options)
    answer = get_answer(problems[test_qid], args.options)
    lecture = get_lecture_text(problems[test_qid])
    solution = get_solution_text(problems[test_qid])

    test_example = create_one_example(args.prompt_format,
                                      question,
                                      context,
                                      choice,
                                      answer,
                                      lecture,
                                      solution,
                                      test_example=True)
    examples.append(test_example)

    # create the prompt input
    prompt_input = '\n\n'.join(examples)

    return prompt_input
