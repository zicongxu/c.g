---
title: Congguo Depth Studio
summary: Offline desktop product for turning ordinary video into a branded relative-depth video
status: draft
owner: Congguo Product Team
updated: 2026-09-19
review_cycle: monthly
source_of_truth: true
confidentiality: internal
tags: [product, video-ai, depth-estimation, desktop]
related: [../../10-tools/software/congguo-depth-studio/README.md, ../../10-tools/cli/cgcli/README.md]
---

# Congguo Depth Studio (葱果深度工坊)

## Product definition

Congguo Depth Studio lets a creator select or drop an ordinary monocular video and receive a grayscale relative-depth MP4 without uploading the source. The experience is built around the Congguo character, clear three-stage progress, and in-app access to completed outputs.

## Current status

- Stage: usable prototype; human product acceptance is still required.
- Release: `2.1.0`, macOS arm64 internal build.
- Health: functional baseline verified; distribution signing/notarization and Windows packaging remain open.
- Canonical implementation and handoff: [`10-tools/software/congguo-depth-studio/`](../../10-tools/software/congguo-depth-studio/README.md).
- Automation surface: [`cgcli video depth`](../../10-tools/cli/cgcli/README.md), backed by the same processing API.

## Target users and jobs

- Video creators who need a depth-map style render for preview, compositing, or downstream experimentation.
- Internal production teams evaluating depth-based motion and visual workflows.
- Users who require local processing because the source video is private or too large to upload.

## Goals

- Make a selected video visibly acknowledged, cancellable, and easy to retrieve after processing.
- Keep processing local and independent of Codex, ChatGPT, API keys, or cloud inference.
- Produce temporally stabilized relative depth with optional source audio.
- Express the Congguo IP consistently in the icon, interface, processing state, and copy.

## Non-goals

- Metric depth measurement.
- Skeletal joints, FBX/BVH export, or full 3D motion capture.
- Multi-view reconstruction or production-grade geometry.
- Cloud collaboration, accounts, or remote asset management in the current release.

## Acceptance baseline

- Drag/drop and picker both show file name, resolution, and duration immediately.
- 24/30/60 FPS output and optional audio work on supported formats.
- Processing remains responsive and cancellable.
- A completed output appears in Recent Outputs with Play and Reveal actions.
- The layout remains operable at `680x600` and with the macOS Dock visible.
- Packaged execution completes a sanitized end-to-end sample without network access.

## Open decisions

- Name a human product owner and release owner.
- Choose controlled storage for model weights and signed release artifacts.
- Decide whether the product remains relative-depth only or later adds skeletal motion capture.
- Define Windows release priority and distribution channel.
