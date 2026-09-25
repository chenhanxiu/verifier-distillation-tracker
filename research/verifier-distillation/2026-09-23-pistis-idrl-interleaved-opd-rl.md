# Pistis Technical Report

## 基本信息

- **作者**：Heyun Chen、Xiaohan Lan、Jiaxi Li、Zhilin Lu、Qi She、Weiwen Xu、Fei Yu、Yujie Zhong、Jinghuan Chen、Zijian Feng、Siyu Jiao、Yiheng Lin、Xinhao Wang、Sihan Yang、Jieyu You、Changbin Zhang、Hengyu Zhang、Xudong Zhang、Yunqing Zhao、Shuai Zheng
- **首次公开日期**：2026-09-23
- **版本日期**：2026-09-23（v1）
- **原始论文**：https://arxiv.org/abs/2609.28554
- **DOI**：https://doi.org/10.48550/arXiv.2609.28554
- **代码/模型**：论文页面未给出公开代码仓库

## 一句话结论

把 OPD 与 RL 交替而非静态混合，可能更适合长时程 Agent 的“教师迁移—环境纠偏”闭环，但当前公开摘要不足以证明收益来自交替机制本身。

## 真正新增的内容

【论文原文】提出 Interleaved Distillation and Reinforcement Learning（IDRL），在同一训练循环中交替执行 on-policy distillation 与 reinforcement learning；并训练 Pistis-Thinking、Pistis-Agentic 两类 27B/9B 多模态模型。作者声称交替优化改善知识迁移、稳定性与长时程轨迹信用分配，并提出无需更新参数或增加交互预算的 Pistis-Auto-Harnessing。

【分析推断】相对“OPD 预热后再 RL”或固定加权联合损失，IDRL 的关键可检验增量是时序调度本身；需要等量 token、环境交互和 teacher 调用的消融才能确认。

## 核心方法

【论文原文】先进行大规模多模态 SFT，再在单一循环中交替 OPD 与 RL；Agentic 版本额外使用长轨迹、规划和工具调用数据。PAH 在模型外迭代优化 inference harness。

【分析推断】可把一次循环实现为：student rollout → teacher score/token 分布 → OPD 更新 → 环境结算 → RL 更新。这样 teacher 提供稠密方向，程序化真值修正 teacher 的系统偏差。

## 关键实验结果

【论文原文】两个规模均优于对应基础模型；Pistis-Agentic 在多模态搜索上尤其强，PAH 在不增大交互预算时继续提升表现。摘要未给出具体分数、方差或 IDRL 对静态混合的完整消融。

## 证据质量与局限

证据来自单篇技术报告和作者自报实验。公开摘要没有交代 teacher 成本、交替频率敏感性、独立复现、长轨迹信用指标或 sealed evaluator；因此“更稳定/更精确信用分配”应视为待验证主张。

## 最接近的相关工作

最接近 γOPD 的终局奖励混合、RL Starts before RL 的阶段关系、RetireOPD 的 teacher 退出和 Low-Bit OPD 的部署路径训练。Pistis 的区别是把 OPD/RL 交替写入一个统一循环，并同时优化 Agent harness。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 输出拆成序数分布与生成式 critique：OPD 阶段蒸馏 score distribution，RL 阶段只让环境/程序真值决定奖励方向；teacher 与环境冲突时记录为 T/INCONCLUSIVE，而不是平均。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 新增 `OPD→RL`、`RL→OPD`、细粒度交替、静态联合四组等预算基线。
- pairwise A/B/T 保留 teacher–oracle 冲突，测试交替是否减少冲突积累。
- 只在可执行环境结算后强化 critique state，避免 harness 与 evaluator 共适应。
- 高熵分叉继续保留多候选；不要让 OPD 先行压缩探索。
- 最终成绩必须由冻结 harness、冻结 verifier、未参与训练的 sealed eval 报告。