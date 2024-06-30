# PsychoPy Code Sync

[English](README.md) | [中文说明](README.zh.md)

**PsychoPy Code Sync** is designed to enhance the manageability and editability of your PsychoPy experiments. 

It allow you extract code components from the `.psyexp` file to **standalone Python files**, edit them in your favorite IDE, and reintegrate them back to the `.psyexp` file **with just one click**.

✅ One-Click Sync: From extraction to reintegration—all it takes is a single click.
✅ Out of The Box: Run it immediately without any setup or configurations.
✅ Open Source: Licensed under MIT. So you can directly put it in your project without any copyright concerns.

### Why Even Bother?

- Utilize both your favorite IDE and PsychoPy builder. 
- More readable Git history for code components.

## Usage

WARNING: Before first try, make sure to backup your experiment file. And only run this script in your experiment directory when you are sure it works. Data loss will ruin your day.

1. Copy the [code-sync.py](code-sync.py) file to your experiment directory, so it is on the same level as your `.psyexp` file. So it looks like this:

```
experiment/
├── *.psyexp
├── code-sync.py
├── ...
```

2. run it directly.

## How It Works

If you first run the script, it will create several python files in your experiment directory. Each file corresponds to a code component in your experiment. It looks like this:

```
experiment/
├── my_experiment.psyexp
├── code-sync.py
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

---

After you modify the code in the builder, simply delete the corresponding python file. The script will create a new python file with the updated content.

```
experiment/
├── my_experiment.psyexp
├── code-sync.py
├── code__routine1__code1.py
├── (deleted)
├── code__routine2__code1.py
├── ...
```

will result in

```
my_experiment.psyexp -> code__routine1__code2.py
```
