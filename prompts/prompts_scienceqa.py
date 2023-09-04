base_prompt = \
"""Answer the question. Your reply MUST include your answer with tags, e.g., <Answer>A/B/C</Answer>. 

"""

cot_prompt = \
"""Please answer the question. Your reply MUST include your answer with tags at the end, e.g., <Answer>A/B/C</Answer>. 

Here is an example: 
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
leap - lucky
Context: N/A
Options: (A) lay (B) lord

Answer: 
The guide words at the top of a dictionary page help indicate the first word and the last word listed on that page. A word that falls alphabetically between those guide words would be on that page.

Given the guide words "leap" and "lucky", let's evaluate the options:

(A) "lay" - This word falls alphabetically between "leap" and "lucky". It comes after "leap" and before "lucky".

(B) "lord" - This word does not fall alphabetically between "leap" and "lucky". It comes after both "leap" and "lucky".

So, the word you would find on a dictionary page with the guide words "leap" - "lucky" would be: <Answer>B</Answer> lord
\"\"\

"""




chain_3_answer = \
"""
Answer:
The guide words at the top of a dictionary page provide the first word and the last word that appear on that page in alphabetical order. Therefore, any words that alphabetically fall between these guide words will be on that page.

Given the guide words "get" and "goes", the word "group" (A) would not be found on this page because it comes after "goes" alphabetically. On the other hand, "gnaw" (B) would be found on this page because it comes after "get" and before "goes" alphabetically.

So, the correct answer is: <Answer>B</Answer>
"""

chain_5_answer =\
"""
Answer:
In a dictionary, guide words at the top or bottom of each page tell you the first and last words appearing on that page. They help you to locate a word you're looking for. If you are searching for a word, you would use these guide words to help determine whether the word would be found on that page.

The guide words you provided are "get" and "goes". This means that all the words on this page will fall alphabetically between these two words.

Looking at option (A) "group", it would come after "goes" in the alphabet, so it's not likely to be on this page.

For option (B) "gnaw", it would come after "get" and before "goes" alphabetically, so it fits the criteria and would be on this page.

<Answer>B</Answer>
\"\"\"

"""


chain_4_answer = \
"""
Answer:
To determine which word would be found on a dictionary page with the guide words "get" and "goes," we need to consider the alphabetical order and position of words between these guide words.

1. The first guide word is "get," which means we need to look for words that come alphabetically after "get."

2. The second guide word is "goes," which means we are looking for words that come alphabetically before "goes."

3. Comparing the guide words, we can see that "gnaw" comes before "goes" alphabetically, while "group" comes after "get."

4. Since we are looking for a word that falls between "get" and "goes," the correct option would be (B) gnaw.

<Answer>B</Answer>
"""


chain_7_answer = \
"""
Answer:
1. Dictionary pages often have guide words at the top of each page. These words provide an indication of the first and last word entries found on that particular page.
2. The first guide word ("get") indicates that the first word on the page will be "get" or a word that comes after "get" in alphabetical order.
3. The second guide word ("goes") indicates that the last word on the page will be "goes" or a word that comes before "goes" in alphabetical order.
4. Now let's consider the options (A) "group" and (B) "gnaw".
5. Option (A) "group" comes after "get" in alphabetical order, but it also comes after "goes". Therefore, it would not be found on a page with "get" and "goes" as the guide words.
6. Option (B) "gnaw" comes after "get" and before "goes" in alphabetical order. Therefore, it could be found on a page with "get" and "goes" as the guide words.
7. So, based on the alphabetical order, the word that would be found on a dictionary page with the guide words "get" - "goes" is <Answer>B</Answer> gnaw.
"""


one_shot_cot_prompt = \
f"""
Please answer the question by thinking step by step. Your reply MUST include your answer with tags at the end, e.g., <Answer>A/B/C</Answer>. 

An example:
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
get - goes
Context: N/A
Options: (A) group (B) gnaw

{chain_4_answer}
\"\"\"

"""














zeroshot_cot_prompt = \
"""Answer the question after thinking step by step. Your MUST provide your answer with TAGS at the end, e.g., <Answer>A/B/C</Answer>. 
"""


