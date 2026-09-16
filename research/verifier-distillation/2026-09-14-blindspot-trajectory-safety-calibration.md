# BLINDSPOT: A Benchmark for Safety and Refusal Calibration in Long-Horizon Tool-Using Agents

## 基本信息
- **作者**：Sadia Asif；Mohammad Mohammadi Amiri；Momin Abbas；Tejaswini Pedapati；Prasanna Sattigeri
- **首次公开日期**：2026-09-14
- **版本日期**：2026-09-14（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16305
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】Agent 安全必须按完整轨迹而非单轮二分类衡量；BLINDSPOT 用状态化工具和执行真值把结果分成安全完成、正确拒绝、不安全完成、过度拒绝、不可判五类，并发现失败可在多步安全行为后才出现。

## 真正新增的内容
【论文原文】基准把 evolving authorization、持久状态、环境反馈和自适应攻击放进实时模拟，形成 22 类攻击、35 个场景、7 个领域、超过 2,500 条轨迹，平均 14.7 轮；评价同时覆盖安全、效用、稳定性与拒绝后的再次失守。

【分析推断】五类结果天然对应比二元 pass/fail 更有用的序数/类别分布，可作为安全维度的 distributional verifier 标签。

## 核心方法
1. 用户—Agent—环境进行长时程自适应对抗交互。
2. 工具调用改变持久状态与授权条件。
3. 用 execution-grounded adjudication 判断真实结果。
4. 轨迹归入五类结果，而非仅统计攻击/任务成功。
5. 八项指标覆盖 unsafe completion、appropriate refusal、benign utility、over-refusal、重复稳定性和 post-refusal failure。

## 关键实验结果
【论文原文】评估 13 个闭源和开源模型，观察到显著的安全—效用校准差异；部分失败只在若干初始安全步骤之后出现。

【证据边界】摘要将结果称为 preliminary，未给出这里可核验的完整模型分数与统计显著性；平均 14.7 轮仍不能代表多日 Agent。

## 证据质量与局限
- 多模型、状态化执行和 2,500+ 轨迹提供较强行为证据。
- 五类标签并非天然线性序数；正确拒绝与安全完成需结合任务可行性判断。
- 自适应攻击生成器和 adjudicator 若共享知识，可能夸大或遗漏特定攻击模式。

## 最接近的相关工作
SafeBranch、CRATE、Cheap Verifiers Large Blind Spots、Harness-of-Harness、S3Gym 和长轨迹安全评测。BLINDSPOT 的特点是执行真值、动态授权及 post-refusal failure。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】训练 verifier 输出五类概率而非单安全分，并额外预测“当前可恢复性”和“未来失守风险”。程序化环境确认动作与状态，LLM Judge 解释授权语义和拒绝是否适当。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：分别优化安全完成与正确拒绝，不能把拒绝统一当高奖励。
- A/B/T：同一 state 下安全行动、危险行动和等价安全行动形成分支对；不可判为 Tie/abstain。
- 环境真值：授权变化、工具副作用和持久状态具有不可覆盖的 veto。
- critique states：记录导致 post-refusal failure 的承诺、状态遗漏和授权漂移。
- 探索：安全不确定时保留询问/只读 probe 分支，而非直接拒绝或执行。
- sealed eval：隐藏攻击族、独立 adjudicator、重复运行，并分别报告过拒绝和延迟失守。