# -*- coding: utf-8 -*-
"""面知 种子数据生成器：一次定义 100+ 企业岗位与 80 道企业真题，
输出后端 JSON（app/seed_data/*.json）与前端 TS（frontend/src/mock/seed_data.ts），
保证前后端数据完全一致，也便于后续用 CSV/JSON 导入合并。

用法：python tools/generate_seed.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 一、企业岗位池（企业 → 岗位配置 + 岗位名列表）
# 字段：industry 行业 / duration 分钟 / total 题量 / mode 模式 / answer_mode 答题方式 / types 题型
# ============================================================
COMPANIES = {
    # ---------- 互联网（47） ----------
    "字节跳动": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["技术深挖", "行为面试 STAR", "项目经历"],
               "roles": ["后端开发工程师", "算法工程师", "前端开发工程师", "客户端开发工程师",
                         "测试开发工程师", "大数据开发工程师", "产品经理", "数据分析师"]},
    "腾讯": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["AI全栈", "技术深挖", "产品分析", "行为面试 STAR"],
            "roles": ["AI全栈工程师", "后端开发工程师", "前端开发工程师", "产品经理",
                      "游戏策划", "游戏客户端开发工程师", "云产品经理", "内容运营"]},
    "阿里巴巴": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["技术深挖", "电商运营", "行为面试 STAR"],
               "roles": ["Java开发工程师", "算法工程师", "前端开发工程师", "产品经理", "电商运营"]},
    "美团": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["技术深挖", "行为面试 STAR", "情景模拟"],
            "roles": ["后端开发工程师", "算法工程师", "产品经理", "配送运营专员"]},
    "百度": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["技术深挖", "算法题", "行为面试 STAR"],
            "roles": ["算法工程师", "后端开发工程师", "自动驾驶工程师"]},
    "京东": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["技术深挖", "物流运营", "行为面试 STAR"],
            "roles": ["Java开发工程师", "产品经理", "物流管培生"]},
    "网易": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["游戏策划", "产品分析", "行为面试 STAR"],
            "roles": ["游戏策划", "游戏开发工程师", "产品经理"]},
    "拼多多": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
              "types": ["技术深挖", "电商运营"],
              "roles": ["后端开发工程师", "电商运营专员"]},
    "快手": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["技术深挖", "产品分析"],
            "roles": ["后端开发工程师", "算法工程师"]},
    "小红书": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
              "types": ["产品分析", "社区运营", "情景模拟"],
              "roles": ["产品经理", "内容运营专员"]},
    "哔哩哔哩": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "voice",
               "types": ["内容运营", "产品分析"],
               "roles": ["内容运营专员", "产品经理"]},
    "滴滴出行": {"industry": "互联网", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["技术深挖"],
               "roles": ["后端开发工程师"]},
    "小米": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
            "types": ["技术深挖", "硬件基础", "行为面试 STAR"],
            "roles": ["安卓开发工程师", "MIUI产品经理", "硬件测试工程师", "嵌入式开发工程师"]},
    # ---------- 国企央企（18） ----------
    "国家电网": {"industry": "国企", "duration": 25, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "专业基础", "时政认知"],
               "roles": ["电气工程岗", "信息通信岗", "财务管理岗", "综合管理岗"]},
    "中国移动": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "专业基础", "时政认知"],
               "roles": ["网络工程师", "市场运营岗", "信息技术岗"]},
    "中国石油": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "专业基础", "情景模拟"],
               "roles": ["油气储运岗", "安全管理岗"]},
    "中国石化": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "专业基础", "情景模拟"],
               "roles": ["化工工艺岗", "安全环保岗"]},
    "中国建筑": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["专业基础", "工程管理", "情景模拟"],
               "roles": ["土木工程师", "工程管理岗"]},
    "中国烟草": {"industry": "国企", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["综合素养", "情景模拟"],
               "roles": ["综合管理岗", "市场营销岗"]},
    "工商银行": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "金融科技", "情景模拟"],
               "roles": ["金融科技岗", "综合业务岗", "客户经理岗"]},
    # ---------- 外企（12） ----------
    "微软中国": {"industry": "外企", "duration": 25, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["英文面试", "技术深挖", "系统设计"],
               "roles": ["软件开发工程师", "云计算工程师"]},
    "苹果中国": {"industry": "外企", "duration": 25, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["英文面试", "技术深挖", "硬件基础"],
               "roles": ["软件工程师"]},
    "特斯拉中国": {"industry": "外企", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
                 "types": ["英文面试", "专业基础", "供应链"],
                 "roles": ["工艺工程师"]},
    "宝洁": {"industry": "外企", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "voice",
            "types": ["行为面试 STAR", "英文面试", "供应链"],
            "roles": ["供应链管培生", "市场管培生"]},
    "联合利华": {"industry": "外企", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "voice",
               "types": ["行为面试 STAR", "市场分析"],
               "roles": ["市场管培生", "销售管培生"]},
    "欧莱雅中国": {"industry": "外企", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "voice",
                 "types": ["市场分析", "行为面试 STAR"],
                 "roles": ["市场管培生"]},
    "四大会计师事务所": {"industry": "外企", "duration": 25, "total": 10, "mode": "pressure", "answer_mode": "text",
                    "types": ["案例分析", "英文面试", "专业基础"],
                    "roles": ["审计助理", "咨询顾问", "税务助理"]},
    # ---------- 金融（6） ----------
    "蚂蚁集团": {"industry": "互联网", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["技术深挖", "金融风控"],
               "roles": ["后端开发工程师", "算法工程师", "金融风控岗"]},
    "招商银行": {"industry": "国企", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["综合素养", "金融科技", "情景模拟"],
               "roles": ["金融科技岗", "零售客户经理"]},
    "中金公司": {"industry": "外企", "duration": 25, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["专业基础", "案例分析", "英文面试"],
               "roles": ["投行分析员"]},
    # ---------- 制造/科技（13） ----------
    "华为": {"industry": "制造业", "duration": 25, "total": 10, "mode": "pressure", "answer_mode": "text",
            "types": ["AI全栈", "技术深挖", "综合素养", "压力测试"],
            "roles": ["AI全栈工程师", "通信研发工程师", "嵌入式软件工程师", "硬件工程师", "海外销售经理"]},
    "大疆": {"industry": "制造业", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
            "types": ["技术深挖", "专业基础"],
            "roles": ["嵌入式软件工程师", "算法工程师"]},
    "比亚迪": {"industry": "制造业", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
              "types": ["技术深挖", "专业基础", "市场分析"],
              "roles": ["电池研发工程师", "整车研发工程师"]},
    "宁德时代": {"industry": "制造业", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["技术深挖", "专业基础"],
               "roles": ["电池系统工程师", "材料研发工程师"]},
    "海康威视": {"industry": "制造业", "duration": 20, "total": 10, "mode": "pressure", "answer_mode": "text",
               "types": ["技术深挖", "算法基础"],
               "roles": ["算法工程师", "嵌入式工程师"]},
    # ---------- 快消/医药/文职（8） ----------
    "伊利集团": {"industry": "快消", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "voice",
               "types": ["市场分析", "情景模拟"],
               "roles": ["市场管培生", "销售管培生"]},
    "玛氏中国": {"industry": "快消", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "voice",
               "types": ["行为面试 STAR", "供应链"],
               "roles": ["销售管培生", "供应链管培生"]},
    "药明康德": {"industry": "医药", "duration": 20, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["专业基础", "行为面试 STAR"],
               "roles": ["药物研发岗", "分析化学岗"]},
    "通用行政": {"industry": "文职", "duration": 15, "total": 8, "mode": "normal", "answer_mode": "text",
               "types": ["情景模拟", "行为面试 STAR"],
               "roles": ["人力资源专员", "行政管理专员"]},
}

# 企业英文 id 前缀
EN_ID = {
    "字节跳动": "bytedance", "腾讯": "tencent", "阿里巴巴": "alibaba", "美团": "meituan",
    "百度": "baidu", "京东": "jd", "网易": "netease", "拼多多": "pdd", "快手": "kuaishou",
    "小红书": "xiaohongshu", "哔哩哔哩": "bilibili", "滴滴出行": "didi", "小米": "xiaomi",
    "国家电网": "sgcc", "中国移动": "cmcc", "中国石油": "petrochina", "中国石化": "sinopec",
    "中国建筑": "cscec", "中国烟草": "tobacco", "工商银行": "icbc", "微软中国": "microsoft",
    "苹果中国": "apple", "特斯拉中国": "tesla", "宝洁": "pg", "联合利华": "unilever",
    "欧莱雅中国": "loreal", "四大会计师事务所": "big4", "蚂蚁集团": "ant", "招商银行": "cmb",
    "中金公司": "cicc", "华为": "huawei", "大疆": "dji", "比亚迪": "byd", "宁德时代": "catl",
    "海康威视": "hikvision", "伊利集团": "yili", "玛氏中国": "mars", "药明康德": "wuxiapptec",
    "通用行政": "admin",
}


def build_jobs():
    jobs = []
    for company, cfg in COMPANIES.items():
        en = EN_ID[company]
        for i, role in enumerate(cfg["roles"], 1):
            jobs.append({
                "id": f"{en}-{i:02d}",
                "name": role,
                "company": company,
                "industry": cfg["industry"],
                "duration": cfg["duration"],
                "question_types": cfg["types"],
                "answer_mode": cfg["answer_mode"],
                "mode": cfg["mode"],
                "total_questions": cfg["total"],
            })
    return jobs


# ============================================================
# 二、企业真题（q36+，基于公开面经；前 35 题在 data.py 保留，此处并入最终清单）
# ============================================================
EXTRA_QUESTIONS = [
    # 腾讯
    {"id": "q36", "title": "（腾讯）如何设计一个端到端的 AI 应用（从数据到模型部署）？", "type": "AI全栈", "difficulty": "困难", "industry": "互联网", "company": "腾讯",
     "reference_answer": "业务定义 → 数据获取与标注 → 模型选型与训练 → 评估 → 部署与监控 → 迭代闭环。", "template": "数据 → 模型 → 部署 → 监控闭环"},
    {"id": "q37", "title": "（腾讯）如何设计一个付费点，让玩家愿意买单又不破坏平衡？", "type": "游戏策划", "difficulty": "困难", "industry": "互联网", "company": "腾讯",
     "reference_answer": "明确付费目标与玩家分层 → 非数值型付费(皮肤/外观)优先 → 数值付费做上限保护 → 小额高频降低门槛。", "template": "目标分层 → 非数值优先 → 上限保护"},
    {"id": "q38", "title": "（腾讯）如何设计一个高可用的消息队列方案？", "type": "技术深挖", "difficulty": "困难", "industry": "互联网", "company": "腾讯",
     "reference_answer": "集群与主从 → 数据多副本(同步/异步) → 消费端幂等与重试 → 降级与限流 → 故障演练。", "template": "集群 → 副本 → 幂等 → 演练"},
    # 字节
    {"id": "q39", "title": "（字节跳动）广告点击率低，你会如何分析与优化？", "type": "产品分析", "difficulty": "中等", "industry": "互联网", "company": "字节跳动",
     "reference_answer": "拆漏斗(曝光/点击/转化) → 素材/定向/出价归因 → A/B 实验验证 → 放量。", "template": "漏斗拆解 → 归因 → A/B → 放量"},
    {"id": "q40", "title": "（字节跳动）如何提升直播间的停留时长？", "type": "产品分析", "difficulty": "中等", "industry": "互联网", "company": "字节跳动",
     "reference_answer": "内容节奏(留人钩子) → 互动玩法(福袋/连麦) → 算法推荐优化 → 数据验证。", "template": "内容 → 玩法 → 推荐 → 验证"},
    # 阿里
    {"id": "q41", "title": "（阿里巴巴）双11 大促系统如何保障稳定性？", "type": "技术深挖", "difficulty": "困难", "industry": "互联网", "company": "阿里巴巴",
     "reference_answer": "容量预估与压测 → 限流/降级/熔断 → 缓存与异步化 → 预案与演练 → 监控告警。", "template": "预估 → 限流降级 → 异步 → 演练"},
    {"id": "q42", "title": "（阿里巴巴）如何设计一个「猜你喜欢」推荐位？", "type": "产品分析", "difficulty": "中等", "industry": "互联网", "company": "阿里巴巴",
     "reference_answer": "目标指标(点击/转化) → 冷启动策略 → 召回/排序 → 业务规则干预 → 效果评估。", "template": "指标 → 冷启动 → 召回排序 → 评估"},
    # 美团
    {"id": "q43", "title": "（美团）高峰期骑手运力不足，如何调度？", "type": "情景模拟", "difficulty": "中等", "industry": "互联网", "company": "美团",
     "reference_answer": "需求预测与提前调度 → 动态定价激励 → 单量熔断与时效兜底 → 事后复盘。", "template": "预测 → 激励 → 熔断 → 复盘"},
    # 百度
    {"id": "q44", "title": "（百度）如何评估自动驾驶系统的安全性？", "type": "技术深挖", "difficulty": "困难", "industry": "互联网", "company": "百度",
     "reference_answer": "场景覆盖度与仿真测试 → 实车路测里程 → 安全冗余设计(失效降级) → 事故归因体系。", "template": "仿真 → 路测 → 冗余 → 归因"},
    # 京东
    {"id": "q45", "title": "（京东）如何优化仓库拣货效率？", "type": "情景模拟", "difficulty": "中等", "industry": "互联网", "company": "京东",
     "reference_answer": "波次与路径优化 → 货位布局(ABC分类) → 设备/系统辅助 → 数据指标监控。", "template": "路径 → 布局 → 工具 → 指标"},
    # 网易
    {"id": "q46", "title": "（网易）MMO 新版本如何做留存提升？", "type": "游戏策划", "difficulty": "中等", "industry": "互联网", "company": "网易",
     "reference_answer": "分析流失节点 → 前期目标感与新手引导 → 中后期社交与目标线 → A/B 验证。", "template": "流失分析 → 新手 → 社交 → 验证"},
    # 拼多多
    {"id": "q47", "title": "（拼多多）如何理解极致低价策略的可持续性？", "type": "产品分析", "difficulty": "中等", "industry": "互联网", "company": "拼多多",
     "reference_answer": "供给端(白牌/工厂直供) → 需求端(下沉市场) → 平台补贴与广告变现平衡 → 长期壁垒。", "template": "供给 → 需求 → 变现 → 壁垒"},
    # 快手
    {"id": "q48", "title": "（快手）如何平衡流量分发与创作者生态？", "type": "产品分析", "difficulty": "中等", "industry": "互联网", "company": "快手",
     "reference_answer": "普惠分发 vs 头部效应 → 创作者成长阶梯 → 流量与商业激励 → 生态指标监控。", "template": "分发 → 成长 → 激励 → 监控"},
    # 小红书
    {"id": "q49", "title": "（小红书）如何治理社区虚假种草？", "type": "情景模拟", "difficulty": "中等", "industry": "互联网", "company": "小红书",
     "reference_answer": "识别(内容/行为特征) → 处置(限流/标注) → 平台规则与公示 → 用户教育。", "template": "识别 → 处置 → 规则 → 教育"},
    # 小米
    {"id": "q50", "title": "（小米）如何优化安卓应用的内存占用？", "type": "技术深挖", "difficulty": "中等", "industry": "互联网", "company": "小米",
     "reference_answer": "内存泄漏定位(Mat/LeakCanary) → 图片与缓存策略 → 生命周期管理 → 压测对比。", "template": "定位 → 缓存 → 生命周期 → 对比"},
    # 国企
    {"id": "q51", "title": "（国家电网）什么是源网荷储一体化？", "type": "时政认知", "difficulty": "中等", "industry": "国企", "company": "国家电网",
     "reference_answer": "电源/电网/负荷/储能协同互动 → 提升新能源消纳与系统灵活性 → 结合岗位谈实践。", "template": "概念 → 作用 → 岗位结合"},
    {"id": "q52", "title": "（中国移动）谈谈 5G 在垂直行业的典型应用。", "type": "时政认知", "difficulty": "中等", "industry": "国企", "company": "中国移动",
     "reference_answer": "大带宽/低时延/大连接特性 → 工业互联网/车联网/远程医疗等场景 → 商业模式。", "template": "特性 → 场景 → 商业"},
    {"id": "q53", "title": "（中国石油）如何理解安全生产「一岗双责」？", "type": "综合素养", "difficulty": "简单", "industry": "国企", "company": "中国石油",
     "reference_answer": "岗位职责与安全责任并重 → 谁主管谁负责 → 结合本岗位风险点举例。", "template": "概念 → 原则 → 岗位结合"},
    {"id": "q54", "title": "（中国建筑）如何理解工程项目的安全管理体系？", "type": "专业基础", "difficulty": "中等", "industry": "国企", "company": "中国建筑",
     "reference_answer": "安全责任制 → 教育培训与交底 → 隐患排查治理 → 应急管理 → 复盘改进。", "template": "责任 → 教育 → 排查 → 应急"},
    {"id": "q55", "title": "（工商银行）柜面如何防范电信网络诈骗风险？", "type": "情景模拟", "difficulty": "中等", "industry": "国企", "company": "工商银行",
     "reference_answer": "转账场景识别异常特征 → 风险提示与核实 → 触发限额/暂停 → 上报联动反诈。", "template": "识别 → 提示 → 管控 → 联动"},
    {"id": "q56", "title": "（中国烟草）专卖体制下如何做好客户服务？", "type": "综合素养", "difficulty": "中等", "industry": "国企", "company": "中国烟草",
     "reference_answer": "合规前提下提升服务 → 客户分层与需求分析 → 配送与售后标准化 → 满意度闭环。", "template": "合规 → 分层 → 服务 → 闭环"},
    # 外企
    {"id": "q57", "title": "（微软）Describe a highly available system you have designed. (English)", "type": "英文面试", "difficulty": "困难", "industry": "外企", "company": "微软中国",
     "reference_answer": "Use STAR: context → architecture (redundancy/load balance) → failure handling → measurable SLA.", "template": "Context → Architecture → Failure → SLA"},
    {"id": "q58", "title": "（苹果）如何平衡产品散热与续航？", "type": "技术深挖", "difficulty": "困难", "industry": "外企", "company": "苹果中国",
     "reference_answer": "功耗评估 → 散热结构设计 → 软件功耗优化 → 温控策略 → 实测验证。", "template": "功耗 → 散热 → 软件 → 温控"},
    {"id": "q59", "title": "（特斯拉）如何评估一条产线的节拍与瓶颈？", "type": "专业基础", "difficulty": "中等", "industry": "外企", "company": "特斯拉中国",
     "reference_answer": "测节拍时间 → 瓶颈工序识别(节拍最长) → 消除瓶颈(并行/优化) → 平衡率指标。", "template": "测节拍 → 找瓶颈 → 消除 → 平衡率"},
    {"id": "q60", "title": "（宝洁）如何降低供应链库存成本？", "type": "情景模拟", "difficulty": "中等", "industry": "外企", "company": "宝洁",
     "reference_answer": "需求预测优化 → ABC 分类与安全库存 → 供应商协同(VMI) → 周转率监控。", "template": "预测 → 分类 → 协同 → 监控"},
    {"id": "q61", "title": "（联合利华）如何为一款新品制定上市计划？", "type": "情景模拟", "difficulty": "中等", "industry": "外企", "company": "联合利华",
     "reference_answer": "目标人群与定位 → 定价与渠道 → 营销节奏(预热/首发/持续) → 效果复盘。", "template": "定位 → 渠道 → 节奏 → 复盘"},
    {"id": "q62", "title": "（欧莱雅）如何策划美妆新品的社媒种草？", "type": "情景模拟", "difficulty": "中等", "industry": "外企", "company": "欧莱雅中国",
     "reference_answer": "人设与卖点提炼 → KOL 矩阵与内容策略 → 话题与活动 → 转化与数据复盘。", "template": "卖点 → 矩阵 → 话题 → 复盘"},
    {"id": "q63", "title": "（四大）如何设计一个舞弊风险识别方案？", "type": "案例分析", "difficulty": "困难", "industry": "外企", "company": "四大会计师事务所",
     "reference_answer": "风险信号识别 → 数据抽样与异常分析 → 穿行测试 → 与管理层沟通 → 出具意见。", "template": "信号 → 分析 → 测试 → 沟通"},
    {"id": "q64", "title": "（四大）客户利润下滑，请给出诊断框架。", "type": "案例分析", "difficulty": "中等", "industry": "外企", "company": "四大会计师事务所",
     "reference_answer": "收入/成本拆解 → 对标竞品与行业 → 内部流程与效率 → 提出改善优先级。", "template": "拆解 → 对标 → 内部分析 → 改善"},
    # 金融
    {"id": "q65", "title": "（蚂蚁集团）如何识别电商交易中的刷单行为？", "type": "技术深挖", "difficulty": "中等", "industry": "互联网", "company": "蚂蚁集团",
     "reference_answer": "特征工程(频次/设备/时间) → 规则+模型双通道 → 团伙识别(图算法) → 误伤控制与申诉。", "template": "特征 → 模型 → 团伙 → 误伤控制"},
    {"id": "q66", "title": "（招商银行）如何理解零售银行的数字化运营？", "type": "综合素养", "difficulty": "中等", "industry": "国企", "company": "招商银行",
     "reference_answer": "数据驱动客户分层 → 场景化营销 → 线上渠道与 App 运营 → 风控与合规并重。", "template": "数据 → 场景 → 渠道 → 风控"},
    {"id": "q67", "title": "（中金公司）如何对一家公司做 DCF 估值？", "type": "专业基础", "difficulty": "困难", "industry": "外企", "company": "中金公司",
     "reference_answer": "预测自由现金流 → 确定折现率(WACC) → 终值假设 → 敏感性分析 → 交叉验证。", "template": "现金流 → WACC → 终值 → 敏感性"},
    # 制造
    {"id": "q68", "title": "（华为）如何把大模型落地到行业场景？", "type": "AI全栈", "difficulty": "困难", "industry": "制造业", "company": "华为",
     "reference_answer": "场景价值评估 → 数据与算力准备 → 微调/RAG/Agent 选型 → 部署与成本 → 效果度量。", "template": "场景 → 数据 → 技术选型 → 落地"},
    {"id": "q69", "title": "（华为）如何优化 5G 基站覆盖与能耗的平衡？", "type": "技术深挖", "difficulty": "困难", "industry": "制造业", "company": "华为",
     "reference_answer": "网络规划与站址优化 → 功率与波束管理 → 节能技术(休眠/符号关断) → 实测验证。", "template": "规划 → 功率 → 节能 → 验证"},
    {"id": "q70", "title": "（大疆）如何保证无人机飞行稳定性？", "type": "技术深挖", "difficulty": "困难", "industry": "制造业", "company": "大疆",
     "reference_answer": "传感器融合(IMU/GPS/视觉) → 控制算法(姿态/位置环) → 抗风与容错 → 实飞验证。", "template": "感知 → 控制 → 容错 → 实飞"},
    {"id": "q71", "title": "（比亚迪）如何理解整车热管理系统设计？", "type": "技术深挖", "difficulty": "困难", "industry": "制造业", "company": "比亚迪",
     "reference_answer": "乘员舱/电池/电机热管理协同 → 集成热泵方案 → 能耗与性能平衡 → 试验验证。", "template": "协同 → 方案 → 平衡 → 验证"},
    {"id": "q72", "title": "（宁德时代）如何提升电池包能量密度？", "type": "技术深挖", "difficulty": "困难", "industry": "制造业", "company": "宁德时代",
     "reference_answer": "电芯材料升级(高镍/硅碳) → 结构创新(CTP/CTC) → 减重与集成 → 安全与寿命权衡。", "template": "材料 → 结构 → 集成 → 权衡"},
    {"id": "q73", "title": "（海康威视）如何设计城市级视频分析系统？", "type": "技术深挖", "difficulty": "困难", "industry": "制造业", "company": "海康威视",
     "reference_answer": "海量视频接入与存储 → 分布式计算与推理 → 算法(检测/跟踪/检索) → 业务应用与运维。", "template": "接入 → 计算 → 算法 → 应用"},
    # 快消/医药/文职
    {"id": "q74", "title": "（伊利）如何做一款新品的地推冷启动？", "type": "情景模拟", "difficulty": "中等", "industry": "快消", "company": "伊利集团",
     "reference_answer": "选点(人流/目标人群) → 试饮与促销组合 → 导购话术培训 → 数据回收与调整。", "template": "选点 → 组合 → 培训 → 调整"},
    {"id": "q75", "title": "（玛氏）如何管理多渠道价盘冲突？", "type": "情景模拟", "difficulty": "中等", "industry": "快消", "company": "玛氏中国",
     "reference_answer": "统一价盘规则 → 渠道差异化产品/包装 → 窜货监控与处罚 → 渠道利润保护。", "template": "规则 → 差异化 → 监控 → 保护"},
    {"id": "q76", "title": "（药明康德）如何保证实验室数据的完整性？", "type": "专业基础", "difficulty": "中等", "industry": "医药", "company": "药明康德",
     "reference_answer": "ALCOA+ 原则(可归属/清晰/同步/原始/准确) → 电子记录与审计追踪 → 双人复核。", "template": "ALCOA+ → 电子记录 → 复核"},
    {"id": "q77", "title": "（通用）如何组织一场大型校招宣讲会？", "type": "情景模拟", "difficulty": "中等", "industry": "文职", "company": "通用行政",
     "reference_answer": "目标院校与排期 → 场地物料与嘉宾 → 报名与到场管理 → 现场执行与复盘转化。", "template": "排期 → 物料 → 执行 → 复盘"},
    {"id": "q78", "title": "（通用）如何设计应届生入职培训体系？", "type": "情景模拟", "difficulty": "中等", "industry": "文职", "company": "通用行政",
     "reference_answer": "需求调研 → 课程模块(文化/技能/导师制) → 考核与反馈 → 90天留存跟踪。", "template": "调研 → 模块 → 考核 → 跟踪"},
]


def build_questions():
    return EXTRA_QUESTIONS


def slug(name):
    return re.sub(r"\s+", "-", name.strip())


def main():
    jobs = build_jobs()
    questions = build_questions()

    seed_dir = os.path.join(ROOT, "app", "seed_data")
    os.makedirs(seed_dir, exist_ok=True)

    # 幂等合并：保留既有数据（如历史导入、CSV 导入的岗位/题目），按 id 去重
    def merge_write(name, fresh):
        path = os.path.join(seed_dir, name)
        existing = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                existing = json.load(f)
        seen, merged = set(), []
        for item in existing + fresh:
            if item["id"] not in seen:
                seen.add(item["id"])
                merged.append(item)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=1)
        return len(merged)

    n_jobs = merge_write("jobs.json", jobs)
    n_qs = merge_write("questions.json", questions)

    # 前端 TS（mock 数据：jobConfigs + questions 驼峰，全部来自合并后的 JSON）
    with open(os.path.join(seed_dir, "jobs.json"), encoding="utf-8") as f:
        all_jobs = json.load(f)
    with open(os.path.join(seed_dir, "questions.json"), encoding="utf-8") as f:
        all_qs = json.load(f)

    js_jobs = [{
        "id": j["id"], "name": j["name"], "company": j["company"], "industry": j["industry"],
        "duration": j["duration"], "questionTypes": j["question_types"],
        "answerMode": j["answer_mode"], "mode": j["mode"], "totalQuestions": j["total_questions"],
    } for j in all_jobs]
    js_questions = [{
        "id": q["id"], "title": q["title"], "type": q["type"], "difficulty": q["difficulty"],
        "industry": q["industry"], "company": q.get("company", ""),
        "referenceAnswer": q["reference_answer"], "template": q["template"],
    } for q in all_qs]

    def to_ts(objs):
        lines = []
        for o in objs:
            items = ",\n    ".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in o.items())
            lines.append("  {\n    " + items + "\n  }")
        return "[\n" + ",\n".join(lines) + "\n]"

    ts = (
        "// 本文件由 backend/tools/generate_seed.py 自动生成，请勿手改；修改数据后重新运行生成器。\n"
        "import type { JobConfig, QuestionItem } from '@/types'\n\n"
        f"export const seedJobs: JobConfig[] = {to_ts(js_jobs)}\n\n"
        f"export const seedQuestions: QuestionItem[] = {to_ts(js_questions)}\n"
    )
    ts_path = os.path.abspath(os.path.join(ROOT, "..", "frontend", "src", "mock", "seed_data.ts"))
    os.makedirs(os.path.dirname(ts_path), exist_ok=True)
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write(ts)

    print(f"JOBS={n_jobs}  QUESTIONS={n_qs}")
    print("OK ->", os.path.join(seed_dir, "jobs.json"))
    print("OK ->", os.path.join(seed_dir, "questions.json"))
    print("OK ->", ts_path)


if __name__ == "__main__":
    main()
