# Environmental Feedback Modeling Matters: Rethinking Feedback Treatment in Agentic Hindsight Self-Distillation

- **作者**：Hangxi Guo；Fengyuan Liu；Yue Wang；Yuhua Qi；Haoyi Xiong；Fei Sun；Mengnan Du
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11384
- **Canonical URL**：https://arxiv.org/abs/2610.11384
- **代码**：未发现公开代码链接

## 一句话结论

SELF 表明 Agent 自蒸馏不应把环境反馈只当作上下文文本：同时学习预测反馈，并蒸馏“看过真实反馈的 hindsight teacher”，能显著改善长轨迹决策。

## 真正新增的内容

【论文原文】SELF 联合训练两项能力：预测下一步环境响应，以及从可见真实反馈的 self-teacher 向当前 student 蒸馏反馈条件化决策。它显式把环境反馈建模误差纳入 hindsight self-distillation。

【分析推断】这提供了 student-generated critique state 的自然结构：先预测会发生什么，再与真实结果比较，critique 应围绕可验证的预测残差生成，而非自由文本反思。

## 核心方法

1. 在多轮 Agent 轨迹上训练模型预测动作后的环境反馈。
2. 构造能看到实际后续反馈的 hindsight self-teacher。
3. 将 teacher 的反馈条件化决策知识蒸馏回只看到当前历史的 student。
4. 联合优化反馈建模与策略蒸馏，使改进来自对环境动力学的吸收，而不只是结果模仿。

## 关键实验结果

【论文原文】在 Qwen3-8B 上，SELF 的 τ-bench 成功率分别比 SDPO 和 GRPO 高 6.4 与 4.1 个百分点；AppWorld task goal completion 分别高 10.71 与 3.57 个百分点。

## 证据质量与局限

【论文原文】在两个真实感较强的多轮 Agent 基准上对强基线取得明显提升。  
【局限】环境反馈本身可能不完整、延迟或受 harness 影响；反馈预测准确不等同于任务正确。论文摘要未说明在分布外工具、不可逆副作用、对抗反馈或冻结 sealed evaluator 下的表现。

## 最接近的相关工作

与 The Tasteful Agent 的 hindsight distillation、DENSE、PaperDoctor、Grounding Agent Memory、FLARE 和 Persistent Teacher Anchoring 最接近。SELF 的独特之处是把“反馈生成模型”与“反馈条件化蒸馏”联合起来。

## 如何复用或推进 LLM-as-a-Verifier

可训练生成式 verifier 同时输出：预期环境变化、可核验观察、未完成义务、序数风险分布和 critique。真实反馈到达后，以残差校准 verifier；只有能指向具体 observation/tool result 的 critique 才进入后续蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将 outcome score 拆成“预测反馈分布”与“观察到的结果分数”，对两者分别蒸馏。
- **A/B/T 与序数分布**：由多个可能反馈诱导 A/B/T；预测区间未覆盖真实反馈时输出 T/不可判定。
- **程序化/环境真值门控**：真实 tool/environment response 是 teacher 信号的硬锚，语言反馈只提供解释和幅度。
- **student-generated critique states**：用预测—现实残差生成 critique，并要求证据指针与可重放结果。
- **高熵分叉**：保留反馈分布多峰的动作分支，而不是让 hindsight teacher 把所有路径压成单一答案。
- **sealed eval**：冻结环境、工具版本、harness 与独立 evaluator，并单独测试 feedback model 的校准与策略成功率。

总体判断：【分析推断】SELF 直接补上现有路线中“环境反馈如何进入 verifier 蒸馏”的缺口，优先级很高；但硬真值必须来自可重放环境，而非模型预测本身。