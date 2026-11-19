# Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates

- **作者**：Jiapeng Pei、Yuhang Yao、Sitan Liu、Hanxin Chen、Hao Li、Guogeng Li、Jiapei Liu、Ruijie Chen、Hongshan Lin、Yang Mo、Tianyu Shi、Shangding Gu
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.23651
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.23651；DOI: 10.48550/arXiv.2611.23651

## 一句话结论

【论文原文】个人 Agent 的自我更新应经过“新旧版本对照、失败复跑、临时回滚、修复确认与拒绝默认”闭环，而不是让单次 Judge 通过后直接写入长期指令。

## 真正新增的内容

【论文原文】为 Kicker 个人健康助手构建 prompt-only RSI 的 update-evaluation component：固定模型权重与运行时代码，候选指令只有在可执行安全与任务测试均通过后才采用；否则保留当前版本。基准覆盖邮件、日历、健康、市场、授权复用、记忆与 tool-output injection。

## 核心方法

1. 对候选与当前指令做配对测试，并重复失败 case。
2. 暂时撤销更新以定位回归，用失败证据指导修复。
3. 修复后重新跑安全与任务性能；无版本通过则 fail closed。
4. 用独立 runtime probes 检查记忆删除与 OAuth scope 等环境权限。

## 关键实验结果

【论文原文】29 个可执行 case、3 个模型、2 个故意危险编辑中拒绝 21 次更新里的 20 次。一次获准的 GPT-5.6 Luna 修复把攻击违规从 10.7% 降至 0%，安全任务完成从 89.7% 升至 100%。更强攻击下，跨模型修复使违规从 69.0% 降至 17.9%，安全完成从 19.5% 升至 64.4%，仍未完全修复。

## 证据质量与局限

【论文原文】有真实工具域、恶意更新、回滚和跨模型转移；但只有 29 个 case、两类风险编辑，且改动限于 prompt。一次评测 snapshot 仍遗漏本地 OAuth scope，说明 benchmark pass 不能证明全局安全。

## 最接近的相关工作

接近 verified memory/skill update、SkillAA、RSIAgent、proof-carrying cognition、authorization monitor 与 continual Agent self-improvement。差异是把版本回滚和修复确认纳入可执行发布门。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将 Agent 的 critique、memory 或 skill 更新视为待发布 artifact：teacher 生成候选修复，程序化 suite 与独立 verifier 共同决定 accept/reject；版本差分和回滚结果形成高价值 A/B/T 蒸馏样本。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏“候选更新相对当前版本”的安全与效用差分，而非绝对总分。
- **pairwise A/B/T 与序数分布**：新旧版本配对；安全改善但效用下降时保留多轴分布或 T。
- **程序化/环境真值门控**：授权、记忆和注入 probe 为硬门；Judge 不得覆盖明确违规。
- **student-generated critique states**：critique/修复只有在回滚对照与复跑确认后才准入长期记忆。
- **高熵分叉探索**：对跨模型转移失败和权限边界状态保留多修复分支。
- **sealed eval**：隐藏攻击、权限 scope 与版本回归集冻结，防止更新生成器和 evaluator 共同适配公开 case。
