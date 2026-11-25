# HUB-J：从人类—Judge 分歧中发现并缓解评价偏差

- **论文标题**：Auditing the Judge: Human-Derived Bias Discovery, Quantification, and Mitigation in LLM Judges
- **作者**：Hamin Koo, Chanjoo Jung, Fangzhao Wu, Jaehyung Kim
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（v1）
- **原始论文**：https://arxiv.org/abs/2611.33065
- **DOI**：https://doi.org/10.48550/arXiv.2611.33065
- **代码链接**：未见公开代码
- **会议**：NeurIPS 2026

## 一句话结论

HUB-J 用真实人类—LLM 分歧发现可解释偏差，再通过受控修改量化其因果影响，并以训练外回归扣除偏差效应，为 Judge 校准提供可审计闭环。

## 真正新增的内容

**论文原文结论**：框架先从分歧案例发现 bias factors，再利用原本一致的案例做受控修改、测量偏差强度，最后进行 training-free regression mitigation；该方法降低偏差驱动的 verdict flips，并能跨模型迁移。**分析推断**：它可作为 verifier 蒸馏前的 teacher 清洗层，但只能校正已发现的表面偏差，不能替代环境真值。

## 核心方法

从人类与 Judge 不一致的样本归纳可解释偏差因子；在一致样本上仅改变该因素，控制任务语义不变，估计对分数/偏好的影响；回归模型在不重新训练 Judge 的情况下扣除估计偏差，并在不同模型上测试泛化。

## 关键实验结果

**论文报告**：HUB-J 能减少由偏差因素触发的判决翻转，并在多个 Judge 之间泛化。公开摘要未给出完整偏差类别、绝对改善和置信区间，因此当前不能判断其对极端 OOD Agent 轨迹的收益大小。

## 证据质量与局限

“发现—受控干预—缓解”的三段式设计比相关性审计更强，且 training-free 便于部署。局限是人类标签也可能有系统偏差；回归残差化不能证明构念有效性，已知偏差减少后仍可能保留隐藏偏差或错误因果。对被策略主动利用的动态偏差尚无证据。

## 最接近的相关工作

与 MAWILE 的受控扰动、Who Judges Matters 的家族偏差、Reward Score 残差化审计以及 Agreement Overstates Evidence 的相关错误分析最接近。HUB-J 的增量是让偏差因子来源于真实人机分歧，再做因果式干预验证。

## 如何复用或推进 LLM-as-a-Verifier

在 verifier teacher 输出旁记录偏差敏感度向量，并同时蒸馏原始序数分布与校正后分布；若两者差距大则输出 T/abstain。偏差审计样本应覆盖长度、语气、位置、解释密度、模型家族与 harness 格式，并由程序真值确认语义不变。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：在 score-level OPD 前加入 HUB-J 风格的样本级去偏权重，但与未校正分数、环境回报并列记录，避免残差化掩盖失效。A/B/T 数据需双顺序、跨家族 Judge 和语义保持扰动。独立 sealed eval 保留未见偏差因子及策略自适应攻击，检查 student 是否学到新的 evaluator 漏洞。
