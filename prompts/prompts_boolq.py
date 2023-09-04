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

# cot_one_shot_prompt  = \
# """
# You need to answer the question by thinking step by step. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. 

# Here is an example:
# \"\"\"
# Q: is confectionary sugar the same as powdered sugar?
# A: 1. Confectioner's sugar and powdered sugar are both terms used in cooking and baking. They describe a type of sugar that is significantly more fine than granulated sugar.

# 2. In many regions, these two terms are used interchangeably. For example, in the United States, both terms refer to the same type of sugar.

# 3. In terms of texture, both confectioner's sugar and powdered sugar are finely ground. This fine texture allows them to dissolve more easily in recipes, making them ideal for use in icings, frostings, and other similar applications.

# 4. Both confectioner's sugar and powdered sugar often contain a small amount of anti-caking agent such as cornstarch. This helps prevent the finely ground sugar particles from clumping together.

# Based on these steps, we can conclude that confectioner's sugar and powdered sugar are indeed the same thing.

# <Answer>yes</Answer>
# \"\"\"


# """


base_prompt_zeroshot = \
"""Answer the question. You MUST enclose your answer with TAGS, <Answer>yes</Answer> or <Answer>no</Answer>. 
"""

base_prompt_oneshot = \
"""
Answer the question. Your reply MUST only include \'<Answer>yes</Answer>\' or \'<Answer>no</Answer>\'. 

An example: 
Q: do texas state troopers have to wear hats?
A: <Answer>yes</Answer>


"""

cot_zeroshot_prompt = \
"""Answer the question by thinking step by step. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. 
"""

cot_oneshot_prompt = \
"""Answer the question by thinking step by step. Your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. 

An example:
\"\"\"
Question: do texas state troopers have to wear hats?

Answer: 
1. Texas State Troopers, who are integral members of the Texas Department of Public Safety, are typically subject to specific guidelines regarding their uniform. These guidelines often detail the mandatory components of the uniform, the correct way to wear them, and appropriate occasions for each piece.
2. Building upon that, the standard uniform for Texas State Troopers has traditionally included a Stetson-style campaign hat.
3. It's important to note that hats are often considered a formal part of the uniform for many state troopers across various states, including Texas. 
4. Therefore, while the specific regulations may vary and are subject to change, it is safe to say that Texas State Troopers are generally required to wear hats as part of their official uniform.

The answer is <Answer>yes</Answer>. 
\"\"\"

"""




example0 = \
"""
Here is an example: 
\'\'\'
Question: 
do texas state troopers have to wear hats?

Response: 
- **Explanation of Terms**:
    - Texas State Troopers: They are law enforcement officers who work for the Texas Department of Public Safety. Their duties include enforcing laws, preventing crimes, and responding to emergencies.
    - Hats: In the context of uniforms, hats are a piece of clothing that is worn on the head. Different types of hats may be part of different uniforms, depending on the specific guidelines of the organization.

- **Subquestion Decomposition and Answering**:
    - What is the standard uniform for Texas State Troopers?
        - As of my knowledge cutoff in September 2021, Texas State Troopers typically wear a uniform that includes a shirt, pants, belt, boots, and often, a hat. However, the specifics might change over time or vary for different tasks or events.
    - Do these uniforms include a hat?
        - Yes, traditionally the uniform of a Texas State Trooper often includes a hat. However, this could vary based on the situation, the specific task at hand, or changes in the uniform policy.

- **Rationale for Arriving at the Answer**:
    - To answer the question definitively, we would need information about the current uniform regulations of the Texas Department of Public Safety, which I do not have beyond September 2021.
    - However, based on common practices in law enforcement and the traditional uniform of Texas State Troopers, it is reasonable to infer that they may be required to wear hats as part of their uniform.

- **Provide Your Answer WITH TAGS**:
    - Given the lack of up-to-date, specific information and based on the available knowledge and reasoning, my educated guess is:

    <Answer>yes</Answer>
\'\'\'
"""

example1 = \
"""
Here is an example:
\'\'\'
Question:
do iran and afghanistan speak the same language?

Response: 
- **Subquestion Decomposition and Answering**: 

  1. **Subquestion1**: What is the official language of Iran? 
     - Answer1: The official language of Iran is Persian (Farsi).

  2. **Subquestion2**: What are the official languages of Afghanistan?
     - Answer2: The official languages of Afghanistan are Pashto and Dari. Dari is a dialect of the Persian language, also known as Afghan Persian.

- **Explanation of Terms**: 

  - **Iran**: Iran is a country in the Middle East, known officially as the Islamic Republic of Iran. The official language of Iran is Persian (Farsi).

  - **Afghanistan**: Afghanistan is a landlocked country located within South and Central Asia. The official languages of Afghanistan are Pashto and Dari. Dari is a dialect of the Persian language, also known as Afghan Persian.

  - **Same language**: This means that the primary or official language spoken in both countries is identical.

- **Rationale for Arriving at the Answer**: 

  The official language of Iran is Persian (Farsi), and one of the official languages of Afghanistan is Dari, which is a dialect of Persian. Therefore, Iran and Afghanistan do share a language, but it's also important to note that they aren't exactly the same. Dari, while a form of Persian, has its own unique characteristics and differences when compared to Iranian Persian. Plus, Afghanistan has another official language, Pashto, that isn't spoken officially in Iran.

- **Provide Your Answer WITH TAGS**: 

  Given the above explanation and rationale, the answer to the question "Do Iran and Afghanistan speak the same language?" is <Answer>yes</Answer>, but with the caveat that the languages, while sharing a root, have distinct characteristics and that Afghanistan also has an additional official language.
\'\'\'
"""

