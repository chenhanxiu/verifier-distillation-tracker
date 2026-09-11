# FARM: Reading Failure Signals from the Internal Predictive States of a Frozen Robotic World Model

- **作者**：Haoran Pei、Mingrui Luo、Senbao Wang、Haoran Lv、Jie Guo、Sheng Zhong、Ruixi Ci
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11445
- **DOI**：https://doi.org/10.48550/arXiv.2609.11445
- **代码**：https://github.com/HaoranPei-casia/FARM

## 一句话结论

FARM 从冻结机器人世界模型的预测状态中训练仅 33,985 参数的失败读出器，以亚毫秒开销输出逐步失败分数和轨迹风险，是轻量 distributional process verifier 的直接原型。

## 真正新增的内容

**论文原文结论**：世界模型的内部 predictive states 已包含可读出的失败信号；小型监督 readout 无需微调 VLA-JEPA，即可完成 step-level failure scoring 与因果式 trajectory-risk 聚合。  
**分析推断**：这比仅看动作 token 或自然语言 critique 更贴近环境动力学，但适用于 LLM Agent 时需要可访问的 latent world model，不能直接假设文本模型隐藏状态具有同等可迁移性。

## 核心方法

冻结 VLA-JEPA，在内部预测状态上训练 33,985 参数 readout，生成逐步失败概率，并按时间因果聚合为轨迹风险；通过跨任务、跨平台和少量适配测试读出稳定性。

## 关键实验结果

七任务五折 out-of-fold 汇总 AUROC/AUPRC 为 85.68/88.59，并在 15 个匹配基线的 seen 设置中最佳。PIPER X、SO-101、Franka 真机扩展实验中，某 zero-shot 汇总为 84.70/79.13，少量适配后为 98.48/98.41；其他 shift 下存在明显波动。额外延迟约 0.2256 ms。

## 证据质量与局限

含 OOF、15 个基线和多真机平台，且报告延迟，证据扎实；但训练依赖监督失败标签与特定 world-model states，跨分布结果不均匀。机器人“失败”定义通常比企业 Agent 的部分完成/可恢复/副作用更窄，尚无序数校准、开放世界工具链或 evaluator 优化压力测试。

## 最接近的相关工作

World-model anomaly/failure detection、process reward models、Speculative Uncertainty、HaWMPO 的世界模型可靠性权重、hidden-state readout verifier、机器人 reward models。

## 如何复用或推进 LLM-as-a-Verifier

在 Agent world/state model 的预测 latent 上蒸馏多头 readout：下一步失败概率、可恢复性、义务遗漏和副作用风险；用可执行 outcome 与传感器信号校准，而把自然语言 generative verifier 作为解释层。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：latent risk 分布控制蒸馏强度，环境终值决定更新方向。
- **A/B/T**：同状态分支的风险区间和恢复概率形成 A/B/T；差异不稳时保留 T。
- **真值门控**：用传感器、执行状态和安全约束否决仅靠 latent 的乐观判断。
- **critique states**：让 student critique 指向高风险时间段，再由 latent/readout 与回放共同验真。
- **高熵探索**：在策略高熵但预测风险低且不确定性可控时保留探索；高风险分支升级强 verifier。
- **sealed eval**：按机器人平台、任务和故障类型隔离，冻结独立传感器标签，防止 readout 与训练世界模型共适应。