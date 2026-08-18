# LongRCA Bench：长时程 Agent 失败的角色归因与根因定位

## 基本信息
- **论文标题**：LongRCA Bench: Diagnosing Responsible Roles and Root Causes in Long-Horizon Agent Failures
- **作者**：Yunfei Zhang, Boyu Feng, Changhua Pei, Zexin Wang, Zhihuang Peng, Xinlong Liu, Hengyue Jiang, Difeng Ma, Jiayi Zhang, Yongzhou Yao, Yanan Zhao, Fei Sun, Yintong Huo, Zhaoyang Liu, Jingjing Li, Gaogang Xie, Dan Pei
- **首次公开日期**：2026-08-15
- **版本日期**：2026-08-15（v1）
- **原始论文**：https://arxiv.org/abs/2608.15242
- **DOI**：10.48550/arXiv.2608.15242
- **代码**：论文列表称已公开，但摘要页未提供可可靠解析的 GitHub URL

## 一句话结论
LongRCA 提供 1,140 条真实失败、 median 145-step 的长 Agent 轨迹，并将“责任角色”与“最早决定性根因步骤”分开标注；这是训练和 sealed 测试 trajectory verifier 的稀缺高质量目标。

## 真正新增的内容
**论文原文**：不注入合成错误，而从五个真实 benchmark 的失败执行中人工标注 responsible role、earliest decisive root-cause step 和 rationale；提出训练-free RCTA，通过分段摘要召回候选错误，再追溯交接指令。

**分析推断**：可把根因 step 前后的候选动作构造成 A/B/T 或 ordinal contribution 样本，用于 student-generated critique verifier；但人工标签是事后归因，不等于反事实因果效应。

## 核心方法
统一不同 agent 框架的日志为 step index、role、content，并保留工具/verifier metadata。22 名计算机专业硕博生阅读任务、完整轨迹和 source evaluator outcome，每条通常需 30–40 分钟；多标注冲突经复核得到最终标签。

## 关键实验结果
数据来自 SWE-bench Pro、Terminal Bench 2、TravelPlanner、VitaBench、WebArena Verified；覆盖软件修复、终端、旅行规划、服务工具和网页交互。最强普通 baseline exact root-step 仅 13.2%；RCTA responsible-role accuracy 51.1%，exact root-step 24.1%。RCTA 在 ≤100 step 上 30.3%，101–200 与 201–400 step 降至约 20%。

## 证据质量与局限
优势是真实失败、五领域、完整人类标签和长轨迹。局限是每条最终只有一个 role/step 标签；rationale 不评分；事后 full-log diagnosis，不测试在线预警；未评估完整因果链；TravelPlanner 占 60.1%，分布不均；标签是专家判断而非 matched counterfactual replay。

## 最接近的相关工作
Agent failure attribution、trajectory segmentation/retrieval、process supervision、root-cause analysis、TRACE/CrEST、DHD 式反事实贡献估计。

## 如何复用或推进 LLM-as-a-Verifier
以 root step 为正例、邻近非根因 step 为 hard negative；让 verifier 输出角色分布、step 序数分布与 critique。用 rationale 训练 generative verifier，但以 role/step 标签评估定位，以环境重放另评估因果贡献。

## 对 Agent verifier × OPD 路线的影响
- **score-level**：将“成为最早根因”的概率作为 step score 分布。
- **A/B/T**：比较两个候选 step/role 的责任概率，Tie 表示证据不足。
- **真值门控**：source benchmark outcome 只确认失败；根因方向还需环境重放验证。
- **critique states**：在 student 对候选根因的解释上做 OPD。
- **探索**：不可按单次 root-step judge 直接删除分支；先测可恢复性。
- **sealed eval**：按 benchmark、生成模型和 trajectory length 划分，防止相同任务/框架泄漏。

## 结论边界
LongRCA 是强诊断 benchmark，不是因果 credit-assignment ground truth。最适合作为 sealed failure-localization 测试集，并与反事实环境标签互补。
