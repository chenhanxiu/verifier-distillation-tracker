# FAER: Auditable Utility-Aligned Trajectory Replay for Language Model Post-Training

- **作者**：Miaobo Hu, Shuhao Hu, Xiaobo Guo, Xin Wang, Bokun Wang, Tianshu Fu, Daren Zha, Jun Xiao
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.00385
- **代码**：未发现公开代码链接

## 一句话结论

FAER 证明“缓存轨迹本身正确”与“它对当前 learner 有训练价值”不是同一目标，并以虚拟更新估计 learner-aware replay utility。

## 真正新增的内容

【论文原文】常见 replay selector 按格式、置信度、新鲜度或长度排序，但 cache correctness 可能和下游学习价值错位。FAER 冻结可观测字段与 replay trace 后才接入评价标签；FAER-UTILITY 用一次可丢弃的 optimizer-aware virtual update 构造含幅度的效用表面。

【分析推断】对 verifier 蒸馏而言，不应仅筛“teacher 判高分”的轨迹，而应筛真正改善 student 的轨迹，同时防止选择器窥视最终标签。

## 核心方法

提供无需训练的固定 selector 协议基线；在不相交 calibration block 上拟合 learner-aware selector；以 gradient alignment 和虚拟更新估计候选轨迹对 learner 的边际效用。

## 关键实验结果

【论文原文】GSM8K/Qwen2.5-1.5B、128 次更新中，固定 selector 质量 0.6329，uniform 0.5482，format-feedback 0.6037；cross-fitted metadata selector 为 0.6476±0.0139（8 seeds），完整 FAER-UTILITY 达 0.6624。format-feedback 选中轨迹 correctness 更高（0.6953 对 0.3594），却不具最佳下游效用。

## 证据质量与局限

成本、八种子和审计协议报告完整；但核心实验集中在 GSM8K 小模型，尚未验证长轨迹 Agent、非平稳 student 或 verifier 共适应。

## 最接近的相关工作

RoboDrop、IWD、S²D-OPD、One-Shot OPD、Agent Error Dataset。

## 如何复用或推进 LLM-as-a-Verifier

将每条轨迹的 verifier score 与 learner utility 分账：前者描述质量，后者由短虚拟更新或小规模在线实验估计；只在两者均合格时进入 replay。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：用预期 learner improvement 取代单纯 Judge 分数作为采样权重。
- **A/B/T 与序数分布**：比较两条轨迹的虚拟更新收益；置信区间重叠为 T。
- **硬真值门控**：环境正确性是准入门，不等于 replay 排序目标。
- **student-generated critique states**：critique 需证明可提升 learner，不能因表达漂亮被选中。
- **高熵分叉**：优先 replay 对 student 当前盲区有增量的多样分支。
- **sealed eval**：选择字段与轨迹先冻结，再接入独立标签；校准块与最终测试隔离。
