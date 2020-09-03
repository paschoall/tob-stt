def write_story(intent, utter, file, iterations=1):
    result_string = ''
    for i in range(iterations):
        name = input("What concept: ").strip('\n')
        utter_name = name.replace(' ', '_')
        result_string += f'\n## {intent} {name}\n' + \
                         f'* {intent}\n' + \
                         '  - slot{"concept": ' + f'"{name}"' + '}\n' + \
                         f'  - utter_{utter}_{utter_name}\n'
    with open(file, 'a') as fp:
        fp.write(result_string)


def write_response(utter, file, iterations=1):
    result_string = '\n'
    for i in range(iterations):
        name = input("What concept: ").strip('\n')
        response = input("What answer: ").strip('\n')
        utter_name = name.replace(' ', '_')
        result_string += f'utter_{utter}_{utter_name}:\n' + \
                         f'  - text: "{response}"\n'
    with open(file, 'a') as fp:
        fp.write(result_string)
