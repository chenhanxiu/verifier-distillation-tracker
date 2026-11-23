# Composable Soft-Prompt Distillation of RL Experts: Toward Continual Post-Training

- **作者**：Zhen Zhang、Changyi Yang、Xuehai He、Chengzhi Liu、Yutong Yin、Ziyue Liu、Zhuoran Yin、Yangmin Li、Zhihan Liu、Jisen Li、Mingyu Jin、Chuhan Li、Zhaotian Weng、Ruoyu He、Wenyao Gao、Jiaxin Deng、Chenwei Wu、Hui Shen、Wenhao Chai、Chenyang Zhao、Zhuofan Ying、Kieran Liu、Andrew Chen、Pony Ma、Zhaoran Wang、Alkesh Patel、Zhe Gan、Xin Eric Wang
- **首次公开日期**：2026-11-20
- **当前版本日期**：2026-11-20（v1）
- **原始论文**：https://arxiv.org/abs/2611.27376
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.27376；DOI: 10.48550/arXiv.2611.27376

## 一句话结论

CSPD 将每个 RL expert 独立蒸馏成可拼接 soft prompt，在 22/23 个数学、代码和 Agent 设置中恢复至少 90% teacher 增益，并在多专家组合上匹配 MOPD，为持续加入 verifier specialist 提供了不重训主干的替代路线。

## 真正新增的内容

**论文原文**：固定 pre-RL 主干，每个 expert 单独蒸馏一个 soft prompt；新增 expert 时无需重新合并全部权重或重新运行多 teacher OPD，组合时直接串接 prompt。

**分析推断**：这为 verifier ensemble 提供“专家模块化”思路：可以分别蒸馏 outcome、process、safety、evidence verifier，再组合。但论文蒸馏的是 RL policy expert，不等于已证明 verifier score 可无损组合。

## 核心方法

- 冻结 pre-RL 模型，不修改主干参数。
- 每个 RL expert 独立训练一个 soft prompt。
- 多专家通过输入空间拼接 prompt 组合，无需联合训练。
- 与 weight merging、LoRA 和 multi-teacher OPD 比较能力恢复、泛化和吞吐。

## 关键实验结果

**论文原文**：

- 单 prompt 在 22/23 个数学、代码和 Agent 设置中恢复至少 90% teacher 增益。
- 多专家平均表现随新增 expert 持续上升。
- 完整组合与 MOPD 基本持平：67.83 对 67.79。
- 六个 held-out 基准上组合泛化最佳。
- 吞吐在未适配主干的 1.5% 内，并达到 rank-4 LoRA 的 2.40 倍。

## 证据质量与局限

覆盖多领域、Agent 设置和多种适配基线，数字清晰。局限是超长作者列表但公开摘要未说明组合顺序敏感性、冲突专家的最坏情况、校准或 verifier 分布；soft prompt 组合可能随上下文长度和模型架构变化。

## 最接近的相关工作

最接近 multi-teacher OPD、model merging、adapter composition、Lightning Weave、VG-OPD 与 RetireOPD。CSPD 的区别是把 expert 知识放在可组合输入参数中而非合并主干。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：为每个评分维度训练独立 verifier prompt，并以环境类型路由组合；组合后重新校准 A/B/T 或序数分布，不能假定单专家校准在拼接后保持。冲突维度应显式输出向量而非提前求和。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：探索按维度独立蒸馏 score head/prompt，再在推理时组合。
- **A/B/T 与序数分布**：每个专家保留自己的分布，最后用可解释聚合器融合。
- **真值门控**：程序/环境专家拥有最高优先级；软专家不得覆盖硬失败。
- **critique states**：不同专家产生的 critique 分开存储，只有证据一致部分进入共享记忆。
- **高熵探索**：专家分歧可作为分叉信号，而非强行平均。
- **sealed eval**：新增专家后必须在冻结任务上测遗忘、组合冲突与校准漂移。