least_to_most_decomposer_prompt = \
"""
- To judge a sentense is true or false, you need to provide a series of sub-questions that lead us to the final answer. 
- You MUST enclose each subquestion with TAGS <subquestion>[your_subquestion]</subquestion>)

There are a few examples: 
Q:
    Judge whether the sentense is true or false: Jane got some weird looks because she wore sunglasses outside at 4 PM.
A:
    To judge the truthfulness of the statement "Jane got some weird looks because she wore sunglasses outside at 4 PM," we would need to know the answers to the following sub-questions:

    <subquestion>Did Jane wear sunglasses outside at 4 PM?</subquestion>
    <subquestion>Did people notice Jane wearing sunglasses?</subquestion>
    <subquestion>Did people give Jane strange looks?</subquestion>
    <subquestion>Is it unusual or socially unacceptable to wear sunglasses outside at 4 PM in the context in which Jane was present?</subquestion>

Q: 
    Judge whether the sentense is true or false: The college coach had been paying his players so he was praised by the media.
A: 
    To judge the truthfulness of the statement "The college coach had been paying his players so he was praised by the media," we would need to know the answers to the following sub-questions:

    <subquestion>If the college coach did pay his players, was this behavior considered acceptable or unethical by the media?</subquestion>
    <subquestion>If the media did praise the college coach, was this praise based solely on his performance as a coach, or did it take his alleged payments to players into account?</subquestion>

Q:
    Judge whether the sentense is true or false: As the weather was very cold he put on his jacket to protect himself. 
A:
    To judge the truthfulness of the statement "As the weather was very cold he put on his jacket to protect himself," we would need to know the answers to the following sub-questions:

    <subquestion>Was the weather very cold?</subquestion>
    <subquestion>Did he have a jacket available to put on?</subquestion>
    <subquestion>Did he put on his jacket as a response to the cold weather?</subquestion>
    <subquestion>Was the purpose of putting on the jacket to protect himself from the cold?</subquestion>

"""


# least_to_most_subq_solver_prompt = \
# """
# You need to answer the question based on the given context.

# An example:
# \"\"\"
# Jane got some weird looks because she wore sunglasses outside at 4 PM.
# Q: Is it confirmed that Jane wore sunglasses outside at 4 PM?
# A: This requires a factual confirmation, either from Jane herself, an eyewitness, or a form of recording like a picture or video.

# Q: Are there any social norms or cultural expectations in Jane's location that might make wearing sunglasses at 4 PM unusual?
# A: This would depend on Jane's geographical location, the local weather, and cultural norms. For example, in sunny regions, wearing sunglasses at 4 PM may be perfectly normal.

# Q: Is there any evidence to support the claim that the looks Jane received were indeed "weird"?
# A: To determine this, we would need detailed accounts from Jane or other eyewitnesses about the reactions she received. 
# \"\"\"

# Now, according to the context, answer the question. 
# """


least_to_most_subq_solver_prompt = \
"""
Answer the questions one by one according to the context. 

There are two examples: 
\"\"\"
Jane got some weird looks because she wore sunglasses outside at 4 PM.
Q: Did Jane wear sunglasses outside at 4 PM?
A: Yes, based on the statement "Jane got some weird looks because she wore sunglasses outside at 4 PM," it can be inferred that Jane did indeed wear sunglasses outside at 4 PM.

Q: Did people notice Jane wearing sunglasses?
A: Yes, based on the statement "Jane got some weird looks", it can be inferred that people noticed Jane wearing sunglasses outside at 4 PM and their reaction was noticeable enough for Jane to feel uncomfortable or self-conscious about it.

Q: Did people give Jane strange looks?
A: Yes, based on the statement "Jane got some weird looks", it can be inferred that people gave Jane strange looks for wearing sunglasses outside at 4 PM.


The college coach had been paying his players so he was praised by the media.
Q: Does the college coach in question actually pay his players?
A: This would involve verifying the information from reliable sources. In the context of collegiate sports, particularly in the United States, this action is typically against NCAA regulations. As of my knowledge cutoff in September 2021, college athletes were not allowed to be paid directly by their coaches or institutions, although recent changes had begun to allow athletes to profit from their name, image, and likeness.

Q: Has this action been made public?
A: We would need to know whether the media is aware of this behavior. If the action is not publicly known, the media would not be in a position to praise or condemn the coach.

Q: Has the media actually praised the coach for this action?
A: This would involve researching media coverage. It's important to note that the media is not a single monolithic entity, so the reactions may vary from one media outlet to another.

Q: If the media has praised the coach, is it specifically for paying the players?
A: The media may praise a coach for various reasons, such as the team's performance, the coach's leadership, etc. We would need to verify that the praise is specifically related to the action of paying the players.

Q: Is the sentense true or false, "The college coach had been paying his players so he was praised by the media"? Your reply MUST include '<Answer>True</Answer>' or '<Answer>False</Answer>' at the end.
A: Based on the overall context and norms within college sports, it's unlikely that a college coach would be praised by the media for paying his players, given that this is typically against the rules of most collegiate sports associations. Therefore, based on the information available to me, I would judge the statement as likely being false. <Answer>False</Answer>
\"\"\"


"""




