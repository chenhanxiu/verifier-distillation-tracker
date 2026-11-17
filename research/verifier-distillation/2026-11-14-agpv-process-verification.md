# Agent-Guided Process Verification for Mathematical Self-Correction

- **作者**：Rui Zou、Mengqi Wei、Xin Zhao、Ji-Rong Wen
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19122
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.19122；DOI: 10.48550/arXiv.2611.19122

## 一句话结论

【论文原文】AGPV 将解答拆成有序关键 claim，逐条调用共享数学工具验证并在首错处停止，再用证据化诊断驱动后续重推，平均准确率从最佳基线 50.3% 提升到 63.8%。

## 真正新增的内容

【论文原文】方法同时处理局部错误定位与完整性：验证 agent 检查关键 claim，summarization agent 把失败证据压成诊断，correction agent 从首错后重推，并根据修订解动态调整下一轮验证。作者还在 claim 覆盖充分、局部验证可靠条件下证明全通过意味着正确且完整。

【分析推断】这是 generative verifier 的“证据—首错—修复”闭环，可直接迁移到长 Agent 轨迹；关键是 claim coverage 必须由独立机制检查，否则 verifier 可能通过遗漏义务获得虚假全通过。

## 核心方法

1. 将当前解答分解为有序关键 claim。
2. 逐条验证并按需调用共享工具，检测首错即停止。
3. 汇总失败证据，指导从首错处重推，并另行检查 completeness。

## 关键实验结果

【论文原文】在 5 个困难数学推理数据集、DeepSeek/Qwen/GPT 的 4 个模型上平均准确率 63.8%，比最强代表性基线 50.3% 高 13.5 个百分点；repair coverage 也高于程序验证基线。实现还压缩长上下文并复用成功工具结果。

## 证据质量与局限

【论文原文】覆盖多数据集、多模型、过程/结果基线，并给出条件性正确性与完整性保证。

【分析推断】保证依赖 claim 覆盖和局部 verifier 可靠，实际最难部分正是这两个前提；数学工具结果比开放式 Agent 环境更干净。需测试工具错误、缺失 claim 和真实副作用环境。

## 最接近的相关工作

最接近 FLARE、PaperDoctor、STRIDE、Beyond Solver Verdicts 与 CoVer。AGPV 的区别是显式首错停止、动态修订验证和 completeness 检查。

## 如何复用或推进 LLM-as-a-Verifier

把 Agent trajectory 分解为状态变更、前置条件、工具结果和未完成义务；逐条验证并在首错处生成带证据指针的 critique。轻量 student 蒸馏首错位置与诊断分布，硬结算仍由工具/环境完成。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：按首错前后分段，正确前缀保留、错误后缀停止蒸馏。
- **pairwise A/B/T 与序数分布**：比较修复前后同一 claim；工具无法判定时标 T。
- **环境真值门控**：共享工具和执行断言负责 claim verdict。
- **student-generated critique states**：只接纳引用首错证据且通过 completeness 检查的诊断。
- **高熵探索**：首错前保留多路径；修复后从失败点重新分叉而非整轨迹模仿。
- **sealed eval**：隐藏 claim coverage oracle、工具变体和遗漏义务，防止 verifier 学会只检查易项。

