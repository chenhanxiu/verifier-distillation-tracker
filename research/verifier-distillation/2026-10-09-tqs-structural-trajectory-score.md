# Quality, Not Just Outcome: A Structural Scoring Framework for Selecting Coding-Agent Trajectories for Supervised Fine-Tuning

- **作者**：Sida Li；Yuanxin Liu；Shicheng Li；Linli Yao；Xu Sun；Haoli Bai；Xiaohui Li
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13152
- **Canonical URL**：https://arxiv.org/abs/2610.13152
- **DOI**：10.48550/arXiv.2610.13152
- **代码**：未发现公开代码链接

## 一句话结论

TQS 不依赖 LLM Judge，而用信息聚焦、意图—动作一致性和策略动态对成功 coding 轨迹做线性时间结构评分，证明“最终通过”之外仍需筛除低质量过程监督。

## 真正新增的内容

【论文原文】成功轨迹也可能包含重复读文件、工具使用不稳定和延迟修改等低质量行为；TQS 直接从轨迹结构评价“结构化收敛”，用于 SFT 数据选择。  
【分析推断】它适合作为 LLM Judge 之外的异质 verifier 通道：不回答语义正确性，而检查动作序列是否具有可迁移的过程质量。

## 核心方法

1. 从交互轨迹抽取信息聚焦、意图—动作对齐和 policy dynamics 特征。
2. 在线性时间内计算 Trajectory Quality Score。
3. 在已通过测试的轨迹内部排序。
4. 选择高分子集做 SFT，并与随机/低分子集比较。

## 关键实验结果

【论文原文】在 155,144 条公开许可的成功轨迹上评分；高分轨迹训练的 coding agent 在 SWE-bench Verified 上持续优于随机和低分子集。摘要未披露统一绝对增益，需结合正文表格判断效应量。

## 证据质量与局限

样本规模大，并用下游训练而非离线相关性验收，证据中等偏强。局限是结构启发式可能偏好某种操作风格；只在成功轨迹与 coding 域验证，且高 TQS 不保证事实或安全正确。

## 最接近的相关工作

与 FLARE、Continuous Process-Level Evaluation、RECAP、RELACE、BATON、MedSNIP 和 OnTrack 最接近。区别在于无需生成式 Judge、计算线性且面向训练数据筛选。

## 如何复用或推进 LLM-as-a-Verifier

将 TQS 类结构信号作为独立 process channel，与五维语义 Judge、环境终局和错误归因并列；先用硬真值确定有效性，再用结构分过滤重复、漂移和无效操作，避免 Judge 单点共因误差。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：结构分作为有界 process weight，不改变硬真值符号。
- **A/B/T 与序数分布**：同 outcome 内按结构质量做 A/B；不同风格但等效时保留 T。
- **程序化/环境真值门控**：仅在通过执行检查后使用结构分筛选正样本。
- **student-generated critique states**：critique 应指向重复动作、无证据编辑或工具抖动等可计算结构事件。
- **高熵分叉**：不要把必要探索误判为低效；对信息增益高的分支单独建模。
- **sealed eval**：下游 Agent 在未见仓库和不同 harness 上复验，防止结构启发式过拟合。