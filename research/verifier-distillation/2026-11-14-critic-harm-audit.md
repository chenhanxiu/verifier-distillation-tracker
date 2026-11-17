# The Critic Can Hurt: On the Safety of Critics in LLM-Guided AutoML Search

- **作者**：Gaoyuan Du、Xiaoyang Liu、Rex Zhou、Dengdu Jiang、Rong Fu、Meng Ding、Defu Cao
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19037
- **代码/基准**：CRITFAULT 计划公开，当前未发现仓库链接
- **标识符**：arXiv:2611.19037；DOI: 10.48550/arXiv.2611.19037

## 一句话结论

【论文原文】未经审计的 8B critic 在 8 个表格数据集中的 7 个把搜索推到无 critic 随机搜索基线以下，最坏损失 0.245 AUC；有方向性的 critic 错误尤其危险。

## 真正新增的内容

【论文原文】论文用四臂对照隔离 critic 的边际作用，并通过受控 fault injection 区分无方向错误与方向性错误。best-so-far 搜索能容忍前者，但后者会持续耗尽有限搜索机会；简单 validation gate 和 learned detector 只能降低而不能保证消除损失。

【分析推断】这给 student-generated critique 和 generative verifier 一个明确反例：critique 不是免费增益，错误方向比随机噪声更会破坏探索。因此 teacher critique 必须与 no-critic/control 分支并列评估。

## 核心方法

1. 四臂实验隔离无 critic、不同 critic 与搜索本身的效果。
2. 注入不同类型和强度的 critic 错误，测量搜索容忍度。
3. 测试可观测 validation gate 与学习式 harmful-feedback detector。

## 关键实验结果

【论文原文】朴素 8B critic 在 7/8 数据集低于 no-critic random-search floor，最坏损失 0.245 AUC。强 critic 在该套件上减弱损失，但没有通用能力阈值；无方向错误近乎无代价，方向错误消耗搜索预算。两种 gate 都不能保证保住完整预算下的 no-critic 基线。

## 证据质量与局限

【论文原文】含边际效应对照、受控错误注入和防御实验，并计划公开 CRITFAULT。

【分析推断】结论来自 AutoML 和表格数据，是否扩展到工具 Agent 仍需验证；最强 critic 也可能在不同 frontier/budget 下反转。必要条件不是部署证书，不能据此直接设全局阈值。

## 最接近的相关工作

最接近 ImpossibleRubrics、PROSE、Reward Hacking monitor、Calibration Is Not Verification 与 IWD。本文新增的是 critic 相对于 no-critic floor 的直接伤害审计。

## 如何复用或推进 LLM-as-a-Verifier

每次加入 critic/verifier 前保留 no-critic、随机反馈和 oracle-feedback 三个控制臂；训练 harmful-feedback detector 只作软门控，最终方向由环境验证。对长期搜索记录 critic 建议与实际增益的因果配对。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：报告 teacher-on 与 teacher-off 的边际收益，不只报告最终模型。
- **pairwise A/B/T 与序数分布**：方向性错误样本优先标 T/拒绝蒸馏。
- **环境真值门控**：真实验证集或执行结果决定 critic 建议是否采纳。
- **student-generated critique states**：critique 必须经过反事实执行或 held-out validation。
- **高熵探索**：保留 no-critic 分支，避免错误 critic 吃掉全部搜索预算。
- **sealed eval**：冻结预算、frontier 与无 critic floor，审计不同错误注入下的最坏损失。