example0 = \
"""
An example: 
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
get - goes
Context: N/A
Options: (A) group (B) gnaw
    
Response: 
- **Explanation of Terms**: 
    - Term 1: Dictionary Page: A dictionary page is a page in a dictionary that contains a list of words and their meanings. The words are usually arranged in alphabetical order.
    - Term 2: Guide Words: Guide words are the words printed at the top of a page in a reference book such as a dictionary or encyclopedia. They help to indicate the first and the last words on that page.

- **Subquestion Decomposition and Answering**: 
    - Subquestion 1: What is the alphabetical position of the guide words and the options?
    - Answer to subquestion 1: The guide words are "get" and "goes". In alphabetical order, "get" comes before "goes". The options are "group" and "gnaw". "Group" comes after "goes" in alphabetical order, and "gnaw" comes before "get".

    - Subquestion 2: Which of the options can be found between the guide words?
    - Answer to subquestion 2: In a dictionary, words are arranged in alphabetical order. Therefore, any word that can be found between the guide words "get" and "goes" would be a word that comes after "get" and before "goes" in alphabetical order. In this case, only "gnaw" fits this criterion.

- **Rationale for Arriving at the Answer**: 
    Based on the alphabetical order, the word "gnaw" comes after "get" and before "goes". Therefore, it is the word that you would find on a dictionary page with the guide words "get - goes". The word "group" comes after "goes", so it would not be on this page.

- **Provide Your Answer WITH TAGS**: 
    <Answer>B</Answer>
\"\"\"
"""


example1 = \
"""
An example: 
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
get - goes
Context: N/A
Options: (A) group (B) gnaw
    
Response: 
- **Explanation of Terms**: 
    - Term 1: Dictionary Page: A dictionary page is a page in a dictionary that contains a list of words and their meanings. The words are usually arranged in alphabetical order.
    - Term 2: Guide Words: Guide words are the words printed at the top of a page in a reference book such as a dictionary or encyclopedia. They help to indicate the first and the last words on that page.

- **Subquestion Decomposition and Answering**: 
    - Subquestion 1: What is the alphabetical position of the guide words and the options?
    - Answer to subquestion 1: The guide words are "get" and "goes". In alphabetical order, "get" comes before "goes". The options are "group" and "gnaw". "Group" comes after "goes" in alphabetical order, and "gnaw" comes before "get".

    - Subquestion 2: Which of the options can be found between the guide words?
    - Answer to subquestion 2: In a dictionary, words are arranged in alphabetical order. Therefore, any word that can be found between the guide words "get" and "goes" would be a word that comes after "get" and before "goes" in alphabetical order. In this case, only "gnaw" fits this criterion.

- **Rationale for Arriving at the Answer**: 
    Based on the alphabetical order, the word "gnaw" comes after "get" and before "goes". Therefore, it is the word that you would find on a dictionary page with the guide words "get - goes". The word "group" comes after "goes", so it would not be on this page.

- **Provide Your Answer WITH TAGS**: 
    <Answer>B</Answer>
\"\"\"
"""

# example0 = ''
# example1 = ''

