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

def handle_code_component(routine: ET.Element, component: ET.Element):
    code_params: dict[str, ET.Element] = {param.attrib['name']: param for param in component}

    for stage in CODE_STAGES:
        code_param = code_params.get(stage)
        if code_param is None:
            logging.warning(f'stage {stage} is missing in routine [{routine.attrib["name"]}] component [{component.attrib["name"]}]')
            continue
        encoded_code = code_param.attrib['val']
        decoded_code = html.unescape(encoded_code)
        # TODO: continue here

   

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