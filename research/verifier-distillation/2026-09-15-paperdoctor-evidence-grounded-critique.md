# PaperDoctor: Evidence-Grounded and Actionable Feedback for Scientific Papers in Progress

## 基本信息
- **作者**：Kevin Qinghong Lin；Siyuan Hu；Pan Lu；Yu Chen；Yanzhe Chen；Owen Queen；Yupeng Chen；Jialin Yu；Junchi Yu；Zifeng Ding；Yuanfeng Ji；Sheng Liu；Jindong Gu；Linjie Li；Mike Zheng Shou；Philip Torr；James Zou
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16995
- **代码**：https://github.com/QinghongLin/paperdoctor
- **项目页**：https://paperdoctor.github.io/

## 一句话结论
【论文原文】PaperDoctor 把自动评审从总分 Judge 改成分层诊断：表层筛查、按 claim 类型路由 verifier、按重要性重现实验；每条 critique 必须包含观察、证据指针和修改建议。

## 真正新增的内容
【论文原文】三层系统覆盖写作、版式、引用、代码、理论、相关工作和实验。L2 将不同 claim 路由到对应证据，L3 在计算预算下选择性重建并运行实验，揭示只读论文无法发现的复现问题。

【分析推断】它提供了 student-generated critique state 的可操作 schema：critique 不只是自然语言理由，而是可执行、可定位、可复核的结构化状态。

## 核心方法
1. L1 做低成本表层筛查。
2. L2 typed verifiers 按 claim 类型选择论文、代码、公式或引用证据。
3. 每个 finding 记录 observation、精确 evidence pointer、revision suggestion。
4. L3 按 claim 重要性与预算选择性重现实验。
5. 将诊断而非单一 verdict 呈现给作者。

## 关键实验结果
【论文原文】在 30 篇进行中的论文上获得 70.6% agreement，并得到全部正向整体评价；另在 40 篇跨机器学习、自然科学、社会科学且含人类/AI 作者与代码的稿件上评估。作者报告其反馈比人类和其他 agent reviewer 更可审计，并覆盖部分人类易遗漏维度。

【证据边界】70.6% agreement 不是完整正确率，也未证明自动修订后论文质量或真实复现成功率提升；“更可审计”部分来自输出格式设计。

## 证据质量与局限
- 多领域、含真实 in-progress papers 和执行重现，生态有效性较好。
- 样本规模仍有限，复杂实验复现受环境和预算影响。
- reviewer、reproducer 与最终评价若共享模型可能共适应；错误证据指针会让 critique 显得可信。

## 最接近的相关工作
AutoSciRub、ClaimReceipt、ProofJudge、EquiReview-R、Continual Search RCA 和 student-generated critique/refinement。区别是 typed verifier + prioritized reproducer + 强制证据指针。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】把 Agent 轨迹 claim 分为目标状态、工具执行、权限、安全、效率和用户承诺，分别路由到环境 oracle、日志检查器或 LLM Judge。所有 critique 输出统一为“观察—证据—反事实修复—验证测试”。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：先产生 typed diagnosis，再将可验证 finding 映射为分维 score。
- A/B/T：以修复前后轨迹作 A/B；证据不足或两者均通过测试时 Tie。
- 环境真值：高重要 claim 必须触发重放/工具复现，语言证据不能覆盖执行失败。
- critique states：只蒸馏带 evidence pointer 和可执行 test 的 critique。
- 探索：对多个可行修复保留并行候选，由复现结果筛选。
- sealed eval：训练诊断器与最终复现环境隔离，报告 critique precision、coverage 和修复后成功率。