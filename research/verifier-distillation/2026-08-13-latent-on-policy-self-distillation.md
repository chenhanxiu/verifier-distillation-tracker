# Latent On-Policy Self-Distillation（LOPD）

## 基本信息

- **论文标题**：Latent On-Policy Self-Distillation
- **作者**：Guibin Zhang、Jiayang Lyu、Ran Sun、Xinlei Yu、Haoyu Zhao、Qibing Ren、Shuicheng Yan
- **首次公开日期**：2026-08-13
- **版本日期**：2026-08-13（arXiv v1）
- **arXiv ID**：2608.13040
- **DOI**：10.48550/arXiv.2608.13040
- **原始论文**：https://arxiv.org/abs/2608.13040
- **代码**：https://github.com/bingreeky/LOPD

## 一句话结论

LOPD 不再手工规定 self-teacher 应读取答案、反馈、技能或轨迹，而是把检索经验压成端到端学习的连续 latent privileged context，并用可验证 margin 防止 teacher 退化；在工具使用与代码生成上以不到 GRPO/Skill-SD 30% 的 rollout 预算取得更高综合结果。

## 真正新增的内容

**论文原文结论**：LOPD 把 OPSD 的核心设计变量从“选择哪种人工 privileged artifact”改成“让经验表示本身可学习”。检索到的原始经验经 composer 转成连续 latent tokens，teacher 在这些 token 条件下监督 student 真实访问的 prefix。

关键新增不是单纯 latent memory，而是把 composer、privileged context 与 on-policy student 联合优化，并加入 privileged-margin constraint，要求 teacher 相对 student 保持由环境奖励确认的 log-probability 优势。

## 核心方法

1. 从经验库检索与当前任务相关的历史轨迹。
2. composer 将检索经验与当前任务压缩为连续 latent tokens（默认每条经验 32 个 token、检索 3 条）。
3. student 只看任务与交互历史并产生 on-policy 轨迹；self-teacher 额外读取 latent context，在每个 student-visited prefix 输出密集 token 分布。
4. 通过 distillation 更新 student，同时训练 composer；privileged-margin objective 用环境奖励 (A(\tau)=2r(\tau)-1) 约束 latent teacher 必须比 student 更有优势，避免联合优化把 teacher 拉回 student。
5. 推理时删除检索器、经验库、composer 和 latent context，仅保留已内化能力的 student。

## 关键实验结果

**论文报告**：

- 覆盖 3 个模型 backbone、7 个基准，包含 EnvScaler、BFCL-v3、ACEBench、LiveCodeBench、EvalPlus 等工具使用与代码生成任务；10 个 backbone–benchmark 聚合比较均为最佳。
- Qwen3-4B：LOPD 在 EnvScaler 为 63.7；BFCL-v3 平均 27.38；ACEBench 平均 60.6。对照 GRPO 分别为 61.8、25.25、56.0。
- Qwen3-8B：LOPD 为 66.4、29.88、62.7；GRPO 为 57.3、29.00、58.0。
- LOPD 用不到 GRPO 与 Skill-SD 30% 的 rollout 预算即超过二者。
- 消融显示仅检索经验不够；无约束联合优化可能使 teacher 向 student 坍缩；latent capacity 存在阈值，32 tokens/experience 是实验中逃离低容量区间的最小设置。

## 证据质量与局限

- **证据质量：中等偏强。** 有多个 backbone、工具与代码基准、预算对照、联合优化/检索/margin 消融，且代码与模型公开。
- **论文未单列局限章节；以下为基于实验范围的分析**：工具 rollout 最多 30 个环境步，尚不足以证明超长时程稳定性；经验检索和 latent composer 在训练期增加系统复杂度及潜在泄漏面。
- latent tokens 的 LM-head 投影不可直接解释，论文也承认“不可读”不等于已经证明 teacher 实际使用了何种信息。
- 环境 reward 既约束 latent teacher 又参与比较，若 verifier 有系统偏差，margin 可能放大 evaluator 共适应；现有实验未给出独立 sealed verifier。
- “不到 30% rollout”不等于总计算低于基线，检索、composer 和双分布前向的成本需单独核算。

## 最接近的相关工作

最接近 OPSD/SDPO 的答案或反馈条件 self-teacher、Skill-SD 的自然语言技能、SDFT 的反馈轨迹，以及检索/latent memory 方法。LOPD 与它们的核心区别是：不固定 privileged context 的离散格式，而让可微 latent substrate 根据最终蒸馏价值学习应保留的经验信息。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：

- 将“teacher policy 的 latent context”改成“verifier 的 latent evidence context”：检索相似 Agent 轨迹、程序执行记录、失败分叉与 critique，composer 生成 latent evidence，teacher verifier 输出 score distribution。
- privileged-margin 不应只约束 teacher 对已采样 token 的概率，可约束 teacher verifier 在程序/环境真值下对正确轨迹的序数优势，或对 A/B/T 三类的 margin。
- 为避免 latent context 学成 evaluator shortcut，应同时训练 invariance：等义轨迹描述保持分布，改变真实环境结果的反事实才允许移动分布。
- 通过蒸馏把 latent-evidence teacher 压回无需检索的部署 verifier，但最终用独立 sealed verifier 与程序真值检验是否真正内化。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：这是最直接的新分支。teacher verifier 读取检索轨迹的 latent evidence，student verifier 只读当前 student-generated trajectory/critique state，蒸馏完整 ordinal score distribution。
- **pairwise A/B/T 与序数评分**：composer 可同时读取 A、B 及共享环境证据，teacher 输出 A/B/T 和 (1\ldots K) 分布；margin 由环境胜负或程序化检查门控，不能只由 teacher 自证。
- **student-generated critique states**：经验库应包含 student 自身成功/失败 critique 与后续结果，使 latent context 学习哪些回顾信号可转移，而不是固定使用人工 critique 模板。
- **高熵分叉保留探索**：只在 margin 被真值确认时蒸馏；高熵且无可验证 teacher 优势的分叉不施加强 latent 对齐，保留多策略探索。
- **sealed eval**：训练期 composer、teacher verifier 和检索库均不得访问 sealed 任务族；最终同时测无检索 student verifier、带检索 teacher verifier和外部 judge，区分内化收益、检索收益与 evaluator 共适应。
