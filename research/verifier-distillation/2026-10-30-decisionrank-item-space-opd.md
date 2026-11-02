# DecisionRank：面向决策模型重排器的 On-Policy Distillation

- **论文标题**：DecisionRank: On-Policy Distillation for Decision-Model Rerankers
- **作者**：Yanran Wu, Dian Yu, Chongyang Bai, Jieyi Zhang, Rui Liu, Tianyi Chen, Shike Mei, Hang Cui, Frank Shyu, Sandeep Pandey, Luke Simon, Chunwei Liu, Xi Liu
- **首次公开日期**：2026-10-30
- **版本日期**：2026-10-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.42128
- **DOI**：https://doi.org/10.48550/arXiv.2610.42128
- **代码链接**：论文页面未列出

## 一句话结论

DecisionRank 把 student 的标量 item scores 排序成 on-policy 列表，再让生成式 teacher 针对该列表返回条件反馈，证明“结构化动作上的 score-level OPD”可以让 1.7B 决策模型超过 27B teacher。

## 真正新增的内容

**论文原文结论**：生成式 teacher 的输出空间是文档 ID 序列，而 decision student 在首 token 位置直接输出各 item 分数；论文提出 item-space OPD，显式跨越两种输出接口，而不是要求二者共享 token 分布。

**分析推断**：这比常规 token-level OPD 更接近当前 verifier 路线：可把一组 Agent 分支的 verifier 分数排序为“动作列表”，再由强 teacher 对 student 自己诱导出的排序提供条件反馈，从而直接蒸馏 score geometry，而不必复制 teacher 文风或 tokenizer。

## 核心方法

1. student 对候选 item 输出标量分数，并按分数排序，形成 student on-policy ranking。
2. 生成式 teacher 读取该 ranking list，给出依赖当前 student 排序的条件反馈。
3. 反馈直接监督 student scores，并与离线 ranking supervision 联合训练。
4. 训练目标始终覆盖 student 实际会产生的排序状态，降低固定 teacher 列表造成的分布偏移。

## 关键实验结果

**论文原文报告**：

- 在 TREC DL、BEIR、BRIGHT 等四个基准上，item-space OPD 一致优于替代训练目标。
- 1.7B DecisionRank 在 TREC DL19–23 上超过 27B 生成式 teacher。
- 8B 模型优于生成式 listwise 对应模型，同时在 TREC DL 上快 24.5 倍、在 BRIGHT 上快 16.7 倍。

## 证据质量与局限

证据覆盖通用与推理密集检索，并有模型规模和效率对照，支持“score interface + on-policy ranking”本身有价值。但任务仍是静态候选重排，不含长时程环境状态、不可逆动作或延迟回报；论文也未验证序数校准、A/B/T 平局标签或 evaluator 共适应。超过 teacher 只在所报检索设置成立，不能外推为通用 weak-to-strong 结论。

## 最接近的相关工作

最接近的是 reward-based on-policy reranker distillation、常规 GKD/OPD、listwise KD，以及仓库中的 RouteOPD、CompassOPD、GVPO++ 与 VG-OPD。DecisionRank 的独特处在于把 OPD 从 token 空间提升到 item-score 诱导的结构化排序空间。

## 如何复用或推进 LLM-as-a-Verifier

- 对同一 Agent 状态采样多个动作/critique，student verifier 输出分数并形成排序；teacher 只评价这一 on-policy 排序。
- 同时保留 pointwise score、pairwise A/B/T 与 listwise ranking 三种头，检查三者是否满足传递性和序数一致性。
- 对 teacher 反馈用程序化/环境真值门控：真值决定方向，teacher 只补充相对间隔和解释。
- 高熵排序不应强行压成单一顺序，可保留 top-k 等价类或 T 标签。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：应新增一个“item-space score OPD”基线：在共享状态下生成 (K) 个 student actions，student verifier 得到 (K) 个 scores；teacher 对排序后的 ID 列表返回 pairwise/ordinal 目标，再只更新 verifier score head。与 token-level OPD、独立 pairwise 训练、离线 teacher 排序做三方对照。训练期间可使用 student-generated critique states，但最终必须在冻结任务、隐藏环境真值与独立 evaluator 上做 sealed eval，防止 teacher 与 student 共同适应同一排序协议。