system_message_generic = "You are a helpful assistant"
user_message_generic = "What is the capital of Iran?"

system_message_blog_topics = """
When I ask you to generate an organized list of blog topic ideas, you will do this:
Understand the Context: Familiarize yourself with the provided information to fully understand it.
Identify the Audience: Keep our target audience in mind. What are their interests and needs related to our industry?
Innovate: Propose 5 unique blog ideas that stand out from typical content. Each idea should resonate deeply with our audience's core interests.
Offer Unique Insights: Your content should provide fresh perspectives or original research that readers can't find elsewhere.
Craft Engaging Headlines: Each idea should come with a compelling headline that captures attention and clearly reflects the content's value.
Deliver Value: Ensure the content is actionable and informative, fulfilling the promise of its headline.
Be Original: Steer clear of cliches. Use distinct and specific language that aligns with our brand and the topic.
Focus on Written Content: Focus on the written elements of the blog only, since images and other aspects are handled separately.
Structure Your Ideas: Present your top 5 ideas clearly, each with a headline and outlined guidance that follows this structure.

Format each blog idea like this example:
1. **Headline:**
   - **Overview:**
   - **Target Audience:**
   - **Unique Angle:**
   - **Value Proposition:**
   - **Key Takeaways:**
   - **Engagement Triggers:**
   - **SEO Keywords:**
   - **Tone and Style:**
"""
user_message_blog_topics = """
Generate an organized list of blog topic ideas for this:

{
  "Plant Based Gastroenterologist": {
    "Natural LSIs": [
      "vegan gastroenterologist",
      "vegetarian gastroenterology specialist",
      "plant-based digestive health doctor",
      "gastrointestinal doctor specializing in plant-based diets",
      "plant-based diet gastroenterologist"
    ],
    "Child LSIs": [
      "digestive health specialist",
      "gastrointestinal consultant",
      "digestive disorders physician",
      "gastroenterology expert",
      "digestive system doctor"
    ],
    "Parent LSIs": [
      "gastroenterologist",
      "medical doctor",
      "healthcare provider",
      "medical specialist",
      "clinical expert"
    ],
    "Related LSIs": [
      "dietary consultation",
      "plant-based nutrition advising",
      "gastrointestinal health screening",
      "digestive system diagnostics",
      "holistic health management"
    ],
    "Image Alt Text": [
      "Close-up headshot of Dr. Angie Sadeghi, smiling vegan gastroenterologist in a white lab coat.",
      "Dr. Angie Sadeghi, plant-based diet gastroenterologist, cheerfully looking at the camera with a light background.",
      "Professional portrait of Dr. Angie Sadeghi, showcasing a compassionate plant-based digestive health doctor.",
      "Dr. Angie Sadeghi appearing thoughtful, a specialist in vegetarian gastroenterology, with a gray backdrop.",
      "Caring and smiling Dr. Angie Sadeghi in her lab coat, expert in plant-based gastrointestinal health.",
      "Dr. Angie Sadeghi, a dedicated advocate for plant-based diets in gastroenterology, posing in her white coat.",
      "Engaging image of Dr. Angie Sadeghi, a medical doctor specializing in plant-based nutritional health.",
      "Portrait of Dr. Sadeghi, a gastrointestinal consultant focused on vegan dietary approaches, with a soft gray background.",
      "Dr. Sadeghi, in her medical attire, embodying professionalism as a plant-based diet gastroenterologist.",
      "Close view of Dr. Angie Sadeghi, radiant in her commitment to plant-based gastroenterology and patient care."
    ]
  }
}
Provide your top 5 ideas that are unique, engaging, interesting, valuable to the reader and captivating.
"""

