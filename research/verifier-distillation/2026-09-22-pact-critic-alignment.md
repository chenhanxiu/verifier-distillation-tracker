# PACT: From Credit Assignment to Critic Alignment

- **作者**：Jiayan Fu, Hang Xu, Yong Zhang, Zhaokai Luo, Yao Hu, Dongyan Zhao, Mu Chuan
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.26355
- **Canonical URL**：https://arxiv.org/abs/2609.26355
- **DOI**：10.48550/arXiv.2609.26355（arXiv DataCite，待注册）
- **代码**：未见论文专用公开仓库；实验基于 Dressage/slime
- **arXiv ID**：2609.26355

## 一句话结论

【论文原文】在 Completeness、Prefix Consistency、Neutrality 三个条件下，token credit 唯一等于相邻前缀价值之差；理想 OPD teacher 等价于隐式 critic，而 practical critic 若落后于 actor，一个很小的价值误差就可能淹没长轨迹中稀疏的真实 credit。

## 真正新增的内容

【论文原文】论文首次给出一组公理化条件下 token-level credit 的唯一刻画，并把 OPD、RLOO 与 GAE 放进同一梯度视角：理想 on-policy teacher 诱导的期望梯度与 token credit 成比例；response-level RLOO 虽粗，却在期望策略梯度贡献上可匹配；GAE 的中间 critic error 在长轨迹稀疏 credit 下可能占主导。PACT 因此先更新 actor，再用 importance-corrected target 同步 critic。

【分析推断】这为“score-level on-policy verifier distillation”提供理论坐标：teacher score 的关键不是越细越好，而是与当前 student policy 对齐，且误差不能大于真实局部贡献。

## 核心方法

1. 以 filtration 上的条件价值定义每个 token 后的 (V_i=E[R|F_i])，credit 为 (C_i=V_i-V_{i-1})。
2. 证明三条正则条件唯一确定上述 credit，并证明 bounded outcome reward 下大 credit 近似稀疏。
3. 分解 GAE：当 λ<1 时中间 critic error 保留；λ=1 消除中间误差，仅剩 prefix value error。
4. PACT 采用 Actor-then-Critic 顺序；actor 更新后，用 continuation importance ratio 将旧 rollout 重加权为新 policy 的 critic target。
5. 实际实现用 detached current-token ratio 与区间 mask 近似长序列乘积，只需一次额外 forward pass。

## 关键实验结果

- agentic 数学推理四基准 Avg@16 为 72.87%，高于 GRPO 64.07%、PPO(λ=1) 59.71% 和 SAO 51.14%。
- 去掉 importance sampling 的 PACT 为 67.74%，说明 critic-policy 对齐本身贡献约 5.13 个百分点。
- SWE-bench Verified 上 PACT pass@1 67.4%，高于 GRPO 65.4%、PPO 65.0%、SAO 63.6%。
- PPO λ=0.95 在数学训练中崩溃到 26.31%，而 λ=1 达 59.71%，与中间 critic error 分析一致。

## 证据质量与局限

【论文原文】理论结果清晰，实验覆盖数学与 agentic coding，且包含去 IS 消融。限制是唯一性依赖三条所选公理，并不排除其他 credit 定义；理论中的精确 continuation ratio 在长序列中高方差，实践只用局部近似；论文仍未解决 token credit 的精确高效估计。SWE-bench 只报告单一模型/主要指标，尚缺跨 harness 与独立复现。

【分析推断】PACT 的 critic 和 actor 共享训练闭环，不能替代 sealed evaluator；提升也可能来自更稳定优化而非更“真实”的因果归因。

## 最接近的相关工作

最接近 γOPD 的 token/sequence 时间信用统一、BATON 的轨迹内/轨迹间双轴归因、PGPO 的状态势能、VinePPO/GAE，以及 RLOO/GRPO。与这些方法不同，PACT把理想 OPD teacher 明确解释成隐式 critic，并把训练顺序造成的 policy mismatch 作为主要误差源。

## 如何复用或推进 LLM-as-a-Verifier

- 将 verifier 的 score distribution 解释为 prefix value 分布，训练相邻前缀差而非独立步骤标签。
- A/B/T 可由两个候选 continuation 的 value interval 产生；差异小于 critic 误差界时标 T。
- 用程序/环境终局奖励校准 critic 方向，LLM critique 只解释 credit 发生在哪个局部。
- 对 student-generated critique state，要求其加入后能稳定改变后续 (V) 且在重放中被验证，否则不授予正 credit。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】下一轮应把 PACT 作为 score-level OPD 的 critic 基线：同一批 on-policy 轨迹比较 sequence reward、λ=1 prefix critic、privileged teacher OPD 与两者混合。teacher/critic 必须随 student 更新或做 importance correction；高熵分叉中若 critic error 与预测 credit 同量级，应保留探索而非强蒸馏。sealed eval 仍由冻结程序 oracle 和未参与 critic 训练的任务组成，用来检测 actor–critic 共同漂移。