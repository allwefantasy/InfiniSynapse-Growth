#!/usr/bin/env bash
# AI 出图（OpenOctopus CLI）→ <bundle>/images/cover-ai.png
#
# 与 render-html-to-png.sh 的关系：
#   render-html-to-png.sh = HTML 模板渲染（首选；文字精确、可版本化）
#   generate-cover-image-ai.sh = AI 出图（互补；写实/插画风、A/B 多版、prototype）
#
# 默认输出文件名是 cover-ai.png，而不是 cover.png/hero-*.png，
# 避免覆盖团队已有的 HTML 渲染产物。
#
# Usage:
#   # 单篇（按 slug；slug 即 SEO/Blog/ 下的目录名）
#   bash SEO/Blog/scripts/generate-cover-image-ai.sh 2026-05-19-data-agent-new-civilization
#
#   # 跑全部带 prompts/cover.prompt 的 bundle
#   bash SEO/Blog/scripts/generate-cover-image-ai.sh all
#
#   # 直接给 prompt（不用 prompt 文件）
#   bash SEO/Blog/scripts/generate-cover-image-ai.sh 2026-05-19-foo --prompt "A cinematic ..."
#
# 常用 flags:
#   --model openoctopus/imagen-4 | openoctopus/nano-banana-pro | openoctopus/imagen-4-fast | ...
#   --aspect-ratio 16:9 | 1:1 | 4:3 | 9:16 | 3:4
#   --resolution 1k | 2k | 4k          (4k 仅 nano-banana-pro 支持)
#   --output-name cover-ai.png         (默认；可改成 hero-ai.png 等)
#   --prompt-file path/to.prompt       (覆盖默认 prompts/cover.prompt)
#   --prompt "inline prompt"           (覆盖文件方式)
#   --force                            (允许覆盖已有图)
#   --dry-run                          (只打印命令、估价，不执行)
#
# 价格速查（2026-05 抓取自 ooct models inspect）：
#   imagen-4              $0.038 / 张
#   imagen-4-fast         $0.038 / 张（更快）
#   imagen-3 / 3-fast     极便宜
#   nano-banana-2         $0.045–0.14 / 张
#   nano-banana-pro       $0.14（1k/2k）/ $0.24（4k）/ 张
#   gpt-image-2-text-input  按提供商定价
#
# 约定：prompts/cover.prompt 是纯文本（可多行），整份内容会作为 --prompt 单参数传入。
# 文件顶部连续的 `# ` 注释行 + 紧随其后的空行会被剥离，剩余正文原样保留。
#
# 强制规则（English-only）：
#   - 剥离注释后的 prompt 正文必须是英文（不允许 CJK 字符与中文标点）。
#   - prompt 里务必写 "no text, no lettering, no logos"，避免 AI 在图里乱涂中英文字。
#   - 中文注释/经验/标题写在 `# ` 注释行里没问题，会被自动剥离。
#   - --prompt 内联参数同样会被检查；含中文将直接拒跑。

set -euo pipefail

ROOT="/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth"
BLOG_ROOT="$ROOT/SEO/Blog"

DEFAULT_MODEL="openoctopus/imagen-4"
DEFAULT_ASPECT="16:9"
DEFAULT_RESOLUTION="2k"
DEFAULT_OUTPUT_NAME="cover-ai.png"

MODEL="$DEFAULT_MODEL"
ASPECT="$DEFAULT_ASPECT"
RESOLUTION="$DEFAULT_RESOLUTION"
OUTPUT_NAME="$DEFAULT_OUTPUT_NAME"
PROMPT_INLINE=""
PROMPT_FILE_OVERRIDE=""
FORCE=0
DRY_RUN=0
TARGETS=()

usage() {
  sed -n '2,46p' "$0"
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)            usage 0 ;;
    --model)              MODEL="$2"; shift 2 ;;
    --aspect-ratio)       ASPECT="$2"; shift 2 ;;
    --resolution)         RESOLUTION="$2"; shift 2 ;;
    --output-name)        OUTPUT_NAME="$2"; shift 2 ;;
    --prompt)             PROMPT_INLINE="$2"; shift 2 ;;
    --prompt-file)        PROMPT_FILE_OVERRIDE="$2"; shift 2 ;;
    --force)              FORCE=1; shift ;;
    --dry-run)            DRY_RUN=1; shift ;;
    --) shift; while [[ $# -gt 0 ]]; do TARGETS+=("$1"); shift; done ;;
    -*) echo "❌ 未知 flag: $1"; usage 1 ;;
    *)  TARGETS+=("$1"); shift ;;
  esac
