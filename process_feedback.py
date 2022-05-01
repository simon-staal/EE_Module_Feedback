import csv
import json

NUM_FEEDBACK_FIELDS = ['Content', 'Organisation', 'Lecturer', 'Overall']
TEXT_FEEDBACK_FIELDS = ['Comments']
OUT_FILE = 'test_out.md'

def main():
    raw_file = input('Please specify the path to the .csv containing the survey results\n')
    raw_file = 'test_feedback.csv' # DELETE AFTER TESTING
    raw_feedback = parse_feedback(raw_file)
    feedback = process_feedback(raw_feedback)
    year = input('Please specify the academic year the feedback is from (i.e. \'2021/22\')\n')
    write_markdown(feedback, year)


def parse_feedback(raw_file):
    feedback = {}

    with open(raw_file) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        column_idx = {}
        for row in csv_reader:
            if line_count == 0:
                for i, field in zip(range(len(row)), row):
                    # Define survey fields here
                    if field == 'Which term was your module in?':
                        column_idx['term'] = i
                    elif field == 'Module (Autumn)':
                        column_idx['autumn'] = i
                    elif field == 'Module (Spring)':
                        column_idx['spring'] = i
                    elif field == 'How would you rate the module content (interesting, useful, etc.)':
                        column_idx['Content'] = i
                    elif field == 'How would you rate the module organisation':
                        column_idx['Organisation'] = i
                    elif field == 'How would you rate the lecturer(s) (engaging, passionate, etc.)':
                        column_idx['Lecturer'] = i
                    elif field == 'How would you rate the module overall':
                        column_idx['Overall'] = i
                    elif field == 'Please leave comments about the module (Optional)':
                        column_idx['Comments'] = i
            else:
                # process row
                if row[column_idx['term']] == 'Autumn':
                    module = row[column_idx['autumn']]
                elif row[column_idx['term']] == 'Spring':
                    module = row[column_idx['spring']]

                if module not in feedback:
                    feedback[module] = {}
                    for field in NUM_FEEDBACK_FIELDS:
                        feedback[module][field] = [int(row[column_idx[field]])]
                    for field in TEXT_FEEDBACK_FIELDS:
                        feedback[module][field] = [row[column_idx[field]]]
                else: 
                    for field in NUM_FEEDBACK_FIELDS:
                        feedback[module][field].append(int(row[column_idx[field]]))
                    for field in TEXT_FEEDBACK_FIELDS:
                        feedback[module][field].append(row[column_idx[field]])
                    
            line_count += 1
        print(f'Successfully parsed {line_count - 1} reviews')

    return feedback

def process_feedback(raw_feedback):
    feedback = {}
    for module, fields in raw_feedback.items():
        feedback[module] = {}
        for field in NUM_FEEDBACK_FIELDS:
            values = fields[field]
            n = len(values)
            feedback[module][field] = sum(values) / n
        feedback[module]['n_of_reviews'] = n

        for field in TEXT_FEEDBACK_FIELDS:
            feedback[module][field] = []
            for comment in fields[field]:
                if len(comment) > 0:
                    feedback[module][field].append(comment)

    print('Successfully processed feedback')
    return feedback
    
def write_markdown(feedback, year):
    with open(OUT_FILE, 'w') as file:
        for module, fields in feedback.items():
            file.write(f'### {module}\n')
            file.write(f'#### {year}\n')
            file.write('**Quick Summary**\n\n')
            file.write(f'*Average module scores from {fields["n_of_reviews"]} respondants.*\n')
            for field in NUM_FEEDBACK_FIELDS:
                file.write(f'- {field}: {round(fields[field], 2)} out of 5\n')
            file.write('\n')

            for field in TEXT_FEEDBACK_FIELDS:
                if fields[field]:
                    file.write(f'**{field}**\n\n\n')
                for resp in fields[field]:
                    file.write(f'{resp}\n\n\n')
    
    print(f'Successfully generated markdown, saved to {OUT_FILE}')

        


if __name__ == '__main__':
    main()
