# python_package_template 文档

:::{admonition} 模板占位
在这里写一段话，说明这个包做什么、给谁用。
:::

文档分三部分，各自面向一类读者：

- [使用指南](user/index.md)：怎么安装、怎么用。
- [开发指南](developer/index.md)：这个包如何设计，怎样修改它。
- [Agent 指南](agents/index.md)：写给 AI agent，分为"使用本包"和"修改本仓库"两份。

中英文术语的对应关系见[术语表](glossary.md)。

```{toctree}
:hidden:

user/index
developer/index
agents/index
glossary
```

```{toctree}
:hidden:
:caption: 参考

apidocs/index
```
