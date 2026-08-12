# ReOrder-OPD：基于 Teacher 续写可靠性的 On-Policy Distillation 排序

## 基本信息

- **论文标题**：ReOrder-OPD: Reliability-Aware Prompt Ordering for On-Policy Distillation
- **作者**：Ximo Zhu, Ruiqi Liu, Rong Wang, Ping Wu, Xiang Zheng, Wenzhuo Xu, Xubin Yao, Zhiyuan Yan, Bo Li, Jun Gao, Xiaolei Lv
- **首次公开日期**：2026-08-11
- **当前版本日期**：2026-08-11（v1）
- **arXiv ID**：2608.10905
- **原始论文**：https://arxiv.org/abs/2608.10905
- **代码**：截至记录时未发现公开代码仓库

## 一句话结论

ReOrder-OPD 不修改 token-level OPD 目标，而是优先训练 teacher 能从 student 状态可靠续写到正确答案的 prompts；它证明 prompt 访问顺序本身会改变 on-policy 学习路径，但其 ROUGE-5 代理不适合直接充当 Agent 状态价值。

## 真正新增的内容

**论文原文结论：** 作者定义 prompt-level teacher continuation reliability：从当前 student 轨迹采样前缀后，teacher 续写到 verifier-correct 结果的平均概率。由于精确估计昂贵，实用方法用一条独立 student rollout 与同题正确 teacher 轨迹库的最大 ROUGE-5 F1 排序 prompts，再用全新的 student rollout 进行 vanilla OPD。

**分析推断：** 这把“是否监督当前轨迹”与“何时访问某类状态”分开，说明 verifier × OPD 除了 loss/gating，还应显式研究数据调度的路径依赖。

## 核心方法

1. 用二元答案 verifier 定义 prefix-level teacher 续写成功率，再对 student 轨迹和前缀求期望得到 prompt-level (R)。
2. 精确 (R) 仅用于诊断；实际代理为一条 student 完整响应与同题 verifier-correct teacher 响应库的最大 ROUGE-5 F1。
3. 按代理分数从高到低访问 prompts；用于打分的 rollout 不参与训练，训练时重新采样 on-policy 轨迹。
4. 所有 prompts 保留，低分项目只是延后；动态版本会对尚未访问的队列重新打分。
5. 该调度层可与 FiRe-OPD、ExOPD 等 trajectory-level 监督方法组合。

## 关键实验结果

**论文报告：**

- 主 teacher 为 Qwen3-30B-A3B-Instruct-2507，students 为 Qwen3-1.7B/4B/8B；另测试 Gemma4-26B-A4B-it 到 E2B/E4B。
- 数学实验覆盖 DeepMath-1K/5K/17K，评测 AIME24/25/26 与三项 HMMT；代码评测 HumanEval+、MBPP+、LiveCodeBench V6。
- 五种 student 配置的六项数学聚合分均提高 1.09–2.58 个百分点；15 个模型×随机种子聚合差值全部为正，30 个模型×benchmark 均值中 27 个提高。
- 代理分数十等频分箱中，真实平均 (R) 从 0.29 单调升至 0.98。
- ReOrder 在全部六个 FiRe-OPD/ExOPD 组合设置中继续带来增益。
- 代价方面，主设置需预生成每题最多 16 条 verifier-correct teacher 轨迹及一条额外 student 打分轨迹；匹配比较只等化训练更新数，没有等化总生成/验证成本。

## 证据质量与局限

**证据较强处：** 两个模型家族、多个 student 规模、数学与代码、三随机种子、固定 prompt pool/更新预算，并把打分 rollout 与训练 rollout 分离。

**局限与分析：**

- 代理依赖正确 teacher 轨迹库和表面 ROUGE-5 相似度；不同但同样正确的策略可能被低估。
- verifier 只检查最终答案，不验证中间推理的因果贡献。
- 报告的 matched gain 没有等化预生成 teacher 库与额外 student rollout 成本。
- 只验证数学/代码短任务，尚无长时程 Agent 状态分叉证据。
- 高可靠到低可靠的课程可能延后罕见、困难但研究价值高的状态；固定预算下这些状态甚至不会被访问。

## 最接近的相关工作

Prune-OPD、FiRe-OPD、PW-OPSD、SOD 处理已采样轨迹内部的监督可靠性；PG-OPD、RG-OPD 使用 continuation 或 verifier 信号；ExOPD 改变蒸馏目标。ReOrder-OPD 的差异是提前决定 prompt 访问顺序。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 用 teacher verifier 从当前 Agent 状态续跑多次，估计“可恢复到成功”的概率分布，而非文本相似度。
- 将 (R) 扩展为失败/部分完成/可恢复/成功的序数分布，并蒸馏给轻量 student verifier。
- 对 student-generated critique states 计算“critique 后续跑的环境成功率”，作为调度分数。
- 将打分 rollout、训练 rollout 和最终 sealed eval 三者严格分离。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：增加 state/prompt scheduler，在 score-distribution distillation 前优先访问 teacher continuation 可靠但 student 尚不稳定的状态。
- **A/B/T**：同一状态多分支续跑，环境结果不可区分时保留 tie；不能以轨迹文本相似度直接判胜负。
- **真值门控**：以工具回执、程序测试、环境终态估计 continuation reliability。
- **Critique states**：比较有无 student critique 的反事实续跑成功率，决定其训练优先级。
- **保留探索**：为低可靠、高熵状态预留固定预算，避免课程排序把困难分叉永久推迟。
- **Sealed eval**：teacher 正确轨迹库不得来自最终测试任务或共享 evaluator。

ReOrder-OPD 最适合作为现有 loss-level 实验之外的一条“可靠性调度”消融，而不是替代序数 verifier。