done

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "❌ 缺少目标。用法：bash $0 <slug|all> [flags]"
  usage 1
fi

if ! command -v ooct >/dev/null 2>&1; then
  echo "❌ 未找到 ooct。先装 CLI：sudo npm i -g @openoctopus/cli"
  exit 1
fi

if ! ooct auth status 2>/dev/null | grep -q "Authenticated."; then
  echo "❌ 未登录。先跑：ooct auth login"
  exit 1
fi

# 单价（USD/张）
price_for() {
  case "$1" in
    openoctopus/imagen-4|openoctopus/imagen-4-fast)        echo 0.038 ;;
    openoctopus/imagen-3|openoctopus/imagen-3-fast)        echo 0.020 ;;
    openoctopus/nano-banana-pro)
      case "$RESOLUTION" in 4k) echo 0.24 ;; *) echo 0.14 ;; esac ;;
    openoctopus/nano-banana-2)                             echo 0.07 ;;
    openoctopus/nano-banana)                               echo 0.045 ;;
    openoctopus/gpt-image-2-text-input)                    echo 0.05 ;;
    *)                                                     echo 0.05 ;;
  esac
}

read_prompt() {
  local file="$1"
  # 剥离文件顶部的 `# ` / `#` 注释块 + 紧随其后的空行；之后的内容原样输出
  awk '
    BEGIN { header = 1 }
    header && /^#($| )/ { next }
    header && /^[[:space:]]*$/ { next }
    { header = 0; print }
  ' "$file"
}

# 检测 stdin 中是否包含 CJK 字符（中日韩统一表意 + 中文标点 + 全角字符）。
# 命中（含 CJK）→ exit 0；未命中（纯英文）→ exit 1。
contains_cjk_stdin() {
  perl -CS -e '
    my $t; { local $/; $t = <STDIN>; }
    exit($t =~ /[\x{3000}-\x{303f}\x{3400}-\x{4dbf}\x{4e00}-\x{9fff}\x{ff00}-\x{ffef}]/ ? 0 : 1);
  '
}

# 内联 prompt 必须英文（函数定义之后才能调用）
if [[ -n "$PROMPT_INLINE" ]]; then
  if printf '%s' "$PROMPT_INLINE" | contains_cjk_stdin; then
    echo "❌ --prompt 内联文本含 CJK 字符（中文/中文标点）。"
    echo "   规则：所有 AI 出图 prompt 必须是英文（避免模型乱涂字、走形）。"
    exit 1
  fi
fi

# 展开目标 slug 列表（兼容 macOS bash 3.2，不用 mapfile）
SLUGS=()
for t in "${TARGETS[@]}"; do
  if [[ "$t" == "all" ]]; then
    while IFS= read -r p; do
      [[ -z "$p" ]] && continue
      d="$(dirname "$(dirname "$p")")"
      SLUGS+=("$(basename "$d")")
    done < <(find "$BLOG_ROOT" -mindepth 3 -maxdepth 3 -type f -path '*/prompts/cover.prompt' 2>/dev/null | sort)
  else
    SLUGS+=("$t")
  fi
done

