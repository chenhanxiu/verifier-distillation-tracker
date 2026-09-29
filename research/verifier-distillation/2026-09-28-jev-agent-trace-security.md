# JEV as a Judge for Agent Trace Security: An Empirical Comparison with Generative LLM Judges

- **作者**：Zhiqiang Wang, Yichao Gao
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34862
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】在 5,219 条安全轨迹上，JEV 的平均正类 F1、有效输出覆盖率和时延均显示它适合作为低成本筛查器，但跨数据集精确率/召回率权衡明显，不应单独承担最终裁决。

## 真正新增的内容

【论文原文】论文首次在统一风险 rubric 和行为级标签下，跨四个 agent-trace security benchmark 直接比较 typed decision model JEV 与四种生成式 Judge。

## 核心方法

1. 统一四套安全轨迹的风险 rubric 和行为级标签。\n2. 比较 JEV 与四个 generative Judge 的正类 F1、有效覆盖率、时延与成本。\n3. 按 benchmark 分析 precision/recall 与胜负差异。

## 关键实验结果

【论文原文】JEV 平均正类 F1 为 77.8，最强生成式配置 GLM-5.2 为 74.1；有效覆盖率分别 95.5% 与 94.4%。JEV 中位成功调用时延 0.99 秒，平均每个有效判断估计成本 0.000195 美元；但 JEV 与 GLM 在不同数据集各有领先。

## 证据质量与局限

【论文原文】样本量大、覆盖四个 benchmark，并统一 rubric，适合工程选型。局限是只比较 retrospective 分类，未测在线门控后果、校准误差、对抗 state 注入或 sealed deployment；成本和延迟也依赖具体服务版本。

## 最接近的相关工作

最接近 JEV-as-a-Judge、JEV vs LLMs as Rubric Judges 与 JevAdvBench；本作新增 agent trace security 场景和 5,219 轨迹实证。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】用 JEV 做第一层概率筛查，低风险/高置信区可自动处理，高风险或高熵区转 generative verifier 与环境 replay；结合 JevAdvBench 对 state/critique 注入做鲁棒性测试。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：可蒸馏 JEV 的 typed score，但要按数据集重校准。\n- **A/B/T 与序数分布**：高熵或跨 Judge 分歧输出 T 并升级。\n- **真值门控**：安全硬证书不可被 JEV 概率覆盖。\n- **Critique states**：生成式解释作为独立补充，不回填成 JEV 的事实输入。\n- **探索**：低置信安全状态应保守路由，而非奖励探索。\n- **Sealed eval**：锁定 JEV/LLM 版本并保留对抗与跨域安全集。
