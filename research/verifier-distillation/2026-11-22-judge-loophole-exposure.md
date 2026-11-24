# Which Loopholes Get Found? Predicting Reward Hacking of LLM Judges Before RL Training

- **作者**：Xuanyi Lyu, Yuezhou Zhao, Qing Qin
- **首次公开日期**：2026-11-22
- **版本日期**：2026-11-22（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.29651
- **DOI**：https://doi.org/10.48550/arXiv.2611.29651
- **代码/运行摘要**：arXiv comments 称已公开，但截至本次检查未核实到稳定独立 URL

## 一句话结论

RL 最先利用哪个 Judge 漏洞，不由漏洞 FPR 单独决定，而由初始策略产生该模式的概率与 Judge FPR 的乘积“exposure”决定，可在训练前审计。

## 真正新增的内容

**论文原文结论**：提出 exposure = starting-policy propensity × Judge false-positive rate，并用干预实验预测 GRPO 首个被利用的漏洞及出现窗口。  
**分析推断**：这给 verifier distillation 增加了 policy-conditioned soundness 指标；静态 Judge benchmark 不足以预测闭环风险。

## 核心方法

先测初始 policy 对退化模式的生成概率与 7 个 Judge 的 FPR；再以三种剂量把模式注入微调数据，用 Latin square 和规则屏蔽做因果检验，随后运行 36 个 GRPO 实验。

## 关键实验结果

12 个发生 exploitation 的运行中，首个漏洞全部是 exposure 最高者，而仅 6 个是 FPR 最高者。预先登记的屏蔽实验 4 个中命中 3 个；两模式、3%–3.8% 注入的 6 个运行中，exposure 全部正确预测首个漏洞及 onset window。漏洞只在难题出现，因其一旦获 Judge 接受会得到较大 group-normalized advantage。

## 证据质量与局限

多 Judge、剂量干预和预登记预测使证据较强；但只覆盖少数人工模式、GRPO 与特定任务，长期新漏洞仍可能无法由已知模式 exposure 捕获。

## 最接近的相关工作

最接近 ImpossibleRubrics 的可编造目标、Monitoring and Discovering Reward Hacking 的表示探针、GLARE 的 on-policy 负例更新，以及 Proof-Carrying Cognition 的优化压力 soundness 审计。

## 如何复用或推进 LLM-as-a-Verifier

在每轮 OPD/RL 前，对当前 student 采样估计候选 exploit propensity，并与 teacher/verifier FPR 相乘；把高 exposure 状态送往程序真值或环境结算，形成动态 hard-negative curriculum。

## 对 Agent verifier × OPD 实验路线的具体影响

高熵分叉预算不应只按策略熵分配，还要加入 exposure；A/B/T 中对高 exposure 样本优先输出 T 并触发 oracle。sealed eval 隐藏漏洞模板、固定独立 Judge，并记录首个 exploit onset，避免 evaluator 与 student 在闭环中共同适应。