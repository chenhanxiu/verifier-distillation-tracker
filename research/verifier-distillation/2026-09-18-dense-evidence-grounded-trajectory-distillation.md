# DENSE：把无结果标签的 Agent 轨迹蒸馏为证据化捷径树

- 论文标题：DENSE: Distilling Agent Trajectories into Evidence-Grounded Shortcut Trees for Self-Refinement
- 作者：Siyuan Liu；Fan Yu；Dongyu Ru；Yizhu Liu；Yifan Yang；Xuezhi Cao；Xunliang Cai；Yixin Cao
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21423
- DOI：https://doi.org/10.48550/arXiv.2609.21423
- 代码：v1 提供匿名 supplementary package，但未给出持久公开代码 URL

## 一句话结论

DENSE 表明即使拿不到 post-hoc 成败标签，也能从局部进展、恢复证据与未完成义务中提炼可复用 critique state，并在重置后的 Terminal-Bench 任务上同时提高成功率、降低执行 token。

## 真正新增的内容

- 【论文原文】把长轨迹组织成 nested shortcut tree：压缩重复尝试，保留恢复证据，把已完成局部分支与仍未满足的父级义务显式连接。
- 【论文原文】提出 REFIT：所有反馈方法共享同一初始轨迹，生成反馈时看不到 post-hoc outcome；随后重置环境和模型上下文，以新执行的成功率衡量反馈的真实效用。
- 【论文原文】强调“历史上完成过”不等于当前环境已经完成，避免 critique/memory 把旧状态误当成当前事实。
- 【分析推断】这比直接保存整段反思更接近可审计的 student-generated critique state：每条建议都绑定来源证据、作用域和剩余义务。

## 核心方法

DENSE 先把轨迹按嵌套子任务分解，识别局部成功、失败探索和恢复动作；随后建立可复用 shortcut，跨层 reconcile 冲突，把完成分支摘要化、未解决分支展开化。REFIT 将这些结构化反馈输入到全新执行中，并与 task-prior、raw trajectory、all-at-once、step-by-step 和 privileged verifier feedback 等条件做 source-paired 比较。

## 关键实验结果

- 【论文原文】在 Terminal-Bench 2.1、四个 recipient model 上，DENSE 相对首次执行的 strict pass 提升 7.12–15.64 个百分点。
- 【论文原文】recipient 观察到的执行 token 分别下降 19.0%、20.0%、43.6%、23.7%。
- 【论文原文】GPT-5.5 上，strict pass 从 68.54% 提升到 75.66%，执行 token 从 319.1K 降到 179.9K；去掉 shortcut/reconciliation 或层级结构后均退化。
- 【论文原文】主实验和消融合计 7,842 次执行，主结果按 3 次重复和等任务权重汇总。

## 证据质量与局限

- 【论文原文】有共享源轨迹、环境重置、上下文重置、privileged-feedback 对照和组件消融，能较好隔离“反馈内容”而非额外尝试带来的收益。
- 【论文原文】只在 Terminal-Bench 2.1 验证；raw trajectories、实际反馈文件和 verifier logs 未包含在匿名包中，外部复核仍有限。
- 【分析推断】REFIT 是很强的反馈效用评测，但不是完全 sealed：反馈生成器、recipient 与 benchmark 分布仍可能共享先验；也没有直接证明提炼出的每条 critique 在跨任务、跨环境时都保持正确。
- 【分析推断】没有 outcome label 是工程优势，不应被解释为“无需环境真值”；高风险记忆的最终准入仍应由可执行检查或隐藏验收门控。

## 最接近的相关工作

最接近 Reflexion 类轨迹反思、ExpeL/经验检索、verified retry、process evaluation 和 critique utility evaluation。与 RSIAgent、Grounding Agent Memory、PaperDoctor 的共同点是证据化记忆；DENSE 的新增点是 outcome-blind、source-paired、reset 后测效用的协议。

## 如何复用或推进 LLM-as-a-Verifier

可把 verifier 输出从单一 0–3 分扩展为结构化状态：已验证完成项、局部证据指针、失败但有信息的尝试、恢复路径、剩余义务、作用域/时效。Judge 不只评价 critique 是否“看起来合理”，还要在重置环境中测它是否提高下一次执行的成功率，形成 critique utility 标签。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：把 reset rerun 的增益作为 critique teacher 的校准信号；没有可重放条件时仅作低权重软监督。
- pairwise A/B/T：对同一源轨迹生成多种 critique，让相同 recipient 在重置环境中 A/B；差异落入噪声区间时标 T。
- 真值门控：记忆中的“完成”必须带环境快照和作用域；跨 run 只能迁移过程，不能迁移完成状态。
- student-generated critique states：直接采用“证据—局部结论—恢复动作—剩余义务”的 schema，拒绝无证据的全局结论。
- 高熵探索：保留失败分支中已发现的有效证据和可恢复路径，而不是只保存最终成功轨迹。
- sealed eval：固定 source trajectory 后，冻结并重置环境、recipient 上下文和评测器；训练 feedback generator 不得看到 rerun 的隐藏终局结果。
