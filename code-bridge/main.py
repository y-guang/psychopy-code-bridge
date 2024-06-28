import pathlib
import xml.etree.ElementTree as ET
import logging
import html

CODE_STAGES = [
    'Before Experiment',
    'Begin Experiment',
    'Begin Routine',
    'Each Frame',
    'End Routine',
    'End Experiment',
]

STAGE_COMMENT_TEMPLATE = """
########################################################################################################################
# {stage} ----------------- auto generated. DO NOT MODIFY THE COMMENT
########################################################################################################################
""".strip()

CODE_FILENAME_TEMPLATE = 'code_{routine_name}.py'


TOOL_FOLDER = pathlib.Path(__file__).resolve().parent
EXPERIMENT_FOLDER = TOOL_FOLDER.parent

# TODO: what if more than one .psyexp file is found?
# find the .psyexp experiment in the experiment folder
for file in EXPERIMENT_FOLDER.iterdir():
    if file.suffix == '.psyexp':
        experiment_file = file
        break
else:
    raise FileNotFoundError('No .psyexp file found in the experiment folder')


def handle_code_component(routine: ET.Element, component: ET.Element):
    # extract codes form the component
    code_params: dict[str, ET.Element] = {
        param.attrib['name']: param for param in component}
    codes: list[str] = []

    for stage in CODE_STAGES:
        code_param = code_params.get(stage)
        if code_param is None:
            logging.warning(
                f'stage {stage} is missing in routine [{routine.attrib["name"]}] component [{component.attrib["name"]}]')
            continue
        encoded_code = code_param.attrib['val']
        decoded_code = html.unescape(encoded_code)
        codes.append(
            f'{STAGE_COMMENT_TEMPLATE.format(stage=stage)}\n{decoded_code}\n')

    # save to the EXPERIMENT_FOLDER
    routine_name = routine.attrib['name']
    code_file_name = CODE_FILENAME_TEMPLATE.format(routine_name=routine_name)
    code_file_path = EXPERIMENT_FOLDER / code_file_name
    with code_file_path.open('w') as code_file:
        code_file.write(''.join(codes))


# parse the .psyexp file
tree = ET.parse(experiment_file)
root = tree.getroot()
routines = root.find('Routines')
assert routines is not None
for routine in routines:
    for component in routine:
        if component.tag != 'CodeComponent':
            continue
        handle_code_component(routine, component)
