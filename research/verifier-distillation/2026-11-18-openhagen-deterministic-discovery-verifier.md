# Openhagen Worlds: Calibrated Environments for Measuring and Training Scientific Discovery Agents

- **作者**：Alexander Boesgaard Lorup
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.24711
- **托管评测**：https://eval.openhagen.ai
- **代码链接**：未发现完整公开代码；论文提供 48 个开发样例及 scripted-oracle ancillary files
- **标识符**：arXiv:2611.24711；DOI: 10.48550/arXiv.2611.24711

## 一句话结论

【论文原文】Openhagen Worlds 用隐藏真值、确定性 verifier、显式评分规则和 oracle/shortcut 校准，构造最多八阶段以上的科学发现任务，为长时程 Agent 的 sealed RLVR 与探索评估提供高质量环境。

## 真正新增的内容

【论文原文】发布 27 个程序生成 world、178 个校准难度级别；每个观察明确评分规则，任务只有在 scripted oracle、非演绎策略和 shortcut policy 满足预设成功区间后才入选。92 个 core level 适合小模型训练，86 个 frontier rung 扩展到多阶段 campaign。

## 核心方法

1. Agent 在预算内选择实验，并对隐藏系统提交答案。
2. 确定性 verifier 对 finite truth space 或 simulator-grounded truth 评分。
3. 每级使用 64 个开发实例做 oracle、非演绎和 shortcut gate 校准。
4. withheld frontier 与 core hosted service 分离；提供 scripted-oracle 开发轨迹。

## 关键实验结果

【论文原文】84 个 withheld frontier instance 上，DeepSeek V4.1 Flash 默认推理强度解出 32 个，最大推理强度解出 57 个，oracle 为 79；最大 headroom 出现在八阶段 campaign。On-policy expert iteration 使 9B 模型在已训练 family 的 core success 从 0.090 升到 0.148，部分收益来自动作格式，GPQA Diamond 未检测到下降。

## 证据质量与局限

【论文原文】隐藏真值、确定性评分、shortcut gate 和 withheld frontier 提供强评测设计；但单作者，公开样本只有 48 个，9B 训练收益较小且部分是格式改善。模拟科学 world 与真实实验室之间仍有外部有效性差距。

## 最接近的相关工作

接近 RLVR environments、AutoGym、CrossEnv、scientific discovery agents、procedural generation 与 GameLogicBench。关键差异是对每个难度级别显式校准 oracle 与 shortcut headroom。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把每次实验选择、信息增益、阶段承诺和终局隐藏真值转成 distributional process verifier 标签；teacher 用 oracle trajectory 与确定性终局共同监督，student 在 on-policy 高熵实验分叉上学习何时继续探索或提交。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：终局确定性 verifier 定方向，oracle/信息增益仅分配局部幅度。
- **pairwise A/B/T 与序数分布**：从同一 belief state 比较不同实验；等信息增益或多条可行实验标 T。
- **程序化/环境真值门控**：隐藏 truth 与预算约束为硬门，不允许 Judge 覆盖。
- **student-generated critique states**：critique 需说明当前证据排除了哪些 hypothesis，并由 truth-space 计算验证。
- **高熵分叉探索**：八阶段 campaign 是核心压力测试；避免用短期 reward 淘汰高信息但未立即得分的实验。
- **sealed eval**：保留未见 world/rung、隐藏 seeds 和 shortcut gate；训练 oracle 与 hosted evaluator 版本隔离。
