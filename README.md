# Fight Video Create Skill

[中文](README.md) | [English](README.en.md) | [更新日志](changelog.md)

将一句打斗构思，扩展为可执行的剧情、动作设计、空间路线、分镜和视频生成提示词；也能把用户提供的打斗资料分类吸收到可检索的参考库中。

> 适用于漫剧、真人动作、动画、武侠、仙侠与能力战。资料是创作参考，不会覆盖你锁定的人物、武器、胜负、时长或结尾。

## 能做什么

- **从构思到成稿**：由模糊剧情生成冲突、动作因果、空间调度、分镜和生成约束。
- **分层检索**：按场景、动作/分镜方案、招式、示例剧本依次检索；先命中，再读取正文。
- **招式合理性校验**：检查武器、距离、姿态、场景支点、时长与角色能力是否兼容；不合适时采用原创动作。
- **资料吸收与维护**：将 `.docx`、`.txt` 等资料拆分为场景、导演方案、招式或示例剧本，并同步维护路由元数据。
- **可验证的资料库**：提供确定性路由器与结构校验脚本，避免无关键词时硬套资料。

## 安装

### 克隆仓库

```bash
git clone https://github.com/qualsenWeb/fight-video-create-skill.git
```

### 在智能体中安装

向支持 Skill 安装的智能体发送：

```text
帮我安装这个 skill：https://github.com/qualsenWeb/fight-video-create-skill
```

## 快速开始

### 设计一场战斗

```text
调用 fight-video-create-skill：
一个持长枪的男人与一个持长剑的女人在废墟中高速交锋，
最后由女剑客借断墙反弹完成破招。制作 15 秒、16:9、电影感分镜。
```

Skill 会先确定场景与可用动作方案；命中多个方案时会列出推荐项并等待你确认，再生成可执行的设计。

### 吸收新的参考资料

```text
调用 fight-video-create-skill 吸收以下资料：
《竹林打斗.docx》、`河滩战斗.txt`
```

Skill 会先说明每份资料的建议入库位置、可复用内容与重复风险。确认后才写入资料库并校验路由。

## 工作方式

1. 提炼人物、武器、能力、场景、对战规模、时长和结尾等锁定事实。
2. 检索场景资料；若没有关键词命中，则设计原创场景。
3. 检索动作/分镜方案；命中时由你确认主方案，零命中时在原创方案与自定义方案之间选择。
4. 仅在需要具体兵器技法、武学绑定或逐招拆解时检索招式库。
5. 参考示例剧本的结构，不复用其专有角色或无关情节。
6. 输出剧情、动作链、空间路线、分镜与生成约束。

## 仓库结构

```text
SKILL.md                                  # 工作流与约束
reference/
  scenes/                                 # 场景与空间资料
  action-storyboard-design/               # 动作/分镜导演方案
    招式库/                                # 兵器、武学、连招资料
  example-scripts/                        # 示例剧本与成片结构
scripts/
  route_reference.py                      # 确定性关键词路由
  validate_routes.py                      # 路由元数据校验
```

## 本地校验

资料入库或修改路由后，运行：

```bash
python -X utf8 scripts/validate_routes.py
```

可用以下命令查看路由结果：

```bash
python -X utf8 scripts/route_reference.py design --query "竹林 刀剑 追击"
```

## 文档

- [使用说明与完整工作流](SKILL.md)
- [更新日志](changelog.md)
- [English README](README.en.md)

## 贡献

欢迎提交新的场景、动作导演方案、招式专项或示例剧本。新增、删除或重命名资料时，请同步更新对应目录的 `00-路由元.json`，并运行校验脚本。


