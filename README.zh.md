# PsychoPy Code Sync (PsychoPy 代码同步)

[English](README.md) | [中文说明](README.zh.md)

**PsychoPy Code Sync** 致力于增强您的 PsychoPy 实验的管理性和可编辑性。

它允许您从 `.psyexp` 文件提取代码组件到**独立的 Python 文件**，在您喜欢的 IDE 中编辑它们，并**一键**重新整合到 `.psyexp` 文件中。

- ✅ 一键同步：从提取到重新整合——只需一次点击。
- ✅ 开箱即用：立即运行，无需任何设置或配置。
- ✅ 开源：在 MIT 许可下。因此，您可以直接将其放入您的项目中，无需担心版权问题。

### 为什么使用这个工具？

- IDE 香香的代码提示和 PsychoPy Builder 我都要。
- 更清晰的 Git 历史记录。

## 使用方法

### 准备工作

注意：在首次尝试之前，请确保备份您的实验文件。只有在确定它可以正常工作时才运行此脚本。数据丢失太痛苦了。

1. 将 [code-sync.py](code-sync.py) 文件复制到您的实验目录中，使其与您的 `.psyexp` 文件处于同一层级。看起来像这样：

```
实验文件夹/
├── 我的实验.psyexp
├── code-sync.py
├── ...
```

2. 直接使用 Python 运行这个脚本。

### 第一次运行(从 .psyexp 文件中提取所有代码)

如果您首次运行脚本，它将在您的实验目录中创建几个 Python 文件。每个文件对应于实验中的一个代码组件。它看起来像这样：

```
实验/
├── 我的实验.psyexp
├── code-sync.py
├── code__例程1__代码1.py
├── code__例程1__代码2.py
├── code__例程2__代码1.py
├── ...
```

请注意，它只会为实验文件中存在代码组件的例程创建 Python 文件。例如，例程3没有代码组件，则不会创建 Python 文件。

### 上传（从 Python 文件到 .psyexp 文件）

当您对 Python 文件进行更改后，再次运行脚本。它将更新实验文件中 Python 文件的内容。也就是说，

```
code__例程1__代码1.py -> 我的实验.psyexp
code__例程1__代码2.py -> 我的实验.psyexp
code__例程2__代码1.py -> 我的实验.psyexp
```

注意：在这之后，重新加载 Builder 中的实验以查看更改。

### 下载（从.psyexp 文件到 Python 文件）

当您在 Builder 中修改代码后，只需删除相应的 Python 文件。脚本将创建一个更新的 Python 文件

```
实验/
├── 我的实验.psyexp
├── code-sync.py
├── code__例程1__代码1.py
├── (已删除)
├── code__例程2__代码1.py
├── ...
```

将会使得

```
我的实验.psyexp -> code__例程1__代码2.py
```

### Python 文件

所有的 Python 文件都将与 .psyexp 文件中的相应代码组件同步，以下情况除外：

- `code__preface.py` 文件不会同步。它用于为语言服务器提供代码补全提示。
- 每个 Python 文件中的 `Prologue` 部分将不会同步。你可以在里面添加一些初始化内容，来让语言服务器满意。例如 `text = visual.TextStim(win=win)`。这样在后续部分你可以获得完整的代码补全支持。