# T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning

- **作者**：Bo-Wen Zhang, Junwei He, Maoqi Liu, Feiran Li, Song-Lin Lv, Wentao Ma, Rongyi Lin, Shuhan Zhong, Lan-Zhe Guo
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.00388
- **代码**：未发现公开代码链接

## 一句话结论

T2SPO 从历史成功轨迹学习“距成功还剩多少步”，以相邻状态的距离变化给当前 Agent 动作分配步骤信用。

## 真正新增的内容

【论文原文】成功轨迹中的中间状态可监督未来交互。T2SPO 用这些状态及剩余距离作为上下文，让预训练 TabPFN 在不更新参数的情况下估计新 rollout 每个状态到成功的距离，并以距离变化产生辅助信用。

【分析推断】它把“目标推进”具体化为可更新的 potential difference，很适合无唯一参考答案但有终局成功标记的长轨迹。

## 核心方法

从成功轨迹提取 state representation 与 remaining-distance target；TabPFN 条件化这些样例预测新状态距离；连续状态预测差与 task-level reward 共同训练策略，新增成功轨迹持续刷新上下文。

## 关键实验结果

【论文原文】1.5B 与 7B 模型在 ALFWorld、WebShop 上均稳定优于 GRPO；摘要未报告绝对提升或距离估计误差。

## 证据质量与局限

覆盖两种规模和两个交互环境，且不需训练额外 value model；但“步数更少”不必然表示更安全或更优，成功轨迹库的覆盖偏差可能惩罚合理绕行与恢复路径。

## 最接近的相关工作

PGPO、BATON、RLDS、ArenaFlow、potential-based reward shaping。

## 如何复用或推进 LLM-as-a-Verifier

把 remaining distance 扩展为多维 potential：目标推进、风险、未完成义务和可恢复性；verifier 输出其联合序数分布，而不是单一距离。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：用 potential delta 作为 step/segment score，再调节 OPD 强度。
- **A/B/T 与序数分布**：两个动作的距离后验不可分时标 T；保留方差而非只取均值。
- **硬真值门控**：成功库与状态表示必须由环境结算验证。
- **student-generated critique states**：critique 可预测未完成义务，但要由后续距离下降验收。
- **高熵分叉**：保留多个等距成功路径，避免把最短路误当唯一好路。
- **sealed eval**：训练成功库不得包含 sealed 任务或同构状态。
