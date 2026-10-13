# EvoBelief: Falsifiable World Models for Self-Improving LLM Agents

- **作者**：Janet Wang；Jiang Guo；Yi Xiang；Jiaqing Yuan；Mingwen Dong；Hideo Kobayashi；Shuaichen Chang；Chandan K. Reddy；Jiarong Jiang
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12789
- **Canonical URL**：https://arxiv.org/abs/2610.12789
- **DOI**：10.48550/arXiv.2610.12789
- **代码**：未发现公开代码链接

## 一句话结论

EvoBelief 把 Agent 的环境知识写成带证据、作用域和可反驳条件的假设，只有经后续观察或受控实验独立验证后才能影响规划，为 critique/memory 的真值准入和回滚提供了完整原型。

## 真正新增的内容

【论文原文】不更新语言模型参数，而是在部署中演化可证伪世界模型：意外结果和决策相关未知触发假设，独立验证决定启用，反例会缩小作用域或退休规则。  
【分析推断】这可将 student-generated critique 从自由文本升级为“假设—证据—适用范围—反证条件—影响决策”的结构化状态。

## 核心方法

1. 从预测失败或关键未知中生成环境规则假设。
2. 通过后续观察与受控实验获得独立证据。
3. 仅让通过支持阈值的规则进入预测/规划。
4. 保存规则与证据、作用域和受影响决策的绑定。
5. 环境漂移出现反例时收缩或撤销规则。

## 关键实验结果

【论文原文】覆盖静态动力学、隐藏漂移与科学发现四类 benchmark。ALFWorld 在不使用 actor-side transition memory 时，相对 matched Frozen World Model，Claude Haiku 4.5 和 GPT-5.4 分别提升 23.9% 与 31.3%。DiscoveryWorld Reactor Lab 达到 Normal 83.3%、Challenge 58.3%，所比较 baseline 均为 0%；MiniGrid 能在未通知动力学变化后修订旧规则并恢复。

## 证据质量与局限

跨环境且含显式漂移和科学发现，机制证据较好。局限是强模型参与假设生成，受控实验成本可能较高；规则级成功不等于全局因果正确，跨任务复用仍可能传播共同误差。

## 最接近的相关工作

与 RSI-Anything、Grounding Agent Memory、RSIAgent、SkillAA、Proof-Carrying Cognition、Reality Is the Final Verifier 和 JANUS 最接近。其优势是把“可证伪与退休”做成规则生命周期的一等对象。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier critique 输出强制为结构化假设，并要求证据指针、覆盖状态、预期后果和可执行反证测试；未验证规则只能用于建议采样，不能直接改变评分或策略。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：仅从已验证且作用域匹配的规则产生 teacher score。
- **A/B/T 与序数分布**：有冲突证据或作用域外状态输出 T；后验支持度形成序数置信分布。
- **程序化/环境真值门控**：受控实验和真实状态转换是规则启用的硬门。
- **student-generated critique states**：采用假设—证据—反证—退休状态机。
- **高熵分叉**：用决策相关未知触发探索，优先能区分竞争假设的实验。
- **sealed eval**：在冻结环境变体和隐藏漂移上检测规则过拟合与错误传播。