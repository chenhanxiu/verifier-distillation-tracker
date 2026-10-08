# Decoupling Exploration from Optimization in RLVR

- 作者：Saif Punjwani、Micah Goldblum
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.10536
- Canonical URL：https://arxiv.org/abs/2610.10536
- 代码：论文称将发布全部代码与检查点；当前可见项目页为 https://capricious-hydrogen-41c.notion.site/

## 一句话结论

【论文原文】Exploration-Distillation（ExpDis）把带 novelty bonus 的探索策略与不带 novelty bonus 的 student 优化分离，反复过滤正确、多样的轨迹再蒸馏，避免探索奖励直接破坏主策略。

## 真正新增的内容

【论文原文】不是在同一策略上同时平衡新颖性与任务奖励，而是允许一个或多个 explorer 激进探索，再由正确性和质量过滤器决定哪些轨迹进入独立 student；多轮交替后仍保留更好的 pass@k 多样性。

## 核心方法

【论文原文】explorer 用 novelty bonus 训练；轨迹经可验证正确性与质量筛选；student 仅蒸馏筛选后的探索成果，不承担 novelty objective；循环重复数轮。

## 关键实验结果

【论文原文】在七个数学推理基准和两个模型族上，同等 wall-clock 预算超过 DAPO；pass@k 曲线更好，表明正确解法分布更丰富。摘要未披露统一绝对增益。

## 证据质量与局限

【论文原文】有多基准、双模型族和等时预算比较。【分析推断】证据限于数学推理；过滤器决定“新颖但正确”的边界，若 verifier 漏判，仍会系统性丢弃少数策略。

## 最接近的相关工作

【分析推断】最接近 DDO、EPIG-Tree、Belief-Shift Branching 与 Data-free OPD；本文独特点是将探索策略与接受蒸馏更新的 student 物理分离。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】让 explorer 在 Agent 高熵状态生成候选分支，用程序/环境真值筛正确性，再由 distributional verifier 给质量与不确定性；student 只吸收通过硬门控的多样轨迹。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：比较同策略 novelty、双策略 ExpDis、无探索三组。
- 【分析推断】A/B/T：真值相同但策略差异大的分支保留 T/并列，不强制排序。
- 【分析推断】真值门控：环境成功证书决定是否入池，软 verifier 只排序质量。
- 【分析推断】critique states：只蒸馏经重放验证、能解释恢复机制的 critique。
- 【分析推断】高熵分叉：把探索预算集中到 explorer，防止 student 被 novelty 梯度拖坏。
- 【分析推断】sealed eval：用未参与筛选的任务与 verifier 验证多样性收益。