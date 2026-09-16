# Coupled Calibration and Learning: Mitigating Teacher Bias in LLM Distillation without Target-Domain Reward Feedback

## 基本信息
- **简称**：CCL
- **作者**：Haichen Hu；Yuheng Zhang；David Simchi-Levi
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.17474
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】在目标域没有 reward feedback 时，CCL 用源域奖励反复校准 teacher，并通过 token-level branching 让更新后的 student 反过来影响下一轮校准；理论上可收敛到 student 类中的 oracle，而直接匹配可能保留非零偏差。

## 真正新增的内容
【论文原文】论文研究 covariate shift 下的系统性 teacher bias，不假定强 teacher 在目标域必然可靠。每轮先用源问题奖励校准 teacher，再在目标问题上训练 student；student 的变化进入下一轮 teacher 校准，构成耦合闭环。

【分析推断】它为“训练域有程序真值、真实 Agent 目标域缺少即时真值”的 verifier 蒸馏场景提供了理论模板，但目标域安全仍取决于迁移假设。

## 核心方法
1. 只在 source questions 上取得 reward feedback。
2. 通过 token-level branching 估计并校准 teacher 的偏差。
3. 用校准后的 teacher 监督 target-domain student。
4. student 更新反哺下一轮 teacher calibration。
5. 在自回归策略框架证明 student 到类内 oracle 的平均 KL 以多项式速率收敛。

## 关键实验结果
【论文原文】主要贡献是理论保证：CCL 可控制 teacher calibration error 并推进投影 student gradient；论文还证明 regularized direct matching 即便面对总体更强 teacher，也可能与 oracle student 保持非零误差。

【证据边界】摘要未报告大规模实证和长时程 Agent 结果；理论 oracle 限定在 student class 内，也不是无限制最优策略。

## 证据质量与局限
- 优点是明确刻画 teacher bias 与 student 更新的耦合误差。
- 依赖源域反馈能校准目标域相关偏差；若偏差机制发生结构变化，保证可能失效。
- 反复共适应可能让训练指标改善但目标域真实正确性下降，必须有独立审计。

## 最接近的相关工作
VISTA、DualOPSD、CompassOPD、Proof-Carrying Cognition、GLARE，以及基于 teacher–student 位移的 OPRD。CCL 的区别是目标域无奖励时的耦合校准与收敛分析。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】在可重放模拟环境中校准 verifier 的各维 score 分布，再将校准器迁移到真实/封闭环境；student 的新失败反例只能更新候选校准器，必须经过 source oracle 或小规模现实结算才能生效。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：维护 teacher 原始分数、校准分数和 student 反馈三条日志。
- A/B/T：源域分支有硬标签；目标域仅在校准置信区间足够窄时输出 A/B，否则 Tie。
- 环境真值：Mock Tool/可执行 source 环境用于校准方向，目标域软信号只调幅。
- critique states：student critique 可暴露 teacher 偏差，但不能自行成为真值。
- 探索：目标域不确定状态保留分支并送现实结算，不强行蒸馏。
- sealed eval：冻结最终校准器，在未用于耦合更新的目标域切片上测校准误差和任务成功。