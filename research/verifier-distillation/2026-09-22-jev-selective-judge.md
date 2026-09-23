# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure

- **作者**：Yubo Li, Yidi Miao, Ramayya Krishnan, Rema Padman
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.26550
- **Canonical URL**：https://arxiv.org/abs/2609.26550
- **DOI**：10.48550/arXiv.2609.26550（arXiv DataCite，待注册）
- **代码**：未见独立公开仓库；论文说明公开复现包无需 API/GPU，但内部日志与私有响应不公开
- **arXiv ID**：2609.26550

## 一句话结论

【论文原文】低成本 decision-only Judge 在普通偏好和有证据事实性上可接近强生成式 Judge，并用自身置信度路由难例；但置信度只在目标 workload 内有效，面对华丽错误答案或无参考自然文本时会高置信失败。

## 真正新增的内容

【论文原文】论文系统比较 JEV 与 16 个生成式/奖励模型 Judge，并同时测量准确率、概率质量、格式有效性和真实费用；随后冻结“高置信直接接收、低置信升级”的两阶段策略，并用双顺序 pairwise 概率平均减少位置偏差。其核心不是让便宜 Judge 替代强 Judge，而是把 confidence 作为 selective evaluation 的路由信号。

【分析推断】这是 distributional verifier 部署层的直接原型：小 student 输出 verdict 分布，高熵或已知脆弱 slice 升级到 generative verifier/程序 oracle。

## 核心方法

- decision-only JEV 输出 typed verdict、概率和备注，与生成式 LLM Judge、PairRM、Skywork 等比较。
- 对 pairwise 样本交换 A/B 顺序，平均语义对齐后的概率；无效输出一律视为需升级。
- 在本地 selection set 上选阈值，使覆盖率最大且准确率落后 fallback 不超过预设容差，再在冻结扩展集测试。
- 对 JudgeBench 分歧样本进行盲化人工裁决，并对 benchmark label 误差做敏感性分析。
- 加入 RM-Bench 的 style-adversarial pairs 与 reference-free prose 检查 confidence envelope。

## 关键实验结果

- 普通偏好和 evidence-grounded factuality 上，JEV 距最强比较者不超过 3 个百分点，费用约为其 0.36%。
- 冻结 GPT-6 cascade 在扩展集接受 53.7% 样本，准确率 92.5% 对 93.1%，费用约为 fallback 的 56.8%；论文概括为保留 99% 准确率、约 57% 费用。
- 单顺序 τ=0.9 cascade 升级 34%，达到 91.3% 对 GPT-6 的 91.7%，费用为 47%。
- RM-Bench 中被拒答案更华丽时，JEV 准确率从 84.0% 降至 74.8%，与 GPT-6 差 19.8 个百分点。
- reference-free prose 上各 Judge 接近随机且高置信，JEV error-detection AUROC 0.518，任何阈值都不能有效路由。
- JudgeBench 的 69 个 JEV/GPT-6 分歧中，人工支持 GPT-6 57 次、JEV 1 次。

## 证据质量与局限

【论文原文】优势是冻结样本、双顺序策略、真实费用、人工分歧裁决、风格对抗 slice 和 threshold-transfer 负结果。限制包括扩展多模型比较带探索性、专业领域未测、部分 benchmark label 含糊、实时串行延迟未测、某些 fallback 阈值不迁移，且 JEV 服务本身非完全公开。

【分析推断】置信度不能当真值证书，只能当已验证 workload 内的资源分配特征；一旦 student 或输入分布更新，阈值必须重新做 sealed 校准。

## 最接近的相关工作

最接近 speculative uncertainty、CoVeR 的 verifier-call routing、Robust Conformal Consensus、Rethinking Verbalized Confidence，以及选择性分类/拒答。区别在于本文同时量化 typed verdict、费用与人工分歧，而非只报告 Judge 相关系数。

## 如何复用或推进 LLM-as-a-Verifier

- student verifier 输出完整 A/B/T 概率和有效性状态；低熵普通样本直接处理，高熵、格式无效或风格对抗样本升级。
- 阈值按任务 slice 校准，不共用一个全局阈值；无参考文本直接要求证据检索或程序验证。
- 用人工/环境真值构建 style-adversarial sealed set，专门测“华丽错误”高置信失效。
- 将 generative critique 只用于升级样本，以降低长轨迹逐步验证成本。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】可将 JEV 式 student 作为 score-level on-policy distillation 的前置路由器：低熵状态用 student 分布，高熵或 OOD 状态调用 teacher；但训练时保留一定比例的高置信随机审计，以发现 confident blind spot。A/B/T 的 T 应对应升级/继续探索，而不是丢弃。sealed eval 需冻结阈值、候选顺序协议和对抗 slice，并由独立人类或执行 oracle评估，防止便宜 Judge 与 teacher 同时对同一风格共适应。