example0 = ''
example1 = ''

our_reasoner1_prompt = f"""
You are a smart reasoner. 
Follow the outline to solve the question: 
- **Explanation of Terms**: 
- **Subquestion Decomposition and Answering**: 
- **Rationale for Arriving at the Answer**: 
- **Provide Your Answer WITH TAGS**: 
(You MUST give a certain answer with TAGS, <Answer>yes</Answer> or <Answer>no</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )


{example0}


Now, solve the question below by following the outline. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. 
"""



our_reasoner2_prompt = f"""
You are a smart reasoner. 
- **Subquestion Decomposition and Answering**: 
- **Explanation of Terms**: 
- **Rationale for Arriving at the Answer**: 
- **Provide Your Answer WITH TAGS**: 
(You MUST give a certain answer with TAGS, <Answer>yes</Answer> or <Answer>no</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )


{example1}


Now, solve the question below by following the outline. Remember, your reply MUST include <Answer>yes</Answer> or <Answer>no</Answer> at the end. Make an educated guess if the answer CANNOT BE DETERMINED. 
"""





reviewer_example = \
"""
Here is a demonstration: 
For the question: 
\"\"\"
can you use oyster card at epsom station?
\"\"\"

and a solution: 
\"\"\"
- List necessary information to solve the question: 
To answer this question, we need to know the location of Epsom station and the types of transportation systems that accept Oyster cards.

- Explanation of Terms: 
Oyster card: A smart card used for public transportation in London, UK, that can be loaded with credit to pay for fares on buses, trains, trams, and some river services.

Epsom station: A railway station in Epsom, Surrey, UK, operated by South Western Railway.

- Rationale: 
The acceptance of Oyster cards at Epsom station depends on whether it is part of the transportation network that accepts the card. To determine if Oyster cards can be used at Epsom station, we need to examine the location and transportation systems in the area.

- Provide your answer WITH TAGS: 
Yes. <Answer>yes</Answer> Oyster cards can be used at Epsom station, which is part of the South Western Railway network that accepts Oyster cards. However, it is important to note that Oyster cards are not accepted on National Rail services outside of the London fare zones, so it is advisable to check the fare system and ticket options before traveling to and from Epsom station.
\"\"\"


Your response is like:
\"\"\"
# Review Statements One by One

## Necessary Information
The necessary information for solving the question is sufficiently stated. The recognition of the need to understand the location of Epsom station and the transport systems that accept Oyster cards is crucial in answering the question correctly.

## Explanation of Terms
The explanation of terms is accurate. Both the Oyster card and Epsom station are properly defined. However, information that Epsom station is not in the London Oyster card zone could be more explicit since it directly pertains to the question.

## Rationale
The rationale provided is logical. It correctly identifies the need to establish whether Epsom station is part of the transportation network that accepts the Oyster card. However, the conclusion that Epsom station accepts Oyster cards because it is part of the South Western Railway network is not accurate.

## Answer
The answer provided is incorrect. Despite being part of the South Western Railway network, Epsom station is not within the London Oyster card zone and therefore does not accept Oyster cards.

# Reconsider the Question Step by Step and Options Counterfactually
The question asks whether Epsom station accepts Oyster cards. The passage correctly identifies the need to establish whether Epsom station is part of the network that accepts Oyster cards but fails to accurately determine that it is not.

# Provide Your Answer With TAGS
Epsom station is not within the London Oyster card zone and therefore does not accept Oyster cards. Therefore, the correct answer is: <Answer>No</Answer>.
\"\"\"
"""

reviewer_example = ''
our_reviewer_prompt = \
f"""
You are an outstanding reviewer. You are responsible for reviewing a possible solution following the outline: 
    - **Review Statements One by One**
    (Especially, take care of Factualness and Reasoning Errors in the Solution)
        - Explanation of Terms: ...
        - Subquestion Decomposition and Answering: ...
        - Rationale for Arriving at the Answer: ...
        - Answer: ...

    - **Reconsider the Question Step by Step and Consider Counterfactuals**
    (You need to in judge if the sentence is yes or no in general, your reasoning MUST leads to a certain answer. )

    - **Provide Your Answer With TAGS**
    (You MUST enclose your answer with TAGS, <Answer>yes</Answer> or <Answer>no</Answer>. Make an educated guess if the answer CANNOT BE DETERMINED. )


{reviewer_example}

"""