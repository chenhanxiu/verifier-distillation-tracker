# JudgeMix: Judge-Guided Mixed-Rollout Data Synthesis for LLM Agents

- **作者**：Cheng-Yu Hsieh、Ting-Yao Hu、Sanjoy Chowdhury、Oncel Tuzel、Raviteja Vemulapalli
- **首次公开日期**：2026-11-12
- **版本日期**：2026-11-12（v1）
- **原始论文**：https://arxiv.org/abs/2611.16174
- **代码**：未见公开代码仓库
- **标识符**：arXiv:2611.16174；DOI: 10.48550/arXiv.2611.16174

## 一句话结论

【论文原文】JudgeMix 用逐步语义 Judge 决定何时让 expert 接管 mixed rollout，并按判断结果重加权 expert 监督，在 AppWorld 与 AutomationBench 上最多提升 10 个 pass@1 点。

## 真正新增的内容

【论文原文】现有 mixed rollout 往往随机插入 expert，或对每一步均匀施加监督。JudgeMix 根据 target model 当前步骤是否困难动态切换 student/expert，使轨迹成功率与 student 原生状态分布同时得到保持；对已正确步骤降低 expert 覆盖，对错误步骤加强监督。

【分析推断】这是“verifier 路由 teacher + score-level on-policy distillation”的直接数据合成原型。新增价值不只是更高成功率，而是把 Judge 输出同时用于状态采样与监督强度，因而也带来 Judge 误判放大和共适应风险。

## 核心方法

1. student 在自己的状态分布上推进工具轨迹。
2. 逐步语义 Judge 判断当前行为质量与是否需要 expert 介入。
3. expert 仅在困难步骤接管；Judge 分数再用于重加权各步骤的 expert SFT 监督。

## 关键实验结果

【论文原文】在 AppWorld 和 AutomationBench 上持续优于既有数据合成方法，最大提升为 10 个 pass@1 点。摘要未报告 Judge 校准误差、A/B/T 分布、跨 Judge 稳健性或独立 sealed eval。

## 证据质量与局限

【论文原文】证据来自两个程序化工具使用基准，至少覆盖多步环境交互。

【分析推断】若同一 Judge 既决定 expert 何时介入又评价最终训练效果，会产生 selection–evaluation overlap；即使终局 benchmark 是程序化的，训练状态也可能被 Judge 过滤成低熵、易纠正区域。需要报告 Judge 的错误类型、介入覆盖率和未介入高熵状态表现。

## 最接近的相关工作

最接近 DAgger、mixed rollout、STRIDE、AC-OPD、OnPoKD 与 verifier-gated OPD。JudgeMix 的区别是用逐步语义评价同时做 expert 路由和监督重权，而非固定混合率、随机切换或只依赖 teacher–student gap。

## 如何复用或推进 LLM-as-a-Verifier

将单点 Judge 改成 distributional verifier：输出 A/B/T 与序数概率，并将环境测试、权限约束和未完成义务作为硬通道。只有硬真值或多证据一致时才让 expert 接管；对 T 或高熵状态保留 student 分支并追加反事实 rollout。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：直接实现逐状态 verifier 分数控制 expert logits/监督权重。
- **A/B/T 与序数分布**：以“student 继续/teacher 接管”为 A/B；不确定时 T，不强制切换。
- **环境真值门控**：终局和关键写操作由程序断言校正 Judge 方向。
- **critique states**：只在 Judge 能指出证据与可修复错误时生成 critique；无证据的风格偏好不进入蒸馏。
- **高熵探索**：对多种可行行动维持多分支，设置最大 expert 接管率，防止训练分布被 teacher 单一路径占满。
- **sealed eval**：使用未参与路由的隐藏程序测试和冻结 evaluator，比对相同 state coverage 下的真实成功率。
