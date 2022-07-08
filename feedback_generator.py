from cgitb import text
import csv
from io import TextIOWrapper
from typing import Dict, List
import re

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

class FeedbackGenerator:
    def __init__(self) -> None:
        self._feedback = None

    # ----------------------------------------------------
    # ---------------- Public Methods --------------------
    # ----------------------------------------------------

    def extract_feedback_from_csv(self, 
            raw_csv_path: str, 
            survey_field_mapping: Dict[str, str] = DEFAULT_SURVEY_FIELD_MAPPING, 
            num_feedback_fields: List[str] = DEFAULT_NUM_FEEDBACK_FIELDS, 
            text_feedback_fields: List[str] = DEFAULT_TEXT_FEEDBACK_FIELDS):
        """
        Extracts the feedback from the path specified by raw_csv_path.
        """
        self._survey_field_mapping = survey_field_mapping
        self._num_feedback_fields = num_feedback_fields
        self._text_feedback_fields = text_feedback_fields

        raw_feedback = self._parse_feedback(raw_csv_path)
        self._feedback: Dict[str, Dict] = self._process_feedback(raw_feedback)

    def get_feedback(self):
        """
        Returns the aggregated feedback as a dictionary of the following format:

        {
            module_name : {
                num_feedback_field : average_score,
                text_feedback_field : [list, of, responses]
            }
        }
        """
        if not self._feedback:
            raise Exception('[ERROR] No feedback found. Please call extract_feedback_from_csv first.')
        
        return self._feedback

    def write_feedback_to_file(self, dest_md_file: str, year: str, feedback: Dict[str, Dict]):
        """
        Formats and writes the given feedback (in the format produced by get_feedback()) for a particular year as markdown to the file specified by dest_md_path. If dest_md_path does not exist, the file will be created. To be honest you probably don't need to use this function, but leaving it public just in case.
        """   
        with open(dest_md_file, 'w') as out_file:
            for module, feedback in self._feedback.items():
                out_file.write(f'### {module}\n')
                self._write_feedback(out_file, year, feedback)
    
        print(f'[INFO] Successfully generated markdown, saved to {dest_md_file}')

    def append_to_feedback_file(self, old_feedback_path: str, dest_feedback_path: str, year: str):
        """
        Adds the formatted feedback for a given year to the existing formatted feedback markdown file specified by old_feedback_path, and saves the resulting combined feedback to dest_feedback_path. Will leave old_feedback_path unchanged. If dest_feedback_path does not exist will create a new file.
        """
        if not self._feedback:
            raise Exception('[ERROR] No feedback found. Please call extract_feedback_from_csv first.')
        
        feedback = self._feedback

        with open(dest_feedback_path, 'w') as out_file:
            with open(old_feedback_path, 'r') as in_file:
                curr_module = None
                while line := in_file.readline():
                    module_regex_match = re.search(r'(?<=^### )[A-Za-z ()]*$', line)
                    if module_regex_match:
                        curr_module = module_regex_match.group(0)
                        added_new_feedback = False

                    year_regex_match = re.search(r'(?<=^#### )([0-9]{4}-[0-9]{2})|(Older)$', line)
                    if year_regex_match and not added_new_feedback:
                        added_new_feedback = True
                        if curr_module not in feedback:
                            print(f'[WARNING] Could not find module {curr_module} in processed feedback') 
                        else:
                            print(f'[INFO] Wrote feedback for {curr_module}')
                            self._write_feedback(out_file, year, feedback[curr_module])
                            feedback.pop(curr_module)

                    out_file.write(line) # Write current line back
        print(f'[INFO] Finished generating formatting feedback, the updated feedback file can be found at {dest_feedback_path}')
        if feedback:
            print(f'[WARNING] Could not find existing feedback for the following modules: {list(feedback.keys())}')
            out_file = f'additional_feedback_{year}.md'
            #print(f'[INFO] Writing formatted feedback for these modules to {out_file}')
            self.write_feedback_to_file(out_file, year, feedback)

    # ----------------------------------------------------
    # ---------------- Private Methods -------------------
    # ----------------------------------------------------
                
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
                    if row[column_idx['_term']] == 'Autumn':
                        module = row[column_idx['_autumn']]
                    elif row[column_idx['_term']] == 'Spring':
                        module = row[column_idx['_spring']]

                    if module not in raw_feedback:
                        raw_feedback[module] = {}
                        raw_feedback[module]['_term'] = row[column_idx['_term']]
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
            print(f'[INFO] Successfully parsed {line_count - 1} reviews')
        
        return raw_feedback

    def _process_feedback(self, raw_feedback):
        feedback = {}
        for module, fields in raw_feedback.items():
            feedback[module] = {}
            for field in self._num_feedback_fields:
                values = fields[field]
                n = len(values)
                feedback[module][field] = sum(values) / n
            feedback[module]['_n_of_reviews'] = n

            for field in self._text_feedback_fields:
                feedback[module][field] = []
                for comment in fields[field]:
                    if len(comment) > 0:
                        feedback[module][field].append(comment)

        print('[INFO] Successfully aggregated feedback')
        return feedback

    def _write_feedback(self, out_file: TextIOWrapper, year: str, single_feedback: Dict):
        out_file.write(f'#### {year}\n')
        out_file.write('**Quick Summary**\n\n')
        out_file.write(f'*Average module scores from {single_feedback["_n_of_reviews"]} respondants.*\n')
        for field in self._num_feedback_fields:
            out_file.write(f'- {field}: {round(single_feedback[field], 2)} out of 5\n')
        out_file.write('\n')

        for field in self._text_feedback_fields:
            if single_feedback[field]:
                out_file.write(f'**{field}**\n\n')
            for resp in single_feedback[field]:
                out_file.write(f'{resp}\n\n\n')
