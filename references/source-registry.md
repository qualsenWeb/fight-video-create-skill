# 样本吸收登记表

> 用途：识别 `资料/` 中尚未吸收的新文件。已登记文件视为不可变基线；新增样本只追加登记，不重新读取旧文件。

## 公共规则与模板

- `00-通用公式与技巧实例.txt` → `01-core-guidelines.md`：九要素、关键词、连招和一致性入门规则；由原 `00-通用公式与技巧.txt` 更名，内容未变。
- `高燃打斗.md` → `01-core-guidelines.md`：空间锚点、观察轴、物理闭环和镜头契约。
- `高频打斗提示词模板（稳定版）(1).txt` → `02-template-stable.md`：事实卡、四阶段连续和质检。
- `高频打斗提示词模板（疯癫版）(1).txt` → `02-template-impact-anime.md`：资产绑定、短时高密度、特效和声音。
- `武打skill.md` → `02-template-combat-library.md`：角色、武学、兵器、镜头规格、视觉风格和场景知识库。

## 题材样本

- `01-现代格斗动作.txt` → `03-topic-modern.md`
- `02-现代枪战军事.txt` → `03-topic-modern.md`
- `03-古代武侠.txt` → `03-topic-eastern-fantasy.md`
- `04-修仙仙侠.txt` → `03-topic-eastern-fantasy.md`
- `05-科幻机甲.txt` → `03-topic-scifi-supernatural.md`
- `06-魔幻奇幻.txt` → `03-topic-western-history.md`
- `07-古战场冷兵器.txt` → `03-topic-western-history.md`
- `08-异能超自然.txt` → `03-topic-scifi-supernatural.md`
- `09-忍者武士剑道.txt` → `03-topic-eastern-fantasy.md`
- `10-中国神话玄幻.txt` → `03-topic-eastern-fantasy.md`
- `11-妖兽魔兽.txt` → `03-topic-creatures-tokusatsu.md`
- `12-西部牛仔枪战.txt` → `03-topic-modern.md`
- `13-海盗海战.txt` → `03-topic-western-history.md`
- `14-空战.txt` → `03-topic-vehicles-war.md`
- `15-古罗马角斗.txt` → `03-topic-western-history.md`
- `16-特摄怪兽.txt` → `03-topic-creatures-tokusatsu.md`
- `玄幻快速拼招+大招首尾模板.txt` → `03-topic-eastern-fantasy.md`：新增宏观远距仙侠对轰、分段首尾状态契约、特效状态连续性和碰撞顺序；提炼规则，不复制原始长提示词。

## 增量登记格式

新增样本吸收后追加：

```text
- `[相对文件名]` → `[reference 文件]`：[新增价值摘要]；[合并/保留/跳过及原因]。
```

## 去重判定

- 只有题材名、角色名或颜色变化：登记为同构变体，不复制正文。
- 新增动作机制、空间结构、镜头方法或素材协议：提炼为规则并追加到对应 reference。
- 同时覆盖多个题材：选择一个主 reference，登记一个辅标签，不复制到两个文件。
- 与现有规则冲突：保留目标工具明确约束；否则记录冲突并请求用户裁定，不静默覆盖。