system_message_fine_tune_data = """
When I ask you to create technical questions and answers using the information provided, you will craft in-depth training questions and answers and you will focus on:

Precision & Accuracy: Ensure responses use precise AMA Guides terminology, accurately reflecting its medical classifications and evaluation criteria.
Contextual Grasp: Design content to deepen understanding of the Guides' application in medical evaluations, emphasizing the relevance to legal and insurance contexts.
Scenario-Based Learning: Incorporate diverse hypothetical medical cases to teach practical application of the Guides across various conditions and impairments.
Clarity & Directness: Phrase questions clearly to avoid ambiguity, aiming directly at the learning objective.
Comprehensive & Contextual Responses: Ensure answers are thorough, contextualized, and reference specific AMA Guides sections where relevant.
Critical Analysis: Encourage questions that demand critical thinking, prompting analysis and evidence-based reasoning in line with AMA Guides principles.
Interdisciplinary Insight: Include content that bridges medical assessments with their implications in legal and insurance arenas, preparing for multidisciplinary collaboration.
Focus on creating high-quality, insightful content that fosters deep understanding and application of the AMA Guides in real-world scenarios.

Format your training data in prompt/response pairs.

Example:

**Question:** In cases of spinal cord injuries affecting the corticospinal tract, how should impairments that extend to the upper or lower extremities and potentially impact autonomic functions be accurately rated?

**Answer:** When spinal cord injuries involve the corticospinal tract and extend to the upper or lower extremities, it's essential to identify the specific nature and extent of the injury carefully. Use Table 15-6 for guidance on rating impairments of the upper extremities or station and gait impairments for the lower extremities. In instances where autonomic functions, such as bowel, bladder, or neurologic sexual functions, are also impaired, these should be concurrently evaluated and combined with the extremity impairment ratings. This requires a nuanced understanding of different spinal cord injury types and their impacts on the corticospinal tract, emphasizing the need for comprehensive assessments and potentially consultation with a spinal cord injury specialist. By thoroughly evaluating both motor and autonomic impairments, physicians can ensure a more holistic and accurate representation of the individual's impairment.

---

Provide exactly 5 questions and accurate, detailed answers based on the provided text.
"""
user_message_fine_tune_data = """
The thoracic spine impairment DRE categories are summarized in Table 15-4.


15.6  DRE: Cervical Spine

15.6a Criteria for Rating Impairment Due to Cervical Disorders
For cervical problems localized to the cervical or cervicothoracic region, use Table 15-5. If the cervical spine problem also leads to isolated bowel and/or bladder dysfunction not due to corticospinal damage, obtain the appropriate estimates for bowel and

bladder dysfunction from the gastrointestinal and urology chapters (Chapters 6 and 7) and combine these with the appropriate cervical spine DRE category from DRE I to V, listed in Table 15-5. If the cervical spine problem is due to corticospinal tract involvement, use Table 15-6 alone.

The DRE cervical categories are summarized in Table 15-5.

Figure 15-5 illustrates the relationship of nerve roots to the vertebral level.

The level at which nerve roots exit the spine relative to the vertebrae. The neurologic level of involvement is determined by identifying the lowest normally functioning nerve root.

In prior editions of the Guides, rating spinal cord injury was done either through a combination of DRE categories or in the nervous system chapter. It was decided in this edition to evaluate spinal cord injuries based on the criteria in the nervous system chapter (Chapter 13). These criteria are repeated in this section. For bilateral neurologic or corticospinal tract damage, consultation with a spinal cord injury specialist and review of Chapter 13, The Central and Peripheral Nervous System, is recommended. Thus, for an individual with a spinal cord injury affecting the upper extremities, use Table 15-6 and the appropriate impairment rating for impairment of one or both upper extremities. For impairments involving loss of use of the lower extremities, use the section in Table 15-6 pertaining to station and gait impairment. If there is additional bowel or bladder dysfunction, combine the upper extremity or lower extremity loss with impairments in bladder, anorectal, and/or neurologic sexual impairment as warranted.

Once a class has been selected, the exact value is obtained by combining the value with the corresponding additional impairment from DRE categories II through V for cervical and lumbar impairment and DRE categories II through IV for thoracic impairment. An exact value is determined based on the degree of impairment of ADL. Table 15-6 and the following examples illustrate the method for impairment rating of spinal cord injury.

All impairment estimates shown in the tables of this section are expressed as whole person impairments. Section 15.13 explains how to express a whole person spine impairment as a regional spine impairment. Tables 15-8 through 15-14 provide estimates for rating ankylosis and range of motion, while neurologic impairments are rated based on Tables 15-15 through 15-18. The data on standards and normal functioning described in this section are based on both medical studies and consensus judgments.15,18-27
"""
message_template_fine_tune_generic = """
I'm doing a comprehensive training to provide a very deep understanding of the topic below for a group of people who are already experts, but I'm helping to make them world-class leaders on the topic. My goal is to create a large number of questions and answers to train them in significant detail. Please create ideal training content from this data. Since your generated output is the only training questions and answers I will have for this specific text, be sure to cover as much as possible and go as in-depth as possible.

{DATA_FOR_TRAINING}!
"""
message_template_fine_tune_ama = """
I'm training a fellow physician to have a very deep understanding of the AMA Guides to assist doctors and attorneys with Workers' Compensation cases, now that I'm retiring. My goal is to create a large number of questions and answers to train the physician on the guides in significant detail. Please create ideal training content from this data. Since your generated output is the only training questions and answers I will have for this specific text, be sure to cover as much as possible and go as in-depth as possible.

{DATA_FOR_TRAINING}!
"""

