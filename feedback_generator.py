from cgitb import text
import csv
from io import TextIOWrapper
from typing import Dict, List
import re

DEFAULT_SURVEY_FIELD_MAPPING = {
    'Which term was your module in?': 'term',
    'Module (Autumn)': 'autumn',
    'Module (Spring)': 'spring',
    'How would you rate the module content (interesting, useful, etc.)': 'Content',
    'How would you rate the module organisation': 'Organisation',
    'How would you rate the lecturer(s) (engaging, passionate, etc.)': 'Lecturer',
    'How would you rate the module overall': 'Overall',
    'Please leave comments about the module (Optional)': 'Comments'
}

# These should match the fields above
DEFAULT_NUM_FEEDBACK_FIELDS = ['Content', 'Organisation', 'Lecturer', 'Overall']
DEFAULT_TEXT_FEEDBACK_FIELDS = ['Comments']

class FeedbackGenerator:
    def __init__(self) -> None:
        self._feedback = None

    def extract_feedback_from_csv(self, 
            raw_csv: str, 
            survey_field_mapping: Dict[str, str] = DEFAULT_SURVEY_FIELD_MAPPING, 
            num_feedback_fields: List[str] = DEFAULT_NUM_FEEDBACK_FIELDS, 
            text_feedback_fields: List[str] = DEFAULT_TEXT_FEEDBACK_FIELDS):
        self._survey_field_mapping = survey_field_mapping
        self._num_feedback_fields = num_feedback_fields
        self._text_feedback_fields = text_feedback_fields

        raw_feedback = self._parse_feedback(raw_csv)
        self._feedback: Dict[str, Dict] = self._process_feedback(raw_feedback)

    def _parse_feedback(self, raw_csv: str):
        raw_feedback = {}

        with open(raw_csv) as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            column_idx = {}
            for row in csv_reader:
                if line_count == 0: # Process header
                    for i, field in zip(range(len(row)), row):
                        if field in self._survey_field_mapping:
                            column_idx[self._survey_field_mapping[field]] = i
                else:
                    # process row
                    if row[column_idx['term']] == 'Autumn':
                        module = row[column_idx['autumn']]
                    elif row[column_idx['term']] == 'Spring':
                        module = row[column_idx['spring']]

                    if module not in raw_feedback:
                        raw_feedback[module] = {}
                        raw_feedback[module]['term'] = row[column_idx['term']]
                        for field in self._num_feedback_fields:
                            raw_feedback[module][field] = [int(row[column_idx[field]])]
                        for field in self._text_feedback_fields:
                            raw_feedback[module][field] = [row[column_idx[field]]]
                    else: 
                        for field in self._num_feedback_fields:
                            raw_feedback[module][field].append(int(row[column_idx[field]]))
                        for field in self._text_feedback_fields:
                            raw_feedback[module][field].append(row[column_idx[field]])
                        
                line_count += 1
            print(f'Successfully parsed {line_count - 1} reviews')
        
        return raw_feedback

    def _process_feedback(self, raw_feedback):
        feedback = {}
        for module, fields in raw_feedback.items():
            feedback[module] = {}
            for field in self._num_feedback_fields:
                values = fields[field]
                n = len(values)
                feedback[module][field] = sum(values) / n
            feedback[module]['n_of_reviews'] = n

            for field in self._text_feedback_fields:
                feedback[module][field] = []
                for comment in fields[field]:
                    if len(comment) > 0:
                        feedback[module][field].append(comment)

        print('Successfully aggregated feedback')
        return feedback

    def get_feedback(self):
        if not self._feedback:
            raise Exception('No feedback found. Please call extract_feedback_from_csv first.')
        
        return self._feedback

    def write_feedback_to_file(self, dest_md_file: str, year: str, feedback: Dict[str, Dict]):
        """
        Formats and writes the feedback
        """   
        with open(dest_md_file, 'w') as out_file:
            for module, feedback in self._feedback.items():
                out_file.write(f'### {module}\n')
                self._write_feedback(out_file, year, feedback)
    
        print(f'[INFO] Successfully generated markdown, saved to {dest_md_file}')

    def append_to_feedback_file(self, old_feedback_file: str, dest_feedback_file: str, year: str):
        if not self._feedback:
            raise Exception('No feedback found. Please call extract_feedback_from_csv first.')
        
        feedback = self._feedback

        with open(dest_feedback_file, 'w') as out_file:
            with open(old_feedback_file, 'r') as in_file:
                curr_module = None
                while line := in_file.readline():
                    out_file.write(line)
                    module_regex_match = re.search(r'(?<=^### )[A-Za-z ()]*$', line)
                    if module_regex_match:
                        curr_module = module_regex_match.group(0)
                        added_new_feedback = False

                    year_regex_match = re.search(r'(?<=^#### )([0-9]{4}/[0-9]{2})|(Older)$', line) # Remove 'Older' part of regex after 2021/22
                    if year_regex_match and not added_new_feedback:
                        added_new_feedback = True
                        if curr_module not in feedback:
                            print(f'[WARNING] Could not find module {curr_module} in processed feedback') 
                        else:
                            print(f'[INFO] Wrote feedback for {curr_module}')
                            self._write_feedback(out_file, year, feedback[curr_module])
                            feedback.pop(curr_module)
        print(f'[INFO] Finished generating formatting feedback, the updated feedback file can be found at {dest_feedback_file}')
        if feedback:
            print(f'[WARNING] Could not find existing feedback for the following modules: {list(feedback.keys())}')
            out_file = f'additional_feedback_{year}.md'
            print(f'[INFO] Writing formatted feedback for these modules to {out_file}')
            self.write_feedback_to_file(out_file, year, feedback)
                    

    def _write_feedback(self, out_file: TextIOWrapper, year: str, single_feedback: Dict):
        out_file.write(f'#### {year}\n')
        out_file.write('**Quick Summary**\n\n')
        out_file.write(f'*Average module scores from {single_feedback["n_of_reviews"]} respondants.*\n')
        for field in self._num_feedback_fields:
            out_file.write(f'- {field}: {round(single_feedback[field], 2)} out of 5\n')
        out_file.write('\n')

        for field in self._text_feedback_fields:
            if single_feedback[field]:
                out_file.write(f'**{field}**\n\n\n')
            for resp in single_feedback[field]:
                out_file.write(f'{resp}\n\n\n')
