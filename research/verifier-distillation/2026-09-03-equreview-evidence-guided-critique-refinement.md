# More Criticism Does Not Make a Better Review: EquiReview-R

## 基本信息

- **作者**：Zexing Zhang, Jichao Li, Tianyang Lei, Yude Fu, Yang Kewei
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **原始论文**：https://arxiv.org/abs/2609.03943
- **代码/数据**：论文声明发布 ReviewTrace，但公开页未给出独立链接
- **arXiv**：2609.03943
- **DOI**：https://doi.org/10.48550/arXiv.2609.03943

## 一句话结论

EquiReview-R 把 critique 视为可修订的结构化 concern set，分别控制遗漏与过度批评，并显式返回 stop/continue/defer；更多 critique 本身不是更好的 verifier 信号。

## 真正新增的内容

**论文原文结论**：对已有 concerns 先用局部证据做 resolve/revise，再从独立与 review-conditioned 两个视角搜索遗漏，建立遗漏与 overcritique 的双风险评估。

**分析推断**：student-generated critique states 不应直接累计进 verifier 上下文或训练集；应先做证据处置、去除无支持指控，并允许 defer。该结构可映射为 Agent 轨迹的错误候选集合。

## 核心方法

- 将 review 表示成结构化 concerns，而非单段自由文本。
- 每个 concern 绑定局部证据并进行保留、修订或删除。
- 从独立视角与受现有 review 条件化的视角搜索遗漏。
- 输出 stop、continue 或 defer，避免无限生成批评。
- 构建 evidence-linked trajectory corpus ReviewTrace，用于分析 revision、disagreement 与 provenance。

## 关键实验结果

- 在冻结的未见论文 cohort 上，满足 major omission 的预设 non-inferiority 标准。
- major overcritique 从 **15.5% 降至 8.1%**。
- major omission 的单侧上界为 **9.9%**。
- **52.4%** 的论文上能够停止。
- 等算力控制、受控样本对和消融表明收益来自 revision，而非更多推理或更短输出。

## 证据质量与局限

- **质量：中高。** 有冻结 cohort、预设标准、双风险指标与等算力控制。
- 任务是论文审稿，不是 Agent 环境；“证据”多为文本局部证据，缺少可执行状态。
- omission 上界不等于对所有错误类型的召回保证。
- corpus 发布链接在公开页未明确给出，复现可用性需后续核实。

## 最接近的相关工作

与 MuseCritic、AutoSciRub、LLM Judge 的遗漏盲区、ClaimReceipt 和 SARA 最接近；共同主题是把整体判断拆成可证据化子项，并区分漏报、误报与不确定。

## 如何复用或推进 LLM-as-a-Verifier

- 把 Agent critique state 表示为 `{claim, cited_steps, expected_effect, evidence_status, severity}`。
- teacher 先 resolve 现有 critique，再搜索新错误；避免每轮只追加批评导致状态膨胀。
- 输出 ordinal concern distribution 和 stop/continue/defer，而不是单一 reward。
- 对可执行 claim 运行环境检查；无证据项降权或 defer，不能直接形成负标签。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏已处置 concern 的分布，未处置 critique 不进入强监督。
- **A/B/T 与序数分布**：按 concern 严重度与证据状态聚合；遗漏风险与 overcritique 风险分别校准。
- **真值门控**：环境证据可否决无支持批评，也可补充 Judge 遗漏。
- **critique states**：采用 revise-before-search，并对每条 critique 保留 provenance。
- **高熵探索**：defer 状态触发额外分支/工具验证，而非立即收敛。
- **sealed eval**：冻结错误清单与证据 adjudication，避免训练 critique 生成器和评价器共享同一遗漏模式。