system_message_fine_tune_data_2 = """
When I ask you to create technical questions and answers using the information provided, you will craft in-depth training questions and answers and you will focus on:

Precision & Accuracy: Ensure responses use precise AMA Guides terminology, accurately reflecting its medical classifications and evaluation criteria.
Contextual Grasp: Design content to deepen understanding of the Guides' application in medical evaluations, emphasizing the relevance to legal and insurance contexts.
Scenario-Based Learning: Incorporate diverse hypothetical medical cases to teach practical application of the Guides across various conditions and impairments.
Clarity & Directness: Phrase questions clearly to avoid ambiguity, aiming directly at the learning objective.
Comprehensive & Contextual Responses: Ensure answers are thorough, contextualized, and reference specific AMA Guides sections where relevant.
Critical Analysis: Encourage questions that demand critical thinking, prompting analysis and evidence-based reasoning in line with AMA Guides principles.
Interdisciplinary Insight: Include content that bridges medical assessments with their implications in legal and insurance arenas, preparing for multidisciplinary collaboration.
Focus on creating high-quality, insightful content that fosters deep understanding and application of the AMA Guides in real-world scenarios.

Format your training data in prompt/response pairs.

Example:

**Question:** In cases of spinal cord injuries affecting the corticospinal tract, how should impairments that extend to the upper or lower extremities and potentially impact autonomic functions be accurately rated?

**Answer:** When spinal cord injuries involve the corticospinal tract and extend to the upper or lower extremities, it's essential to identify the specific nature and extent of the injury carefully. Use Table 15-6 for guidance on rating impairments of the upper extremities or station and gait impairments for the lower extremities. In instances where autonomic functions, such as bowel, bladder, or neurologic sexual functions, are also impaired, these should be concurrently evaluated and combined with the extremity impairment ratings. This requires a nuanced understanding of different spinal cord injury types and their impacts on the corticospinal tract, emphasizing the need for comprehensive assessments and potentially consultation with a spinal cord injury specialist. By thoroughly evaluating both motor and autonomic impairments, physicians can ensure a more holistic and accurate representation of the individual's impairment.

---

Provide exactly 5 questions and accurate, detailed answers based on the provided text.
"""
user_message_fine_tune_data_2 = """
Passive motion is that produced by an external force to determine the freedom and range of motion existing at a joint when all muscles are relaxed. An example,
is Bunnell's test for intrinsic tightness in the hand. Assisted active motion is the result of active muscle contraction and an external force applied to the joint; it allows for stabilization of a segment to improve the mechanical advantage of the muscles that move the joint being measured. In both cases, approximately 0.5 kg of force is applied while a segment of the joint is stabilized. Measurements of active motion take precedence in the Guides. The actual measured goniometer readings or linear measurements are recorded.

Many different factors can limit the normal range of motion of the joints of the upper extremities.
Limitation of active motion can be due to failure of the nerve, muscle, or tendon to execute the motion. Limitation of passive motion can be from involvement of the joint itself, a fixed contracture, or the antagonistic muscle or tendon that holds back the motion because it is adherent or too short. Sound clinical knowledge and measurement techniques are necessary for appropriate impairment evaluation and rating.

Digital joints are measured with the wrist held in neutral position and the forearm pronated. To measure the ROM of individual joints, the proximal joint(s) are stabilized in extension, and only the joint being measured is flexed. Note that if all three joints are flexed simultaneously, as in making a fist, active flexion of the metacarpophalangeal joint will be decreased. In some cases of decreased finger motion due to limited excursion of the activating musculotendinous unit or blockage of motion by the antagonistic musculotendinous unit, the measurement of individual joints, as described earlier, can be normal or near normal. In these situations, the total active range of motion (TAM) of the digit is measured.
Flexion of each joint is measured while all three joints are held in a position of maximum active flexion, or the finger is flexed as a whole unit; similarly, extension of each joint is measured while all three joints are held in maximum extension. The methods used to derive motion impairment of a digit using individual joint measurements and the total active range of motion of a digit are different, as explained on p. 465, Combining Abnormal Motion at More Than One Finger Joint. The joint measurement technique that best reflects the existing impairment is selected.


16.4 b Principle for Motion Impairment Calculation: A = E + F
The arc of motion is the total number of degrees of excursion measured between the two extreme angles of a plane of motion of a joint, for example, from maximum extension to maximum flexion. When there is complete loss of joint motion, or ankylosis, the total number of degrees of lost motion (A) equals the sum of lost extension degrees (E) and lost flexion degrees (F), or A = E + F. A always equals the total number of degrees of the normal arc of motion.
"""

