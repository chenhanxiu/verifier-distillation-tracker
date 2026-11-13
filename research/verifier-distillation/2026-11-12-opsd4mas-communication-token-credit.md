# Turning Multi-Agent Communication into Token-Level Credit with On Policy Self Distillation

- **作者**：Zixu Wang、Yu Zhao、Xing Zheng、Bingbing Xu、Tian Xueyun、JiaTang Luo、Weiqiang Wang、Bowen Song、Huawei Shen、Xueqi Cheng
- **首次公开日期**：2026-11-12
- **版本日期**：2026-11-12（v1）
- **原始论文**：https://arxiv.org/abs/2611.16206
- **代码**：https://github.com/Camel-Prince/OPSD4MAS
- **标识符**：arXiv:2611.16206；DOI: 10.48550/arXiv.2611.16206

## 一句话结论

【论文原文】OPSD4MAS 把多 Agent 后续通信中的事实与协作关系转成 token 级 on-policy 自蒸馏信用，并与 GRPO 联合训练，数学任务的 pass@4 相比 GRPO 最多提升 20 个百分点。

## 真正新增的内容

【论文原文】不同于把整段通信压成标量奖励，方法先由外部模型抽取事实并判断其与轨迹的关系，再用 leave-one-out 方式测量这些事实对目标 token 和各 Agent outcome advantage 的影响，最后让带事实条件的策略给出细粒度信用。完整过滤与 frozen-history 注入诊断支持这些事实信号确有作用。

【分析推断】真正与 verifier 蒸馏相关的新增点，是把“通信内容是否有用”从轨迹级 reward 拆成可蒸馏的 token 级方向信号；它比单纯 score-level OPD 更接近长轨迹中的局部信用分配，但外部事实抽取器仍相当于一个未充分校准的 generative verifier。

## 核心方法

1. 从 student 自己生成的多 Agent 轨迹中抽取通信事实，并做轨迹关系粗过滤。
2. 对候选事实做 leave-one-out 细过滤，估计事实对目标 token 及 Agent 级 outcome advantage 的边际影响。
3. 用 fact-conditioned policy 产生 token 级蒸馏信用；与 GRPO 通过线性退火的联合目标优化。

## 关键实验结果

【论文原文】数学任务上，pass@4 相比 GRPO 最多提升 20.00 个百分点；消融支持粗细两级过滤，frozen-history 注入实验支持事实的因果效用。摘要未给出跨域、长时程工具环境或 sealed evaluator 的结果。

## 证据质量与局限

【论文原文】证据包含主结果、过滤消融和历史注入诊断，并已公开代码。

【分析推断】当前证据仍集中在数学协作，尚不能说明通信事实在 AppWorld、SWE 或具真实副作用的环境中同样可靠；外部模型同时抽取并判断事实，可能把自己的偏差蒸馏进 student。需要用程序真值核验事实，并用独立 evaluator 复核，而不能只看训练闭环内 pass@4。

## 最接近的相关工作

最接近的是 MAS-OPD、AgentOPSD、VETTA 与 CREST：前两者把 privileged/on-policy teacher 信号用于多 Agent 或多轮 token 蒸馏，后两者显式协调 turn/token 信用。OPSD4MAS 的区别是把未来通信事实本身变成 token 信用，而不是只依赖 teacher logits 或标量终局回报。

## 如何复用或推进 LLM-as-a-Verifier

可把事实抽取器改造成输出证据指针、关系类型与置信分布的生成式 verifier，再将 leave-one-out 贡献离散为 A/B/T：支持、反对、证据不足。程序化或环境真值用于门控方向，事实 verifier 只决定幅度；对高熵分叉保留多个事实解释，不把单一路径压成确定标签。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“通信事实贡献”分数通道，可与轨迹 verifier score 做分层蒸馏。
- **pairwise A/B/T 与序数分布**：同一状态下对“保留事实/移除事实”构造 A/B；边际影响置信区间跨零时标 T，并保留序数分布。
- **环境真值门控**：只有可由环境重放或程序断言确认的事实允许决定更新方向。
- **student-generated critique states**：critique 中的每个事实先通过来源与状态一致性核验，再进入蒸馏。
- **高熵探索**：对贡献接近或不稳定的事实降低权重，不提前坍缩为唯一协作模式。
- **sealed eval**：冻结独立事实核验器、终局环境测试与隐藏协作任务，避免事实抽取器和策略共同适应。
