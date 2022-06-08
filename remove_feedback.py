import re

# Removes the feedback from a certain year (to keep the file size manageable). As a rule of thumb, remove feedback older than 3 years (this might be better to do manually tbh)

# Getting user input with ArgParse would be nicer but I don't want this program to have any external dependencies
def main():
    old_feedback_path = input('Please specify the existing feedback file you\'d like to remove feedback from\n')
    new_feedback_path = input('Please specify the filename you\'d like to save the new feedback to\n')

    user_target = get_target_from_user(old_feedback_path)
    remove_feedback(old_feedback_path, new_feedback_path, user_target)


def get_target_from_user(old_feedback_path: str):
    print('[Info] Parsing feedback for possible years to remove...')
    targets = set()
    with open(old_feedback_path, 'r') as f:
        while line := f.readline():
            year_regex_match = re.search(r'(?<=^#### )([0-9]{4}-[0-9]{2})|(Older)$', line)
            if year_regex_match:
                targets.add(year_regex_match.group(0))

    print('[Info] Possible targets:')
    for target in targets:
        print(f'\t{target}')

    user_target = input('Please specify a target to remove\n')
    while user_target not in targets:
        user_target = input(f'Input {user_target} did not math any of the possible targets, please try again\n')
    
    return user_target

def remove_feedback(old_feedback_path: str, new_feedback_path: str, target: str):
    with open(old_feedback_path, 'r') as in_file:
        with open(new_feedback_path, 'w') as out_file:
            in_target_section = False
            while line := in_file.readline():
                if re.search(r'^#+ ', line): # If a line starts with one or more hashes followed by a space it's a header
                    in_target_section = False
                if f'#### {target}' in line:
                    in_target_section = True
                
                if not in_target_section:
                    out_file.write(line)



if __name__ == '__main__':
    main()
