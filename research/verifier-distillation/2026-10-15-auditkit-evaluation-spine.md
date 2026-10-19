# AuditKIT: A Unified Evaluation Spine for Benchmarking, Judging, and Comparing Large Language Models and Agentic Systems

## 基本信息

- 作者：Shreeyans Arora, Utsav Avaiya, Zera Lyngkhoi, Hem Gosalia, Ram Mohan Rao Kadiyala, Vinay Kumar Sankarapu, Pratinav Seth
- 首次公开日期：2026-10-15
- 版本日期：2026-10-15（v1）
- arXiv：2610.22511
- 原始论文：https://arxiv.org/abs/2610.22511
- DOI：https://doi.org/10.48550/arXiv.2610.22511
- 代码：https://github.com/Lexsi-Labs/AuditKIT
- 代码状态：公开仓库；论文页称 source-available

## 一句话结论

AuditKIT 把 verified outcome、轨迹诊断、工具调用匹配和配置指纹放进统一结果契约，并把不可观察证据标为 unscored，适合作为 Agent verifier × OPD 的 sealed-eval 工程底座。

## 真正新增的内容

**论文原文结论：** 该库统一 benchmark、Judge、运行性能、工具行为和检索评价，强调方向感知的 metric contract、配置 fingerprint、turn-aware tool matching，以及“终局真值”和“轨迹诊断”分离。

**分析推断：** 它不是新 verifier 模型，而是防止实验定义漂移和 evaluator 共适应的记录层；对当前路线最关键的是把 T/不可判定状态写进协议，而不是默认为失败。

## 核心方法

1. 用统一 `RunResult` 表示数据、模型、配置、样本级预测和聚合指标。
2. 通过稳定 SHA-256 fingerprint 绑定模型、seed、任务与配置。
3. 对 Agent 区分并行/串行工具调用并做 turn-aware 匹配。
4. 把 verified task outcome 作为 headline，把 trace/Judge/tool scores 作为 diagnostics。
5. 对缺失或不可观察证据标记为 unscored。
6. 提供 benchmark、LLM-as-Judge、确定性代码检查、RAG、pairwise、安全和性能等后端。

## 关键实验结果

**论文原文：** 论文给出七个案例，覆盖模型比较、推理后端、检索、工具调用和互操作性，展示答案抽取、运行行为与指标选择会改变评价结果。公开仓库报告约 3,000 项测试、11 类指标、6 个 CLI 子命令和稳定 fingerprint；这些是工程覆盖信息，不是 verifier 准确率证据。

**分析推断：** 对研究路线的价值在可复现性和语义隔离，而非证明其默认 Judge 更可靠。

## 证据质量与局限

- 有公开实现、测试和可检查的数据结构，工程可复现性较强。
- 七个案例不足以证明跨任务构念有效性；统一接口也不能自动消除错误 metric。
- fingerprint 能发现配置变化，但不能冻结闭源 endpoint 的隐藏版本。
- source-available 许可并非等同于宽松开源许可，复用前需检查许可证约束。

## 最接近的相关工作

- AutoTuneBench 的冻结协议、anti-cheat 和证据账本；
- Transect 的长轨迹可追溯时间线；
- Ground-truth-as-code；
- Harness or Model? 的环境/脚手架混杂控制；
- Agent trace diagnosability 的 abstention。

## 如何复用或推进 LLM-as-a-Verifier

扩展 `RunResult`：保存 teacher/student/verifier 快照、每步 score 分布、A/B/T、证据指针、程序真值、查询顺序和 OPD 权重。对 sealed split 单独生成 fingerprint，并禁止训练进程读取其样本级结果。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** 逐样本保存原始 score、校准后分布和最终 loss 权重，便于审计。
- **A/B/T 与序数分布：** 将 unscored 显式映射为 T，而非负类；保存完整分布。
- **真值门控：** verified outcome 与 Judge diagnostics 分栏，硬真值优先。
- **critique states：** 保存来源、版本、作用域和是否被接纳，不只保存文本。
- **高熵探索：** 记录候选覆盖、分叉位置和被 verifier 淘汰的路径。
- **sealed eval：** 用配置指纹、独立结果表和不可见样本级反馈实施；闭源模型还需额外记录 endpoint 时间与重复运行。
