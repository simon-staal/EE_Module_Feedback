# EE Module Feedback <!-- omit in toc -->
Welcome to the repository with the tools to help maintain the module feedback resources for 3rd and 4th year modules. Hopefully, the previous EEE/EIE departmental representative gave you a brief overview of how to use this repository (harass them to do so if they haven't). Otherwise, you can always reach out to me (Simon Staal) by posting an issue on the repository (or find me on LinkedIn). Please find a guide on how to use the tools in the repository below:

# Table of contents <!-- omit in toc -->
- [The module feedback survey](#the-module-feedback-survey)
  - [Adding/Changing fields to the feedback survey](#addingchanging-fields-to-the-feedback-survey)
- [The python scripts](#the-python-scripts)

## The module feedback survey
As the EEE/EIE representative, you are responsible for gathering feedback from the current 3rd / 4th year cohorts regarding the modules available to them. For the most seemless experience, please use a survey similar to the one [here](https://forms.office.com/r/B8bkf2pGsE). Hopefully, the previous representative has a template you can use. You can share an existing survey with whoever the new representative using the microsoft forms UI, and they can create a fresh copy of it, updating the year and adding any new modules. Adding a new module to the survey *should* not break anything (hopefully). Really try to push to get feedback at the end of each term (use email / whatsapp / whatever to ask the students in the 3rd and 4th year cohorts). Make sure you use the same survey for entire duration of the year. Once you have obtained enough survey results, export the results to a excel file using the microsoft forms UI, and then save it as a .csv file.

### Adding/Changing fields to the feedback survey
If you would like to change the format of the feedback survey, you will need to update the tooling to ensure everything still works. You might find it useful to read about [how the tooling works](#the-python-scripts) before you try updating it. At the top of the [feedback_generator.py](feedback_generator.py) file, you should find 3 constants:
```python
DEFAULT_SURVEY_FIELD_MAPPING = {
    'Which term was your module in?': '_term',
    'Module (Autumn)': '_autumn',
    'Module (Spring)': '_spring',
    'How would you rate the module content (interesting, useful, etc.)': 'Content',
    'How would you rate the module organisation': 'Organisation',
    'How would you rate the lecturer(s) (engaging, passionate, etc.)': 'Lecturer',
    'How would you rate the module overall': 'Overall',
    'Please leave comments about the module (Optional)': 'Comments'
}

# These should match the fields above
DEFAULT_NUM_FEEDBACK_FIELDS = ['Content', 'Organisation', 'Lecturer', 'Overall']
DEFAULT_TEXT_FEEDBACK_FIELDS = ['Comments']
```
You need to ensure that the keys of `DEFAULT_SURVEY_FIELD_MAPPING` matches the question text on your form (you can check the headers of the survey feedback csv for the exact text). The mapped value is what will be rendered in the generated markdown as the sub-headings for the relevant feedback fields. You need to define whether these sub-headings represent numeric or text feedback by adding them to the relevant lists (`DEFAULT_NUM_FEEDBACK_FIELDS` for numeric fields and `DEFAULT_TEXT_FEEDBACK_FIELDS` for the textual feedback fields). 

Any fields in `DEFAULT_NUM_FEEDBACK_FIELDS` will be have their results averaged and rendered in the order they are defined in the *Quick Summary* section of a module:
    **Quick Summary**

    *Average module scores from 6 respondants.*
    - Content: 3.0 out of 5
    - Organisation: 3.0 out of 5
    - Lecturer: 2.67 out of 5
    - Overall: 2.5 out of 5

Any fields in `DEFAULT_TEXT_FEEDBACK_FIELDS` will have their contents rendered after the *Quick Summary* in the order in which they are defined, and will use their field name as the header:
    **Comments**

    This module is not be to judged by it's title - whilst the concepts themselves are quite fundamental to developing a foundation on AI, and despite the interesting and humorous delivery of the professor, the tutorials and labs proved to be barely effective in preparing for the final exam which turned out be the most challenging out of all the years taught and extremely time consuming. 


    Did not like this module. The lectures are way too long, boring and not useful. The content is fairly simple though, but the exam was way too long, no one could finish it. If you take this module, don't waste your time by watching all the lectures, find some other resources on the internet (online courses), they can be much better.

    etc...

Fields which start with an `_` (`_term`, `_autumn`, etc.) are used for internal processing, and should not be touched unless you know what you're doing (i.e. you've read and understood the code)

## The python scripts
To generate the feedback for the next year, you will require the following (for simplicity, place all files in the same directory as the scripts):
- The survey results for the current year saved as a .csv file
- The previous year's feedback **markdown** (.md) file
