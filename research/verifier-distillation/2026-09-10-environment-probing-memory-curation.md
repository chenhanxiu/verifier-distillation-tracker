# Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents

- **作者**：Susheel Suresh、Hazel Mak、Sahil Bhatnagar、Chhaya Methani、Alejandro Gutierrez Munoz
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11060
- **DOI**：https://doi.org/10.48550/arXiv.2609.11060
- **代码**：截至记录时未发现公开代码

## 一句话结论

仅从成功/失败轨迹总结 memory 不足以证明经验正确、可泛化或仍然有效；给异步 curator 最小权限的只读环境工具，可显著提升 memory 准入质量与后续 Agent 效率。

## 真正新增的内容

**论文原文结论**：提出 environment-probing curator，在写入长期 memory 前主动查询真实系统，验证、缩小适用范围或刷新候选经验，同时保持任务 Agent 与写权限不变。  
**分析推断**：这是 student-generated critique/memory state 的程序化真值门控方案；其核心可迁移到 verifier 蒸馏的数据准入，而不是把 curator 本身当作最终 evaluator。

## 核心方法

任务轨迹产生候选 memory；异步 curator 通过 least-privilege、read-only world tools 获取外部证据，对候选条目执行验证、范围限定、更新或拒绝。无需重新训练基础模型，也不授予 curator 写环境的权力。

## 关键实验结果

在 GHCP-like harness 上，CLBench pass 从 39 提至 73，pass-discounted reward 从 8.60 提至 22.60，平均查询从 8.8 降至 4.7，成本从 3.38 美元降至 1.68 美元。在 90 个改编 APEX 任务上，18 个 memory-vs-baseline 均值比较均为正，调用下降 16%–75%，在 6 个 world 中有 5 个取得最高 reward/美元；Sonnet 4.6 与 Opus 4.7 上均有效。

## 证据质量与局限

同时报告成功率、成本、调用量并跨模型验证，工程证据较强；但环境与任务仍有限，curator 依赖 LLM 解释和可用的只读 API。尚未充分覆盖恶意工具返回、长周期概念漂移、权限缺失或不可观测状态；结果也不是 verifier 蒸馏的直接训练实验。

## 最接近的相关工作

Agent memory curation、experience/skill distillation、APEx、LongWoF-Bench、MemGuard、环境真值 verifier、student-generated critique filtering。

## 如何复用或推进 LLM-as-a-Verifier

将候选 critique/memory 拆成可验证主张，附上环境查询 receipt、时间戳、作用域和不确定性。训练小 verifier 预测“接受/拒绝/待核验”的序数分布，但真实写入由只读探针证据硬门控。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：仅对被环境探针证实且范围明确的 critique 施加正向蒸馏。
- **A/B/T**：同一前缀的两条记忆建议由实际 world state 比较；信息不足时标 T/待核验。
- **critique states**：采用 candidate → probe → scoped critique → replay 的准入链，并保存 evidence receipt。
- **高熵探索**：不确定条目不立即删除；隔离为待核验池，保留可能的策略多样性。
- **sealed eval**：训练 curator 不能读取 sealed 环境；用独立账户、工具权限和未来状态测试过期/共适应问题。