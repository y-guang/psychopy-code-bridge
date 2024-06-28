import logging.config
import pathlib
import xml.etree.ElementTree as ET
import logging
import html
from typing import List, Dict, Tuple
import shutil

# settings
STAGE_COMMENT_TEMPLATE = """
########################################################################################################################
# {stage}
# It is auto generated. DO NOT MODIFY THE COMMENT
########################################################################################################################
""".strip()

PREFACE_COMMENT_TEMPLATE = """
########################################################################################################################
# Prologue
# It is auto generated. DO NOT MODIFY THE COMMENT.
# This part will NOT be synced and executed. Add what you want to make the language server happy.
########################################################################################################################
{code_import}
""".strip()

CODE_FILENAME_TEMPLATE = 'code__{routine_name}__{code_name}.py'
PREFACE_FILENAME = 'code__preface.py'

CODE_STAGES = [
    'Before Experiment',
    'Begin Experiment',
    'Begin Routine',
    'Each Frame',
    'End Routine',
    'End Experiment',
]

RELATIVE_CODE_PATH_OF_EXPERIMENT = '.'

logging.basicConfig(level=logging.INFO)

# evaluate the paths
TOOL_FOLDER = pathlib.Path(__file__).resolve().parent
EXPERIMENT_FOLDER = TOOL_FOLDER.parent
CODE_FOLDER = (EXPERIMENT_FOLDER / RELATIVE_CODE_PATH_OF_EXPERIMENT).resolve()
PREFACE_SRC_PATH = TOOL_FOLDER / 'resources' / 'preface.py'


def find_experiments(folder_path: pathlib.Path) -> List[pathlib.Path]:
    """
    Find all the experiment files in the experiment folder.
    """
    experiment_files = [
        file for file in folder_path.iterdir() if file.suffix == '.psyexp']
    return experiment_files


def extract_routines(tree: ET.ElementTree) -> ET.Element:
    """
    Extract routines element from the tree.
    """
    root = tree.getroot()
    routines = root.find('Routines')
    assert routines is not None, 'No Routines element found in the experiment file'
    return routines


def extract_routines_code(routines: ET.Element) -> List[Tuple[ET.Element, ET.Element]]:
    """
    Extract code components from the routines with their parent routine element
    """
    code_components: List[Tuple[ET.Element, ET.Element]] = []
    for routine in routines:
        for component in routine:
            if component.tag != 'CodeComponent':
                continue
            code_components.append((routine, component))
    return code_components


def build_code_file_name(routine: ET.Element, code: ET.Element) -> str:
    routine_name = routine.attrib['name']
    code_name = code.attrib['name']
    return CODE_FILENAME_TEMPLATE.format(routine_name=routine_name, code_name=code_name)


def build_code_preface(import_files: List[pathlib.Path]) -> str:
    code_import = '\n'.join(
        f'from {file.stem} import *' for file in import_files)
    preface = f'{PREFACE_COMMENT_TEMPLATE.format(code_import=code_import)}\n'
    return preface


def download_code_files(routine: ET.Element, component: ET.Element, path: pathlib.Path, prev_file: pathlib.Path):
    """
    Save the code component to the path.
    """
    # extract codes form the component
    code_params: Dict[str, ET.Element] = {
        param.attrib['name']: param for param in component}
    codes: List[str] = [build_code_preface([prev_file])]

    # extract the interested code stages
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

    with path.open('w') as code_file:
        code_file.write(''.join(codes))


def upload_code_files(routine: ET.Element, component: ET.Element, path: pathlib.Path):
    """
    Upload the code file to the component.
    """
    code_params: Dict[str, ET.Element] = {
        param.attrib['name']: param for param in component}

    # read the code file
    with path.open('r') as code_file:
        all_stage_code = code_file.read()

    # reversely parse the code to the component
    reverse_stages = CODE_STAGES.copy()
    reverse_stages.reverse()
    for stage in reverse_stages:
        # find the stage code
        stage_comment = STAGE_COMMENT_TEMPLATE.format(stage=stage)
        start = all_stage_code.find(stage_comment)
        if start == -1:
            logging.error(f'SKIP current file: stage {stage} is missing in the code file {path.name}.')
            break
        copy_start = start + len(stage_comment)  # skip the newline
        code = all_stage_code[copy_start:].strip()  # skip the newline
        all_stage_code = all_stage_code[:start]

        # put the code to the component
        code_param = code_params.get(stage)
        if code_param is None:
            logging.error(
                f'stage {stage} is missing in routine [{routine.attrib["name"]}] component [{component.attrib["name"]}')
            break
        old_code = html.unescape(code_param.attrib['val']).strip()
        if code != old_code:
            escaped_code = html.escape(code)
            code_param.attrib['val'] = escaped_code
            logging.info(f'[{routine.attrib["name"]}] [{component.attrib["name"]}] [{stage}] is updated')



def copy_preface_file(preface_dest_path: pathlib.Path):
    """
    Prepare the preface file.
    """
    try:
        shutil.copy(PREFACE_SRC_PATH, preface_dest_path)
    except FileNotFoundError as e:
        logging.error('Preface file is missing')
        raise e
    except FileExistsError as e:
        logging.error('Preface file already exists')
        raise e
    except Exception as e:
        logging.error(f'Error: {e}')


def sync_experiment(experiment_path: pathlib.Path):
    """
    Sync the experiment with the code files.
    """
    # copy the preface to the code folder
    preface_path = CODE_FOLDER / PREFACE_FILENAME
    if not preface_path.exists():
        try:
            copy_preface_file(preface_path)
            logging.info('Preface file is created')
        except Exception as e:
            return

    # parse the .psyexp file
    tree = ET.parse(experiment_path)
    routines = extract_routines(tree)
    code_components = extract_routines_code(routines)

    # check if these code components are already in the code folder
    prev_file: pathlib.Path = preface_path
    code_paths = [(CODE_FOLDER / build_code_file_name(routine, code)).resolve()
                  for routine, code in code_components]
    for i, code_path in enumerate(code_paths):
        routine, code = code_components[i]
        if not code_path.exists():
            # create the code file
            download_code_files(routine, code, code_path, prev_file)
            logging.info(f'{code_path.name} is created')
        else:
            # update the code file to experiment
            upload_code_files(routine, code, code_path)
        prev_file = code_path
    
    # write the changes to the experiment
    tree.write(experiment_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    experiment_paths = find_experiments(EXPERIMENT_FOLDER)
    assert len(
        experiment_paths) > 0, 'No .psyexp file found in the experiment folder'

    # preparing
    if not CODE_FOLDER.exists():
        CODE_FOLDER.mkdir()

    for experiment_path in experiment_paths:
        logging.info(f'Syncing experiment {experiment_path.name}')
        sync_experiment(experiment_path)
