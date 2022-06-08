# EE Module Feedback <!-- omit in toc -->
Welcome to the repository with the tools to help maintain the module feedback resources for 3rd and 4th year modules. Hopefully, the previous EEE/EIE departmental representative gave you a brief overview of how to use this repository (harass them to do so if they haven't). Otherwise, you can always reach out to me (Simon Staal) by posting an issue on the repository (or find me on LinkedIn). Please find a guide on how to use the tools in the repository below:

# Table of contents <!-- omit in toc -->
- [Quick Start](#quick-start)
- [The module feedback survey](#the-module-feedback-survey)
  - [Adding/Changing fields to the feedback survey](#addingchanging-fields-to-the-feedback-survey)
- [The python scripts](#the-python-scripts)
- [Converting markdown to pdf](#converting-markdown-to-pdf)
  - [Markdown Viewer (Chrome Extension)](#markdown-viewer-chrome-extension)
  - [Markdown to PDF (Visual Studio Code Extension)](#markdown-to-pdf-visual-studio-code-extension)
  - [pandoc (Linux Terminal)](#pandoc-linux-terminal)

# Quick Start
1. Clone this repo
2. Add the survey results as a .csv to the folder
3. Add the previous year's markdown review to the folder
4. Run `python3 update_feedback.py` and follow the prompts
5. Convert the produced markdown to a pdf
6. Upload both the raw markdown file and the pdf to the [EE OneDrive](https://imperiallondon-my.sharepoint.com/:f:/r/personal/eeearn_ic_ac_uk/Documents/EE%20Resources?csf=1&web=1&e=8DrLe8)

# The module feedback survey
As the EEE/EIE representative, you are responsible for gathering feedback from the current 3rd / 4th year cohorts regarding the modules available to them. For the most seemless experience, please use a survey similar to the one [here](https://forms.office.com/r/B8bkf2pGsE). Hopefully, the previous representative has a template you can use. You can share an existing survey with whoever the new representative using the microsoft forms UI, and they can create a fresh copy of it, updating the year and adding any new modules. Adding a new module to the survey *should* not break anything (hopefully). Really try to push to get feedback at the end of each term (use email / whatsapp / whatever to ask the students in the 3rd and 4th year cohorts). Make sure you use the same survey for entire duration of the year. Once you have obtained enough survey results, export the results to a excel file using the microsoft forms UI, and then save it as a .csv file.

## Adding/Changing fields to the feedback survey
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

# The python scripts
To generate the feedback for the next year, you will require the following (for simplicity, place all files in the same directory as the scripts):
- The survey results for the current year saved as a .csv file
- The previous year's feedback **markdown** (.md) file

To generate the feedback for your year, simply run `python3 update_feedback.py` and follow the prompts! The script itself should be quite simple to read through, it uses the [feedback generator class](feedback_generator.py) to do all the work.

As more feedback gets added to the file, it might get a bit long. By running `python3 remove_feedback.py`, you will be able to remove sections of feedback which are linked to a year of your choice. Once again, just follow the prompts and you should be fine. I think a reasonable initial approach is to remove feedback that is older than 3 years, but use your common sense. It might also be better to preserve older reviews for modules with very little feedback. The best way of doing this is to manually move these into an "Older" section with a different header, that way it won't be automatically removed by the script. 

Also note that the "General Advice" and "Industrial Placement" sections of the feedback should be handled manually. As a rep, feel free to reach out to your year to ask if anyone wants to give general advice, otherwise for the moment I think what's there is plenty sufficient.

# Converting markdown to pdf
Ideally, we want to have a nicely rendered pdf uploaded to the EE OneDrive that's pleasant to read. There are many ways to do this (google is your friend), but I'll list some of my personal preferences here.

## Markdown Viewer (Chrome Extension)
[Markdown Viewer](https://chrome.google.com/webstore/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk?hl=en) is a Chrome Extension that lets you open markdown files in chrome. I like it because the resulting pdf matches the way github renders markdown files very closely. Once it's installed, simply perform the following steps:

1. Drag the file into Chrome to render it
2. Right click and select Print (Ctrl+P)
3. Select Save as PDF (Should be the default option)

## Markdown to PDF (Visual Studio Code Extension)
[Markdown to PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf) is a Visual Studio Code Extension that lets you save markdown files in a variety of formats (including pdf). I think it's nice (especially since I use VS Code to edit markdown files and don't use Chrome regularly) but I prefer the style of [markdown viewer](#markdown-viewer-chrome-extension). Once it's installed, just open the markdown file in VS Code, right click the editor window and select `Markdown PDF: Export (pdf)`. You can play around with the extension settings to change how it renders it, maybe you can find something that looks nicer than markdown viewer.

## pandoc (Linux Terminal)
[pandoc](https://pandoc.org/) is a CLI tool that you can use to convert pretty much any markup / markdown format to anything other format. You can install it (and its dependecies) using the following:
```
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra
```
You can then convert your file using:
```bash
pandoc example.md -o example.pdf
pandoc example.md --pdf-engine=xelatex -o example.pdf # Try this to see if it looks better?
```
This comes out looking similar to standard redered latex, so it could actually be quite nice! I'm not sure if it has stuff like emoji support / other github-flavoured markdown related stuff, but it could be worth a go.

