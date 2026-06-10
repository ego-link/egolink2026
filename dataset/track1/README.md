# Track 1 Dataset

## Overview

Track 1 is built on [E3 (Exploring Embodied Emotion)](https://github.com/Exploring-Embodied-Emotion-official/E3) and adopts a unified MCQ-based protocol to ensure objectivity and reproducibility.

**Video source:** All video clips come from the [E3 Dataset](https://github.com/Exploring-Embodied-Emotion-official/E3/tree/main/dataset). On top of E3, we performed careful dataset design and annotation for the EgoLink Track 1 challenge.

**Important:** Please use the E3 video data together with our label and MCQ files. **Do not use the original labels from the E3 dataset.**

## Files

| File | Description |
|------|-------------|
| [`E3_train.json`](E3_train.json) | **Part 1 — Labels.** Updated training labels paired with E3 videos. Each entry includes video path, person, emotion, temporal boundaries, sentiment/degree, and textual reason annotations. |
| [`train_MCQ.jsonl`](train_MCQ.jsonl) | **Part 2 — Training MCQ.** Curated multiple-choice questions for model training, covering social reasoning dimensions such as emotional perception, causal reasoning, intent prediction, and egocentric summarization. |
| [`val_MCQ.jsonl`](val_MCQ.jsonl) | **Validation MCQ.** Multiple-choice questions for local validation during development. |

Each MCQ record typically includes `id`, `question`, `choices`, `answer`, `question_type`, `path` (relative to the E3 video root), and `annotation_difficulty`.

## Usage Notes

1. Download the E3 videos from the [E3 dataset repository](https://github.com/Exploring-Embodied-Emotion-official/E3/tree/main/dataset).
2. Align video paths in our JSON/JSONL files with your local E3 video directory.
3. Use `E3_train.json` and `train_MCQ.jsonl` together for training.
4. Use `val_MCQ.jsonl` to validate your approach before final submission.

**Please note:** The validation set (`val_MCQ.jsonl`) is a **subset of the complete evaluation set**. It is intended for development and sanity checks only; final leaderboard scoring uses the held-out evaluation set released separately according to the challenge timeline.
