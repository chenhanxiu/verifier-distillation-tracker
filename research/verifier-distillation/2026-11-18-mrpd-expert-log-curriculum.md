# Replay, Don't Resample: Off-Policy Consolidation of Long-Horizon RL Experts

- **作者**：Zhenrui Yue、Gongxiaohui Chen、Huimin Zeng、Honglei Zhuang、Jiashuo Sun、Zhen Han、Dong Wang
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.24059
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.24059；DOI: 10.48550/arXiv.2611.24059

## 一句话结论

【论文原文】MRPD 不重新采样环境，而按各专家原始学习顺序重放带概率和奖励的 RL 日志，在 logged prefix 上联合重算 policy gradient 与蒸馏最终专家，约以七分之一专家训练算力超过在线 MOPD。

## 真正新增的内容

【论文原文】把专家训练日志视为 curriculum 而非静态数据混合：沿专家自身轨迹重放使 student 在 consolidation 中保持接近 logged policy、减少 train–inference mismatch；无需再次调用环境、reward model 或专家采样。

## 核心方法

1. 保存专家 RL rollout、采样概率、奖励与时间顺序。
2. Student 按原顺序消费轨迹，在每步重算 clipped policy gradient。
3. 最终专家在 logged prefix 上提供 token distribution 蒸馏项。
4. 比较日志顺序、数量、reward 及 RL/蒸馏消融。

## 关键实验结果

【论文原文】在 reasoning、search、SQL 三个长时程 Agent 域上，MRPD 得到最佳 student，超过在线 RL 与相同专家的 MOPD；consolidation 成本约为训练专家算力的七分之一。日志分析显示 replay trajectory 携带大部分收益，policy-gradient 与 distillation 项均有贡献；顺序的重要性大于日志数量或 reward。

## 证据质量与局限

【论文原文】覆盖三类长轨迹任务，并有日志与目标项消融；但摘要未给出具体成功率和方差，方法依赖完整保存 behavior probability。其“quasi-on-policy”建立在沿专家轨迹保持 clip range 的经验条件上，不等同真正 student on-policy 数据。

## 最接近的相关工作

最接近 MOPD、offline RL、experience replay、policy distillation、DAgger 与 curriculum replay。区别是保留专家训练时间顺序，并在历史前缀上同时使用 RL 与最终专家分布。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可重放 verifier 训练过程中的历史 on-policy 轨迹、当时 score 分布和最终 verifier teacher，在不重跑昂贵环境的情况下合并多域专家；但应保留 evaluator 版本，避免用最终 teacher 静默重写历史真值。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：保存行为策略、teacher/verifier 版本和 score，比较按原顺序 replay 与随机混合。
- **pairwise A/B/T 与序数分布**：历史 pair 标签与最终 teacher 分布并存，翻转样本标记为 evaluator drift。
- **程序化/环境真值门控**：历史硬结果不可被最终 soft teacher 覆盖；环境版本变化需单独分层。
- **student-generated critique states**：按专家实际学习阶段重放 critique，而非只蒸馏最终“干净答案”。
- **高熵分叉探索**：replay 会缺少 student 新分叉，需保留少量在线校验臂检测 coverage gap。
- **sealed eval**：在未重放、未参与专家训练的独立任务上评估，防止 curriculum 记忆被误当泛化。
