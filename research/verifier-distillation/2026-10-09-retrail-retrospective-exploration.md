# Travel Back To Move Forward: Retrospective Exploration and Evolving for Long Horizon Agents

- **作者**：Ziang Ye；Wentao Shi；Lei Chen；Zhengzhou Cai；Yu Wang；Zhiyuan Yao；Zihan Wang；Xierui Song；Fuli Feng；Yixin Cao
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13058
- **Canonical URL**：https://arxiv.org/abs/2610.13058
- **DOI**：10.48550/arXiv.2610.13058
- **代码**：https://github.com/whi497/ReTRAIL（论文声明；检查时链接返回 404）

## 一句话结论

ReTRAIL 允许环境状态回退但保留废弃分支学到的知识，并从同一回访状态比较后续轨迹，把“高熵探索、可恢复性和失败经验复用”统一到长时程训练闭环。

## 真正新增的内容

【论文原文】单纯增加 rewind 原语可能无效甚至退化；有效做法是环境回退、知识前进，并联合 State-Anchored GRPO 与 branch-advancement reward。  
【分析推断】这为 Agent verifier × OPD 提供理想训练单元：同一快照下的原分支、回退分支和反思分支可构造 A/B/T，并由后续环境进展确定相对信用。

## 核心方法

1. 识别无效或死胡同状态并回退到较早环境快照。
2. 保留已验证进展以及从废弃分支抽取的知识。
3. State-Anchored GRPO 比较同一回访状态下的替代 continuation。
4. branch-advancement reward 依据后续探索的进展训练反思。

## 关键实验结果

【论文原文】在 Minesweeper、Sokoban、ALFWorld 和 ScienceWorld 四个交互 benchmark 上验证；只提供 rewind 的 baseline 收益有限且可能退化，ReTRAIL 通过废弃分支知识复用改善长时程求解。摘要未给出统一绝对提升。

## 证据质量与局限

覆盖四类可重置交互环境，能区分 rewind 原语与学习机制贡献。局限是现实 GUI、办公或有副作用工具未必能精确回退；从失败分支抽取的知识可能错误，代码链接当前不可访问也影响复现。

## 最接近的相关工作

与 REVERSAL-BENCH、EPIG-Tree、Belief-Shift Branching、DDO、STRIDE、DENSE 和 SynAct 最接近。新增点是“环境回退但知识不回退”的同任务持续探索。

## 如何复用或推进 LLM-as-a-Verifier

对可重放环境保存状态快照，记录分支进入、回退原因、保留知识及后续真实进展；verifier 应分别评价即时动作、可恢复性、知识有效性和回退后的净进展。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：在同一 anchor state 上蒸馏替代 continuation 的分数，而非跨状态粗比较。
- **A/B/T 与序数分布**：原分支、回退分支、反思分支构成自然 A/B/T。
- **程序化/环境真值门控**：后续环境进展和最终完成度裁决反思是否有效。
- **student-generated critique states**：只有让回退后分支产生可复现增益的知识才入库。
- **高熵分叉**：允许探索失败并回退，避免因短期低 reward 过早压缩策略支持。
- **sealed eval**：使用隐藏环境变体与不可见分支，检查知识是否泛化而非记忆状态。