if [[ ${#SLUGS[@]} -eq 0 ]]; then
  echo "ℹ️  没有匹配的 slug。"
  exit 0
fi

# 跑批前先打印计划 + 估价
total_price="0"
PLAN=()
for slug in "${SLUGS[@]}"; do
  bundle="$BLOG_ROOT/$slug"
  if [[ ! -d "$bundle" ]]; then
    PLAN+=("SKIP|$slug|目录不存在")
    continue
  fi

  prompt_path=""
  if [[ -n "$PROMPT_INLINE" ]]; then
    prompt_path="(inline)"
  elif [[ -n "$PROMPT_FILE_OVERRIDE" ]]; then
    prompt_path="$PROMPT_FILE_OVERRIDE"
  elif [[ -f "$bundle/prompts/cover.prompt" ]]; then
    prompt_path="$bundle/prompts/cover.prompt"
  fi

  if [[ -z "$prompt_path" ]]; then
    PLAN+=("SKIP|$slug|缺少 prompt（既无 --prompt / --prompt-file，也无 prompts/cover.prompt）")
    continue
  fi

  # 文件 prompt 走 CJK 检查（内联 prompt 已在前面检查过一次性）
  if [[ "$prompt_path" != "(inline)" ]]; then
    if read_prompt "$prompt_path" | contains_cjk_stdin; then
      PLAN+=("SKIP|$slug|prompt 含 CJK（规则：英文 only；中文写在 # 注释里会被剥离）")
      continue
    fi
  fi

  out_png="$bundle/images/$OUTPUT_NAME"
  if [[ -f "$out_png" && $FORCE -ne 1 ]]; then
    PLAN+=("SKIP|$slug|已存在 $OUTPUT_NAME（加 --force 覆盖）")
    continue
  fi

  price="$(price_for "$MODEL")"
  total_price="$(awk -v a="$total_price" -v b="$price" 'BEGIN{printf "%.3f", a+b}')"
  PLAN+=("RUN|$slug|$prompt_path|$out_png|$price")
done

echo "──────── 计划 ────────"
echo "  模型      : $MODEL"
echo "  aspect    : $ASPECT"
echo "  resolution: $RESOLUTION"
echo "  输出文件名: $OUTPUT_NAME"
echo "  目标数    : ${#SLUGS[@]}"
echo "  预估总价  : \$$total_price USD"
echo ""
for line in ${PLAN[@]+"${PLAN[@]}"}; do
  IFS='|' read -r action slug rest1 rest2 rest3 <<<"$line"
  case "$action" in
    RUN)  printf "  ✓ %-60s prompt=%s  (\$%s)\n" "$slug" "$(basename "$rest1")" "$rest3" ;;
    SKIP) printf "  - %-60s %s\n" "$slug" "$rest1" ;;
  esac
done
echo ""

run_count=0
for line in ${PLAN[@]+"${PLAN[@]}"}; do [[ "$line" == RUN\|* ]] && run_count=$((run_count+1)); done

if [[ $run_count -eq 0 ]]; then
  echo "ℹ️  没有需要执行的任务。"
  exit 0
fi

if [[ $DRY_RUN -eq 1 ]]; then
  echo "(dry-run) 退出。"
  exit 0
fi

# 跑批 ≥2 张或单价 ≥$0.20 的，都先确认
need_confirm=0
[[ $run_count -ge 2 ]] && need_confirm=1
awk -v p="$(price_for "$MODEL")" 'BEGIN{exit !(p+0 >= 0.20)}' && need_confirm=1
if [[ $need_confirm -eq 1 ]]; then
  read -r -p "确认提交 $run_count 张图（约 \$$total_price）？[y/N] " ans
  ans_lc="$(printf '%s' "$ans" | tr '[:upper:]' '[:lower:]')"
  [[ "$ans_lc" == "y" || "$ans_lc" == "yes" ]] || { echo "已取消。"; exit 0; }
fi

# 真正执行
for line in ${PLAN[@]+"${PLAN[@]}"}; do
  [[ "$line" == RUN\|* ]] || continue
  IFS='|' read -r _ slug prompt_path out_png _ <<<"$line"

  if [[ -n "$PROMPT_INLINE" ]]; then
    prompt_text="$PROMPT_INLINE"
  else
    prompt_text="$(read_prompt "$prompt_path")"
  fi

  mkdir -p "$(dirname "$out_png")"

  echo "▶ $slug"
  echo "    model : $MODEL"
  echo "    out   : $out_png"
  echo "    prompt: $(echo "$prompt_text" | head -c 120 | tr '\n' ' ')…"

  set +e
  ooct run "$MODEL" \
    --prompt "$prompt_text" \
    --aspect-ratio "$ASPECT" \
    --resolution "$RESOLUTION" \
    --output "$out_png"
  rc=$?
  set -e

  if [[ $rc -eq 0 && -f "$out_png" ]]; then
    sz="$(sips -g pixelWidth -g pixelHeight "$out_png" 2>/dev/null | awk '/pixel/ {print $2}' | xargs | tr ' ' 'x' || echo "?")"
    echo "  ✅ $out_png  ($sz)"
  else
    echo "  ❌ 失败（exit=$rc）"
  fi
  echo ""
done

echo "✅ 全部完成。"
