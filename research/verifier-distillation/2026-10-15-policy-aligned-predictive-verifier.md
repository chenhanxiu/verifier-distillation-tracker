# Policy-Aligned Predictive Verification：预测动作前缀是否仍可成功续接

- **论文标题**：Policy-Aligned Predictive Verification for Adaptive VLA Action-Chunk Execution
- **作者**：Minkyu Kim, Junhoo Lee, Seungyeon Kim, Suhyun Jeon, Baekseung Kim, Donghoon Han, Nojun Kwak
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.21434
- **代码**：论文页面未提供公开代码链接

## 一句话结论

PAV 不用未来预测来生成动作，而是估计候选 action prefix 执行后还能否成功续接，并用终局 outcome 加定位先验学习局部 validity，是长轨迹 distributional process verifier 的直接原型。

## 真正新增的内容

**论文原文**：在 VLA 内部任务条件表示空间评价已有动作候选，而非依据生成稳定性或多预测一致性决定执行长度；把轨迹级 survival 监督与“失败轨迹中仍保留有用行为”的 localization prior 结合，输出前缀 validity 并自适应选择 action-chunk horizon。

**分析推断**：其关键价值不是机器人领域本身，而是把“失败轨迹≠所有步骤都错”形式化，可用于 Agent 工具调用前的局部 verifier 和 score-level OPD。

## 核心方法

对多个候选动作前缀预测后续成功兼容性；用终局成功/失败作 survival 标签，再以定位先验避免把失败轨迹中的早期正确动作全部标负；按 validity 选择实际执行长度。

## 关键实验结果

**论文原文**：在 pi_0 与 pi_0.5、LIBERO、RoboTwin 2.0 和真实机器人操作上改善 success–query trade-off。摘要未报告具体幅度。

## 证据质量与局限

同时覆盖模拟与真实执行、两个 VLA policy，且直接用任务 outcome；但摘要缺少绝对数字和校准指标。机器人 action chunk 与语言 Agent 的离散工具调用不同，迁移时需重新定义“可成功续接”和 recoverability。

## 最接近的相关工作

与 HaWMPO 的 action-chunk 可靠性、FARM 的逐步失败概率、REVERSAL-BENCH 的 recoverability oracle，以及 Verify–Act–Distill 的执行前验证最接近。

## 如何复用或推进 LLM-as-a-Verifier

对每个候选工具调用前缀预测“仍存在成功 continuation”的概率，并输出失败位置分布；将环境重放得到的 recoverability 作为硬标签，把 LLM critique 作为定位先验而非真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏 survival/validity 分布而非单一终局分数，并按前缀 recoverability 加权。
- **A/B/T 与序数分布**：比较不同 action prefix 的可续接概率；证据不足输出 T。
- **真值门控**：真实执行或可重放环境决定 survival 标签。
- **critique states**：只保存能定位风险步骤且经重放验证的 critique。
- **高熵探索**：高不确定但可恢复的前缀允许更长执行；高风险且不可恢复的前缀提前截断。
- **sealed eval**：在未参与训练的场景、扰动和硬件上校准 validity，分开报告任务成功率、查询次数和不可恢复失败率。
