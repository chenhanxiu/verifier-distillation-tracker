# DynaWeave: Learning to Adapt through Dynamic Scenario Synthesis

- **作者**：Xuan Yang、Chunxiao Liu、Hongsheng Xin、Hao Xu、Ning Miao
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29443
- **arXiv ID**：2610.29443
- **DOI**：https://doi.org/10.48550/arXiv.2610.29443
- **代码/项目**：https://github.com/Miaow-Lab/DynaWeave

## 一句话结论

DynaWeave 用事件 DAG 和只修改受影响检查项的动态 verifier，把静态 Agent 任务扩展成带外生变化、可执行结算的长轨迹训练环境。

## 真正新增的内容

系统生成需求变化、环境状态变化和外部信息变化，并确保 verifier 随实际发生的事件局部更新，而非重新生成整个 rubric 或继续使用已过期真值。

## 核心方法

以 DAG 表示外生事件依赖，由执行引擎在交互中触发；动态 verifier 保留未受影响的检查，只修订相关约束，据此收集并验证适应性轨迹。

## 关键实验结果

在 36 个环境收集 2,095 条验证轨迹并用于 Qwen3.5 SFT；三个模型规模在 Gaia2、CostBench、ToolMaze 上均提升，其中 CostBench 完成率增加 67.34 个百分点，ToolMaze 上超过 Gemini-3.1-Pro-Preview。

## 证据质量与局限

跨三 benchmark、三规模且有大幅增益；但摘要只报告 SFT，未验证 verifier 蒸馏或 OPD，也未量化动态检查自身的误报漏报。

## 最接近的相关工作

最接近 AutoGym、Ground-truth-as-code Agent Evaluation、DynSTEER、ContrAgent、GameLogicBench 与 StoreBench。

## 如何复用或推进 LLM-as-a-Verifier

用事件 DAG 产生共享前缀后的受控分叉；将“旧计划继续执行、检测变化后调整、无证据过度调整”组成 A/B/T，并以局部更新后的程序检查给方向信号。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】高熵分叉不应只来自模型不确定性，还应来自环境外生事件；可用动态真值决定偏好方向，用 verifier 分布决定幅度。sealed eval 应冻结事件生成器种子和未受影响检查，防止训练过程中悄然重定义成功。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
