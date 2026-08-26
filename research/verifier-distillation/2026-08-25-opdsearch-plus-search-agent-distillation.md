# OPDSearch+: On-Policy Distillation with RL Refinement for Search-Augmented Reasoning

## 基本信息

- 作者：Qinglin Ye、Zhiyuan Gu、Jingjie Xia、Yiheng Zhang、Kaiyan Zhao、Shunchao Zheng、Yuhang Mu、Wenchao Du、Yiming Wang
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24310
- 原始论文：https://arxiv.org/abs/2608.24310
- DOI：https://doi.org/10.48550/arXiv.2608.24310
- 代码：论文公开页未提供

## 一句话结论

OPDSearch+ 先让 student 在真实动态检索响应上接受冻结通用 teacher 的 per-position forward-KL 蒸馏，再用 RL 突破 teacher 上限；3B 模型在 HotpotQA 和 2WikiMultihopQA 分别提升 13.1% 和 8.5%。

## 真正新增的内容

**论文原文结论：** 无需任务专用 teacher 微调，通过“OPD 重塑可探索策略分布 + 后续 RL refinement”训练搜索增强小模型；teacher 的作用是构造更好的 RL 起点，而非给出最终能力上限。

**分析推断：** 对 Agent OPD 而言，动态工具返回必须在 student 的真实 on-policy 状态中生成；静态 teacher 轨迹或离线 SFT 无法覆盖相同的工具条件分布。

## 核心方法

阶段一由 student 与 live search engine 交互，冻结 instruct teacher 在相同 prefix 上提供 per-position forward-KL；阶段二用任务奖励做 RL，从被重塑的策略分布继续优化证据搜索与整合。

## 关键实验结果

跨七个 QA benchmark，3B OPDSearch+ 持续优于既有 3B RL baseline；HotpotQA 提升 13.1%，2WikiMultihopQA 提升 8.5%。摘要未给出全部绝对分数、搜索成本与统计区间。

## 证据质量与局限

证据质量中等：跨七个 benchmark 且是动态搜索设置，但论文仅 9 页、暂无代码链接；不能从摘要确认检索器版本、搜索预算是否完全匹配，也未隔离 teacher 蒸馏与额外交互数据的贡献。

## 最接近的相关工作

最接近 SOPD、MERA、SimpleOPD 与搜索 Agent 的 RLVR；区别在于把 off-the-shelf teacher 当作策略分布预调器，再由 RL 超越其表现。

## 如何复用或推进 LLM-as-a-Verifier

在检索 Agent 中增加证据 verifier：先程序化检查引用可访问性和证据覆盖，再让 Judge 评价证据—结论一致性；其分数用于第二阶段 RL，并校准第一阶段 teacher 信号。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** student 必须在当前工具响应上采样，teacher 只评价同一 prefix。
- **A/B/T：** 比较不同查询、检索结果和证据整合分支，而不是只比较最终答案。
- **真值门控：** URL/文档可访问性、引用覆盖与答案可验证项构成硬 gate。
- **Student critique states：** 从检索失败、证据冲突和错误归因生成局部 critique。
- **高熵探索：** OPD 只负责提供可行搜索起点，RL 继续探索超越 teacher 的路径。
- **Sealed eval：** 固定隐藏语料快照或独立搜索环境，防止检索内容漂移和 evaluator 共适应。
