# 小红书口播视频工程

- 主题：Data Agent 是驶向新文明的第一艘飞船
- 规格：1280x720 横屏口播卡片视频
- 集数：EP01
- TTS：Edge `zh-CN-XiaoxiaoNeural`

生成命令：

```bash
SKILL=/Users/mac/projects/william-docs/skills/global/article-to-narrated-video-skill
cd /Users/mac/projects/william-docs/社交媒体/2026-0517-20/Xiaohongshu/data-agent-new-civilization/video
python3 $SKILL/assets/validate_shots.py EP01
bash $SKILL/assets/build_episode.sh EP01
```

成品：

```text
output/EP01.mp4
```
