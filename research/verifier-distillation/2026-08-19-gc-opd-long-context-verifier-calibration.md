# Beyond Teacher Likelihood：长上下文的 Group-Calibrated OPD

## 基本信息

- **论文标题**：Beyond Teacher Likelihood: Group-Calibrated On-Policy Distillation for Long-Context Reasoning
- **作者**：Zhu Zhang、Jixun Wang、Xiaoang Xu、Xiaorong Wang、Zihan Zhou、Zhiyuan Wang、Shuo Wang、Chaojun Xiao、Yuezhi Zhou
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.19181
- **DOI**：10.48550/arXiv.2608.19181
- **论文**：https://arxiv.org/abs/2608.19181
- **代码**：https://github.com/SolereZhang/GC-OPD

## 一句话结论

GC-OPD 把组内标准化的 verifier reward 与轨迹级 OPD score 之差作为有符号残差，再按 token 的相对 OPD advantage 分配该残差，是目前最直接贴合“score-level on-policy verifier distillation”的方法之一。

## 真正新增的内容

### 论文原文结论

作者发现长上下文越长，teacher likelihood 与任务 verifier 的排序越容易冲突：在 Multi-Table Extraction 中，组内 pairwise disagreement 从 40.6% 升至 64.0%；High-Recall Retrieval 从 35.2% 升至 60.2%。GC-OPD 不直接叠加 verifier reward，而计算 `ρ=z(R_verifier)-z(S_OPD)`，只校正 teacher 与 verifier 不一致的部分，同时保留原始密集 OPD 信号。

### 分析推断

这比“成功轨迹加权、失败轨迹丢弃”更适合长时程 Agent：它保留 graded outcome 的相对间距，并能表达 verifier 认为某条轨迹被 teacher 高估或低估的方向。不过论文验证的是长上下文答案生成，不是多轮环境 Agent。

## 核心方法

1. 每个 prompt 采样一组 student rollouts，teacher 提供 token 级 log-prob 差，任务 verifier 提供二元或 [0,1] 分数。
2. 对每条轨迹平均 token advantage 得到轨迹级 OPD score。
3. 在 rollout group 内分别 z-score verifier reward 与 OPD score，取二者差为 teacher–verifier disagreement residual。
4. RACA 将每个 token 相对本轨迹均值的 OPD advantage 映射到 (0,2) 的正权重；残差只调节强度，不把 token advantage 解释为 token 正确性。
5. 校正项加入原 OPD advantage，无需额外 teacher/student 前向。

## 关键实验结果

### 论文原文

- 训练集为 GoLongRL 的 9,527 个、最长 32K token 的 prompt，含 9 类任务、binary 与 graded verifier。
- Qwen3-4B 五项平均从 29.08 提升到 40.47；Vanilla OPD 为 39.31。
- Qwen3-8B 从 35.12 提升到 44.65；Vanilla OPD 为 43.56。
- 消融显示有符号 residual 优于直接加入组归一化 reward，RACA 优于均匀 token 分配。

## 证据质量与局限

- **质量**：同设置比较两种模型尺度、五个 benchmark；有 teacher–verifier disagreement 诊断和 residual/RACA 分离消融；代码公开。
- **局限**：绝对增益相对 Vanilla OPD 约 1.1 点，仍属中等幅度；verifier 多为任务特定程序指标，尚未证明对噪声 LLM Judge 稳健；训练任务以 retrieval/evidence aggregation 为主；v1 预印本。
- 论文未报告独立人工偏好评估，也没有长期 evaluator–policy 共适应测试。

## 最接近的相关工作

RG-OPD、Reward-Weighted OPD、Uni-OPD、SG-OPD、SCOPE、MOPD/OPSD，以及 GRPO 的 group-relative reward normalization。其差别是显式保留“verifier 与 teacher 轨迹排序的残差”。

## 如何推进 LLM-as-a-Verifier

- 将单标量 verifier reward 替换为校准后的序数分布期望值，并保留方差。
- 对 pairwise A/B/T，可由组内两条轨迹的 verifier 分布差产生 A/B；置信区间重叠时标为 T。
- 对 LLM Judge，应先做离线 AUC/校准筛查，再进入 residual；否则 GC-OPD 会系统性放大 Judge 偏差。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：可直接采用 `z(score_verifier)-z(score_teacher)` 作为轨迹级修正，而不是让 verifier 替代 teacher。
- **程序真值门控**：环境成功、单元测试和状态检查优先进入 R；LLM Judge 只补充不可验证维度。
- **Student-generated critique states**：可以对同组 rollout 生成 critique，再让 verifier 输出含 critique/不含 critique 两套序数分布，比较其增量。
- **高熵探索**：组内标准化天然保留相对多样性；对高熵但 verifier 差异不显著的分支应进入 T，不做强更新。
- **Sealed eval**：训练 verifier、β 选择和 rollout group 均不得接触 sealed 任务；另用冻结 Judge 与环境真值报告 teacher–verifier disagreement，防止双方共同漂移。