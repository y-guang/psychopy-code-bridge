# PsychoPy 代码同步

PsychoPy 代码同步工具。自动提取 PsychoPy 实验中的代码组件到单独文件。并同步到 PsychoPy 实验文件 (.psyexp)。

### 为什么使用这个工具？

- IDE 香香的代码提示和 PsychoPy Builder 我都要。
- 更清晰的 Git 历史记录。

## 使用方法

1. 将整个 [code-sync](code-sync) 文件夹复制到您的实验目录中，使其结构如下所示：

```
实验/
├── *.psyexp
├── code-sync/
│   ├── main.py
├── ...
```

2. 在 code-sync 目录中运行 [main.py](code-sync/main.py)。

## 工作原理

如果您首次运行脚本，它将在您的实验目录中创建几个 Python 文件。每个文件对应于实验中的一个代码组件。它看起来像这样：

```
实验/
├── 我的实验.psyexp
├── code-sync
├── code__例程1__代码1.py
├── code__例程1__代码2.py
├── code__例程2__代码1.py
├── ...
```

---

当您对 Python 文件进行更改后，再次运行脚本。它将更新实验文件中 Python 文件的内容。也就是说，

```
code__例程1__代码1.py -> 我的实验.psyexp
code__例程1__代码2.py -> 我的实验.psyexp
code__例程2__代码1.py -> 我的实验.psyexp
```

注意：在这之后，重新加载 Builder 中的实验以查看更改。