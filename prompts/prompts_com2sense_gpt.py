base_prompt = \
"""Jugde whether the given sentence is truthful. Your reply MUST only include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\'. 
"""

cot_prompt = \
"""Jugde whether the given sentence is truthful. Your reply MUST include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\' at the end. 
"""

one_shot_cot_prompt = \
"""
Jugde whether the given sentence is truthful. Your reply MUST include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\' at the end. 

An example: 
\"\"\"
Q: Judge whether the sentense is true or false: "If I want to weigh down some papers, it is much better to use an empty plastic bag than a baseball."
A: This statement appears to be making a comparison between the effectiveness of an empty plastic bag and a baseball for the purpose of weighing down papers. An empty plastic bag is typically light with minimal mass, and thus would not be very effective in preventing papers from being moved around, especially in the presence of wind or air movement. On the other hand, a baseball is significantly heavier and would be more effective in keeping papers in place due to its mass. Therefore, the assertion that an empty plastic bag is "much better" than a baseball for this purpose appears to be incorrect. 

Therefore, the answer is <Answer>False</Answer>. 
\"\"\"

"""


few_shot_cot_prompt2 = \
"""
Following the example below to think step by step: 

Q: Judge whether the sentense is true or false: "I prefer a stronger more bitter coffee, whereas my sister prefers a smoother, lighter coffee, so I like Starbucks better than my sister does."
A: The sentence you've given is subjective, based on personal preferences and not a universally applicable fact that could be definitively labeled as true or false. However, based on the information you've provided, we can make an educated inference.

The sentence states that the speaker prefers a stronger, more bitter coffee. Starbucks is generally known for having a bold, robust flavor profile, which could be interpreted as stronger and more bitter. So it would seem reasonable that someone with these preferences might favor Starbucks.

On the other hand, the speaker's sister prefers a smoother, lighter coffee. If Starbucks' flavor profile doesn't match her preferences, she might not like Starbucks as much as the speaker does.

Given these points, the sentence seems plausible based on the preferences stated. So, an educated guess would be:

<Answer>True</Answer>


"""


selfconsistent_prompt = \
"""Jugde whether the given sentence is truthful. Your reply MUST include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\' at the end. 
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


"""
Jane got some weird looks because she wore sunglasses outside at 4 PM.
Q: Did Jane wear sunglasses outside at 4 PM?
A: Yes, based on the statement "Jane got some weird looks because she wore sunglasses outside at 4 PM," it can be inferred that Jane did indeed wear sunglasses outside at 4 PM.

Q: Did people notice Jane wearing sunglasses?
A: Yes, based on the statement "Jane got some weird looks", it can be inferred that people noticed Jane wearing sunglasses outside at 4 PM and their reaction was noticeable enough for Jane to feel uncomfortable or self-conscious about it.

Q: Did people give Jane strange looks?
A: Yes, based on the statement "Jane got some weird looks", it can be inferred that people gave Jane strange looks for wearing sunglasses outside at 4 PM.
"""

least_to_most_subq_solver_prompt = \
"""
Answer the questions one by one according to the context. 

There is an example: 
\"\"\"
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
Question: Judge whether the sentense is true or false: 
"I prefer a stronger more bitter coffee, whereas my sister prefers a smoother, lighter coffee, so I like Starbucks better than my sister does."
    
Response: 
- **List necessary information to solve the question**: 

  - The speaker's preference for stronger, more bitter coffee.
  - The sister's preference for smoother, lighter coffee.
  - The characterization of Starbucks coffee as stronger and more bitter or smoother and lighter.

- **Explanation of Terms**: 

  - Starbucks: A multinational chain of coffeehouses and roastery reserves known for their strong and robust coffee.
  - Stronger, more bitter coffee: A type of coffee that has a robust flavor and may have a higher level of acidity or bitterness. This is often associated with dark roast coffee.
  - Smoother, lighter coffee: A type of coffee that has a more delicate flavor and is often less acidic or bitter than darker roasts. This is often associated with light roast coffee.

- **Rationale**: 

  The statement's truthfulness depends on the characterization of Starbucks coffee. If Starbucks coffee is generally stronger and more bitter (which is often the case due to their tendency to roast beans on the darker side), then the statement would be true, as the speaker prefers this type of coffee. However, if Starbucks coffee is generally smoother and lighter, the statement would not be true, as the sister would likely prefer it more.

- **Provide your answer WITH TAGS**: 

  Given that Starbucks is known for its robust and dark roasted coffee, which is typically stronger and more bitter, we can make an educated guess that the statement is true.

  `<Answer>True</Answer>`.
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


our_reasoner1_prompt = f"""
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
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>True/False</Answer>. If the answer cannot be determined, make an educated guess. )

{example0}

Now, solve the question below by following the outline. Remember, You MUST give a certain answer with TAGS, <Answer>True</Answer> or <Answer>False</Answer>. If the answer cannot be determined, make an educated guess. 

"""

# - **Subquestion Decomposition and Answering**: 
# - **Subquestion Decomposition and Answering**: 



