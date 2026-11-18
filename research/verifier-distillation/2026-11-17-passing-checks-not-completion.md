# When Passing Checks Do Not Establish Completion: Evidence Interpretation in Coding Agents

- **作者**：Xueping Gao
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22835
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22835；DOI: 10.48550/arXiv.2611.22835

## 一句话结论

【论文原文】检查通过不自动推出任务完成：verifier 还必须保留执行事实、限定证据适用范围并确认所有检查义务确已履行。

## 真正新增的内容

【论文原文】把 coding-agent verification 分解为 fact preservation、scope interpretation 和 obligation discharge，并用 qualified repository checks、受控 evidence consumers 与可执行 workflow 检验“正确事实→有限 verdict”的断裂。

## 核心方法

1. 13-task 前瞻性 factorial study，控制证据消费者与验证条件。
2. held-out receipt-supply study 检查标签、事实报告和授权范围。
3. 118 次修复、31 个任务的 source interventions，分离 startup reachability、实际 repair、witness production 与 claimed operation。
4. lifetime/resource controls 限定一次 passing validation 能支持的结论边界。

## 关键实验结果

【论文原文】正确报告执行事实仍不一定产生请求的有限 verdict。留出研究的 122 个标签全部正确，但 16 个响应错误复述事实，另 11 个越过授权范围。生成 note 能产生局部修复差异，却会给出错误解释；强普通基线、新任务和 skill-transfer 未显示一致总体优势。

## 证据质量与局限

【论文原文】采用前瞻性设计、留出研究和干预，且主动限制“诊断更优”结论；但规模较小、单作者、领域集中于 coding workflows，摘要未给出统一效应量。它主要审计证据解释，不是 verifier 蒸馏算法。

## 最接近的相关工作

接近 evidence-grounded critique、proof-carrying agents、completion certificates、coding-agent test interpretation、scope-aware authorization 与 diagnosability/abstention 研究。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 输出结构化为 `(observed_fact, evidence_pointer, scope, outstanding_obligation, verdict)`；student 只蒸馏在 scope 内、义务闭合的 verdict。若证据只支持局部检查，应输出 T/INCONCLUSIVE，而不是“完成”。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：分开蒸馏事实正确度、适用范围与完成度，禁止用单标量掩盖 scope error。
- **pairwise A/B/T 与序数分布**：两轨迹都缺少完成证据时标 T/不可判，不因一方语言更自信而选 A/B。
- **程序化/环境真值门控**：check exit code 只在其生命周期、资源和覆盖范围内有效；完成判定还需 obligation ledger。
- **student-generated critique states**：critique 必须保留原始执行事实和证据指针，错误解释不得作为新监督。
- **高熵分叉探索**：优先分叉“证据相同但 scope/义务解释不同”的状态，训练 abstention 与补证策略。
- **sealed eval**：隐藏后续义务、证据有效期和授权边界，独立检查 verifier 是否把局部 pass 夸大为全局完成。
