# PsychoPy Code Sync

A tool that allows user to extract, edit, and reintegrate code components for PsychoPy experiments to simplify the process of creating and editing experiments.

### Why Even Bother?

- Utilize both your favorite IDE and PsychoPy builder. 
- Git history for code components.

## Usage

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
├── *.psyexp
├── code-sync
├── code__routine1__code1.py
├── code__routine1__code2.py
├── code__routine2__code1.py
├── ...
```

---

After you make changes to the python files, run the script again. It will update the python files' content in the experiment file. That is,

```
code__routine1__code1.py -> *.psyexp
code__routine1__code2.py -> *.psyexp
code__routine2__code1.py -> *.psyexp
```
