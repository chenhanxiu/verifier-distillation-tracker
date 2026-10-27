# Continual Learning Exam：长时程经验学习与反馈修订评测

## 基本信息

- **论文标题**：Continual Learning Exam: Benchmarking Long-Horizon RSI and Experiential Learning in LLM Agents
- **作者**：Haoyu Zhao, Sitian Tu, Yuxuan Huang, Huichi Zhou, Zhangyue Yin, Jiahao Huang, Jingyuan Xu, Tianmiao Shi, Jin Shi, Nianxi Zhang, Yangmiao Zhang, Zhuolang Chan, Huiyan Hu, Chenchao Sheng, Yaqing Luo, Yue Chen, Huaxiu Yao, Meng Fang, Jun Wang
- **首次公开日期**：2026-10-25
- **版本日期**：2026-10-25（v1）
- **论文链接**：https://arxiv.org/abs/2610.33956
- **项目页面**：https://haoyu-zhao.github.io/CLE/index.html
- **代码链接**：项目页未明确提供独立代码仓库

## 一句话结论

CLE 用跨五级任务梯子的持续经验积累来评价 Agent，而不是把每个任务独立计分；一次诊断反馈加修订能提高完成率，但前沿系统仍难稳定完成整条梯子。

## 真正新增的内容

**论文原文结论**：120 个专家编写任务各含五个递进 level，共 600 level、89 个职业角色和 12 个领域；只有通过当前 level 才能解锁下一层，后续任务要求利用此前经验。evaluation agent 按人工 rubric 评分，并比较无反馈与失败后一次诊断反馈+修订。

**分析推断**：它为 student-generated critique states 提供比单题“改一次答案”更严格的验收：反馈价值应在后续 level 持续体现，同时不能破坏已学能力；这适合测 verifier critique 的跨任务可迁移性和遗忘。

## 核心方法

- 任务按五级依赖结构排列。
- Agent 在前级任务中积累经验并应用到后级。
- 人工 rubric 约束 evaluation agent。
- 比较 single submission 与 diagnostic-feedback/revision 设置。
- 在 17 个 harness-model 配置上评测。

## 关键实验结果

**论文报告**：反馈与一次修订带来 5.3 个百分点的中位完成率提升；最佳系统只通过 47.7% 的 level，完整完成五级任务的比例仅 23.3%。

## 证据质量与局限

规模、领域和 harness 覆盖较好，任务由 50 多位专家开发。局限是 evaluation agent 仍可能继承 Judge 偏差；摘要没有说明独立人工复核比例、评分一致性或 rubric 泄漏控制，不能把 5.3 点全部归因于 critique 质量。

## 最接近的相关工作

RSIAgent、Self-Direction、SkillAA、AtomSD、DENSE，以及长时程 RCA/continual learning benchmark。CLE 的重点是跨级经验收益而非单条轨迹成功。

## 如何复用或推进 LLM-as-a-Verifier

用同一任务梯子分别训练 outcome verifier、critique generator 和 critique admission gate；评估指标同时报告即时修订收益、后续 level transfer、遗忘率和错误经验传播率。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：以跨 level 的后续增益校准 critique/score，而非只看当前题。
- **A/B/T**：比较使用与不使用某条经验的后续轨迹；效果区间重叠时 T。
- **硬真值门控**：尽可能用可执行产物和状态检查覆盖 rubric Judge。
- **critique states**：只有跨 level 持续有益且无明显遗忘的 critique 才进入长期记忆。
- **高熵探索**：同一经验允许多个应用路径，避免把单次修订固化成唯一策略。
- **sealed eval**：隐藏后续 level 与 transfer 任务，隔离 evaluation agent 和训练反馈。