system_message_fine_tune_data_3 = """
When I ask you to create technical questions and answers using the information provided, you will craft in-depth training questions and answers and you will focus on:

Precision & Accuracy: Ensure responses use precise AMA Guides terminology, accurately reflecting its medical classifications and evaluation criteria.
Contextual Grasp: Design content to deepen understanding of the Guides' application in medical evaluations, emphasizing the relevance to legal and insurance contexts.
Scenario-Based Learning: Incorporate diverse hypothetical medical cases to teach practical application of the Guides across various conditions and impairments.
Clarity & Directness: Phrase questions clearly to avoid ambiguity, aiming directly at the learning objective.
Comprehensive & Contextual Responses: Ensure answers are thorough, contextualized, and reference specific AMA Guides sections where relevant.
Critical Analysis: Encourage questions that demand critical thinking, prompting analysis and evidence-based reasoning in line with AMA Guides principles.
Interdisciplinary Insight: Include content that bridges medical assessments with their implications in legal and insurance arenas, preparing for multidisciplinary collaboration.
Focus on creating high-quality, insightful content that fosters deep understanding and application of the AMA Guides in real-world scenarios.

Format your training data in prompt/response pairs.

Example:

**Question:** In cases of spinal cord injuries affecting the corticospinal tract, how should impairments that extend to the upper or lower extremities and potentially impact autonomic functions be accurately rated?

**Answer:** When spinal cord injuries involve the corticospinal tract and extend to the upper or lower extremities, it's essential to identify the specific nature and extent of the injury carefully. Use Table 15-6 for guidance on rating impairments of the upper extremities or station and gait impairments for the lower extremities. In instances where autonomic functions, such as bowel, bladder, or neurologic sexual functions, are also impaired, these should be concurrently evaluated and combined with the extremity impairment ratings. This requires a nuanced understanding of different spinal cord injury types and their impacts on the corticospinal tract, emphasizing the need for comprehensive assessments and potentially consultation with a spinal cord injury specialist. By thoroughly evaluating both motor and autonomic impairments, physicians can ensure a more holistic and accurate representation of the individual's impairment.

---

Provide exactly 5 questions and accurate, detailed answers based on the provided text.
"""
user_message_fine_tune_data_3 = """
The origins and functions of the peripheral nerves that serve the upper extremities are summarized in Table 16-12. The motor innervation of the upper extremity is shown in Figure 16-47. The cutaneous innervation and related nerves are shown in Figure 16-48, the dermatomes of the upper extremities in Figure 16-49, and a schematic diagram of the brachial plexus in Figure 16-50.

Impairment Determination Method
Use the following method to evaluate the impairment resulting from each peripheral nerve structure:


1. If sensory deficits or pain is present, localize the distribution and relate it to the nerve structure involved (Table 16-12 and Figures 16-48, 16-49,
and 16-50).

2. If motor deficits or loss of power is present, identify the key muscles involved and relate the motor deficit to the nerve structure(s) involved (Table 16-12 and Figures 16-47 and 16-50).

3. Grade the severity of sensory deficits or pain according to Table 16-10a and/or that of the motor deficits according to Table 16-11a.

4. Find the values for maximum impairment of the upper extremity due to sensory and/or motor deficits of the nerve structure involved: individual spinal nerve (Table 16-13), brachial plexus (Table 16-14), and major peripheral nerves (Table 16-15).

5. For each nerve structure involved, multiply the grade of severity of the sensory and/or motor deficits (see step 3 above) by the appropriate maximum upper extremity impairment value (see step 4 above) to determine the upper extremity impairment percent for each function.

6.
For a structure with mixed motor and sensory fibers, determine the upper extremity impairment for each function (steps 1 through 5), then combine the sensory and motor impairment percents (Combined Values Chart, p. 604) to obtain the total upper extremity impairment value.

7. When more than one nerve structure is involved, combine their respective upper extremity impairment values (steps 1 through 5) to obtain the total upper extremity impairment resulting from peripheral nerve disorders (Combined Values Chart).

8. When multiple impairments of the extremity are present because of amputation, loss of motion that is not strictly attributed to a peripheral nerve lesion, or peripheral vascular disorders, combine the peripheral nerve upper extremity impairment value with the other upper extremity impairment values (Combined Values Chart) to obtain the total upper extremity impairment.

9. The total upper extremity impairment is converted to a whole person impairment by means of Table 16-3.

10. If there is bilateral upper extremity involvement, determine separately the impairment values for each side, and convert them to whole person impairment. Combine the whole person impairment values for each side (Combined Values Chart) to obtain the total whole person impairment. Consult page 435 for further comments on bilateral upper extremity involvement.

Grading Sensory Deficits or Pain
A wide range of abnormal sensations may be associated with peripheral nerve lesions, including diminished sensation (anesthesia or hypesthesia), abnormal sensation (dysesthesia or paresthesia), and increased sensation (hyperesthesia). Another possible manifestation is pain of various types, including pain resulting from nonnoxious stimulus (allodynia), overreactive pain (hyperpathia), a state of dysesthetic pain (deafferentation), and, most significantly, the sustained, burning pain present in CRPS I (RSD)
"""

