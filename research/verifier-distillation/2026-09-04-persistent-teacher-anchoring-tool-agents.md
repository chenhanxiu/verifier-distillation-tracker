# Persistent Teacher Anchoring for Tool-Using Agents

- **作者**：Hyun Bin Park、Kyungho Song、Sangmin Lee、Du-Seong Chang
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.04773](https://arxiv.org/abs/2609.04773)
- **DOI**：[10.48550/arXiv.2609.04773](https://doi.org/10.48550/arXiv.2609.04773)
- **发表信息**：EMNLP 2026 Main Conference
- **代码**：截至本次记录未发现作者公开代码

## 一句话结论

PTA 让 teacher 在工具调用真正触发环境副作用前验证并承诺整轮输出，直接修补了普通 OPKD 在 student-OOD 工具轨迹上“先执行、后监督”的结构性漏洞。

## 真正新增的内容

**论文原文结论**：在 chunk-level proposer–verifier 之外加入 turn-level commitment；只有 teacher 验证完整 turn 后，工具调用才到达环境。persistent lookahead 用空闲 rollout 容量推进未来样本，并跨更新保存未完成样本。

**分析推断**：这是程序化/环境真值门控 teacher 信号的强工程原型：先验证动作，再允许它改变环境历史。对 verifier 蒸馏而言，关键是将“可执行承诺”与“文本似然”解耦。

## 核心方法

- student 诱导候选轨迹，teacher 对生成 chunk 进行验证；
- 完整工具 turn 通过 teacher 验证后才 commit 并执行；
- 已验证 chunk 被视为原子生成单元；
- 固定 verifier 下，persistent lookahead 跨 batch/更新携带未完成 rollout，减少等待浪费；
- PTA 预训练后，在相同预算下继续下游 RL。

## 关键实验结果

**论文报告**：

- Search-R1 风格检索与 DeepEyes 风格感知任务中，macro best@4 分别较 OPKD + 同预算 RL 提升 2.5 和 2.8 点。
- MuSiQue mean@4 从 8.20 提升到 10.93，best@4 从 13.94 提升到 18.78。
- 感知任务 macro mean@4 提升 5.32、best@4 提升 2.80；HRBench8K 的 pre-RL best@4 从 58 提升到 65。
- persistent lookahead 提高约 24% 吞吐率。

## 证据质量与局限

**证据质量：中高。** 有工具环境、同预算 OPKD 对照和效率结果，且已被 EMNLP 2026 接收。

**论文局限**：实验仅覆盖检索与视觉感知，尚未验证代码执行、数据库写入、多 Agent 协作等更强副作用环境。

**进一步风险（分析）**：固定 teacher verifier 若有偏差，会稳定地审查错；严格承诺也可能系统性压掉新颖但正确的高熵分支。

## 最接近的相关工作

最接近 proposer–verifier generation、普通 OPKD，以及 SOPD、DART-SD、SAGE、OPDVR。PTA 的差异是把 teacher 的控制边界扩展到环境执行时刻，而不只控制保留哪些文本 token。

## 如何复用或推进 LLM-as-a-Verifier

- 将 turn commitment 实现成两层门：schema/权限/副作用的程序检查拥有否决权，LLM verifier 负责软排序与 critique。
- 对被拒动作输出 A/B/T 或序数分布及理由，而非仅丢弃，作为 verifier/student 的反事实训练样本。
- student-generated critique states 只有在执行重放或 teacher 多视角一致时才写入持久记忆。
- teacher 不确定时应 abstain 并允许沙箱分叉，而不是把高熵候选直接剪掉。

## 对 Agent verifier × OPD 实验路线的具体影响

1. 把 verifier 放到工具调用 commit 之前，比较“执行后打分”和“执行前承诺”对错误传播的影响。
2. score-level OPD 蒸馏 teacher 的整轮接受概率、风险等级与理由分布，不只 next-token logits。
3. A/B/T 数据从同一 prefix 的 accepted/rejected/abstained turns 构造，并用实际环境 outcome 回填。
4. 高熵分叉在隔离环境中保留，只有不可逆副作用路径执行硬拒绝。
5. sealed eval 使用独立 verifier、隐藏工具约束和未见环境；固定训练 verifier 不参与最终裁决。