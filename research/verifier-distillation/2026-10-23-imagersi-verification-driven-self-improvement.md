# ImageRSI：A/B 验证经验准入与离线 Judge 更新

- **论文标题**：ImageRSI: Verification-Driven Recursive Self-Improvement for Agentic Image Generation
- **作者**：Shuo Han、Zhilin Wang、Peng Ling、Wenjia Gong、Yang Liu、Guanjun Jiang、Yukun Cao、Xike Xie
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32120
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32120
- **代码**：未发现公开代码链接

## 一句话结论

ImageRSI 将任务内五维验证—修复、跨任务经验库与离线 Judge 更新串成闭环，并要求候选经验通过成对 A/B 验证后才写入，是 critique/memory 准入与 evaluator 共适应研究的直接案例。

## 真正新增的内容

**论文原文结论**：生成器保持冻结；系统在单任务内验证和修图，把成功经验跨任务复用，并用积累的 image-judgment 记录通过 SFT+GRPO 离线更新 Judge，更新后先评测再投入下一轮。

**分析推断**：它把 policy memory 与 evaluator update 同时纳入递归改进；价值在于显式 A/B 准入，但同一闭环仍可能逐轮共适应。

## 核心方法

1. 五维 verifier 对图像执行检查并生成修复。
2. 候选经验只有在成对 A/B 验证显示净收益后进入经验库。
3. Judge 用积累记录做 SFT 与 GRPO 离线更新。
4. 新 Judge 在复用前接受评测；生成器本体冻结。
5. ImageReq-Bench 提供 961 个复杂真实请求及 checklist。

## 关键实验结果

**论文原文结论**：Checklist Strict Accuracy 在 MindBench（Nano Banana Pro）为 52.6%，在 ImageReq-Bench 为 65.66%。消融中移除 alignment 维度，false-accept rate 从 24.8% 升至 37.1%。

## 证据质量与局限

有新 benchmark、维度消融与不同 Judge 训练配置比较；但任务限于图像生成，严格正确率仍不高。Judge 的训练数据来自自身闭环，未证明长期不漂移；经验 A/B 的评价若由同源 Judge 完成，仍可能强化共同盲点；代码未见公开。

## 最接近的相关工作

接近 VeriEvolve、Dynalize、RSI-Anything、LLM-as-an-Improver、EquiReview-R 与在线 reward-model 更新。区别是生成器冻结、经验库与 Judge 分别演进。

## 如何复用或推进 LLM-as-a-Verifier

将五维 checklist 替换为目标推进、澄清、不确定性、可行性、安全/可恢复性；经验写入前用双顺序 A/B、环境重放和独立 Judge 共同验收。Judge 更新采用同轮冻结、轮间候选更新。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：只对经 A/B 证实提高环境成功率的 critique/repair 蒸馏。
- **A/B/T**：保留双顺序 verdict；分歧或低置信经验标 T，不写入库。
- **真值门控**：执行结果优先于 Judge 的五维分。
- **critique states**：把通过准入的修复经验转成可检索、带证据状态。
- **探索保留**：未证伪的多条修复分支并存，不用单一 Judge 过早淘汰。
- **sealed eval**：冻结独立 Judge、请求集和生成器快照，隔离经验库与 Judge 的共同进化。