blog_topic_params = {
    'variable_name': 'FIVE_BLOG_IDEAS_FULL_RESPONSE_1001',
    'processors': [
        {
            'processor': 'get_markdown_asterisk_structure',
            'depends_on': 'content',
            'extraction': [
                {
                    'key_identifier': 'nested_structure',
                    'key_index': 1,
                    'output_type': 'text'
                },
                {
                    'key_identifier': 'nested_structure',
                    'key_index': 2,
                    'output_type': 'text'
                },
                {
                    'key_identifier': 'nested_structure',
                    'key_index': 3,
                    'output_type': 'text'
                },
                {
                    'key_identifier': 'nested_structure',
                    'key_index': 4,
                    'output_type': 'text'
                },
                {
                    'key_identifier': 'nested_structure',
                    'key_index': 5,
                    'output_type': 'text'
                }
            ]
        }
    ]
}

markdown_asterisk_params = {
    'processors': [
        {
            'processor': 'get_markdown_asterisk_structure',
            'depends_on': 'content',
            'return_broker': 'FIVE_BLOG_IDEAS_FULL_RESPONSE_1001',
            "extraction": [
                {
                    "key_identifier": "nested_structure",
                    "key_index": 1,
                    "output_type": "text"
                },
            ]
        },
    ],
}

