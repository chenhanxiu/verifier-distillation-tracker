# Benchmarks Don't Talk Back: Learning Through Self-Disagreement

- **作者**：Soheil Abbasloo、Peng Cheng
- **首次公开日期**：2026-11-12
- **版本日期**：2026-11-12（v1）
- **原始论文**：https://arxiv.org/abs/2611.17563
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.17563；DOI: 10.48550/arXiv.2611.17563

## 一句话结论

【论文原文】模型可自生成针对自身答案的最强反例，再用同一可验证奖励同时评价答案与“应坚持还是让步”的 ruling，从而训练出不依赖外部 Judge 的 dialectical competence。

## 真正新增的内容

【论文原文】作者把“面对反驳时何时坚持、何时让步”定义为独立于首答准确率的能力，并提出 Self-Disagreement：模型生成 position、antithesis 和 ruling，全程只用可验证奖励，不需要第二模型、偏好数据或人工标注。该能力不能仅靠测试时反思或更多采样获得。

【分析推断】这是 student-generated critique states 的强基线：critique 来自 student 自身，但更新方向由外部可验证结算锚定。它比直接蒸馏 teacher critique 更能保留 student 覆盖到的反例分布，也减少同源 Judge 的风格偏差。

## 核心方法

1. student 给出初始立场，并生成针对自身立场的最强 antithesis。
2. student 判断反例是否成立，形成 hold/yield ruling。
3. 用同一 reference-based verifiable check 评价首答和 ruling，并据此强化学习。

## 关键实验结果

【论文原文】dialectical competence 在 base model 中较弱，经奖励训练后出现；提升不以首答准确率为代价，并泛化到训练时未见、甚至更强的 challenger。摘要未披露基准名称、绝对提升和校准误差。

## 证据质量与局限

【论文原文】方法消除了训练和部署时的第二模型、reward model、偏好数据与人工标注依赖，并设置了更强 challenger 的泛化测试。

【分析推断】适用前提是 ruling 能被同一 reference verifier 可靠结算；在开放式 Agent 任务中，“反例是否成立”常无单一答案。若首答与 ruling 共用一个有漏洞的 oracle，系统仍会共同利用漏洞，必须引入独立环境结算与 sealed adversarial critiques。

## 最接近的相关工作

最接近对比式自蒸馏的正负 teacher log-ratio、LLM-as-an-Improver 的 verify-repair-reselect，以及 PaperDoctor/FLARE 的 critique 闭环。Self-Disagreement 的区别是反例由 student 自己生成，并用可验证奖励训练坚持/让步决策。

## 如何复用或推进 LLM-as-a-Verifier

把 ruling verifier 输出扩展为 A/B/T 与序数置信分布：A=原立场更可靠，B=反例成立，T=证据不足。teacher 只提供软幅度，程序或环境结算决定方向；保存失败反例及其证据，形成高价值 critique-state replay buffer。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏 hold/yield 的分数差，而不是模仿反例文本本身；仅在 oracle 可判时更新方向。
- **pairwise A/B/T 与序数分布**：position 与 antithesis 天然形成 A/B，开放世界无充分证据时加入 T 并保留分布。
- **环境真值门控**：重放工具调用、测试与状态断言验证反例是否真实成立。
- **student-generated critique states**：直接用自生成 antithesis，但通过证据和终局结果双门控后才能回放。
- **高熵探索**：保留多个可成立反例与未知分支，避免 teacher 单一路径覆盖 student 的合理异议。
- **sealed eval**：使用未见 challenger、隐藏反例生成器与独立 oracle，检查是否只学会迎合训练 verifier。

