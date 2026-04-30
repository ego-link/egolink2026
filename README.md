# EgoLink 2026 Challenge

![EgoLink logo](doc/logo.png)

EgoLink (Egocentric Language-Vision Interactive Network Knowledge Challenge) is designed to advance embodied AI in complex, real-world egocentric scenarios.  
The challenge evaluates integrated intelligence across social perception, causal reasoning, intent prediction, multimodal interaction, tool use, and autonomous planning.

---

## Table of Contents

- [Intro](#intro)
- [News](#news)
- [Challenge Tasks](#challenge-tasks)
- [Dataset](#dataset)
- [Evaluation](#evaluation)
- [Important Dates](#important-dates)
- [Presentation Policy](#presentation-policy)
- [Organisers](#organisers)
- [Challenge Chairs](#challenge-chairs)
- [Contact](#contact)
- [License](#license)

---

## Intro

EgoLink goes beyond traditional navigation or static object perception benchmarks.  
It holistically tests whether an AI system can:

- Perceive emotional and social signals from egocentric streams.
- Understand causal relationships and behavioral intent in human interactions.
- Solve practical daily tasks through multimodal dialogue and tool use.
- Plan and execute actions in dynamic, unstructured social environments.

The core goal is to foster tightly coupled perception, reasoning, and decision-making for embodied intelligence.

## News

- **Apr 15, 2026**: Registration is now open. Welcome to sign up.
- **Apr 2, 2026**: Official challenge website initialized.

## Challenge Tasks

### Track 1: Social Reasoning in Egocentric Video

This track focuses on social reasoning in egocentric video, including emotional perception, causal understanding, intent prediction, and semantic summarization in real-world interactions.

It is built on E3 (Exploring Embodied Emotion) and adopts a unified MCQ-based protocol to ensure objectivity and reproducibility.

Subtasks:

1. **Emotional Perception and Localization**: Identify emotion categories and temporal boundaries.
2. **Social Causal Reasoning**: Analyze causes behind observed social emotions and responses.
3. **Behavioral Intent Prediction**: Infer likely future intentions and goals from context.
4. **Egocentric Semantic Summarization**: Select the best high-level summary from ego perspective.

### Track 2: Interactive Agent Challenge

**Multimodal Interaction Task Execution in Social Life Scenarios**

This track evaluates whether an intelligent agent can complete real-world tasks in dynamic social environments via interaction and tool use.

The agent receives first-person visual streams (for example, shopping and food-ordering scenarios), user natural-language instructions, and external tools/APIs. It must complete goals through multi-turn dialogue, accurate tool invocation, autonomous planning, and closed-loop execution.

Key capabilities:

1. **Fine-grained Egocentric Visual Understanding**: Understand temporal object states, spatial relations, and attributes such as color/shape/brand.
2. **Dynamic Tool Invocation and Execution**: Decide when and how to call tools, construct parameters from real-time visual evidence, and use returned results for next actions.
3. **Multi-hop Logical Reasoning and Complex Decision Making**: Handle constraints, ambiguity, and reference resolution in long, multi-object interactions.

## Dataset

### Track 1

- **Foundation**: Based on the E3 egocentric emotion dataset.
- **Scale**: 20,000+ egocentric clips and 70+ hours of video.
- **Coverage**: Meetings, family, education, social gatherings, and service scenarios.
- **Participants**: 500+ individuals with diverse demographics.
- **Supervision Setup**: E3 annotations plus 5,000 MCQs bridging perception and social cognition.

### Track 2

- **Foundation**: Specially constructed for multimodal interaction task execution in social-life scenarios.
- **Scale**: 1,000+ unique tasks, each with 10-20 seconds video duration.
- **Coverage**: Kitchen, retail, restaurant, and food-ordering scenarios.
- **Tools**: 100+ external tools/APIs for agent invocation and manipulation.
- **Supervision Setup**: 10,000+ structured knowledge entries (for example, product details and menus) as execution verification ground truth.

## Evaluation

### Track 1

- **Protocol**: Multi-dimensional MCQ evaluation.
- **Main Metric**: Overall Top-1 Accuracy.
- **Sub-Metrics**: Dimension-wise scores for emotion, causality, intent, and summarization.
- **Maintenance**: Website, leaderboard, and evaluation toolkit are planned to be maintained through 2029.

### Track 2

- **Protocol**: Interactive API-based evaluation with server feedback and tool invocation.
- **Main Metric**: Overall Task Success Rate (based on objective ground truth).
- **Sub-Metrics**: Tool Invocation Accuracy, Database State Accuracy, and Interaction Efficiency (turns).
- **Maintenance**: Website, leaderboard, and evaluation toolkit.

## Important Dates

### Track 1

- **2026.04.15**: E3 dataset available for pre-download.
- **2026.04.30**: Training dataset released.
- **2026.06.08**: Evaluation dataset released.
- **2026.06.22 - 2026.06.25**: Final answer and report submission window.

### Track 2

- **2026.05.25**: Online testing opens.
- **2026.06.22 - 2026.06.25**: Final answer and report submission window.

## Presentation Policy

ACM Multimedia 2026 is an **on-site only** event.  
All accepted papers and challenge contributions must be presented physically on site.  
Remote presentation is not supported. Any no-show contribution may be removed from conference proceedings.

## Organisers

- Jian Liu (Ant Group)
- Weiqiang Wang (Ant Group)
- Chang Yao (Zhejiang University)
- Jingyuan Chen (Zhejiang University)

## Challenge Chairs

- Yueying Feng (Zhejiang University)
- Bohan Yu (Ant Group)
- Renhe Sun (Ant Group)
- Zitong Wang (Ant Group)
- Tong Niu (Ant Group)
- Yunqi Liu (Ant Group)
- Haolin He (The Chinese University of Hong Kong, CUHK)
- Chang Han (Ant Group)

## Contact

- **Track 1**
  - Renhe Sun: `sunrenhe.srh@antgroup.com`
  - Bohan Yu: `ybh441692@antgroup.com`
- **Track 2**
  - Tong Niu: `niutong.niu@antgroup.com`
  - Zitong Wang: `yesi.wzt@antgroup.com`

## License

CC BY-NC-SA 4.0 for non-commercial research and education usage.

---

## Links

- Challenge Homepage: https://github.com/ego-link
- Challenge Repository: https://github.com/ego-link/egolink2026
- E3 Dataset: https://github.com/Exploring-Embodied-Emotion-official/E3/tree/main/dataset
- Registration: https://docs.google.com/forms/d/e/1FAIpQLSeNAkMcjg5znInV8X8iVy6Jx3VK4L1vH0UgHkj-UY6X81iU5w/viewform
