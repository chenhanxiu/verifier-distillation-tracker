# Root-Cause Attribution Is a Search Problem: Continual Search for Long-Horizon Agent Failures

## 基本信息

- **作者**：Harsh Raj；David Lee；Anas Mahmoud；Renxiong Wang；Razvan-Gabriel Dumitru；Chenguang Wang；Tong Zhao；Yunzhong He；Darvin Yi；Vipul Gupta
- **首次公开日期**：2026-09-11
- **版本日期**：2026-09-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.13463
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】长时程 Agent 的根因归因不应是一遍式 Judge 分类；Continual Search 反复要求 Judge 搜索尚未解释的证据，使 GPT-5.5 的根因 F1 从 0.349 提升到 0.498。

## 真正新增的内容

【论文原文】论文把 root-cause attribution 明确建模为持续搜索：一遍式 Judge 容易早早锁定显眼症状，方法通过迭代提示暴露未解决证据并修订假设。作者还构建 MegaRCA-Mix，含 50 条人工标注、执行密集的长轨迹失败案例。

【分析推断】这直接挑战“把整条轨迹交给一次 LLM Judge”的 verifier 设计，也为 generative verifier 的 critique state 提供搜索过程监督，而非仅监督最终标签。

## 核心方法

1. Judge 先提出初始根因假设。
2. 系统识别当前解释未覆盖或相互冲突的轨迹证据。
3. 继续搜索更早的依赖、环境反馈与工具结果。
4. 迭代修订根因，直到证据闭合或预算耗尽。
5. 在四个 RCA 基准及 MegaRCA-Mix 上评估。

## 关键实验结果

【论文原文】GPT-5.5 的 F1 从 0.349 提升到 0.498，增幅超过 40%；采用 Continual Search 的较低层级模型可以超过未使用该方法的更高层级模型。

【证据边界】50 条人工标注长轨迹对定性诊断有价值，但规模仍小；F1 提升不代表根因判断具备因果可干预性，也不自动转化为任务成功率。

## 证据质量与局限

- **质量**：跨四个基准并引入人工标注的执行密集长轨迹，直接评估根因而非只评最终成功。
- **局限**：搜索过程仍由同一 Judge 主导，可能反复强化初始偏见；迭代成本和停止条件需要审计。
- **风险**：没有环境反事实重放时，“最早相关事件”仍可能被误当成真正原因。

## 最接近的相关工作

EDGE 的反事实错误依赖图、AgenticRAG-FP 的失败传播、Key-Step Supervision、Coding Agent 过程评估的因果层级，以及 DRACO 的责任步骤分配。Continual Search 的差异是把 Judge 推理过程本身转成迭代证据搜索。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 输出扩展为分布化根因图：每个候选节点包含概率、证据覆盖、可证伪测试和未解决冲突。随后用环境重放执行干预，只有移除/替换该节点能改变结局时才提升因果置信度。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD 不应把失败奖励均匀回传；先搜索首个具有反事实影响的节点。
- 在共享前缀处用原动作、修复动作和等价动作生成 A/B/T；序数标签表达损害程度与可恢复性。
- 工具返回、状态快照和终态 oracle 对根因方向拥有优先权，LLM critique 负责提出可检验假设。
- student-generated critique 需记录“证据—假设—测试—结果”，不能只存自然语言结论。
- 高熵或证据冲突节点保留多个根因分支，避免早期假设坍缩。
- sealed eval 用独立标注、隐藏反事实和不同 Judge 快照评估归因；同时报告根因 F1 与干预后成功率。