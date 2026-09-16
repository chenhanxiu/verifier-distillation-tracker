# Beyond Token-Local Imitation: Reward-Compatible Temporal Credit Assignment for On-Policy Distillation

## 基本信息
- **方法名**：γOPD / Reward-Compatible Bounded Mixing（RBM）
- **作者**：Shiqi Liu；Zeyu He；Letian Tao；Guojian Zhan；Jiaxin Gao；Feihong Zhang；Jingliang Duan；Wei Xiong；Kehua Sheng；Bo Zhang；Yang Guan；Shengbo Eben Li
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16937
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】γOPD 将 token-level OPD 解释为 sequence-level reverse-KL 的时间近似，以折扣信用在长期目标忠实度与方差之间折中，再用有界混合把可验证结果奖励接入 OPD advantage。

## 真正新增的内容
【论文原文】论文统一 token-level 与 sequence-level OPD 的时间信用视角：前者稳定但短视，后者考虑未来但方差随 horizon 增长。γOPD 引入折扣未来信用并给出与 horizon 无关的方差界；RBM 在受控范围内混合 verifier outcome 与 teacher advantage，减少纯 teacher 依赖。

【分析推断】这为长轨迹 Agent 的 score-level OPD 提供了比“每步独立打分”更严谨的时间传播基线。

## 核心方法
1. 从 sequence-level reverse-KL 梯度推导 token-local OPD 的时间近似。
2. 用折扣因子 γ 将后续 teacher 信号分配给更早 token。
3. 证明梯度估计具有 horizon-independent variance bound。
4. RBM 有界组合可验证 outcome reward 与折扣 OPD advantage。
5. 在单 teacher、规模错配和多 teacher 设置训练。

## 关键实验结果
【论文原文】数学与代码推理实验中，γOPD/RBM 在 vanilla、teacher–student 尺度错配及多 teacher 三类设置均稳定优于已有 OPD 方法。

【证据边界】摘要没有给出完整绝对分数和真实长时程 Agent 实验；理论方差界依赖论文设定，不能自动保证 verifier 偏差受控。

## 证据质量与局限
- 理论统一、方差界与多设置实验相互支撑，证据结构较强。
- 折扣 γ 引入新的偏差—方差选择；错误 outcome verifier 仍会沿时间传播。
- 代码/数学的最终奖励较清晰，开放式 Agent 的部分完成度和可恢复性更难定义。

## 最接近的相关工作
token/sequence OPD、PGPO、DRACO、Key-Step Supervision、LURE、SIGNBALANCE 和 STRIDE。区别是从 reverse-KL 明确推导折扣时间信用，并对 verifier reward 做有界混合。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】让 verifier 输出阶段级序数分布与置信区间，再将期望增益按时间折扣传播；程序化终态负责符号，LLM verifier 只分配软幅度。对首个不可恢复错误采用非对称传播，避免惩罚有效前缀。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：优先实现 γ 扫描与 RBM，比较逐步、阶段和整轨迹监督。
- A/B/T：共享前缀分支的未来回报差异传播到决策点；置信区间重叠标 Tie。
- 环境真值：硬成功/失败与副作用决定 reward 符号，不允许 teacher advantage 覆盖 veto。
- critique states：critique 的信用由其之后的真实轨迹改善决定。
- 探索：高熵状态降低 γ 或混合强度，防止远期噪声导致过早收缩。
- sealed eval：独立报告训练 verifier reward、环境成功率和跨 horizon 稳定性。