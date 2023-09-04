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

one_shot_cot_prompt = \
"""
Please answer the question by thinking step by step. Your reply MUST include your answer with tags at the end, e.g., <Answer>A/B/C</Answer>. 

An example:
\"\"\"
Question: Which word would you find on a dictionary page with the following guide words?
get - goes
Context: N/A
Options: (A) group (B) gnaw

Answer:
Let's think step by step:
1. The guide words on a dictionary page hint at the first and last words on that specific page.
2. 'Get' would be the first word on the page.
3. 'Goes' would be the last word on the page.
4. Alphabetically, words on this page would fall between 'get' and 'goes'.
5. 'Group' starts with 'gr-', which comes after 'go-' alphabetically, so it would not be on this page.
6. 'Gnaw' starts with 'gn-', which comes after 'ge-' (from 'get') but before 'go-' (from 'goes') alphabetically, so it would be on this page.

So, the answer is: <Answer>B</Answer>
\"\"\"

"""



zeroshot_cot_prompt = \
"""Answer the question by thinking step by step. Your MUST provide your answer with TAGS at the end, e.g., <Answer>A/B/C</Answer>. 
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

- **Necessary Information**: 

Guide words are found at the top of each page in a dictionary and they can assist us in locating a particular word. The first guide word usually shows the first word entry on that page, and the second guide word shows the last word entry on that page. Words on the page will be in alphabetical order.

- **Explanation of Terms**: 

- Get: This is the first guide word on the page, so it means that any words that come alphabetically after 'get' could be on this page.
- Goes: This is the second guide word on the page, so it means that any words that come alphabetically before 'goes' could be on this page.

- **Rationale**: 

Words in a dictionary are arranged in an alphabetical order. The guide words "get" and "goes" indicate that any word that falls between these two terms (alphabetically) would be on that page. Thus, we need to choose the word among the options that would come after "get" and before "goes" in the English alphabet. We can easily exclude option A "group" because, alphabetically, "group" comes after "goes". Now looking at option B "gnaw", it comes after "get" and before "goes" alphabetically. Therefore, "gnaw" would be the word you would find on a dictionary page with the guide words "get" and "goes".

- **Provide your Answer WITH TAGS: **

<Answer>B</Answer>
\"\"\"
"""


example1 = \
"""
An example: 
\"\"\"
Question: Judge whether the sentense is true or false: 
"If I want to weigh down some papers, it is much better to use an empty plastic bag than a baseball."

Response: 
- **List necessary information to solve the question**: 

  - Jared has a big test on Wednesday.
  - He wants to go to a basketball game on Tuesday night rather than Thursday night.

- **Explanation of Terms**: 

  - Study: To spend time reading about and understanding a subject, especially in preparation for an exam.
  - Basketball game: An event in which two teams play the sport of basketball against each other, typically in the evening.

- **Rationale**: 

  If Jared has a big test on Wednesday, it would be more beneficial for him to study on Tuesday night rather than attending a basketball game. Going to a basketball game on Tuesday night could leave him with little time to study for the Wednesday test. If his aim is to have enough time to study, it would make more sense to go to the basketball game on Thursday night, after the test has already taken place.

- **Provide your answer WITH TAGS**: 

  Given that Jared's decision to attend a basketball game on Tuesday night rather than Thursday night contradicts his stated aim of having time to study for a Wednesday test, the statement is likely false. Therefore, my answer is: <Answer>False</Answer>
\"\"\"
"""

example0 = ''
example1 = ''

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
""" 
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


Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 
"""


# """
#   - **Subquestion Decomposition and Answering**: 
#   (You need to decompose the question into several subquestions connected logically. )
#     - Subquestion 1: ...
#     - Subquestion 2: ...

#   - **Subquestion Decomposition and Answering**: 
#   (You need to decompose the question into several subquestions connected logically to arrive at the final answer. For each subquestion, provide your answer below it. )
#     - Subquestion 1: ...
#       - Answer to subquestion 1: ...
#     - Subquestion 2: ...
#       - Answer to subquestion 2: ...
# """

