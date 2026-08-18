# SOPD：在 OPD 与 SFT 之间进行 Step-Level On-Policy Distillation

## 基本信息
- **论文标题**：Step-Level On-Policy Distillation: Interpolating Between On-Policy Distillation and Supervised Fine-Tuning
- **作者**：Changhui Sun, Lanbo Liu, Hang Lei, Tong Ling, Jiahang Xie, Zhiyong Zheng, Yujia Wang, Hao Liu, Feng Xiao, Lu Liu, Yanlong Du, Zifeng Cheng, Ziwei Jiang, Qing Gu
- **首次公开日期**：2026-08-17
- **版本日期**：2026-08-17（v1）
- **原始论文**：https://arxiv.org/abs/2608.16333
- **DOI**：10.48550/arXiv.2608.16333
- **代码**：未发现论文官方代码链接

## 一句话结论
SOPD 在 student 完整 on-policy 轨迹的每个 step 起点，让 teacher 独立生成一段连贯修复，而不是只给下一 token 分布；它是目前与长时程 Agent verifier × OPD 路线最直接的新结果之一。

## 真正新增的内容
**论文原文**：标准 OPD 在错误前缀上只给碎片化 token correction，不能展开完整修复路径；SOPD 从每个 student step prefix 生成一个独立 teacher fragment。step 长度趋近 1 时近似 OPD，覆盖整条响应时趋近 SFT。

**分析推断**：可把 teacher fragment 拆成 generative critique + ordinal score target，并以环境执行结果选择哪个 step 的修复真正有效；否则 teacher 连贯并不代表可执行。

## 核心方法
student 先完成完整 trajectory；每个自然 step（Agent 环境 turn 或数学 reasoning step）对应一个 student prefix。teacher 从每个 prefix 独立生成一个 step，作为 SFT-style target。各 teacher query 不执行环境动作，可在轨迹结束后并行。

## 关键实验结果
ALFWorld 中 7B RL teacher 蒸馏 3B student。相对 Vanilla OPD，SOPD 在 Valid Seen 成功率从 65.72% 到 84.29%（+18.57），Valid Unseen 从 60.45% 到 82.09%（+21.64），平均轮数分别减少 3.53 和 4.33；Hard split 成功率与 Vanilla OPD 同为 10.74%。论文同时在四项数学竞赛基准报告优于 SFT/OPD。

## 证据质量与局限
优势是直接含 ALFWorld Agent、seen/unseen/hard、交互轮数和数学任务，且与 SFT/OPD/TCOD 对比。局限是单一 Agent 环境、单一师生配置；Hard split 未改善；teacher fragment 不经过真实环境续跑，可能提出不可执行动作；未报告 sealed evaluator 或多 seed 置信区间。

## 最接近的相关工作
SFT、vanilla OPD、OEC、Agent-RLVR、TCOD、Guided-OPD、ReOPD、student-prefix repair 与 hindsight correction。

## 如何复用或推进 LLM-as-a-Verifier
在 student 每个 step prefix 上让 teacher 生成“诊断—候选下一步—预期进度分布”，再由 score verifier/环境重放选择。可蒸馏生成 critique，也可蒸馏 A/B/T 与 ordinal outcome。

## 对 Agent verifier × OPD 路线的影响
- **score-level**：每个 step 同时获得 teacher fragment 和 score distribution。
- **A/B/T**：比较 student 原 action 与 teacher repair；执行结果相近时保留 Tie。
- **真值门控**：teacher step 必须在复制环境中执行验证，不能只凭文本连贯性。
- **critique states**：SOPD 天然覆盖 student-generated failure prefixes。
- **探索**：每个 prefix 保留多条 teacher/student continuation，尤其高熵节点。
- **sealed eval**：隐藏环境与任务，使用未参与 teacher 生成的 verifier；分别报告 seen/unseen/hard 和恢复成功率。

## 结论边界
论文证明 step-level target 在 ALFWorld 常规 seen/unseen 上明显优于 token OPD，但 Hard 未提升；不能据此认为它已解决复杂长时程规划或 verifier 共适应。
