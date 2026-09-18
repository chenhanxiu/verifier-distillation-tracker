# RetireOPD：Agentic RL 中自退役的 On-Policy Distillation

## 元数据
- **论文标题**：RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning
- **作者**：Yan Yu、Zhengxi Lu、Yizhou Liu、Yichen Pan、Aozhe Wang、Qipeng Chen、Hua Yang、Wenqi Zhang、Weiming Lu、Qianglong Chen、Yongliang Shen
- **首次公开日期**：2026-09-17
- **版本日期**：2026-09-17（v1）
- **原始论文**：https://arxiv.org/abs/2609.20784
- **代码链接**：未发现公开代码链接

## 一句话结论
OPD teacher 的价值具有阶段性；应先用环境奖励训练独立 teacher，再让 student 在能力接近且分布差距不再缩小时自动停止蒸馏，避免后期 teacher 成为上限。

## 真正新增的内容
**论文原文结论**：特权 skill 不保证 teacher 可靠，且 teacher 监督收益随训练阶段变化。RetireOPD 用环境奖励先优化解耦的 skill-conditioned teacher，再联合 RL 与 OPD 训练无 skill student，并依据差距收敛和成功率比例触发 Adaptive Retirement。

**分析推断**：现有 Agent verifier × OPD 路线不应使用固定蒸馏周期；teacher 退役条件应同时包含环境成功率、score-distribution gap 和 sealed eval 趋势。

## 核心方法
1. teacher 与 student 解耦，teacher 带特权 task skill 并先由环境奖励优化。
2. student 在自身 rollout 上同时接受 RL 和密集 OPD。
3. 当 teacher–student discrepancy 不再下降且 student 达到 teacher 成功率的目标比例时，撤掉 teacher，转为纯 RL。

## 关键实验结果
**论文报告**：Qwen2.5 1.5B–7B 上，较 RL 基线，ALFWorld 成功率提高 14.1%–18.8%，WebShop 准确率提高 11.8%–19.0%；所有设置中 student 最终超过其 skill-conditioned teacher。

## 证据质量与局限
优点是直接覆盖多轮 Agent、多个模型规模和两个环境，并验证超过 teacher。局限是只覆盖 Qwen2.5 与两个任务；摘要未说明退役阈值对域外任务的敏感性；teacher 和 student 共用环境可能产生 evaluator 共适应。

## 最接近的相关工作
最接近 DualOPSD、ARISE-RL、RA-OPD、OPDVR 和 SAGE。RetireOPD 的区别是显式处理“teacher 何时退出”，而非仅判断何时接受 teacher 信号。

## 如何复用或推进 LLM-as-a-Verifier
把 verifier teacher 的调用从永久监督改为状态机：冷启动强监督、能力接近后按高熵状态选择性调用、达到退役条件后只保留独立审计。退役后仍在 sealed slice 上周期抽检，发现回归再局部恢复 teacher。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：新增基于分布差距、真值成功率的自适应退役。
- **A/B/T 与序数分布**：teacher 仅在 A/B 可由环境验证时提供方向；分歧状态保留 T。
- **真值门控**：环境 reward 负责训练与评估 teacher 可靠性。
- **critique states**：退役前优先蒸馏 student 当前失败产生的 critique state。
- **高熵探索**：退役不等于禁用 teacher；仅在高熵/不可逆状态路由回来。
- **sealed eval**：退役判据不能使用最终 sealed set，并需监控 teacher–student 同步过拟合。