# PsychoPy Code Sync

[English](README.md) | [中文说明](locale/README_zh.md)

A tool that allows user to extract, edit, and reintegrate code components for PsychoPy experiments to simplify the process of creating and editing experiments.

### Why Even Bother?

- Utilize both your favorite IDE and PsychoPy builder. 
- More readable Git history for code components.

## Usage

WARNING: Before first try, make sure to backup your experiment file. And only run this script in your experiment directory when you are sure it works. Data loss will ruin your day.

1. Copy the whole [code-sync](code-sync) directory to your experiment directory, so it looks like this:

```
experiment/
├── *.psyexp
├── code-sync/
│   ├── main.py
├── ...
```

2. run [main.py](code-sync/main.py) in the code-sync directory.

## How It Works

If you first run the script, it will create several python files in your experiment directory. Each file corresponds to a code component in your experiment. It looks like this:

```
experiment/
├── my_experiment.psyexp
├── code-sync
├── code__routine1__code1.py
├── code__routine1__code2.py
├── code__routine2__code1.py
├── ...
```

---

After you make changes to the python files, run the script again. It will update the python files' content in the experiment file. That is,

```
code__routine1__code1.py -> my_experiment.psyexp
code__routine1__code2.py -> my_experiment.psyexp
code__routine2__code1.py -> my_experiment.psyexp
```

NOTE: after you do that reload the experiment in the builder to see the changes.