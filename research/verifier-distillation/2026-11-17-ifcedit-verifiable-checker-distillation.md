# Learning to Edit IFC Building Models: Verifiable Checkers as the Training Signal for Dependency-Aware Editing Agents

- **作者**：Jiaxin Zhang、Yao Luo、Yuze Dan、Yunqin Li、Bowen Wang
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22307
- **代码链接**：https://github.com/wbw520/ifcgym
- **标识符**：arXiv:2611.22307；DOI: 10.48550/arXiv.2611.22307

## 一句话结论

【论文原文】四类可执行 checker 同时负责筛选 teacher 轨迹、提供 RL 奖励和最终评测，使 9B student 接近 teacher、27B student 超过 teacher，说明“硬真值闭环蒸馏”可覆盖复杂依赖编辑。

## 真正新增的内容

【论文原文】提出 IfcGym 与 IfcEdit：无需唯一 target file，而以输入相对有效性、任务意图、依赖传播、无关对象保持四个 checker 的合取定义 strict success；先蒸馏验证通过的 teacher episodes，再用同一严格成功信号做 GRPO。

## 核心方法

1. CodeAct Agent 在可回放 IFC sandbox 中执行代码。
2. 四个 checker 分别检测新增错误、请求变更、依赖对象传播和无关实体副作用。
3. verified teacher episodes 用于 SFT；严格合取奖励用于 GRPO；训练与测试项目/seed 隔离。

## 关键实验结果

【论文原文】IfcEditBench 含 13 个留出真实项目上的 1,990 个任务。9B student 从 SFT 的 79.15% 提升到 86.78%，与 teacher 的配对置信区间包含零；27B 达 91.76% 并超过 teacher。公开 BIM-Edit/BIBIMBAP 得分 55.19/54.50。四 checker 全用比只用 intent+validity 高 4.83 点。

## 证据质量与局限

【论文原文】有真实项目留出、配对区间、checker 消融及公开基准；但训练和测试共享任务模板，未验证未见模板，依赖规则与几何覆盖不完整。strict success 证明符合当前 specification，不等于更广泛工程正确性；同一 checker 同时训练与主评测存在 evaluator 共适应风险。

## 最接近的相关工作

接近 RLVR、verified trajectory distillation、CodeAct、Text2CAD/ToolCAD、BIM-Edit 与 verifier-aware CAD/BIM Agent。关键区别是多维可执行合取检查，而非目标文件相似度或单一终局 reward。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】这是“程序真值定方向、生成式 verifier 解释幅度”的直接模板：四个 checker 提供不可覆盖的硬门，LLM verifier 只在合取通过后对编辑质量、可维护性与证据进行序数评分；失败轨迹可生成逐 checker critique，并再次执行验证。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：以四维 checker 向量为 teacher anchor，再蒸馏软分数；不要只学习 strict-success 标量。
- **pairwise A/B/T 与序数分布**：同状态两个编辑按四门偏序比较；一好一坏时保留 tie/不可比，而非强制总排序。
- **程序化/环境真值门控**：四门合取直接作为 gate；LLM teacher 不能推翻明确 checker 失败。
- **student-generated critique states**：每条 critique 绑定 diff、失败 checker 和修复后复跑结果，只有复验证实才入库。
- **高熵分叉探索**：在依赖关系不完整或多个合法编辑并存时保留多分支，避免单 target imitation 压缩策略多样性。
- **sealed eval**：新增未见模板、隐藏依赖规则和独立 checker 实现，评估是否只是适配训练 verifier。