fine_tune_data_params = {
    'variable_name': 'FINE_TUNE_DATA_SETS_1001',
    'processors': [
        {
            'processor': 'get_markdown_asterisk_structure',
            'depends_on': 'content',
            'return_broker': 'SOME_PART_OF_FINE_TUNE_DATA',
        },
        {
            'processor': 'data_groups',
            'depends_on': 'get_markdown_asterisk_structure',
            'return_broker': 'SOME_OTHER_PART_OF_FINE_TUNE_DATA',
            "args": {
                "parts_count": 2
            }
        },
        {
            'processor': 'clean_groups',
            'depends_on': 'data_groups',
            'return_broker': 'ANOTHER_PART_OF_FINE_TUNE_DATA',

        },
        {
            'processor': 'add_parts',
            'depends_on': 'clean_groups',
            'return_broker': 'YET_ANOTHER_PART_OF_FINE_TUNE_DATA',
            "args": {
                "additional_parts": []
            }
        },
        {
            'processor': 'define_key_value_pairs',
            'depends_on': 'add_parts',
            "args": {
                "keys": ["user_content", "assistant_content", "system_content", ]
            }
        },
        {
            'processor': 'oai_fine_tuning_data',
            'depends_on': 'define_key_value_pairs',
            "args": {}
        }
    ]
}
system_datapoint_fine_tune = "You are an AMA Guide Expert."


def get_sample_messages(sample_type):
    if sample_type == "generic_data":
        return system_message_generic, user_message_generic
    elif sample_type == "blog_topics":
        return system_message_blog_topics, user_message_blog_topics
    elif sample_type == "fine_tune_data":
        return system_message_fine_tune_data, user_message_fine_tune_data
    elif sample_type == "fine_tune_data_2":
        return system_message_fine_tune_data_2, user_message_fine_tune_data_2
    elif sample_type == "fine_tune_data_3":
        return system_message_fine_tune_data_3, user_message_fine_tune_data_3
    else:
        return system_message_generic, user_message_generic


def get_sample_return_params(params_type):
    if params_type == "blog_topics":
        return blog_topic_params
    elif params_type == "markdown_asterisk_params":
        return markdown_asterisk_params
    elif params_type == "fine_tune_params":
        return fine_tune_data_params
    else:
        return None


def get_fine_tune_message_template(type):
    if type == "generic":
        return message_template_fine_tune_generic
    elif type == "ama_guides":
        return message_template_fine_tune_ama
    else:
        return message_template_fine_tune_generic


def get_system_datapoint_fine_tune(type):
    if type == "generic":
        return system_datapoint_fine_tune
    elif type == "ama_guides":
        return system_datapoint_fine_tune
    else:
        return system_datapoint_fine_tune


processors = [
    {
        'processor': 'get_markdown_asterisk_structure',
        'depends_on': 'content',
    },
    {
        'processor': 'define_key_value_pairs',
        'depends_on': 'add_parts',
    },
    {
        'processor': 'data_groups',
        'depends_on': 'get_markdown_asterisk_structure',
    },
    {
        'processor': 'clean_groups',
        'depends_on': 'data_groups',
    },
    {
        'processor': 'validate_data'
    },
    {
        'processor': 'add_parts',
        'depends_on': 'clean_groups',
    },
    {
        'processor': 'oai_fine_tuning_data',
        'depends_on': 'content',
    },
    {
        'processor': 'oai_fine_tuning_data',
        'depends_on': 'define_key_value_pairs',
    }
]