# our_reasoner1_prompt = \
# f"""
# Follow the outline to solve the question: 
# - **List necessary information to solve the question**: 
# - **Explanation of Terms**: 
# - **Rationale**: 
# - **Provide your answer WITH TAGS**: 
# (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. )


# {example0}

# Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 

# """



# our_reasoner2_prompt = \
# f"""
# Follow the outline to solve the question: 
# - **List necessary information to solve the question**: 
# - **Explanation of Terms**: 
# - **Rationale**: 
# - **Provide your answer WITH TAGS**: 
# (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. )


# {example1}

# Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 

# """




our_reasoner1_prompt = \
f"""
Follow the outline below to solve the question: 
    - **Explanation of Terms**: 
    (You need to explain each term used in the question to remove ambiguity. )
        - Term 1: ...

        - Term 2: ...

    - **Subquestion Decomposition and Answering**: 
    (You need to decompose the question into several subquestions connected logically to arrive at the final answer. For each subquestion, provide your answer below it. )
        - Subquestion 1: ...
        - Answer to subquestion 1: ...
        
        - Subquestion 2: ...
        - Answer to subquestion 2: ...

    - **Rationale for Arriving at the Answer**: 
    (You need to reason step by step for the correct answer based on the previous information. )

    - **Provide Your Answer WITH TAGS**: 
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. )


{example0}

Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 
"""


"""
  - **Subquestion Decomposition and Answering**: 
  (You need to decompose the question into several subquestions connected logically. )
    - Subquestion 1: ...
    - Subquestion 2: ...

  - **Subquestion Decomposition and Answering**: 
  (You need to decompose the question into several subquestions connected logically to arrive at the final answer. For each subquestion, provide your answer below it. )
    - Subquestion 1: ...
      - Answer to subquestion 1: ...
    - Subquestion 2: ...
      - Answer to subquestion 2: ...
"""

our_reasoner2_prompt = \
f"""
Follow the outline below to solve the question: 
    - **Explanation of Terms**: 
    (You need to explain each term used in the question to remove ambiguity. )
        - Term 1: ...

        - Term 2: ...

    - **Subquestion Decomposition and Answering**: 
    (You need to decompose the question into several subquestions connected logically to arrive at the final answer. For each subquestion, provide your answer below it. )
        - Subquestion 1: ...
        - Answer to subquestion 1: ...
        
        - Subquestion 2: ...
        - Answer to subquestion 2: ...

    - **Rationale for Arriving at the Answer**: 
    (You need to reason step by step for the correct answer based on the previous information. )

    - **Provide Your Answer WITH TAGS**: 
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. )


{example0}

Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 
"""


