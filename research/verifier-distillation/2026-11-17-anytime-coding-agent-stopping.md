# Done, But Still Working: Anytime Evaluation of When Coding Agents Should Stop

- **作者**：Zerui Yang、Quan Xue、Miaomiao Dong、Chaorui Zhang、Xuanyu Zheng、Xiyuan Wang、Haolin Ruan、Xueyan Niu、Guangcheng Song、Weixi Zhang、Wei Han、Bo Bai
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22901
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22901；DOI: 10.48550/arXiv.2611.22901

## 一句话结论

【论文原文】何时停止是独立的长轨迹 verifier 问题：相同 patch 连续两次通过可节省成本，但论文没有证明质量非劣，说明“完成概率”必须与“继续工作风险”一起建模。

## 真正新增的内容

【论文原文】提出 anytime evaluation：重放已记录 run 的中间 patch，用隐藏测试逐步评分，在不生成新轨迹的前提下配对比较 stopping/select-earlier policies；并将规则蒸馏进 Agent，评估成本与质量。

## 核心方法

1. 回放中间状态和 patch，以 hidden tests 建立每步真实质量曲线。
2. 分析规则触发率、触发后 patch 是否变化，以及变化是修复还是破坏。
3. 比较 hindsight oracle、可执行 stopping rule 与 imitation-finetuned Agent。
4. 只在 replay 保留相关状态时允许配对因果解释。

## 关键实验结果

【论文原文】约 6,000 个 run、8 个开放模型、2 个 scaffold、SWE-bench Verified。自测通过点可实现的 hindsight saving 随模型/scaffold 从不足 1% 到 57%。同一 patch 连续通过两次的规则在预注册复现实验中节省 23%，但未通过预注册质量非劣检验；模仿该规则微调后六个 seed 平均节省 30%，质量保持仍不确定。

## 证据质量与局限

【论文原文】有大规模 run、预注册复制、配对 replay 和明确负结论；但只覆盖 stopping/select-earlier policy，replay state preservation 是关键假设。SWE-bench hidden tests 仍只是任务 verifier，无法覆盖部署副作用；未证明节省与质量同时成立。

## 最接近的相关工作

接近 early-exit、adaptive computation、coding-agent completion detection、test-time scaling、trajectory pruning 与 process reward/credit assignment。差异是把停止时间作为可回放、逐时刻评估的决策问题。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】训练 distributional stop verifier 输出 `P(done)`, `P(next change repairs)`, `P(next change breaks)`, `expected remaining cost`，并以 hidden environment replay 作 teacher。student 不只学习“当前是否通过”，而学习继续行动的反事实价值。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将停止策略作为独立 head，蒸馏未来 patch 质量分布而非当前 pass/fail。
- **pairwise A/B/T 与序数分布**：比较 stop-now 与 continue；差异落在非劣区间内标 T，而非强行偏好更短轨迹。
- **程序化/环境真值门控**：hidden tests 决定终局方向；自测只作可观测 teacher feature，不能独立授权停止。
- **student-generated critique states**：critique 后继续工作是否修复/破坏要由后续重放标注，避免把“继续思考”默认当正样本。
- **高熵分叉探索**：在 stop/continue 价值接近或未来变化方差大时保留双分支采样。
- **sealed eval**：用未见 issue、隐藏测试和冻结 scaffold 做质量非劣检验；成本节省不得替代质量证据。
