# When Is a Multi-Agent Code Judge Actually Grounded? Two Label-Free Measurements, and a Judge That Declines to Guess

- **作者**：Salma Roshdy Aly, Hussein Assaf, Ziad Kobti
- **首次公开日期**：2026-09-23
- **版本日期**：2026-09-23（v1）
- **原始论文**：https://arxiv.org/abs/2609.30328
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】多 Agent Judge 若使用的“证据”并不独立于候选答案、且在候选间没有差异，就没有比较依据；应以内部日志指标识别这类情形并拒绝猜测。

## 真正新增的内容

【论文原文】论文把 grounded comparison 拆成两个必要条件：证据须独立于待评答案，并须在两个候选之间产生区分；同时提出两个无需外部标签、从 pipeline 日志直接计算的诊断量，支持选择性 abstention。

## 核心方法

1. 原样运行已发表的 MARCH 多 Agent 验证框架。
2. 在两个代码 Judge benchmark 的 80 个 condition×cell 测量中审计证据差异。
3. 以内部日志的 label-free 指标检测“没有比较依据”的样本。
4. 对无依据样本输出 abstain，而非继续产生带理由的确定 verdict。

## 关键实验结果

【论文原文】MARCH 在 78%–95% 的比较中把两份代码判为同样好，准确率仅 4.4%，而同一模型直接判断为 43.7%；更简单问题或更大 Judge 均未解决。使用其中一个 gate 后，准确率从 20.7% 提升至 36.9%，同时回答一半比较。

## 证据质量与局限

【论文原文】优势是对既有框架做原样复现，并用无需标签的内部测量解释失败。局限是仅两个代码 benchmark，abstention 提升选择性准确率但牺牲覆盖率，也没有证明该 gate 能直接泛化到长轨迹 Agent 或序数 reward model。

## 最接近的相关工作

最接近 ClaimReceipt、Agent 轨迹可诊断性、JEV-as-a-Judge 的 selective routing，以及多 Agent debate/verification。核心区别是将“候选间证据是否真的不同”设为比较前置条件。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 输入拆成候选共享证据与候选特异证据，并显式输出 evidence sufficiency；只有后者达到阈值才生成 A/B，否则输出 T/INCONCLUSIVE。该门控可蒸馏为轻量 coverage head，与 correctness head 分离。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：仅在证据充分时蒸馏差值；无依据状态的目标应是 abstain 概率。
- **A/B/T 与序数分布**：T 不只是“分数接近”，还应表示不可辨识/证据缺失。
- **真值门控**：代码测试、环境 replay 与工具日志应优先于语言模型自生成论据。
- **Critique states**：critique 必须附候选特异证据指针，否则不得写入记忆或训练集。
- **探索**：高 abstention 状态可触发补证或对称分叉，而不是任意选边。
- **Sealed eval**：报告 selective risk–coverage 曲线，并用独立测试检查 abstention 是否被策略利用。
