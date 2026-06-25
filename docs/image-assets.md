# 图片资产与许可管理

本仓库的论文图、项目框架图和案例图统一按“来源可追溯、许可可核验、文件可校验”的方式维护。

## 1. 目录结构

```text
assets/images/
├── README.md          # 人类可读的署名与许可表
├── manifest.json      # 机器可读清单、SHA-256 和字节数
└── <note-slug>/       # 按笔记或论文分组的原始图片
```

笔记使用相对于 `notes/` 的路径：

```markdown
![Figure description](../assets/images/<note-slug>/<file>.png)
```

## 2. 本地化许可策略

允许自动本地化的许可：

| 许可 | 处理方式 |
|---|---|
| CC BY 4.0 | 保留作者、论文、Figure 编号和许可链接；不修改时标注 `modified: false` |
| CC BY-NC-ND 4.0 | 仅保存原始字节，不裁剪、不重编码、不叠加标记；保留非商业和禁止演绎说明 |
| MIT | 保留官方仓库、许可链接和项目署名 |
| Apache-2.0 | 保留官方仓库、许可链接和项目署名 |

默认不自动复制的情况：

- 论文只使用 arXiv nonexclusive distribution license；
- 项目站点没有明确许可；
- 图片可能包含第三方素材，且论文或项目没有说明再分发范围；
- 无法确认原始图片与论文 Figure 的对应关系。

这些图片继续使用外链，并在 `maintenance/image-inventory.json` 中标记为 `deferred-license`。

## 3. Manifest 字段

`assets/images/manifest.json` 中每张图片至少记录：

- `id`
- `note`
- `alt`
- `original_url`
- `local_path`
- `source_kind`
- `source_reference`
- `license`
- `license_url`
- `attribution`
- `modified`
- `retrieved_at`
- `sha256`
- `size_bytes`

图片文件发生任何字节变化时，必须同步更新 SHA-256、字节数，并重新判断是否构成许可意义上的修改。

## 4. 工具

重新生成图片清单：

```bash
python scripts/inventory_note_images.py
```

检查本地文件、引用、许可、清单和哈希：

```bash
python scripts/check_images.py .
```

机器可读输出：

```bash
python scripts/check_images.py . --json
```

## 5. CI 校验

`Validate notes` 工作流会检查：

- 笔记中的本地图片必须位于 `assets/images/`；
- 本地图片必须出现在 `manifest.json`；
- SHA-256、字节数和文件类型必须一致；
- 每张本地图片必须被笔记实际引用；
- 外链图片必须在清单中标记为 `deferred-license` 并写明原因；
- 本地化图片只能使用允许的许可；
- CC BY-NC-ND 图片必须声明 `modified: false`；
- 资产目录中不能出现未登记文件。

## 6. 新增图片流程

1. 确认图片确实有助于解释论文方法、实验或失败模式；
2. 核对图片来自论文、官方项目或作者页面；
3. 核对再分发许可，而不是只确认“可以在线访问”；
4. 许可明确时更新本地化配置和 manifest；
5. 许可不明确时保留外链，并记录延后原因；
6. 运行图片清单、单元测试、链接检查和图片完整性检查；
7. 在 PR 中说明新增图片、来源和许可。