our_reasoner2_prompt = f"""
Follow the outline below to solve the question: 
    - **Explanation of Terms**: 
    (You need to explain each term used in the question to remove ambiguity. )
        - Term 1: ...

        - Term 2: ...

    - **Rationale for Arriving at the Answer**: 
    (You need to reason step by step for the correct answer based on the previous information. )

    - **Provide Your Answer WITH TAGS**: 
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>True/False</Answer>. If the answer cannot be determined, make an educated guess. )

{example1}

Now, solve the question below by following the outline. Remember, You MUST give a certain answer with TAGS, <Answer>True</Answer> or <Answer>False</Answer>. If the answer cannot be determined, make an educated guess. 

"""




example_reviewer = \
"""
Here is an example: 
For the question: 
\"\"\"
Judge whether the sentence is true or false: "Jane got some weird looks because she wore sunglasses outside at 4 PM."
\"\"\"


and a solution: 
\"\"\"
- **Explanation of Terms**:
  (You need to explain each term used in the question to remove ambiguity.)

  - Term 1: Weird looks: This refers to strange or odd expressions or glances that other people direct at someone.

  - Term 2: Sunglasses: These are a form of protective eyewear designed to prevent bright sunlight from damaging or discomforting the eyes.

- **Subquestion Decomposition and Answering**:
  (You need to decompose the question into several subquestions connected logically to arrive at the final answer. For each subquestion, provide your answer below it. )

  - Subquestion 1: Is wearing sunglasses at 4 PM an unusual behavior?

  - Answer to subquestion 1: Yes, wearing sunglasses at 4 PM can be considered unusual as the sun is generally not as bright at that time.

  - Subquestion 2: Can unusual behavior elicit weird looks from others?

  - Answer to subquestion 2: Yes, unusual behavior often attracts attention and may result in weird looks.

- **Rationale for Arriving at the Answer**:
  Based on the information provided and the answers to the subquestions, we can infer that Jane's unusual behavior of wearing sunglasses at 4 PM likely resulted in her receiving weird looks from others.

- **Provide Your Answer WITH TAGS**:
  (Based on the rationale and the answers to the subquestions, the statement "Jane got some weird looks because she wore sunglasses outside at 4 PM" is likely true.)
  <Answer>True</Answer>
\"\"\"


Your response is like:
\"\"\"
**Review Statements One by One**

  - **Evaluation of Explanation of Terms**:

    The explanations provided for the terms, "weird looks" and "sunglasses," are clear and accurate, aiding in an understanding of the context.

  - **Evaluation of Subquestion Decomposition and Answering**:

    The decomposition of the question into subquestions is done effectively. However, the answer to the first subquestion ("Is wearing sunglasses at 4 PM an unusual behavior?") may be subject to variation depending on geographical location, weather conditions, and cultural norms. This could have been better addressed.

  - **Evaluation of the Reasoning process**:

    The reasoning process does follow from the subquestions, leading to a plausible inference. However, it assumes that wearing sunglasses at 4 PM is universally unusual, which is not always the case.

  - **Evaluation of the Answer**:

    While the answer ("<Answer>True</Answer>") follows from the outlined reasoning process, it doesn't account for the potential variability in norms and responses to wearing sunglasses at 4 PM.

**Reconsider the Question Step by Step and Consider Counterfactuals**

  - **Your counterfactual reasoning about the option that you need to look out for**:

    - The option that needs to be looked out for is 'False'.

    - **What if we apply this option**: If we consider the statement to be false, it would mean that Jane did not receive weird looks because she wore sunglasses at 4 PM.

    - **Will there be a contradiction**: There is no inherent contradiction in considering the statement as false. It's possible Jane did not receive strange looks for wearing sunglasses at 4 PM.

  - **Your step-by-step reasoning to arrive at the most likely answer**:

    1. Wearing sunglasses at 4 PM may or may not be considered unusual, depending on various factors such as location, weather, and cultural norms.
    2. Even if it is considered unusual in some contexts, it does not automatically imply that it would elicit weird looks from others.
    3. Therefore, without additional context, it's not necessarily true that Jane got weird looks because she wore sunglasses at 4 PM.

**Provide Your Answer With TAGS**

  Reflecting on the variability of norms regarding wearing sunglasses and the lack of context indicating that Jane did receive weird looks, it's plausible that the statement could be false.

  <Answer>False</Answer>

\"\"\"
"""




example_reviewer = ''
our_reviewer_prompt = \
f"""
You are an objective and fair reviewer. You are responsible for evaluating a possible solution following the outline: 
    - **Review Statements One by One**
        (Examine the following aspects of the solution. Especially, watch out for factualness errors and inference errors in the solution)
        - Evaluation of Explanation of Terms: 
        - Evaluation of Subquestion Decomposition and Answering: 
        - Evaluation of the Reasoning process: 
        - Evaluation of the Answer: 

    - **Reconsider the Question Step by Step and Consider Counterfactuals**
        - Your counterfactual reasoning about the option that you need to look out for: 
            - The option that needs to be looked out for is: 
            - What if we apply this option: 
            - Will there be a contradiction: 
            
        - Your step-by-step reasoning to arrive at the most likely answer: 

    - **Provide Your Answer With TAGS**: 
    (You MUST enclose your answer with TAGS, e.g., <Answer>True/False</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )


# {example_reviewer}

"""