# All Verdicts are Not Equal: Rethinking LLM Judge Reliability

- **作者**：Vineet Kumar；Darshita Rathore；Anindya Moitra
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12083
- **Canonical URL**：https://arxiv.org/abs/2610.12083
- **代码**：未发现公开代码链接

## 一句话结论

LLM Judge 即使 temperature=0 且重复输出一致，也可能稳定地错；可靠性必须同时满足可复现、顺序不变和正确，而不能用多数票或“确定性”替代。

## 真正新增的内容

【论文原文】作者审计 6 个前沿模型、4 个基准、5 种提示、2 种候选顺序、3 个温度和每格 10 次重复，并定义 trustworthy verdict rate：判决必须同时可复现、对 A/B 顺序不敏感且与 ground truth 一致。

【论文原文】最确定的 Judge 仍可能系统性错误，某设置准确率仅 51%。  
【分析推断】A/B/T 的 T 应覆盖“稳定但未经真值验证”的样本，而不只是模型自己表现犹豫的样本。

## 核心方法

1. 对同一比较多次采样，测量 test–retest 稳定性。
2. 交换候选顺序，测量位置敏感性和多数判决翻转。
3. 与 ground truth 对照，区分稳定错误和稳定正确。
4. 将三项条件取交集形成 trustworthy verdict rate，并比较 prompting/rubric 方案。

## 关键实验结果

【论文原文】即使 temperature=0 判决也会变化；候选顺序交换可在困难任务上翻转多数判决；最“确定”的 judge 只达到 51% ground-truth 正确率。相较多种格式化提示，整体 rubric scoring 带来的可靠性改善更一致。

## 证据质量与局限

【论文原文】因子设计覆盖模型、任务、提示、顺序、温度与重复次数，能够分离多种不稳定来源。  
【局限】trustworthy rate 依赖可获得 ground truth，且不同任务的准确性阈值未必统一；整体 rubric 也可能泄露目标或被 reward hacking 利用。摘要未涉及长轨迹步骤信用。

## 最接近的相关工作

与 Black-Box Judge 测量不稳定性、Who Judges Matters、Agreement Overstates Evidence、多 Judge 面板有效规模、MAWILE、Rethinking Verbalized Confidence 和 Calibration Is Not Verification 最接近。

## 如何复用或推进 LLM-as-a-Verifier

对每个候选分叉执行双顺序、多次采样和硬真值核验，保留完整判决分布。训练 student verifier 时把“稳定且正确”与“稳定但错误”分开；后者应成为高价值对抗样本，而不是高权重 teacher 标签。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 权重由 trustworthy rate 而非自报置信度决定；稳定错误样本权重归零或反向校准。
- **A/B/T 与序数分布**：A/B 必须过顺序不变性；任何顺序翻转或无 ground-truth 支撑的高一致性进入 T。
- **程序化/环境真值门控**：执行 oracle 决定正确性，Judge 的稳定性只影响软幅度。
- **student-generated critique states**：对 critique 也做重述和顺序扰动；证据结论不变才准入。
- **高熵分叉**：把 judge disagreement 与真正策略不确定性分账，避免裁剪因位置偏差产生的“高熵”。
- **sealed eval**：冻结模型版本、提示、候选顺序随机化和重复次数，公开稳定性、顺序不变性、准确性三项指标。

总体判断：【分析推断】现有 A/B/T 路线应把 T 从“平局”升级为“证据不足或测量不可信”，并将 trustworthy verdict rate 作为 teacher 数据准入标准。