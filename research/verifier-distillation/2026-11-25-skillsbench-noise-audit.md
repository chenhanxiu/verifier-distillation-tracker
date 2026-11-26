# SkillsBench 源码审计：skill lift 可能由 grader 依赖与采样噪声制造

- **论文标题**：What Does Skill Lift Actually Measure? A Source-Code-Level Audit and Noise-Aware Reanalysis of SkillsBench
- **作者**：Haozhe Zhang, Zhen Long
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.33943
- **DOI**：https://doi.org/10.48550/arXiv.2611.33943
- **代码/审计账本**：https://github.com/rrrrr4788/skillsbench-lift-reanalysis

## 一句话结论

源码级审计发现 grader 依赖、空 skill 目录和 harness 内置能力会显著污染 skill lift；用同一日志拟合并选择 gate 还能在随机标签下产生虚假提升。

## 真正新增的内容

**论文原文结论**：7,554 次公开 trial、1,421 个配对 cell 的重分析未发现经多重比较校正后显著的任务级负效应；skill-free score gate 的表面提升在标签打乱后更大，held-out 上不显著。**分析推断**：verifier/critique gate 必须使用独立数据选择与验收，否则极易把噪声蒸馏成策略。

## 核心方法

检查 benchmark 源码、grader、skill 目录和 harness 注入；按配置—任务配对重算效应并做多重检验；将 gate 的拟合/决策与 held-out 评估分离，并用随机标签负控测试选择偏差。

## 关键实验结果

三项受控验证的 grader/定义问题平均 lift 为 74.6 点，而全体为 18.7 点；四个任务含占位 skill，某 harness 多数运行额外注入 48 个内置 skills。58% cell 在最多三次重复下算术上不可能显示下降；gate 在随机标签下仍“提升”4–7 点。

## 证据质量与局限

源码、日志和复现实验公开，负控与 held-out 检验很强。局限是审计对象单一，不能推出所有 skill 方法无效，也未直接训练 reward model。

## 最接近的相关工作

与 Harness or Model?、Reward Score 残差化审计、How Do Agent Harnesses Create Value? 和 SealedLoop 最接近。

## 如何复用或推进 LLM-as-a-Verifier

所有 verifier gate 应加入标签打乱、空 critique、等价 harness 和 grader替换负控；同时保存 A/B/T 的完整计数与不确定性，避免将稀疏重复的符号差异当成可靠序数提升。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：gate 阈值、teacher 选择和 critique 准入只能在 train split 调参，独立 sealed split 报告；程序真值和 harness 元数据并列记录。高熵分叉需足够重复，score-level OPD 的增益要用随机 gate 与无信息 teacher 作对照。
