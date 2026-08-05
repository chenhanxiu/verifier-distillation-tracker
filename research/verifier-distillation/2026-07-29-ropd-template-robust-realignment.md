# ROPD：On-Policy Distillation for LLM Safety

> 补录自「Verifier 蒸馏论文」scheduler 于 2026-07-31 的实际发现。

## 论文信息

- **标题**：On-Policy Distillation for LLM Safety: A Routing Approach to Template-Robust Realignment
- **作者**：Yongjian Guo, Wanlun Ma, Lingyu Shen, Xi Xiao, Sheng Wen
- **发布日期**：2026-07-29（arXiv v1）
- **arXiv**：[2607.27081](https://arxiv.org/abs/2607.27081)
- **HTML 全文**：[arxiv.org/html/2607.27081](https://arxiv.org/html/2607.27081)
- **代码**：论文未提供公开代码链接
- **领域**：安全再对齐、双 teacher 蒸馏、输出概率路由

## 一句话结论

ROPD 的核心价值在于把两个互相冲突的目标分配给不同 teacher：aligned 原模型负责安全拒答，遭攻击但保留任务能力的模型负责专业技能；再按样本来源路由到对应 teacher，并用 top-K KL 蒸馏输出分布。它对多 teacher verifier 蒸馏中的“监督来源路由”和“能力保持”很有启发，但与 Agent verifier × OPD 的直接关系较弱。

## 真正的新意

论文研究微调供应链攻击后的安全修复：模型获得专业能力的同时，被恶意数据植入了有害响应行为。作者指出现有修复方法常遇到三类问题：

1. 修复安全时破坏下游专业能力；
2. 防御依赖攻击者使用的 prompt template；
3. 即使当前模板下修复成功，更换 system prompt 后仍可能再次越狱。

ROPD 使用两个冻结 teacher：

- **Safety teacher**：攻击前的 aligned 原模型，提供相对不依赖表面模板的拒答概率分布；
- **Task teacher**：被攻击后的微调模型，保留下游任务能力。

每个训练样本根据来源路由：

- harmful prompt → safety teacher；
- downstream task → task teacher。

训练目标不是模仿单个回答，而是匹配被路由 teacher 的输出概率。为降低词表计算成本，论文只保留 teacher 的 top-K token 概率，并将其余 token 聚合成一个 tail bucket 后计算 KL。

## 关键实验结果

- 覆盖 Llama-2-7B-Chat、Qwen2.5-7B-Instruct、Gemma-2-9B-it。
- 下游任务覆盖 SQL、SAMSum 和 NL2Bash；与 rollback、RESTA、soft-SFT、SSRD 四类方法比较。
- 在 self defense template 下，无论攻击采用哪种模板，ROPD 的 ASR 范围为：Llama-2 **2.1%–2.4%**、Qwen2.5 **6.6%–11.1%**、Gemma-2 **5.1%–5.6%**，并基本保持下游任务能力。
- 数据效率实验中，约 1,500 个样本把 ASR 从 **62.1% 降至 2.4%**，SQL task score 保持在 **0.626**。
- 双 teacher 消融表明：去掉 task teacher 时安全表现变化不大，但任务能力下降；换成额外训练的 clean task teacher 可进一步提高任务分数，但增加一次训练成本。
- Gemma-2-9B-it + NL2Bash 设置下，ROPD 训练约 **15.7 分钟**，与 SFT 类基线接近。

## 证据质量与局限

**证据质量：中等（跨模型、跨任务和模板评测较全面，但仍是 arXiv v1，且无代码；“on-policy”实现细节也需要进一步审视）。**

支持证据：

- 三个模型、三个任务、三类模板和四个基线；
- 同时测量攻击成功率与任务保持；
- 有双 teacher、数据量、训练动态和成本消融；
- 明确评测 attacker、defender 与 cross-template channel，而不是只看同模板结果。

主要限制：

- 安全 ASR 由 Qwen2.5-32B-Instruct 判断，缺少人工校准或多 judge 一致性分析；
- harmful 数据和真实攻击主要围绕 BeaverTails 与三种模板，外部有效性仍有限；
- ROPD 只能降低而不能消除模板切换风险；mismatched raw defense 下仍会保留明显 ASR；
- 没有公开代码；
- 论文将方法称为 OPD，但算法描述主要呈现“在带 response 的混合语料上做 source-routed token KL”，对 student 自生成 rollout、采样策略和状态分布如何在线更新交代不足。严格意义上的 on-policy 属性需要代码或补充材料确认。

## 与相关工作的关系

ROPD 与单 teacher 安全蒸馏的区别是：它不让一个 teacher 同时承担安全与任务能力，而是用样本来源进行硬路由。这种解耦减少了修复安全时的能力税。top-K + tail bucket 也提供了比完整词表 KL 更低成本的分布蒸馏方式。

它与 LLM-as-a-Verifier 没有直接任务重合：ROPD 蒸馏的是生成策略的 token 概率，而不是 verifier 的评分、排序或校准分布。它提供的是多 teacher 组织方式和低成本概率匹配机制。

## 对 Agent verifier × OPD 的启示

### 可迁移的设计

1. **teacher 职责解耦**：一个 teacher 负责通用评分校准或安全边界，另一个 teacher 负责特定 Agent 任务/工具域知识。
2. **按来源路由**：根据轨迹类型、工具域、错误类别、是否含 privileged evidence 或 teacher 可靠度选择监督源。
3. **能力保持 anchor**：蒸馏新 verifier 能力时，用原 verifier 作为 retention teacher，约束旧 benchmark 的排序与校准不退化。
4. **低成本分布传输**：如果目标是 token-level verifier，可评估 top-K + tail；如果目标是有限档位的 score-level verifier，直接保存完整评分分布通常更简单且信息损失更小。

### 与当前方案的差距

当前目标是让 Qwen student 在自己生成的 critique/state 上接受 teacher 的 A/B/T 或序数评分分布监督。ROPD：

- 没有研究 verifier；
- 没有序数/评分空间；
- 路由由数据来源的已知标签决定，而不是由不确定性、证据质量或动态 competence 决定；
- 论文对 student-generated on-policy states 描述不足。

因此它更适合作为“multi-teacher routing + retention”邻近工作，而不是目标方法的直接基线。

### 建议增加的实验

- 单 teacher、静态双 teacher、按样本类别路由、按 teacher confidence 动态路由；
- 是否保留原 verifier 作为 retention teacher；
- 路由错误率与最终 verifier calibration/ranking 的关系；
- 完整评分分布 vs. top-K/token KL 的性能、显存、吞吐和 API 成本；
- matched domain 与 cross-domain/cross-template 的 verifier 稳健性。

## 结论

**建议选择性精读。** 方法层面最值得借鉴的是“目标解耦后再路由 teacher”，以及以较低成本保持旧能力。对 Agent verifier × OPD 的直接证据有限，但它提醒我们：多 teacher 的关键不只是聚合，更是明确每个 teacher 应该在哪类状态上负责。
