import re
from feedback_generator import FeedbackGenerator

# Getting user input with ArgParse would be nicer but I don't want this program to have any external dependencies
def main():
    raw_data = input('Please specify the path to the .csv containing the survey results\n')
    feedback_generator = FeedbackGenerator()
    feedback_generator.extract_feedback_from_csv(raw_data)
    old_feedback = input('Please specify the existing feedback file you\'d like to build on\n')
    new_feedback = input('Please specify the filename you\'d like to save the feedback to\n')
    year = input('Please specify the academic year the feedback is from (i.e. \'2021-22\')\n')
    while not re.match(r'^[0-9]{4}-[0-9]{2}$', year):
        year = input(f'Input {year} did not match the format YYYY/YY, please try again\n')
    feedback_generator.append_to_feedback_file(old_feedback, new_feedback, year)


if __name__ == '__main__':
    main()
