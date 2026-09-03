# ToolGate：工具依赖评测题的可执行验收流水线

## 基本信息

- **论文标题**：ToolGate: An Executable Acceptance Pipeline for Tool-Dependent Scientific Benchmark Construction
- **作者**：Ke Zhang, Yankang Liu, Roya Zandi, Maziar Raissi
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **arXiv**：[2609.02067](https://arxiv.org/abs/2609.02067)
- **DOI**：[10.48550/arXiv.2609.02067](https://doi.org/10.48550/arXiv.2609.02067)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

ToolGate 将 LLM 生成题一律视为 proposal，必须依次通过可执行答案复现、随机无工具排除和限时工具 Agent 求解三道门，提供了构建程序真值 Agent 数据的清晰准入模板。

## 真正新增的内容

**论文原文结论**：科学 benchmark 的瓶颈不是生成候选，而是决定哪些候选有效、非平凡且能被工具 Agent 实际解决。ToolGate 要求脚本在专业软件中复现答案；多次无工具模型不能从 prompt 直接答出；工具 Agent 在固定预算内必须能解决。最后仍保留领域设计和专家复核。

新增之处是把 validity、non-triviality 与 solvability 分成可审计的串联 gate，并在生成结束后重新筛查，避免生成过程中的筛选配置污染最终报告。

## 核心方法

在 FEniCSx 科学计算环境中生成任务、答案与脚本。第一门本地执行并精确核验；第二门以随机无工具采样排除可猜题；第三门用具备 FEniCSx 的 coding Agent 在时限内求解。最终做精确去重并记录每道门的留存数。

## 关键实验结果

**论文报告**：500 次生成尝试中，本地验证保留 478 条；生成完成后两轮随机无工具复筛排除 222 条，GPT-5.5 medium API 再排除 121 条；剩余 135 条中，GPT-5.5 Codex CLI 工具 Agent 解出 130 条，精确去重后得到 128 个 protocol survivor。结果说明多数可执行候选仍可能过于容易，不能只靠答案复现验收。

## 证据质量与局限

每个阶段有明确计数、执行结果和审计路径，证据清晰，但仅实例化于 FEniCSx、规模 500，且“模型无工具答不出”依赖所选模型与采样预算。第三门要求强 Agent 能解会排除真正困难但有效的题；程序脚本正确也不保证科学问题表述无歧义。尚未公开代码链接。

## 最接近的相关工作

接近 FACET、SPADE、AgentMercury、EnvHarness、ExecRubrics、PaperGym 与 verifier-based data filtering。相较只让 LLM Judge 审题，ToolGate 用执行和对照条件决定准入；相较普通可验证奖励，它还检查题是否确实需要工具。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：可把用户的 Mock Tool case 构建改成类似三门：状态/答案可执行一致；无工具或错误工具路线不能轻易通过；目标 Agent 在预算内存在至少一条成功轨迹。生成式 verifier 负责提出 rubric/case，程序 gate 负责接纳；被拒样本及原因可训练 verifier 的 critique 与 abstention。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：只在通过 validity/non-triviality/solvability 的 case 上蒸馏 verifier 分数。
- **A/B/T 与序数分布**：对有工具、无工具和错误工具三类轨迹构造 A/B/T，保留难度不确定性。
- **真值门控**：执行脚本和状态一致性是最高优先级 teacher；LLM Judge 不可覆盖失败。
- **critique states**：student 解释候选为何无效/平凡/不可解，再由对应 gate 验证。
- **高熵探索**：第三门确认“至少有可行路径”，但训练时仍保留多种成功工具路线。
- **sealed eval**：生成后使用更强且独立的无工具复筛，并冻结最终题池及验证脚本。