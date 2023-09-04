least_to_most_decomposer_prompt = \
"""
- To answer a question is true or false given a passage, you need to provide a series of sub-questions that lead us to the final answer. 
- You MUST enclose each subquestion with TAGS <subquestion>[your_subquestion]</subquestion>)

There are a few examples: 
Q: do good samaritan laws protect those who help at an accident
P: Good Samaritan laws offer legal protection to people who give reasonable assistance to those who are, or who they believe to be, injured, ill, in peril, or otherwise incapacitated. The protection is intended to reduce bystanders' hesitation to assist, for fear of being sued or prosecuted for unintentional injury or wrongful death. An example of such a law in common-law areas of Canada: a good Samaritan doctrine is a legal principle that prevents a rescuer who has voluntarily helped a victim in distress from being successfully sued for wrongdoing. Its purpose is to keep people from being reluctant to help a stranger in need for fear of legal repercussions should they make some mistake in treatment. By contrast, a duty to rescue law requires people to offer assistance and holds those who fail to do so liable.
A:
    To answer the question "do good samaritan laws protect those who help at an accident." we would need to know the answers to the following sub-questions:

    <subquestion>What do Good Samaritan laws offer legal protection for?</subquestion>
    <subquestion>Who are these laws intended to protect?</subquestion>
    <subquestion>Do Good Samaritan laws aim to reduce bystanders' hesitation to assist?</subquestion>
    <subquestion>Can a rescuer who voluntarily helps a victim in distress be successfully sued for wrongdoing under Good Samaritan laws?</subquestion>

Q: is windows movie maker part of windows essentials
P: Windows Movie Maker (formerly known as Windows Live Movie Maker in Windows 7) is a discontinued video editing software by Microsoft. It is a part of Windows Essentials software suite and offers the ability to create and edit videos as well as to publish them on OneDrive, Facebook, Vimeo, YouTube, and Flickr.
A: 
    To answer the question "is windows movie maker part of windows essentials." we would need to know the answers to the following sub-questions:
    
    <subquestion>What is Windows Movie Maker?</subquestion>
    <subquestion>What was Windows Movie Maker known as in Windows 7?</subquestion>
    <subquestion>Is Windows Essentials a software suite that includes Windows Movie Maker?</subquestion>

Q: is batman and robin a sequel to batman forever
P: With the box office success of Batman Forever in June 1995, Warner Bros. immediately commissioned a sequel. They hired director Joel Schumacher and writer Akiva Goldsman to reprise their duties the following August, and decided it was best to fast track production for a June 1997 target release date, which is a break from the usual 3-year gap between films. Schumacher wanted to homage both the broad camp style of the 1960s television series and the work of Dick Sprang. The storyline of Batman & Robin was conceived by Schumacher and Goldsman during pre-production on A Time to Kill. Portions of Mr. Freeze's back-story were based on the Batman: The Animated Series episode ``Heart of Ice'', written by Paul Dini.
A: 
    To answer the question "is batman and robin a sequel to batman forever." we would need to know the answers to the following sub-questions:

    <subquestion>Was Batman Forever successful at the box office?</subquestion>
    <subquestion>Did Warner Bros. commission a sequel to Batman Forever?</subquestion>
    <subquestion>Is Batman & Robin the sequel to Batman Forever?</subquestion>
"""

