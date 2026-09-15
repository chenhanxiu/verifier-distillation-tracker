# Know When to Stop, Where to Restart: Accelerating Multi-Turn Agentic On-Policy Distillation

## 基本信息

- **简称**：STRIDE
- **作者**：Zhiyu Gui；Kexin Huang；Jia Guo；Junkang Wu；Zihao Wang；Zhiqiang Zhang；Jun Zhou；Jiancan Wu；Xiang Wang
- **首次公开日期**：2026-09-13
- **版本日期**：2026-09-13（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.14636
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】多轮 Agent OPD 的 teacher 信息集中在较早回合；STRIDE 在 student 首个错误处对齐监督、对明显 OOD 的后缀提前停止，并从最弱的正确前缀重启，从而显著减少无效 rollout。

## 真正新增的内容

【论文原文】STRIDE 同时回答“何时停止”和“从哪里重启”：跨回合 endorsement loss 锁定 student 的首个错误行动；累计 teacher log-probability 低于阈值时终止 OOD 后缀；prefix buffer 保存正确但薄弱的状态，以后从这些位置继续探索。

【分析推断】这是目前最直接面向多轮 Agent 的 OPD 预算分配方案之一，也为“首错之后不要把整条轨迹一律标负”提供训练侧实现。

## 核心方法

1. 在多轮 student 轨迹上定位首个 teacher 不认可的行动。
2. 将跨回合 endorsement loss 施加到该首错，而非平均覆盖全部回合。
3. 监控累计 teacher log-probability；低于 OOD 阈值时提前终止。
4. 把最弱但仍正确的前缀加入 buffer，后续从该 state 重启 rollout。
5. 在多 teacher/跨域设置复用上述停止与重启机制。

## 关键实验结果

【论文原文】在 tau²-bench Retail 上，STRIDE 匹配完整 OPD，并超过 30B teacher，同时达到 3.73× 加速；相对基线达到 2.34×，跨域多 teacher 达到 4.51×。AIME 2025 和 AIME 2024 分别达到 5.10× 与 3.08× 加速。

【证据边界】速度与性能结果很强，但摘要没有给出全部置信区间、工具副作用错误率或长期真实环境成本；数学任务的收益也不能自动外推到事务型 Agent。

## 证据质量与局限

- **质量**：覆盖多轮 Agent、数学推理和多 teacher，且同时报告质量与加速。
- **局限**：teacher log-probability 低可能代表真正 OOD，也可能是新颖但成功的策略；过早终止会系统性丢失探索。
- **依赖**：首错定位仍受 teacher 偏差影响；若没有环境重放，teacher 的“不认可”不等于行动错误。

## 最接近的相关工作

Key-Step Supervision、DART-SD 的断点后缀蒸馏、SAGE 的高熵选择、Persistent Teacher Anchoring，以及用首个不可恢复错误做信用分配的方法。STRIDE 的独特之处是把首错监督、OOD 早停与正确前缀重启组合成完整的 Agent OPD 加速器。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可用 distributional verifier 取代单一 teacher log-prob 阈值：估计“成功、可恢复、不可恢复”三类概率，并用 conformal 区间决定继续、重启或停止。首错应由环境反事实重放与 LLM critique 共同确认。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 将训练样本单元设为“前缀 state + 候选行动 + 可恢复性分布”。
- A/B/T 由首错行动、teacher 替代行动和环境等价行动构造；等价行动标 Tie。
- 仅在硬真值证实方向错误时施加强负梯度；单纯低似然只降低预算或触发分叉。
- prefix buffer 应保留高熵且尚未失败的状态，避免早停造成探索坍缩。
- student critique 可建议重启点，但必须经重放验证。
- sealed eval 单独测量任务成功、真实步数、被误停的成功路径比例和 evaluator 版本漂移。