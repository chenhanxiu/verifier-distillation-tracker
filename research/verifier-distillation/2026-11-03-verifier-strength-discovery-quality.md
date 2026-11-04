# Verifier strength does not buy discovery quality

## 基本信息

- **完整标题**：Verifier strength does not buy discovery quality: a pre-registered two-domain test of LLM-based automated research, with post-hoc evidence pointing to proposer-pool composition
- **作者**：Peter Chen, Ni Zhang, Siyuan Zhang
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.04420
- **DOI**：https://doi.org/10.48550/arXiv.2611.04420
- **实验材料/脚本**：https://doi.org/10.5281/zenodo.23308866

## 一句话结论

预注册双领域实验发现，更严格、更强的 verifier 虽然能通过 mutation battery，却没有带来更好的自动发现；扩大 proposer 候选池反而比收紧 gate 更有效。

## 真正新增的内容

**论文原文结论**：作者直接检验“verifier 越强，discovery 越好”的隐含假设，并给出否定证据；同时显示 proposer-pool composition 可能是更重要的杠杆。

**分析推断**：这对高熵分叉下的 verifier 蒸馏是关键反例：更精准的 gate 若作用在同质、贫乏候选池上，只会更自信地筛选有限模式，甚至降低探索价值。

## 核心方法

- 两个真实数据领域：job-shop scheduling 与基于 Beijing T-Drive 的 vehicular edge offloading。
- 每个领域 100 对匹配的 LLM/random proposals。
- 三档 verifier，配套 429-case mutation battery 验证强度操纵确实成立。
- 预注册主分析，并另做明确标记的 post-hoc union-pool 分析。

## 关键实验结果

- verifier 强度随 tier 提升，但 LLM 相对 random 的优势没有随之扩大：领域 A 单侧 p=0.1115，领域 D p=0.9994。
- 严格 tier 在领域 D 的 margin contrast 为 **-0.040，p=0.0013**。
- 两个较低 gate 在 100/100 与 99/100 对中选出相同候选，限制了 tier 顺序检验。
- union pool 在领域 A 增加 **+1.52 holdout-value units**（Wilcoxon n=100，p=0.0002）。

## 证据质量与局限

预注册、匹配对照、两个领域、mutation battery 与公开账本使证据质量较高。局限是 union-pool 结论为 post-hoc；只有两个优化领域，且 verifier tier 的选择重合导致部分假设不可检验。不能外推为“强 verifier 无用”。

## 最接近的相关工作

与 best-of-N、LLM proposer–verifier pipeline、reward-guided search、Goodhart 审计和高熵分叉最接近。它补充了只优化 verifier AUROC/准确率而不测最终发现价值的研究。

## 如何复用或推进 LLM-as-a-Verifier

评估 verifier 时必须同时测候选池多样性、最终 holdout value 与 gate 的边际贡献。可把 distributional verifier 用于预算分配：分歧大时扩充 proposer，而不是简单提高阈值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：除 verifier 指标外，报告下游发现/成功率随候选池规模的曲线。
- **A/B/T/序数分布**：T 应触发更多分叉或异构 proposer，而不是被当作丢弃。
- **程序真值门控**：最终结论仍由 holdout 环境真值结算，verifier 只做路由。
- **critique states**：比较“改进同一候选”与“生成新候选”的预算收益。
- **高熵分叉**：把保留探索列为一等目标，审计 gate 是否造成 mode collapse。
- **sealed eval**：使用未暴露的 holdout objective，避免 verifier 与搜索器共同优化可见指标。
