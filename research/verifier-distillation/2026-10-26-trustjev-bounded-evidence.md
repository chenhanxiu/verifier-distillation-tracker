# TrustJev：将策略权威与不可信证据分离

## 基本信息

- **论文标题**：TrustJev: Separating Policy Authority from Untrusted Evidence in LLM-Based Decisions
- **作者**：Zhiwei Xu, Xuyang Liu, Xiaolin Peng, Weixian Deng, Jiabao Gao, Zirui Li, Tian Qiu, Boya Zhou, Wei Jiao, Hai Wan, Xibin Zhao
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.34826
- **代码链接**：未发现公开代码

## 一句话结论

TrustJev 用受保护的 policy score 决定“证据最多能改多少”，防止外部证据中的注入指令越权覆盖应用规则。

## 真正新增的内容

**论文原文结论**：同一 Transformer 从可信 policy 与候选动作计算基础分数和 correction budget；不可信 evidence 只能在预算内修正。paired supervision 同时要求对不改变事实的指令插入保持稳定、对真正改变答案的证据作出变化。

**分析推断**：这为 Agent verifier 的 evidence channel 增加了权限边界：工具返回、网页和 Agent 自述可提供事实，却不应改写 rubric、安全规则或 verifier 的评分协议。

## 核心方法

- 受信 policy/candidate 通道产生基础 decision score。
- 模型同时估计 evidence correction budget。
- 外部 evidence 只允许在有界范围内改变候选分数。
- 用 instruction insertion、事实变化与 authority-insufficient 样本联合监督。

## 关键实验结果

**论文报告**：0.6B 实现与 14 个基线在认证、指令层级和可执行授权规则三个数据集比较，Balance（正常与攻击准确率的调和均值）最高，各数据集比最强基线高 0.57–1.05 点。在授权 benchmark 固定攻击池中，95.77% 的 source 可正确处理全部 32 个攻击，最强对照为 80.98%。

## 证据质量与局限

攻击/非攻击共同评价且有可执行规则，证据较好。局限是域集中在安全决策和固定候选；correction budget 本身仍由模型预测，面对分布外证据可能失准。

## 最接近的相关工作

Jev、Our Own Jev、prompt-injection defense、Persistent Teacher Anchoring，以及 evidence-grounded verifier。核心区别是显式区分“谁有权定规则”和“谁只提供事实”。

## 如何复用或推进 LLM-as-a-Verifier

将 rubric、工具 schema、安全约束作为 protected policy；把工具结果、网页内容、模型 critique 作为 untrusted evidence。verifier 输出基础序数分布、证据修正量和预算，便于审计是否越权。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：仅蒸馏预算内 evidence correction，避免注入污染 teacher logits。
- **A/B/T**：证据不足以改变 protected policy 时保持原 verdict 或 T。
- **硬真值门控**：可执行授权/环境断言优先于文本证据。
- **critique states**：记忆不得携带修改 rubric 的指令。
- **高熵探索**：证据冲突但未越过预算时保留候选分支。
- **sealed eval**：加入隐藏 prompt injection、事实变化和权限冲突三类测试。