our_reasoner2_prompt = \
"""
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


Now, solve the question below by following the outline. Remember, You MUST give a certain answer, with the capital letter included in TAGS, e.g., <Answer>A/B/C</Answer>. If the answer cannot be determined, make an educated guess. 
"""


reviewer_example = \
"""
Here is an example: 
For the question: 
\"\"\"
Judge the sentense is true or false:"Jane got some weird looks because she wore sunglasses outside at 4 PM."
\"\"\"


and a solution: 
\"\"\"
- **List necessary information to solve the question**:
  
  - Jane wore sunglasses outside at 4 PM. 
  - She got some weird looks because of this.

- **Explanation of Terms**:
  
  - Weird looks: Strange or odd expressions or glances directed at someone.
  
- **Rationale**: 

  Wearing sunglasses outside in the late afternoon is uncommon, especially at 4 PM when the sun is likely not that bright anymore. This would likely elicit strange looks from other people.

- **Provide your answer WITH TAGS**:

 Given that wearing sunglasses outside at 4PM, when the sun is no longer that bright, is an unusual action that would likely provoke strange looks from others, we can infer that the statement is likely true. <Answer>True</Answer>
\"\"\"



Your response is like:
\"\"\"
# Review of the Solution

Let's review the solution statement by statement.

## Necessary Information

The solution correctly identifies the necessary information from the sentence, which is Jane wearing sunglasses outside at 4 PM and receiving strange looks as a result.

## Explanation of Terms

The definition of "weird looks" as strange or odd expressions or glances directed at someone is accurate and helpful for understanding the question.

## Rationale

The logic behind the solution's rationale is somewhat flawed. While the solution suggests that wearing sunglasses at 4 PM is uncommon because the sun is "likely not that bright anymore," this is not always the case. The intensity of sunlight at 4 PM can vary greatly depending on geographical location, season, weather conditions, and other factors. In many places and times of the year, the sun can still be quite bright at 4 PM, which could make wearing sunglasses a logical and common choice.

## Answer

The answer provided, <Answer>True</Answer>, assumes that wearing sunglasses at 4 PM would be unusual and therefore cause Jane to receive strange looks. As stated above, this assumption is flawed, as the brightness of the sun at 4 PM can vary widely, making wearing sunglasses potentially common and not out of the ordinary.

# Step by Step and Counterfactual Consideration

Let's reconsider the question step by step:

1. Jane wore sunglasses outside at 4 PM.
2. Because of this, she got some weird looks.

Now let's consider the counterfactuals:

- If Jane wore sunglasses outside at noon, would she get weird looks? Probably not, as it's common to wear sunglasses at the brightest part of the day.
- If Jane wore sunglasses inside or at night, would she get weird looks? Probably, as it's not common to wear sunglasses in low-light conditions.

Given that the brightness at 4 PM can be similar to noon in many cases, it's not necessarily unusual for Jane to wear sunglasses at this time.

# Answer with TAGS

We cannot definitively state that the sentence is true or false without additional context about the brightness of the sun at the time and location where Jane wore her sunglasses. However, considering that 4 PM is not an unusual time to wear sunglasses in many parts of the world, it's not necessarily true that Jane would get weird looks for doing so.

Therefore, the most likely answer is: <Answer>False</Answer>
\"\"\"
"""

reviewer_example = ''

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
"""
You are an objective and fair reviewer. You are responsible for evaluating a possible solution following the outline: 
    - **Review Statements One by One**
        (Examine the following aspects in the solution. Especially, watch out for factualness errors and inference errors in the solution)
        - Evaluation on Explanation of Terms: 
        - Evaluation on Subquestion Decomposition and Answering: 
        - Evaluation on the Reasoning process: 
        - Evaluation on the Answer: 

    - **Reconsider the Question Step by Step and Consider Counterfactuals**
        - Your counterfactual reasoning about the option that you need to look out for: 
            - The option that needs to look out for is: 
            - What if we apply this option: 
            - Will there be a contradition: 
        - Your step-by-step reasoning to arrive at the most likely answer: 

    - **Provide Your Answer With TAGS**
      (you MUST enclose your answer with TAGS, e.g., <Answer>A/B/C</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )



"""

