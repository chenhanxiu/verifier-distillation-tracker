# Expected Value Alignment for Generative Reward Modeling in Formal Mathematics Verification

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：Expected Value Alignment for Generative Reward Modeling in Formal Mathematics Verification
- **作者**：Shihao Ji, Haotao Tan, Zihui Song, Mingyu Li
- **首次公开/版本**：2026-05-31
- **arXiv**：[2606.01160](https://arxiv.org/abs/2606.01160)
- **HTML 全文**：[arxiv.org/html/2606.01160](https://arxiv.org/html/2606.01160)

## 一句话结论

EVA 证明了生成式 critique 与连续 reward 可以共用一个模型接口，和“verifier 输出解释 + 评分分布”高度契合。

## 真正新增的内容与核心方法

模型以结构化 JSON 输出离散整数分数，同时从这些锚点 token 的 logits 计算连续期望；训练把语言建模损失与期望值 MSE 联合起来，在 Lean 4 的 Leibniz reward model 中保留可读解释并减少数值 token 离散化误差。

## 关键实验、证据质量与局限

论文以形式数学验证和中间步骤打分为主要场景，对比零样本与 reward-model baseline，显示连续 logit 评分能降低离散化伪影。证据集中在单一正式验证域，迁移到开放 Agent 轨迹仍需复验。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

这是实现 score-level dense verifier 的直接参考：让 teacher/student 同时输出 critique 与固定评分锚点，再蒸馏评分分布。建议分离 explanation loss 与 score-distribution loss，测试解释质量是否真正改善校准而非仅增加 token 成本。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
