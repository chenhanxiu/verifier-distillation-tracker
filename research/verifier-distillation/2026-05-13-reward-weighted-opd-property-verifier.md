# Reward-Weighted On-Policy Distillation with an Open Property-Equivalence Verifier for NL-to-SVA Generation

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Reward-Weighted On-Policy Distillation with an Open Property-Equivalence Verifier for NL-to-SVA Generation
- **作者**：Qingyun Zou, Yingze Li, Tianen Liu, Bingsheng He, Weng-Fai Wong
- **首次公开/版本**：2026-05-13
- **arXiv**：[2605.13501](https://arxiv.org/abs/2605.13501)
- **HTML 全文**：[arxiv.org/html/2605.13501](https://arxiv.org/html/2605.13501)

## 一句话结论

RWOPD 给出了“开放程序 verifier + student rollout + dense teacher KL”的可复现实例。

## 真正新增的内容与核心方法

student 生成 SVA，SymbiYosys+Z3 的 Property-Equivalence Checker 判定语义等价，再仅在 verifier 可通过的 rollout 上施加 verifier-reward-weighted forward KL。

## 关键实验、证据质量与局限

7B student 在 NL2SVA-Human/Machine 的 pass@1/5/10 上达到新 SOTA，并超过专用模型和更大的通用模型。强项是 reward 可执行、可审计；局限是形式验证域规则明确，开放 Agent 轨迹更难获得同等质量真值。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可作为 environment-truth gating 的强基线。迁移时按工具执行、数据库状态或单元测试生成 hard evidence，再由 LLM verifier 处理软准则；两类信号不应简单平均。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
