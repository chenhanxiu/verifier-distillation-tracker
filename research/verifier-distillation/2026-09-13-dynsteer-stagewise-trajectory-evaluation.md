# DynSTEER: Dynamic Stage-wise Trajectory Evaluation and Execution-time Review for Agents

## 基本信息

- **作者**：Zhichao Shi；Wenjie Zhang；Xuhui Jiang；Xiaojun Wu；Cehao Yang；Chengjin Xu；Jian Guo；Yuanzhuo Wang
- **首次公开日期**：2026-09-13
- **版本日期**：2026-09-13（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.14637
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】DynSTEER 把长轨迹按已完成行动动态分段，用不泄漏隐藏答案的里程碑图与分层 Judge 逐阶段评估，并在确认不可恢复时提前终止失败执行。

## 真正新增的内容

【论文原文】与整轨迹事后打分不同，DynSTEER 在执行期持续更新阶段边界；从公开任务视图编译允许多路径的 milestone graph，避免把单一参考路径当作唯一正确解；再按阶段难度路由不同成本的 Judge，并对不可恢复失败执行 halt。

【分析推断】它为长时程 process verifier 提供了介于“逐步原子评分”和“整轨迹总分”之间的实用粒度，恰好回应 MedSNIP 关于过细原子化破坏依赖结构的警告。

## 核心方法

1. 根据动作完成情况将轨迹动态切分为语义阶段。
2. 仅使用公开可见任务信息构建 path-tolerant milestone graph。
3. 将阶段证据路由给不同能力/成本的 Judge。
4. 聚合阶段判断形成更有区分度的轨迹评价。
5. 识别不可恢复阶段后提前停止，节省失败 rollout 成本。

## 关键实验结果

【论文原文】评价区分能力提高 85.2%，所有模型对都能被显著区分；对失败 rollout 平均节省 34.51% 的执行步数。

【证据边界】这些结果支持动态阶段评价的判别力与成本收益，但不说明 Judge 分数已经校准，也未证明早停不会删去罕见恢复路径。

## 证据质量与局限

- **质量**：同时测量模型区分度和执行成本，并显式处理多条合法路径。
- **局限**：milestone graph 的编译质量决定上限；公开任务视图可能不足以识别隐藏副作用。Judge 路由若与被训练 Agent 共同更新，会产生 evaluator 共适应。
- **风险**：不可恢复判定是一项高代价决策，假阳性比普通评分误差更严重。

## 最接近的相关工作

DRACO 的动态 rubric 信用分配、MedSNIP 的依赖片段粒度、AutoSciRub/ExecRubrics 的结构化 rubric、Thinkingbox 的后端状态检查，以及 STRIDE 的早停与重启。DynSTEER 的主要差异是执行期阶段化和 path-tolerant 里程碑图。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把每个阶段输出建模为序数分布：未开始、部分完成、已完成、完成但有副作用、不可恢复。程序化检查器先提供硬约束，generative verifier 再生成证据化 critique；分布熵决定是否调用更强 Judge 或展开反事实分支。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD 应落在阶段边界，而非对每个 token 等权。
- 同一里程碑下的多条合法路径可自然产生 A/B/T；路径等价时标 Tie。
- 不可恢复标签必须由环境快照重放或事务日志确认，LLM Judge 不应独占否决权。
- 把 student-generated critique 附着到阶段节点，并要求引用可审计的动作/状态证据。
- 对高熵阶段先保留多个后继，不因单一低分立即早停。
- sealed eval 需冻结 milestone 编译器、Judge 快照和 halt 规则，并单报“误杀可恢复轨迹率”。