reviewer_example = \
"""
Here is an example: 
For the question: 
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
get - goes
Context: N/A
Options: (A) group (B) gnaw
\"\"\"


and a solution: 
\"\"\"
- **Explanation of Terms**:
    - Dictionary: a book or electronic resource that lists the words of a language in alphabetical order and gives their meaning, or that gives the equivalent words in a different language.
    
    - Guide words: the words printed at the top of a dictionary page indicating the first and last entries on that page.

- **Subquestion Decomposition and Answering**:

    - Subquestion 1: What are guide words in a dictionary?
    - Answer to subquestion 1: Guide words are the words printed at the top of a dictionary page indicating the first and last entries on that page.

    - Subquestion 2: What are the guide words for the dictionary page that contains the word "get" and "goes"?
    - Answer to subquestion 2: The guide words for the dictionary page that contains the word "get" and "goes" are "get" (the first word) and "goes" (the last word).

    - Subquestion 3: Which word would you find on a dictionary page with the guide words "get" and "goes"?
    - Answer to subquestion 3: Based on the guide words "get" and "goes," the word that would appear on the dictionary page is between those two words in alphabetical order.

    - Subquestion 4: Which word is between "get" and "goes" in alphabetical order?
    - Answer to subquestion 4: The word between "get" and "goes" in alphabetical order is "group."

    - Subquestion 5: Which word would you find on a dictionary page with the guide words "get" and "goes"?
    - Answer to subquestion 5: The word that you would find on a dictionary page with the guide words "get" and "goes" is "group."

- **Rationale for Arriving at the Answer**:
    
    - The question asks which word would you find on a dictionary page with the guide words "get" and "goes." To answer this question, we need to understand what guide words are and what the guide words for the dictionary page that contains the word "get" and "goes" are. The guide words for this page are "get" and "goes," which means that the word we are looking for is between these two words in alphabetical order. The only option that is between "get" and "goes" in alphabetical order is "group," so the answer is (A) group.

- **Provide Your Answer WITH TAGS**: 
    
    - <Answer>A</Answer>
\"\"\"

with option (B) that needs to look out for. 


Your response is like:
\"\"\"
**Review Statements One by One**

    - Evaluation on Explanation of Terms: 
    The terms "Dictionary" and "Guide words" are correctly defined, aiding a user's understanding of the context and the question.

    - Evaluation on Subquestion Decomposition and Answering: 
    The decomposition of the question into subquestions is done systematically and answered appropriately. However, subquestion 5 is redundant as it is identical to subquestion 3.

    - Evaluation on the Reasoning process: 
    The reasoning process is not logically sound in this instance. The solution incorrectly concludes that the word "group" comes between "get" and "goes" in alphabetical order. The correct word from the options given is "gnaw," which does come in between "get" and "goes".

    - Evaluation on the Answer: 
    The answer is incorrect. The word "group" does not come between "get" and "goes" in alphabetical order. The correct word from the options given is "gnaw," which does come in between "get" and "goes".

**Reconsider the Question Step by Step and Consider Counterfactuals**

    - Your counterfactual reasoning about the answer that you need to look out for:   
    The answer that we need to look out for is (B) "gnaw". It is important to consider the word "gnaw," which falls between "get" and "goes" alphabetically. "gnaw" is a word that falls between "get" and "goes", making it a better fit.

    - Your step-by-step reasoning to arrive at the most likely answer: 
    The question asks which word falls between "get" and "goes" in alphabetical order. By comparing the options, we find that "group" comes after "goes," while "gnaw" falls between "get" and "goes." Therefore, "gnaw" is the correct answer.

**Provide Your Answer With TAGS**

    - Answer: <Answer>B</Answer>
\"\"\"
"""

# reviewer_example = ''

# our_reviewer_prompt = \
# f"""
# You are an outstanding reviewer. You are responsible for reviewing a possible solution following the outline: 
# ### Review Statements One by One
# (Especially, take care of Factualness and Reasoning Errors in the Solution)

# ### Reconsider the Question Step by Step and Options Counterfactually
# (Reason step by step to arrive at the most likely answer. Meanwhile, consider what if we apply other options. )

# ### Provide Your Answer With TAGS
# (At the end, you MUST choose ONE option as your final answer and mark it with TAGS, e.g., <Answer>A/B/C/D/E</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )

# {reviewer_example}

# """

our_reviewer_prompt = \
f"""
You are an objective and fair reviewer. You are responsible for evaluating a possible solution following the outline: 
    - **Review Statements One by One**
        (Examine the following aspects in the solution. Especially, watch out for factualness errors and inference errors in the solution)
        - Evaluation on Explanation of Terms: 
        - Evaluation on Subquestion Decomposition and Answering: 
        - Evaluation on the Reasoning process: 
        - Evaluation on the Answer: 

    - **Reconsider the Question Step by Step and Consider Counterfactuals**
        - Your counterfacutal reasoning about the answer that you need to look out for: (think what if this option is applied to the question. If there is a contracdition, double-check between the two provided answers. )
        - Your step-by-step reasoning to arrive at the most likely answer: 

    - **Provide Your Answer With TAGS**
      (you MUST enclose your answer with TAGS, e.g., <Answer>A/B/C</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )

      
{reviewer_example}

"""





term_eval_prompt = \
"""
You are an objective and fair reviewer. You are responsible for evaluating the definition of some given terms following the template below: 
    - **Evaluation on Explanation of Terms**
        - Evaluation on Term 1: 
        - Evaluation on Term 2: 
        ...
    - **Conclusion**
        - <Evaluation>Correct/Partially Correct/Incorrect</Evaluation>
        - (If your evaluate the explanation as Partially Correct/Incorrect, you need to explain your evaluation here)

"""