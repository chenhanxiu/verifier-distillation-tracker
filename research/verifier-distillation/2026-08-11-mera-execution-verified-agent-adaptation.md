# MERA：执行真值驱动的 Agent 模型演化与技能适配

## 基本信息

- **论文标题**：MERA: Model Evolution and Routing with Skill Adaptation for Agentic Systems at Scale
- **作者**：Yuhang Yao, Zeyu Wang, Wanyi Chen, Tongyun Yang, Yuhang Han, Jie Xiao, Chengke Bao, Tianyi Zhao, Lynn Ai, Eric Yang, Tianyu Shi
- **首次公开日期**：2026-08-11
- **当前版本日期**：2026-08-11（v1）
- **arXiv ID**：2608.10333
- **原始论文**：https://arxiv.org/abs/2608.10333
- **代码**：https://github.com/yh-yao/MERA-Evolve

## 一句话结论

MERA 从失败的 Agent 单次调用中获取 execution-verified teacher demonstrations，反复更新 SkillBook 与 student adapter，并以 verifier-backed fallback 保底；它把“失败状态—真值验证—技能蒸馏—部署门控”串成了可运行闭环。

## 真正新增的内容

**论文原文结论：** MERA 不只把简单调用路由给小模型，而是以单次 model invocation 为适配单元，回放失败调用、获取通过执行器验证的强 teacher 示范、抽取重复程序到 SkillBook，并用 SFT/可选 GRPO 提升 student；新 SkillBook、adapter 或 router 只有在联合 replay 保持质量时才准入。

**分析推断：** 这非常接近 Agent verifier × distillation 的工程版本，但蒸馏对象主要是 policy/skill，而不是显式 verifier score。它可为 score-level OPD 提供训练状态、真值门和部署 admission protocol。

## 核心方法

1. 将完整 traces 规范化为 invocation slices：prompt、局部上下文、工具 schema、输出、verifier 结果、retry、fallback 与 skill assignment。
2. 失败 student invocation 由更强 teacher 重做，只保留 execution-verified demonstrations。
3. 将重复局部结构蒸馏为迭代 SkillBook，并用 hard examples 训练 LoRA student（SFT 或 SFT+GRPO）。
4. router 标签来自 small-model 实际可执行结果；部署后 verifier 检查 cheap route，失败则 fallback 到强模型。
5. 通过 joint replay 决定 SkillBook、adapter、router 是否准入；阈值校准 shard 与 held-out policy evaluation 隔离。

## 关键实验结果

**论文报告：**

- HumanEval+MBPP 使用 546 个训练任务和 582 个 task-ID 不重叠的 held-out tasks，三随机种子。
- Qwen2.5-Coder-1.5B direct pass 从 28.7% 提高到 multi-cycle SFT 44.2%、SFT+GRPO 49.7%。
- verifier fallback 下，MERA 达到 88.3% pass，成本为 always GPT-5.6 Luna 的 60.8%；Always Luna 为 86.9%/100% 成本。
- matched artifacts 上，RouteLLM-style + fallback 为 87.0%/97.4% 成本，FrugalGPT-style cascade 为 85.5%/106.7%。
- TAU-2 严格 35-task split 中，Qwen3.5-2B 从 14/35 提至 18/35，略高于未适配 4B 的 17/35；但 McNemar 单侧 p=0.171875，作者明确称证据不足，只支持工具调用可行性。
- HumanEval/MBPP 使用隔离 Python 执行测试；TAU-2 使用官方 evaluator 的环境状态、必需工具动作和自然语言断言。

## 证据质量与局限

**证据较强处：** task-ID 隔离、三种子代码实验、真实执行 verifier、独立 router calibration、明确区分 direct model gain 与 fallback system gain。

**论文明确或可见的局限：**

- 所有路由标签与准入质量取决于 verifier 覆盖；遗漏语义错误会误放行 skill/cheap route。
- 偏向窄、易验证 invocation，困难长时程推理可能长期留在强模型。
- 主要是 trace replay，不能完全复现 policy 更新后的在线分布漂移。
- TAU-2 只有 35 个任务且统计不显著。
- Skill promotion 假设局部行为可稳定规范化；开放式任务未必成立。
- 系统主要蒸馏 demonstrations/skills，而非 teacher verifier 的不确定性或分数分布。

## 最接近的相关工作

Trace2Skill/agent skill distillation、失败回放与 teacher demonstration、模型级 routing/fallback、RLVR/GRPO、verifier-gated deployment。相比纯 routing，MERA 会实际提升 student；相比 OPSD，其训练数据主要来自 replayed failed invocations 与 verified teacher outputs。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 将 invocation slices 直接作为 on-policy verifier distillation 数据单元，为每个 next action 保存环境前后状态、执行结果和 teacher critique。
- 对 execution verifier 无法覆盖的语义维度，让 teacher 输出序数分布并记录置信度，不与硬真值混成单分。
- 只让通过 replay admission 的 teacher labels/skills进入 student verifier 训练。
- 把 verifier-backed fallback 扩成 verifier disagreement fallback：student 高熵或多 head 冲突时请求强 Judge。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：在 MERA 的失败 invocation slices 上蒸馏 teacher 的动作贡献分布，而不仅训练答案 policy。
- **A/B/T**：同一 slice 回放 student/teacher 或两个候选动作，用官方环境结果形成 A/B/T；两者均过或均失败时保留 tie。
- **真值门控**：直接复用执行测试、环境状态和 required tool actions 作为硬门。
- **Critique states**：失败 slice 与 teacher repair 之间的差异可生成可复用 critique/skill。
- **高熵探索**：fallback 不等于删除 student 分支；保留候选并记录其可恢复性，避免只学习强 teacher 单一路径。
- **Sealed eval**：沿用 disjoint task IDs 与 calibration shard，并进一步让最终 evaluator 独立于 replay admission verifier。

MERA 为你的实验路线提供了最实用的数据闭环骨架：先从失败调用和环境真值开始，再在其上增加序数 verifier 蒸馏与独立 sealed eval。