least_to_most_subq_solver_prompt = """
You need to answer the question one by one based on the given context".

An example:
\"\"\"
Now, provide the sub-questions for the question: 
Q: do good samaritan laws protect those who help at an accident.
P: Good Samaritan laws offer legal protection to people who give reasonable assistance to those who are, or who they believe to be, injured, ill, in peril, or otherwise incapacitated. The protection is intended to reduce bystanders' hesitation to assist, for fear of being sued or prosecuted for unintentional injury or wrongful death. An example of such a law in common-law areas of Canada: a good Samaritan doctrine is a legal principle that prevents a rescuer who has voluntarily helped a victim in distress from being successfully sued for wrongdoing. Its purpose is to keep people from being reluctant to help a stranger in need for fear of legal repercussions should they make some mistake in treatment. By contrast, a duty to rescue law requires people to offer assistance and holds those who fail to do so liable.
subQ: What do Good Samaritan laws offer legal protection for?
A: Good Samaritan laws offer legal protection to people who give reasonable assistance to those who are, or who they believe to be, injured, ill, in peril, or otherwise incapacitated.
subQ: Who are these laws intended to protect?
A: Good Samaritan laws are intended to protect individuals who provide reasonable assistance to those in need, especially in emergency situations.
subQ: Do Good Samaritan laws aim to reduce bystanders' hesitation to assist?
A: Yes, the protection offered by Good Samaritan laws is intended to reduce bystanders' hesitation to assist, as it prevents them from fearing being sued or prosecuted for unintentional injury or wrongful death when providing help.
subQ: Can a rescuer who voluntarily helps a victim in distress be successfully sued for wrongdoing under Good Samaritan laws?
A: No, under Good Samaritan laws, a rescuer who voluntarily helps a victim in distress is protected from being successfully sued for wrongdoing. The purpose of these laws is to encourage people to help strangers in need without the fear of legal repercussions if they make some mistake in treatment.
Finally, is the question 'do good samaritan laws protect those who help at an accident.' True or False according to the above content? Your reply MUST include '<Answer>True</Answer>' or '<Answer>False</Answer>' at the end.
A: Good Samaritan laws offer legal protection to those who provide reasonable assistance at an accident, reducing hesitation to help. It means <Answer>True</Answer>.
\"\"\"

"""

cot_one_shot_prompt  = \
"""
You need to answer the question by thinking step by step. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. 

Here is an example:
\"\"\"
Q: is confectionary sugar the same as powdered sugar?
A: 1. Confectioner's sugar and powdered sugar are both terms used in cooking and baking. They describe a type of sugar that is significantly more fine than granulated sugar.

2. In many regions, these two terms are used interchangeably. For example, in the United States, both terms refer to the same type of sugar.

3. In terms of texture, both confectioner's sugar and powdered sugar are finely ground. This fine texture allows them to dissolve more easily in recipes, making them ideal for use in icings, frostings, and other similar applications.

4. Both confectioner's sugar and powdered sugar often contain a small amount of anti-caking agent such as cornstarch. This helps prevent the finely ground sugar particles from clumping together.

Based on these steps, we can conclude that confectioner's sugar and powdered sugar are indeed the same thing.

<Answer>yes</Answer>
\"\"\"


"""


base_prompt = \
"""Answer the question. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer>. 
"""

cot_zeroshot_prompt = \
"""Answer the question by thinking step by step. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. 
"""

# cot_zeroshot_prompt = \
# """
# - Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer>. 
# """


base_prompt_2shot = \
"""
Answer the question based on the passage. Your reply MUST only include \'<Answer>True</Answer>\' or \'<Answer>False</Answer>\'. 


"""



our_reasoner1_prompt = """
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
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>yes/no</Answer>. If the answer cannot be determined, make an educated guess. )


"""
# Now, solve the question below by following the outline. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. 



our_reasoner2_prompt = """
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
    (You MUST choose ONE option, with the capital letter included in TAGS, e.g., <Answer>yes/no</Answer>. If the answer cannot be determined, make an educated guess. )


"""
#Now, solve the question below by following the outline. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. 



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
        - Your counterfacutal reasoning about the option that you need to look out for: 
            - The option that needs to look out for is: 
            - What if we apply this option: 
            - Will there be an contradition: 
        
        - Your step-by-step reasoning to arrive at the most likely answer: 
        (Your reasoning MUST lead to a certain answer. )

    - **Provide Your Answer With TAGS** 
      (You MUST enclose your answer (MUST be certain) with TAGS, e.g., <Answer>yes/no</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )


"""







