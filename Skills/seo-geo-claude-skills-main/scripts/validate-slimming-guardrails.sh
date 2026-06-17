#!/usr/bin/env bash
# validate-slimming-guardrails.sh — semantic regression checks for repository slimming passes.
#
# This script protects high-value discovery aliases, runtime contracts, and
# copy-start templates that generic markdown/YAML validation cannot understand.

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

green='\033[0;32m'
red='\033[0;31m'
nc='\033[0m'

pass() {
  printf "%bPASS%b %s\n" "$green" "$nc" "$1"
  PASS=$((PASS + 1))
}

fail() {
  printf "%bFAIL%b %s\n" "$red" "$nc" "$1"
  FAIL=$((FAIL + 1))
}

require_file() {
  local file="$1"
  if [ -f "$ROOT/$file" ]; then
    pass "$file exists"
  else
    fail "$file exists"
  fi
}

require_text() {
  local file="$1"
  local text="$2"
  local label="$3"

  if grep -Fqi -- "$text" "$ROOT/$file" 2>/dev/null; then
    pass "$label"
  else
    fail "$label (missing '$text' in $file)"
  fi
}

require_frontmatter_text() {
  local file="$1"
  local text="$2"
  local label="$3"

  if awk 'BEGIN{n=0} /^---/{n++; next} n==1{print}' "$ROOT/$file" | grep -Fqi -- "$text"; then
    pass "$label"
  else
    fail "$label (missing '$text' in $file frontmatter)"
  fi
}

require_section_text() {
  local file="$1"
  local heading="$2"
  local text="$3"
  local label="$4"
  local section

  section="$(awk -v h="$heading" '$0==h{found=1; next} found && /^## /{exit} found{print}' "$ROOT/$file" 2>/dev/null)"
  if [ -z "$section" ]; then
    fail "$label (missing section '$heading' in $file)"
  elif printf "%s\n" "$section" | grep -Fqi -- "$text"; then
    pass "$label"
  else
    fail "$label (missing '$text' in $file section '$heading')"
  fi
}

forbid_regex() {
  local file="$1"
  local pattern="$2"
  local label="$3"

  if grep -Eq -- "$pattern" "$ROOT/$file" 2>/dev/null; then
    fail "$label (matched '$pattern' in $file)"
  else
    pass "$label"
  fi
}

forbid_regex_i() {
  local file="$1"
  local pattern="$2"
  local label="$3"

  if grep -Eiq -- "$pattern" "$ROOT/$file" 2>/dev/null; then
    fail "$label (matched '$pattern' in $file)"
  else
    pass "$label"
  fi
}

forbid_normalized_memory_write_path() {
  local file="$1"
  local label="$2"

  if FILE="$ROOT/$file" ruby <<'RUBY'
text = File.read(ENV.fetch("FILE")).downcase.delete("`")
text = text.gsub(%r{\s*/\s*}, "/").gsub(/[ \t]+/, " ")
verbs = /\b(save|append|write|persist|modify|create|update|record|store)\b/
memory_path = /memory\/evolution|memory\/[^\n]*evolution\/?|memory[^\n]*evolution\//
bad = text.lines.any? do |line|
  line.match?(verbs) && line.match?(memory_path) ||
    line.match?(/save\s+.*as\s+a\s+proposed\s+record/)
end
exit bad ? 1 : 0
RUBY
  then
    pass "$label"
  else
    fail "$label (normalized write path found in $file)"
  fi
}

require_equal() {
  local actual="$1"
  local expected="$2"
  local label="$3"

  if [ "$actual" = "$expected" ]; then
    pass "$label"
  else
    fail "$label (expected '$expected', got '${actual:-<empty>}')"
  fi
}

require_command_frontmatter_yaml() {
  local label="$1"

  if ! command -v ruby >/dev/null 2>&1; then
    fail "$label (ruby is required for command YAML parsing)"
    return
  fi

  if ROOT="$ROOT" ruby <<'RUBY'
require "yaml"

root = ENV.fetch("ROOT")
Dir[File.join(root, "commands", "*.md")].sort.each do |path|
  text = File.read(path)
  parts = text.split(/^---\s*$/, 3)
  raise "#{path}: missing frontmatter" unless parts.length >= 3 && parts[1]

  data = YAML.safe_load(parts[1], permitted_classes: [], aliases: false)
  raise "#{path}: frontmatter is not a mapping" unless data.is_a?(Hash)

  %w[name description argument-hint].each do |key|
    raise "#{path}: missing #{key}" if data[key].nil? || data[key].to_s.strip.empty?
  end

  expected_name = File.basename(path, ".md")
  raise "#{path}: name must match filename #{expected_name}" unless data["name"] == expected_name

  if data.key?("allowed-tools")
    raise "#{path}: allowed-tools must be a list" unless data["allowed-tools"].is_a?(Array)
    data["allowed-tools"].each do |tool|
      raise "#{path}: allowed-tools entries must be strings" unless tool.is_a?(String) && !tool.strip.empty?
    end
  end

  if data.key?("parameters")
    raise "#{path}: parameters must be a list" unless data["parameters"].is_a?(Array)
    data["parameters"].each_with_index do |param, index|
      raise "#{path}: parameter #{index + 1} must be a mapping" unless param.is_a?(Hash)
      %w[name type required description].each do |key|
        raise "#{path}: parameter #{index + 1} missing #{key}" unless param.key?(key)
      end
      raise "#{path}: parameter #{index + 1} required must be boolean" unless param["required"] == true || param["required"] == false
    end
  end
end
RUBY
  then
    pass "$label"
  else
    fail "$label"
  fi
}

require_command_inventory_exact() {
  local label="$1"
  local expected actual missing unexpected

  expected="$(printf "%s\n" \
    audit-domain.md \
    audit-page.md \
    check-technical.md \
    contract-lint.md \
    evolve-skill.md \
    generate-schema.md \
    geo-drift-check.md \
    keyword-research.md \
    optimize-meta.md \
    report.md \
    run-evals.md \
    setup-alert.md \
    skillify.md \
    sync-versions.md \
    validate-library.md \
    wiki-lint.md \
    write-content.md | sort)"
  actual="$(find "$ROOT/commands" -maxdepth 1 -type f -name '*.md' -exec basename {} \; | sort)"
  missing="$(comm -23 <(printf "%s\n" "$expected") <(printf "%s\n" "$actual"))"
  unexpected="$(comm -13 <(printf "%s\n" "$expected") <(printf "%s\n" "$actual"))"

  if [ -z "$missing" ] && [ -z "$unexpected" ]; then
    pass "$label"
  else
    fail "$label (missing: ${missing:-none}; unexpected: ${unexpected:-none})"
  fi
}

require_command_section_text() {
  local file="$1"
  local start_pattern="$2"
  local end_pattern="$3"
  local label="$4"
  shift 4
  local expected found missing unexpected
  local section

  section="$(awk -v start="$start_pattern" -v end="$end_pattern" '
    $0 ~ start { found=1; print; next }
    found && $0 ~ end { exit }
    found { print }
  ' "$ROOT/$file" 2>/dev/null)"

  if [ -z "$section" ]; then
    fail "$label (section not found in $file)"
    return
  fi

  expected="$(printf "%s\n" "$@" | sort -u)"
  found="$(printf "%s\n" "$section" | grep -Eo '/seo:[a-z0-9-]+' | sed 's#/seo:##' | sort -u)"
  missing="$(comm -23 <(printf "%s\n" "$expected") <(printf "%s\n" "$found"))"
  unexpected="$(comm -13 <(printf "%s\n" "$expected") <(printf "%s\n" "$found"))"

  if [ -z "$missing" ] && [ -z "$unexpected" ]; then
    pass "$label"
  else
    fail "$label (missing: ${missing:-none}; unexpected: ${unexpected:-none})"
  fi
}

require_no_retired_p2_references() {
  local label="$1"
  local hits

  hits="$(grep -RInE '/seo:p2-review|commands/p2-review\.md|memory/p2-review' "$ROOT" \
    --exclude-dir=.git \
    --exclude='validate-slimming-guardrails.sh' \
    --exclude='VERSIONS.md' 2>/dev/null || true)"

  if [ -z "$hits" ]; then
    pass "$label"
  else
    fail "$label (stale references: $hits)"
  fi
}

require_run_evals_template_boundary() {
  local label="$1"

  if FILE="$ROOT/commands/run-evals.md" ruby <<'RUBY'
require "yaml"

text = File.read(ENV.fetch("FILE"))
fence_re = /^[ \t]{0,3}```([^\n]*)\n(.*?)^[ \t]{0,3}```\s*$/m
text.scan(fence_re).each_with_index do |(info, body), index|
  fence = info.strip.downcase
  next unless fence.empty? || fence == "yaml" || fence == "yml"
  next unless body.match?(/(^|\n)\s*validation_results\s*:/)

  begin
    data = YAML.safe_load(body, aliases: false)
  rescue Psych::Exception => error
    raise "commands/run-evals.md validation_results block #{index + 1} does not parse: #{error.message}"
  end

  results = data.is_a?(Hash) ? data["validation_results"] : nil
  next unless results.is_a?(Hash)
  status = results["status"].to_s
  reason = results.key?("non_validating_reason") ? results["non_validating_reason"].to_s : ""
  unless results["acceptance_eligible"] == true || results["acceptance_eligible"] == false
    raise "commands/run-evals.md validation_results block #{index + 1} has non-boolean acceptance_eligible"
  end
  if status == "passed" && (results["acceptance_eligible"] != true || !reason.strip.empty?)
    raise "commands/run-evals.md validation_results block #{index + 1} allows passed non-validating output"
  end
end
RUBY
  then
    pass "$label"
  else
    fail "$label (run-evals template allows status: passed with non-eligible or non-validating validation_results)"
  fi
}

require_eval_case_count() {
  local min_count="$1"
  local label="$2"
  local count

  if ! command -v ruby >/dev/null 2>&1; then
    fail "$label (ruby is required for eval YAML parsing)"
    return
  fi

  if count="$(ROOT="$ROOT" ruby <<'RUBY'
require "yaml"

root = ENV.fetch("ROOT")
count = 0
Dir[File.join(root, "evals", "*", "cases.md")].sort.each do |path|
  File.read(path).scan(/^[ \t]{0,3}```([^\n]*)\n(.*?)^[ \t]{0,3}```\s*$/m) do |info, body|
    next unless info.strip.downcase.match?(/\Ayaml\z/)
    data = YAML.safe_load(body, aliases: false)
    count += 1 if data.is_a?(Hash) && data["type"] == "eval-case"
  end
end
puts count
RUBY
)"; then
    if [ "${count:-0}" -ge "$min_count" ]; then
      pass "$label"
    else
      fail "$label (expected >= $min_count eval cases, got ${count:-0})"
    fi
  else
    fail "$label (cannot parse eval cases)"
  fi
}

require_routing_eval_targets() {
  local min_count="$1"
  local label="$2"
  local count

  if ! command -v ruby >/dev/null 2>&1; then
    fail "$label (ruby is required for routing eval parsing)"
    return
  fi

  if count="$(ROOT="$ROOT" ruby <<'RUBY'
require "yaml"

root = ENV.fetch("ROOT")
skills = Dir[File.join(root, "{research,build,optimize,monitor,cross-cutting}", "*", "SKILL.md")]
  .map { |path| File.basename(File.dirname(path)) }
count = 0
Dir[File.join(root, "evals", "*", "cases.md")].sort.each do |path|
  File.read(path).scan(/^[ \t]{0,3}```([^\n]*)\n(.*?)^[ \t]{0,3}```\s*$/m) do |info, body|
    next unless info.strip.downcase.match?(/\Ayml|yaml\z/)
    data = YAML.safe_load(body, aliases: false)
    next unless data.is_a?(Hash) && data["id"].to_s.start_with?("routing-")
    raise "#{path}: routing case #{data["id"]} must use type: eval-case" unless data["type"] == "eval-case"
    raise "#{path}: routing case #{data["id"]} target_skill must be an existing skill" unless skills.include?(data["target_skill"])
    raise "#{path}: routing case #{data["id"]} expected_behavior must be a non-empty list" unless data["expected_behavior"].is_a?(Array) && data["expected_behavior"].any?
    count += 1
  end
end
puts count
RUBY
)"; then
    if [ "${count:-0}" -ge "$min_count" ]; then
      pass "$label"
    else
      fail "$label (expected >= $min_count routing eval cases, got ${count:-0})"
    fi
  else
    fail "$label (cannot parse routing eval cases)"
  fi
}

require_evolution_events_parser_grade() {
  local file="$1"
  local label="$2"

  if ! command -v ruby >/dev/null 2>&1; then
    fail "$label (ruby is required for parser-grade EvolutionEvent validation)"
    return
  fi

  if FILE="$ROOT/$file" ruby <<'RUBY'
require "yaml"

path = ENV.fetch("FILE")
text = File.read(path)
event_keys = %w[
  id type simulation target event_type source_signal objective proposed_change
  risk validation_plan validation_results rollback decision
]
source_kinds = %w[
  user_feedback audit_failure geo_drift contract_lint validate_library
  eval_failure handoff_gap stale_reference external_research
  maintainer_observation agent_observation simulation
]
project_local_source_kinds = source_kinds - %w[external_research simulation]
decision_statuses = %w[proposed accepted rejected superseded]
risk_levels = %w[low medium high protocol]
validation_statuses = %w[passed failed mixed not_run]
target_kinds = %w[skill command protocol reference]
change_scopes = %w[description when_to_use handoff instructions references command protocol]

def blank_or_absent?(value)
  return true if value.nil?
  value.to_s.strip.empty?
end

def string_list?(value)
  value.is_a?(Array) && value.any? && value.all? { |item| item.is_a?(String) && !item.strip.empty? }
end

def nonblank_string?(value)
  value.is_a?(String) && !value.strip.empty?
end

def require_mapping!(path, index, data, key)
  fail_event!(path, index, "#{key} must be a mapping") unless data[key].is_a?(Hash)
end

def fail_event!(path, index, message)
  raise "#{path}: EvolutionEvent block #{index}: #{message}"
end

event_key_pattern = /(^|\n)[ \t]{0,3}(#{event_keys.map { |key| Regexp.escape(key) }.join("|")})\s*:/
event_shape_pattern = /(^|\n)[ \t]{0,3}(type\s*:\s*evolution-event|source_signal|proposed_change|validation_results|rollback|decision)\s*:/
fence_re = /^[ \t]{0,3}```([^\n]*)\n(.*?)^[ \t]{0,3}```\s*$/m
outside = text.gsub(fence_re, "\n").sub(/\A---\s*\n.*?^---\s*\n/m, "\n")
fail_event!(path, 0, "event-shaped YAML appears outside fenced YAML block") if outside.match?(event_shape_pattern)

text.scan(fence_re).each_with_index do |(info, body), index|
  fence = info.strip.downcase
  next unless fence.empty? || fence == "yaml" || fence == "yml"

  data = nil
  begin
    data = YAML.safe_load(body, aliases: false)
  rescue Psych::Exception => error
    if fence == "yaml" || fence == "yml" || body.match?(event_key_pattern)
      fail_event!(path, index + 1, "event-shaped YAML does not parse: #{error.message}")
    end
    next
  end

  body_event_like = body.match?(event_key_pattern)
  unless data.is_a?(Hash)
    fail_event!(path, index + 1, "event-shaped YAML must be a mapping") if body_event_like
    next
  end

  keys = data.keys.map(&:to_s)
  event_like = body_event_like || keys.any? { |key| event_keys.include?(key) }
  next unless event_like

  event_keys.each do |key|
    fail_event!(path, index + 1, "missing #{key}") unless data.key?(key)
  end

  fail_event!(path, index + 1, "missing type: evolution-event") unless data["type"] == "evolution-event"
  %w[id event_type objective].each do |key|
    fail_event!(path, index + 1, "#{key} must be a non-empty string") unless nonblank_string?(data[key])
  end
  fail_event!(path, index + 1, "simulation must be boolean") unless data["simulation"] == true || data["simulation"] == false

  source_signal = data["source_signal"]
  source_kind = source_signal.is_a?(Hash) ? source_signal["kind"].to_s : ""
  require_mapping!(path, index + 1, data, "source_signal")
  fail_event!(path, index + 1, "source_signal.kind is missing or invalid") unless source_kinds.include?(source_kind)
  fail_event!(path, index + 1, "source_signal.evidence must be a non-empty string list") unless string_list?(source_signal["evidence"])

  %w[target risk validation_plan validation_results rollback decision].each do |key|
    require_mapping!(path, index + 1, data, key)
  end

  fail_event!(path, index + 1, "target.kind is missing or invalid") unless target_kinds.include?(data.dig("target", "kind").to_s)
  %w[name path].each do |key|
    fail_event!(path, index + 1, "target.#{key} must be a non-empty string") unless nonblank_string?(data.dig("target", key))
  end

  fail_event!(path, index + 1, "proposed_change must be a mapping") unless data["proposed_change"].is_a?(Hash)
  fail_event!(path, index + 1, "proposed_change.summary must be a non-empty string") unless nonblank_string?(data.dig("proposed_change", "summary"))
  fail_event!(path, index + 1, "proposed_change.files_touched must be a non-empty string list") unless string_list?(data.dig("proposed_change", "files_touched"))
  fail_event!(path, index + 1, "proposed_change.scope is missing or invalid") unless change_scopes.include?(data.dig("proposed_change", "scope").to_s)

  risk_level = data.dig("risk", "level").to_s
  fail_event!(path, index + 1, "risk.level is missing or invalid") unless risk_levels.include?(risk_level)
  fail_event!(path, index + 1, "risk.blast_radius must be a non-empty string") unless nonblank_string?(data.dig("risk", "blast_radius"))

  fail_event!(path, index + 1, "validation_plan.required must be a non-empty string list") unless string_list?(data.dig("validation_plan", "required"))
  if data["validation_plan"].key?("eval_cases") && !string_list?(data.dig("validation_plan", "eval_cases"))
    fail_event!(path, index + 1, "validation_plan.eval_cases must be a non-empty string list when present")
  end

  result_status = data.dig("validation_results", "status").to_s
  fail_event!(path, index + 1, "validation_results.status is missing or invalid") unless validation_statuses.include?(result_status)
  fail_event!(path, index + 1, "validation_results.evidence must be a non-empty string list") unless string_list?(data.dig("validation_results", "evidence"))
  unless data.dig("validation_results", "acceptance_eligible") == true || data.dig("validation_results", "acceptance_eligible") == false
    fail_event!(path, index + 1, "validation_results.acceptance_eligible must be boolean")
  end
  if data["validation_results"].key?("non_validating_reason") && !data.dig("validation_results", "non_validating_reason").is_a?(String)
    fail_event!(path, index + 1, "validation_results.non_validating_reason must be a string when present")
  end
  fail_event!(path, index + 1, "rollback.previous_ref must be a non-empty string") unless nonblank_string?(data.dig("rollback", "previous_ref"))
  fail_event!(path, index + 1, "rollback.revert_scope must be a non-empty string") unless nonblank_string?(data.dig("rollback", "revert_scope"))

  decision_status = data.dig("decision", "status").to_s
  fail_event!(path, index + 1, "decision.status is missing or invalid") unless decision_statuses.include?(decision_status)
  fail_event!(path, index + 1, "decision.approved_by is missing or invalid") unless %w[user maintainer skill_inferred].include?(data.dig("decision", "approved_by").to_s)
  fail_event!(path, index + 1, "decision.rationale must be a non-empty string") unless nonblank_string?(data.dig("decision", "rationale"))

  if decision_status == "accepted"
    fail_event!(path, index + 1, "accepted events must use simulation: false") unless data["simulation"] == false
    fail_event!(path, index + 1, "accepted events require project-local source_signal.kind") unless project_local_source_kinds.include?(source_kind)
    fail_event!(path, index + 1, "accepted events require approved_by: user or maintainer") unless %w[user maintainer].include?(data.dig("decision", "approved_by").to_s)
    fail_event!(path, index + 1, "accepted events require validation_results.status: passed") unless result_status == "passed"
    fail_event!(path, index + 1, "accepted events require validation_results.acceptance_eligible: true") unless data.dig("validation_results", "acceptance_eligible") == true
    fail_event!(path, index + 1, "accepted events must not carry non_validating_reason") unless blank_or_absent?(data.dig("validation_results", "non_validating_reason"))
  end
end
RUBY
  then
    pass "$label"
  else
    fail "$label"
  fi
}

require_auditor_skill_validation() {
  local skill="$1"
  local label="$2"

  if bash "$ROOT/scripts/validate-skill.sh" "$skill" >/dev/null 2>&1; then
    pass "$label"
  else
    fail "$label"
  fi
}

require_json_equal() {
  local file="$1"
  local expr="$2"
  local expected="$3"
  local label="$4"
  local actual

  if ! actual="$(jq -r "$expr" "$ROOT/$file" 2>/dev/null)"; then
    fail "$label (cannot read $expr from $file)"
    return
  fi

  if [ "$actual" = "$expected" ]; then
    pass "$label"
  else
    fail "$label (expected '$expected', got '$actual')"
  fi
}

discover_skill_paths() {
  local category
  for category in research build optimize monitor cross-cutting; do
    [ -d "$ROOT/$category" ] || continue
    find "$ROOT/$category" -mindepth 2 -maxdepth 2 -name "SKILL.md" -print \
      | sed "s#^$ROOT/##; s#/SKILL.md\$##; s#^#./#" \
      | sort
  done
}

require_skill_inventory_text() {
  local file="$1"
  local label="$2"
  local missing=""
  local skill_path skill_name

  while IFS= read -r skill_path; do
    skill_name="${skill_path##*/}"
    if ! grep -Fq -- "$skill_name" "$ROOT/$file" 2>/dev/null; then
      missing="${missing:+$missing, }$skill_name"
    fi
  done < <(discover_skill_paths)

  if [ -z "$missing" ]; then
    pass "$label"
  else
    fail "$label (missing: $missing)"
  fi
}

require_resolver_coverage() {
  local label="$1"

  if [ ! -f "$ROOT/references/skill-resolver.md" ]; then
    fail "$label (references/skill-resolver.md missing)"
    return
  fi

  if ROOT="$ROOT" ruby <<'RUBY'
root = ENV.fetch("ROOT")
skill_paths = Dir[File.join(root, "{research,build,optimize,monitor,cross-cutting}", "*", "SKILL.md")].sort
skills = skill_paths.map { |path| File.basename(File.dirname(path)) }
resolver = File.read(File.join(root, "references", "skill-resolver.md"))

rows = resolver.lines.map do |line|
  next unless line.start_with?("| ")
  fields = line.split("|").map(&:strip)
  next if fields[1] == "User intent" || fields[1].start_with?("---")
  next unless fields.length >= 8
  {
    primary: fields[3],
    adjacent: fields[5].split(",").map(&:strip).reject(&:empty?)
  }
end.compact

primary_counts = Hash.new(0)
rows.each { |row| primary_counts[row[:primary]] += 1 }

missing = skills.reject { |skill| primary_counts[skill] == 1 }
extra_primary = primary_counts.keys.reject { |skill| skills.include?(skill) }
bad_adjacent = rows.flat_map { |row| row[:adjacent] }.uniq.reject { |skill| skills.include?(skill) }

next_best_missing = []
skill_paths.each do |path|
  skill = File.basename(File.dirname(path))
  row = rows.find { |item| item[:primary] == skill }
  next unless row
  text = File.read(path)
  section = text[/^## Next Best Skill\n(.*?)(?=^## |\z)/m, 1].to_s
  next_best = section.scan(%r{/(?:research|build|optimize|monitor|cross-cutting)/([^/]+)/SKILL\.md}).flatten.uniq
  missing_next = next_best - row[:adjacent]
  next_best_missing << "#{skill}: #{missing_next.join(", ")}" if missing_next.any?
end

errors = []
errors << "missing or duplicate primary route: #{missing.join(", ")}" if missing.any?
errors << "unknown primary route: #{extra_primary.join(", ")}" if extra_primary.any?
errors << "unknown adjacent skills: #{bad_adjacent.join(", ")}" if bad_adjacent.any?
errors << "missing Next Best Skill links: #{next_best_missing.join("; ")}" if next_best_missing.any?

if errors.any?
  warn errors.join("\n")
  exit 1
end
RUBY
  then
    pass "$label"
  else
    fail "$label"
  fi
}

forbid_stub_sentinel_release_paths() {
  local label="$1"
  local hits=""
  hits="$(
    {
      for dir in research build optimize monitor cross-cutting commands; do
        [ -d "$ROOT/$dir" ] && grep -RIl -- "SEO_GEO_SKILL_STUB" "$ROOT/$dir" 2>/dev/null
      done
      for file in README.md docs/README.zh.md CLAUDE.md AGENTS.md CITATION.cff VERSIONS.md \
        .claude-plugin/plugin.json marketplace.json .claude-plugin/marketplace.json \
        .codebuddy-plugin/marketplace.json gemini-extension.json qwen-extension.json; do
        [ -f "$ROOT/$file" ] && grep -Il -- "SEO_GEO_SKILL_STUB" "$ROOT/$file" 2>/dev/null
      done
    } | sed "s#^$ROOT/##" | sort -u
  )"

  if [ -z "$hits" ]; then
    pass "$label"
  else
    fail "$label (found in: $hits)"
  fi
}

echo ""
echo "Slimming guardrails"
echo "==================="

for file in \
  ".claude-plugin/plugin.json" \
  "marketplace.json" \
  ".claude-plugin/marketplace.json" \
  "gemini-extension.json" \
  "qwen-extension.json" \
  ".codebuddy-plugin/marketplace.json" \
  ".mcp.json" \
  "hooks/hooks.json" \
  "CITATION.cff" \
  "CLAUDE.md" \
  "VERSIONS.md"
do
  require_file "$file"
done

if command -v jq >/dev/null 2>&1; then
  plugin_version="$(jq -r '.version' "$ROOT/.claude-plugin/plugin.json" 2>/dev/null)"
  if [ -n "$plugin_version" ] && [ "$plugin_version" != "null" ]; then
    pass "read plugin version: $plugin_version"
    require_json_equal "marketplace.json" ".metadata.version" "$plugin_version" "root marketplace metadata.version matches plugin"
    require_json_equal "marketplace.json" ".plugins[0].version" "$plugin_version" "root marketplace plugin version matches plugin"
    require_json_equal ".claude-plugin/marketplace.json" ".metadata.version" "$plugin_version" "bundle marketplace metadata.version matches plugin"
    require_json_equal ".claude-plugin/marketplace.json" ".plugins[0].version" "$plugin_version" "bundle marketplace plugin version matches plugin"
    require_json_equal "gemini-extension.json" ".version" "$plugin_version" "Gemini extension version matches plugin"
    require_json_equal "qwen-extension.json" ".version" "$plugin_version" "Qwen extension version matches plugin"
    require_json_equal ".codebuddy-plugin/marketplace.json" ".version" "$plugin_version" "CodeBuddy marketplace version matches plugin"
    require_json_equal ".codebuddy-plugin/marketplace.json" ".plugins[0].version" "$plugin_version" "CodeBuddy plugin version matches plugin"
    if jq empty "$ROOT/hooks/hooks.json" "$ROOT/.mcp.json" >/dev/null 2>&1; then
      pass "runtime JSON files parse cleanly"
    else
      fail "runtime JSON files parse cleanly"
    fi
    require_text "CITATION.cff" "version: \"$plugin_version\"" "CITATION.cff version matches plugin"
    require_text "VERSIONS.md" "### v$plugin_version" "VERSIONS.md has current release heading"
    require_text "CLAUDE.md" "Current bundle version: \`$plugin_version\`" "CLAUDE.md references current bundle version"
    require_text "README.md" "version-$plugin_version" "README badge references current release"
    require_text "docs/README.zh.md" "version-$plugin_version" "Chinese README badge references current release"
    require_text ".github/scripts/sync-skills.js" "--check" "sync-skills supports check mode"

    versions_date="$(sed -n "s/^### v$plugin_version .* (\([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\)).*/\1/p" "$ROOT/VERSIONS.md" | head -1)"
    citation_date="$(sed -n 's/^date-released: "\([^"]*\)".*/\1/p' "$ROOT/CITATION.cff" | head -1)"
    require_equal "$citation_date" "$versions_date" "CITATION.cff date-released matches current VERSIONS.md release date"

    while IFS= read -r skill_file; do
      skill_name="$(awk '/^---/{if(++n==2)exit} n && /^name:/{gsub(/name: */, ""); gsub(/["'"'"']/, ""); print; exit}' "$skill_file" | tr -d '\r')"
      skill_version="$(awk '/^---/{if(++n==2)exit} n && /^version:/{gsub(/version: */, ""); gsub(/["'"'"']/, ""); print; exit}' "$skill_file" | tr -d '\r')"
      table_version="$(awk -F'|' -v name="$skill_name" '
        {
          for (i=1; i<=NF; i++) {
            gsub(/^ +| +$/, "", $i)
          }
          if ($2 == name) {
            print $4
            exit
          }
        }
      ' "$ROOT/VERSIONS.md")"
      require_equal "$table_version" "$skill_version" "VERSIONS.md skill table matches $skill_name version"
      require_equal "$skill_version" "$plugin_version" "$skill_name version matches plugin"
      metadata_version="$(awk '/^---/{if(++n==2)exit} n && /^  version:/{gsub(/ *version: */, ""); gsub(/["'"'"']/, ""); print; exit}' "$skill_file" | tr -d '\r')"
      require_equal "$metadata_version" "$plugin_version" "$skill_name metadata.version matches plugin"
    done < <(find "$ROOT" -name "SKILL.md" -not -path "$ROOT/docs/*" -not -path "$ROOT/.claude/*" | sort)
  else
    fail "read plugin version from .claude-plugin/plugin.json"
  fi
else
  fail "jq is available for version matrix checks"
fi

if cmp -s "$ROOT/marketplace.json" "$ROOT/.claude-plugin/marketplace.json"; then
  pass "marketplace mirror is byte-identical"
else
  fail "marketplace.json and .claude-plugin/marketplace.json are byte-identical"
fi

if command -v jq >/dev/null 2>&1; then
  plugin_skills="$(jq -c '.skills' "$ROOT/.claude-plugin/plugin.json" 2>/dev/null)"
  root_marketplace_skills="$(jq -c '.plugins[0].skills' "$ROOT/marketplace.json" 2>/dev/null)"
  bundle_marketplace_skills="$(jq -c '.plugins[0].skills' "$ROOT/.claude-plugin/marketplace.json" 2>/dev/null)"
  codebuddy_skills="$(jq -c '.plugins[0].skills' "$ROOT/.codebuddy-plugin/marketplace.json" 2>/dev/null)"
  discovered_skills="$(discover_skill_paths | jq -R . | jq -s -c .)"
  require_equal "$root_marketplace_skills" "$plugin_skills" "root marketplace skills list matches plugin.json"
  require_equal "$bundle_marketplace_skills" "$plugin_skills" "bundle marketplace skills list matches plugin.json"
  require_equal "$codebuddy_skills" "$plugin_skills" "CodeBuddy skills list matches plugin.json"
  require_equal "$plugin_skills" "$discovered_skills" "plugin.json skills list matches discovered SKILL.md directories"
  require_equal "$root_marketplace_skills" "$discovered_skills" "root marketplace skills list matches discovered SKILL.md directories"
  require_equal "$bundle_marketplace_skills" "$discovered_skills" "bundle marketplace skills list matches discovered SKILL.md directories"
  require_equal "$codebuddy_skills" "$discovered_skills" "CodeBuddy skills list matches discovered SKILL.md directories"
require_skill_inventory_text "README.md" "README lists every discovered skill"
require_skill_inventory_text "docs/README.zh.md" "Chinese README lists every discovered skill"
require_skill_inventory_text "CLAUDE.md" "CLAUDE.md lists every discovered skill"
fi

echo ""
echo "Command inventory and controlled evolution"
echo "------------------------------------------"

command_count="$(find "$ROOT/commands" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
require_equal "$command_count" "17" "commands directory contains 17 command files"
require_command_inventory_exact "command filenames match expected 17-command inventory"
require_command_section_text "README.md" "^User commands:" "^$" "README lists all user commands under user heading" audit-page check-technical generate-schema optimize-meta report audit-domain write-content keyword-research setup-alert geo-drift-check
require_command_section_text "README.md" "^Maintenance commands:" "^$" "README lists all maintenance commands under maintenance heading" wiki-lint contract-lint run-evals sync-versions validate-library evolve-skill skillify
require_command_section_text "docs/README.zh.md" "^用户命令：" "^$" "Chinese README lists all user commands under user heading" audit-page check-technical generate-schema optimize-meta report audit-domain write-content keyword-research setup-alert geo-drift-check
require_command_section_text "docs/README.zh.md" "^维护命令：" "^$" "Chinese README lists all maintenance commands under maintenance heading" wiki-lint contract-lint run-evals sync-versions validate-library evolve-skill skillify
require_command_section_text "CLAUDE.md" "User commands" "Maintenance commands" "CLAUDE lists all user commands under user heading" audit-page check-technical generate-schema optimize-meta report audit-domain write-content keyword-research setup-alert geo-drift-check
require_command_section_text "CLAUDE.md" "Maintenance commands" "^## " "CLAUDE lists all maintenance commands under maintenance heading" wiki-lint contract-lint run-evals sync-versions validate-library evolve-skill skillify
require_command_frontmatter_yaml "command frontmatter YAML parses and has required fields"
require_text "README.md" "17 commands" "README command count is current"
require_text "docs/README.zh.md" "17 个命令" "Chinese README command count is current"
require_text "README.md" "Daily SEO/GEO work normally uses the user commands only." "README explains daily-user command boundary"
require_text "docs/README.zh.md" "日常 SEO/GEO 工作通常只需要用户命令" "Chinese README explains daily-user command boundary"
require_text "README.md" '`v9.9.5` adds `/seo:skillify`' "README explains 9.9.5 skillify release boundary"
require_text "docs/README.zh.md" '`v9.9.5` 新增 `/seo:skillify`' "Chinese README explains 9.9.5 skillify release boundary"
require_text "CLAUDE.md" "20 skills and 17 commands" "CLAUDE command count is current"
require_text "AGENTS.md" "20 SEO/GEO skills, 17 commands" "AGENTS command count is current"
require_text "VERSIONS.md" "all 20 skills and 17 commands remain" "VERSIONS records v9.9.5 command count"
require_text "VERSIONS.md" "all 20 skills and 16 commands remain" "VERSIONS keeps v9.9.0 historical command count"
require_text "VERSIONS.md" "all 20 skills and 15 commands remain" "VERSIONS keeps v9.5.0 historical command count"
require_text "VERSIONS.md" "/seo:skillify" "VERSIONS records v9.9.5 skillify release"
require_text "VERSIONS.md" "/seo:run-evals" "VERSIONS records v9.9.0 run-evals release"
require_text "CITATION.cff" "20 skills, 17 commands" "CITATION command count is current"
require_text ".claude-plugin/plugin.json" "20 SEO/GEO skills and 17 commands" "plugin description command count is current"
require_text "marketplace.json" "20 SEO/GEO skills and 17 commands" "root marketplace command count is current"
require_text ".claude-plugin/marketplace.json" "20 SEO/GEO skills and 17 commands" "bundle marketplace command count is current"
require_text ".codebuddy-plugin/marketplace.json" "20 SEO/GEO skills and 17 commands" "CodeBuddy marketplace command count is current"
require_text "gemini-extension.json" "20 SEO/GEO skills and 17 commands" "Gemini extension command count is current"
require_file "commands/evolve-skill.md"
require_file "commands/run-evals.md"
require_file "commands/skillify.md"
if [ -f "$ROOT/commands/p2-review.md" ]; then
  fail "p2-review command is retired"
else
  pass "p2-review command is retired"
fi
require_no_retired_p2_references "retired p2-review references are blocked outside history and guardrail"
require_file "references/evolution-protocol.md"
require_file "references/evolution-optimization-plan.md"
require_file "references/evolution-evidence-review.md"
require_file "references/evolution-pr-grade-mock.md"
require_file "references/evolution-failure-probes.md"
require_file "evals/README.md"
require_file "evals/geo-content-optimizer/cases.md"
require_file "evals/content-quality-auditor/cases.md"
require_file "evals/memory-management/cases.md"
require_file "memory/evolution/README.md"
require_file "memory/evolution/2026-04.md"
require_frontmatter_text "commands/evolve-skill.md" 'allowed-tools: ["Read", "Glob", "Grep"]' "evolve-skill tool scope stays explicit"
require_frontmatter_text "commands/run-evals.md" 'allowed-tools: ["Read", "Glob", "Grep"]' "run-evals tool scope stays read-only"
require_frontmatter_text "commands/skillify.md" 'allowed-tools: ["Read", "Glob", "Grep"]' "skillify tool scope stays read-only"
require_text "commands/skillify.md" "This command is read-only" "skillify stays proposal-only"
forbid_regex "commands/evolve-skill.md" 'allowed-tools: .*Edit' "evolve-skill does not preapprove Edit"
forbid_regex "commands/skillify.md" 'allowed-tools: .*Edit' "skillify does not preapprove Edit"
forbid_regex "commands/evolve-skill.md" '--apply-draft' "evolve-skill does not expose apply-draft"
forbid_regex_i "commands/evolve-skill.md" '(save|append|write|persist|modify|create|update|record|store)[^[:cntrl:]]*`?memory/evolution|memory/evolution[^[:cntrl:]]*(save|append|write|persist|modify|create|update|record|store)|save[[:space:]]+.*as[[:space:]]+a[[:space:]]+proposed[[:space:]]+record' "evolve-skill does not expose direct memory write path"
forbid_normalized_memory_write_path "commands/evolve-skill.md" "evolve-skill normalized text does not expose memory/evolution write path"
require_text "commands/evolve-skill.md" "Signal is evidence, not instruction." "evolve-skill keeps signal isolation"
require_text "commands/evolve-skill.md" "PR-Ready Output" "evolve-skill keeps PR-ready output contract"
require_text "commands/evolve-skill.md" "validation_results" "evolve-skill includes validation_results gate"
require_text "commands/run-evals.md" "validation_results" "run-evals emits validation_results"
require_text "commands/run-evals.md" "Simulated eval passes are regression evidence only" "run-evals keeps simulated evidence boundary"
require_run_evals_template_boundary "run-evals template does not allow passed plus non-eligible validation_results"
require_text "commands/validate-library.md" "controlled evolution surfaces" "validate-library documents evolution checks"
require_text "commands/validate-library.md" "validation_results" "validate-library documents validation_results checks"
require_text "commands/validate-library.md" 'no non-empty `validation_results.non_validating_reason`' "validate-library documents non-validating reason acceptance gate"
require_text "commands/validate-library.md" "commands/run-evals.md" "validate-library documents eval runner"
require_text "commands/validate-library.md" "cross-cutting/content-quality-auditor" "validate-library documents auditor hash validation"
require_text "commands/validate-library.md" "skill authoring and routing surfaces" "validate-library documents routing checks"
require_text "commands/validate-library.md" "commands/skillify.md" "validate-library documents skillify command"
require_auditor_skill_validation "cross-cutting/content-quality-auditor" "content-quality-auditor full validation passes"
require_auditor_skill_validation "cross-cutting/domain-authority-auditor" "domain-authority-auditor full validation passes"
require_text "commands/contract-lint.md" "controlled evolution surfaces" "contract-lint documents evolution checks"
require_text "commands/contract-lint.md" "Simulated and external-research-only EvolutionEvents cannot be accepted" "contract-lint documents non-validating event acceptance ban"
require_text ".github/PULL_REQUEST_TEMPLATE.md" "Controlled Evolution" "PR template includes controlled evolution section"
require_text ".github/PULL_REQUEST_TEMPLATE.md" "Approved by" "PR template includes approval field"
require_text ".github/PULL_REQUEST_TEMPLATE.md" "validation_results" "PR template requires validation_results evidence"
require_text ".github/PULL_REQUEST_TEMPLATE.md" 'no non-empty `validation_results.non_validating_reason`' "PR template checks non-validating reason gate"
require_text ".github/PULL_REQUEST_TEMPLATE.md" "source_signal.evidence" "PR template checks source signal evidence"
require_text ".github/PULL_REQUEST_TEMPLATE.md" "External-research-only evidence is not marked" "PR template blocks accepted external-only evidence"
require_text ".github/PULL_REQUEST_TEMPLATE.md" 'not marked `decision.status: accepted`' "PR template blocks accepted simulated evidence"
require_text "references/evolution-evidence-review.md" "Hermes+ controlled maintainer workflow" "external evidence review defines Hermes+ target"
require_text "references/evolution-evidence-review.md" "External evidence is non-validating" "external evidence review keeps non-validating boundary"
require_text "references/evolution-evidence-review.md" '`maintainer_observation` tied to a project-local artifact' "external evidence review separates maintainer observation from review approval"
require_text "references/evolution-optimization-plan.md" "GO for experimental Hermes+ maintainer workflow" "optimization plan records Hermes+ GO scope"
require_text "references/evolution-optimization-plan.md" "9.9.5 17-command state" "optimization plan records current 9.9.5 command state"
require_text "references/evolution-protocol.md" "validation_results" "evolution protocol defines validation_results"
require_text "references/evolution-protocol.md" "external_research" "evolution protocol includes external research source kind"
require_text "references/evolution-protocol.md" "empty string for validating runs" "evolution protocol avoids literal none for validating runs"
require_text "references/evolution-pr-grade-mock.md" "decision:" "PR-grade mock includes EvolutionEvent samples"
require_text "references/evolution-pr-grade-mock.md" "status: accepted" "PR-grade mock includes accepted event sample"
require_text "references/evolution-pr-grade-mock.md" "status: rejected" "PR-grade mock includes rejected event sample"
require_text "references/evolution-pr-grade-mock.md" "status: superseded" "PR-grade mock includes superseded event sample"
require_text "references/evolution-failure-probes.md" "nonvalidating-accepted-flow" "failure probes cover flow-style non-validating acceptance"
require_text "references/evolution-failure-probes.md" "malformed-indented-event" "failure probes cover malformed indented EvolutionEvent blocks"
require_text "references/evolution-failure-probes.md" "accepted-missing-source-evidence" "failure probes cover accepted-event source evidence"
require_text "references/evolution-failure-probes.md" "optional-false-schema-value" "failure probes cover falsey optional schema values"
require_text "references/evolution-failure-probes.md" "run-evals-passed-noneligible" "failure probes cover run-evals non-eligible pass"
require_text "references/evolution-failure-probes.md" "run-evals-passed-nonvalidating-reason" "failure probes cover run-evals passed non-validating reason"
require_text "references/evolution-failure-probes.md" "memory-write-path-split" "failure probes cover split memory/evolution write paths"
require_text "memory/evolution/README.md" "validation_results" "evolution memory template defines validation_results"
require_text "memory/evolution/2026-04.md" "simulation: true" "simulated evolution events are labeled"
require_text "memory/evolution/2026-04.md" "validation_results" "simulated evolution events include validation_results status"
require_eval_case_count "16" "eval suite contains at least 16 simulated cases"
require_file "references/skill-resolver.md"
require_resolver_coverage "skill resolver covers every discovered skill"
require_routing_eval_targets "10" "routing eval cases use real target skills"
forbid_stub_sentinel_release_paths "scaffold stub sentinel is absent from release-bearing paths"
require_text "evals/geo-content-optimizer/cases.md" "status: simulated" "GEO eval seed is labeled simulated"
require_text "evals/content-quality-auditor/cases.md" "status: simulated" "auditor eval seed is labeled simulated"
require_text "evals/content-quality-auditor/cases.md" "content-quality-auditor-sim-005" "auditor eval covers C01 title mismatch veto"
require_text "evals/content-quality-auditor/cases.md" "content-quality-auditor-sim-006" "auditor eval covers R10 contradictory data veto"
require_text "evals/content-quality-auditor/cases.md" "content-quality-auditor-sim-007" "auditor eval covers multi-veto BLOCKED path"
require_text "evals/content-quality-auditor/cases.md" "content-quality-auditor-sim-008" "auditor eval covers artifact gate negative case"
require_text "evals/memory-management/cases.md" "status: simulated" "memory eval seed is labeled simulated"
require_text "evals/README.md" "/seo:run-evals" "eval README documents run-evals entrypoint"
require_text "memory/evolution/2026-04.md" "evo-2026-04-27-run-evals-dry-run-001" "evolution memory records Hermes+ dry run"
require_text "memory/evolution/2026-04.md" "dry-run process exercise only" "Hermes+ dry run remains non-accepting"

for evolution_path in "$ROOT"/memory/evolution/[0-9][0-9][0-9][0-9]-[0-9][0-9].md; do
  [ -f "$evolution_path" ] || continue
  evolution_file="${evolution_path#$ROOT/}"
  require_evolution_events_parser_grade "$evolution_file" "$evolution_file passes parser-grade EvolutionEvent validation"
done
require_evolution_events_parser_grade "references/evolution-pr-grade-mock.md" "PR-grade mock event samples pass parser-grade validation"

echo ""
echo "Discovery alias allowlist"
echo "-------------------------"

require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "robots-txt" "technical SEO keeps robots.txt tag"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "xml-sitemap" "technical SEO keeps sitemap tag"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "canonical-tags" "technical SEO keeps canonical tag"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "hsts" "technical SEO keeps HSTS discovery tag"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "check my robots.txt" "technical SEO keeps robots.txt trigger"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "sitemap issue" "technical SEO keeps sitemap trigger"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "canonical tag issues" "technical SEO keeps canonical trigger"
require_frontmatter_text "optimize/technical-seo-checker/SKILL.md" "HSTS check" "technical SEO keeps HSTS trigger"

require_frontmatter_text "build/geo-content-optimizer/SKILL.md" "ai-seo" "GEO keeps AI SEO tag"
require_frontmatter_text "build/geo-content-optimizer/SKILL.md" "AI optimization" "GEO keeps AI optimization trigger"
require_frontmatter_text "build/geo-content-optimizer/SKILL.md" "generative engine optimization" "GEO keeps expanded GEO trigger"
require_frontmatter_text "build/geo-content-optimizer/SKILL.md" "AI搜索优化" "GEO keeps Chinese AI search trigger"

require_frontmatter_text "build/schema-markup-generator/SKILL.md" "schema-org" "schema skill keeps schema-org tag"
require_frontmatter_text "build/schema-markup-generator/SKILL.md" "schema.org" "schema skill keeps schema.org trigger"

require_frontmatter_text "research/keyword-research/SKILL.md" "Ahrefs alternative" "keyword research keeps Ahrefs alternative alias"
require_frontmatter_text "research/keyword-research/SKILL.md" "Semrush" "keyword research keeps Semrush alias"
require_frontmatter_text "research/keyword-research/SKILL.md" "Google Keyword Planner" "keyword research keeps Keyword Planner alias"
require_frontmatter_text "research/keyword-research/SKILL.md" "Ubersuggest" "keyword research keeps Ubersuggest alias"

require_frontmatter_text "cross-cutting/memory-management/SKILL.md" "remember project context" "memory keeps project context trigger"
require_frontmatter_text "cross-cutting/memory-management/SKILL.md" "remember this for next time" "memory keeps remember trigger"
require_frontmatter_text "cross-cutting/memory-management/SKILL.md" "wiki lint" "memory keeps wiki lint trigger"
require_frontmatter_text "cross-cutting/memory-management/SKILL.md" "what do we know so far" "memory keeps project-knowledge trigger"

echo ""
echo "Template regression matrix"
echo "--------------------------"

require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Crawlability" "robots.txt snapshot" "crawlability template captures robots.txt snapshot"
require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Crawlability" "Recommended robots.txt patch" "crawlability template includes robots.txt patch slot"
require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Crawlability" "sitemap check" "crawlability template includes sitemap check"
require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Crawlability" "only indexable URLs" "crawlability template checks indexable sitemap URLs"
require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Crawlability" "lastmod" "crawlability template checks lastmod freshness"
require_section_text "optimize/technical-seo-checker/references/technical-audit-templates.md" "## Security" "HSTS configured appropriately" "security template includes HSTS"
require_section_text "optimize/technical-seo-checker/references/llm-crawler-handling.md" "## Crawler Matrix" "OAI-SearchBot" "LLM crawler matrix keeps OpenAI search crawler"
require_section_text "optimize/technical-seo-checker/references/llm-crawler-handling.md" "## Crawler Matrix" "Perplexity-User" "LLM crawler matrix keeps Perplexity user fetcher"
require_section_text "optimize/technical-seo-checker/references/llm-crawler-handling.md" "## Search-Only Starter" "OAI-SearchBot" "LLM crawler starter allows OpenAI search retrieval"
require_section_text "optimize/technical-seo-checker/references/llm-crawler-handling.md" "## Search-Only Starter" "Perplexity-User" "LLM crawler starter includes Perplexity user fetcher"
require_section_text "optimize/technical-seo-checker/references/llm-crawler-handling.md" "## Legal/Compliance Notes" "not a complete training opt-out" "LLM crawler reference keeps training opt-out boundary"
require_section_text "optimize/technical-seo-checker/references/robots-txt-reference.md" "## Common User Agents" "OAI-SearchBot" "robots reference keeps OpenAI search crawler"
require_section_text "optimize/technical-seo-checker/references/robots-txt-reference.md" "## Common User Agents" "Perplexity-User" "robots reference keeps Perplexity user fetcher"
require_section_text "optimize/technical-seo-checker/references/robots-txt-reference.md" "## AI Crawler Patterns" "OAI-SearchBot" "robots AI pattern allows OpenAI search retrieval"
require_section_text "optimize/technical-seo-checker/references/robots-txt-reference.md" "## AI Crawler Patterns" "Perplexity-User" "robots AI pattern includes Perplexity user fetcher"

require_section_text "optimize/on-page-seo-auditor/references/audit-templates.md" "## Images" "filename" "image audit keeps filename evidence"
require_section_text "optimize/on-page-seo-auditor/references/audit-templates.md" "## Images" "lazy" "image audit keeps lazy-load evidence"
require_section_text "optimize/on-page-seo-auditor/references/audit-templates.md" "## CORE-EEAT Quick Scan" "Quick Score**: [X]/17" "CORE-EEAT section denominator remains /17"
require_section_text "optimize/on-page-seo-auditor/references/audit-templates.md" "## Step 11: Generate Audit Summary" "CORE-EEAT quick scan (scaled)" "CORE-EEAT roll-up marks scaled /20 score"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Weighted Scorecard" "Content quality | 25%" "on-page scoring keeps content-quality weight"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Weighted Scorecard" "Image optimization | 10%" "on-page scoring keeps image weight"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Benchmarks" "Keyword Density" "on-page scoring keeps keyword density benchmark"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Benchmarks" "500-1,499" "on-page scoring keeps complete content-length partial band"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Accessibility Overlay" "WCAG 2.2 AA" "on-page scoring keeps WCAG overlay"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Score Calculation" "Section percentage" "on-page scoring keeps normalized section interpretation"
require_section_text "optimize/on-page-seo-auditor/references/scoring-rubric.md" "## Resolution Playbook" "Missing descriptive alt" "on-page scoring keeps image-alt remediation"

require_section_text "monitor/performance-reporter/references/report-output-templates.md" "## Executive Summary" "Domain Authority / CITE" "performance executive summary keeps authority metric"
require_section_text "monitor/performance-reporter/references/report-output-templates.md" "## Executive Summary" "AI Citations" "performance executive summary keeps AI citations metric"
require_section_text "monitor/performance-reporter/references/report-output-templates.md" "## Shared Conventions" "Audience" "performance template keeps audience matrix"
require_text "monitor/performance-reporter/references/report-templates.md" "Data Freshness Requirements" "performance report templates keep data freshness requirements"
require_text "monitor/performance-reporter/references/report-templates.md" "All data sources verified and dated" "performance report templates keep dated-source requirement"
require_text "monitor/performance-reporter/references/report-templates.md" "source and date" "performance report templates keep source/date benchmark requirement"
require_text "monitor/performance-reporter/references/kpi-definitions.md" "Organic CTR | Organic clicks / impressions x 100" "KPI definitions keep organic CTR formula"
require_text "monitor/performance-reporter/references/kpi-definitions.md" "AI citation rate | Cited queries / monitored AI-answer queries x 100" "KPI definitions keep AI citation rate formula"
require_text "monitor/performance-reporter/references/kpi-definitions.md" "Toxic link ratio | Toxic backlinks / total backlinks x 100" "KPI definitions keep toxic link ratio formula"
require_section_text "monitor/performance-reporter/references/kpi-definitions.md" "## Benchmarks" "#1 | 25-35%" "KPI definitions keep CTR position benchmark"
require_section_text "monitor/performance-reporter/references/kpi-definitions.md" "## Benchmarks" "INP | <=200ms" "KPI definitions keep INP threshold"
require_section_text "monitor/performance-reporter/references/kpi-definitions.md" "## Interpretation Notes" "source and date" "KPI definitions keep source/date reporting rule"
require_text "commands/audit-page.md" "if fetch is unavailable" "audit-page keeps no-tool content fallback"
require_text "commands/audit-page.md" "DONE_WITH_CONCERNS" "audit-page keeps inferred-keyword nonblocking mode"
require_text "commands/check-technical.md" 'mark CWV metrics `N/A`' "check-technical does not guess CWV metrics"
require_text "commands/report.md" "Require exactly one scope" "report command requires explicit scope"
require_text "commands/report.md" "source/date freshness" "report output keeps source/date freshness"

require_section_text "build/schema-markup-generator/references/schema-templates.md" "## Article / BlogPosting" "[ISO 8601 publish date-time]" "schema templates use placeholder publish dates"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## Product" "[price]" "schema templates use placeholder prices"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## Product" "aggregateRating" "schema templates keep aggregateRating fragment"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## Product" "Optional review extension" "schema templates keep review extension guidance"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## FAQPage" "Question text 2" "schema FAQ template keeps two Q&A pairs"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## Product" "current purchasable offer details" "schema Product template keeps visible price boundary"
require_section_text "build/schema-markup-generator/references/schema-templates.md" "## LocalBusiness" "policy-eligible" "schema LocalBusiness keeps review eligibility boundary"
require_text "commands/generate-schema.md" "omit missing or unverifiable dates, prices, durations, ratings, and review counts" "generate-schema omits unverifiable rich-result facts"
forbid_regex "commands/generate-schema.md" "Use placeholders for dates, prices, durations, ratings, and review counts" "generate-schema forbids unsafe publish placeholders"
forbid_regex "build/schema-markup-generator/references/schema-templates.md" '"date[A-Za-z]*": "20[0-9]{2}-[0-9]{2}-[0-9]{2}' "schema templates do not include literal date/date-time values"
forbid_regex "build/schema-markup-generator/references/schema-templates.md" '"(price|lowPrice|highPrice)": "?[0-9]' "schema templates do not include literal numeric prices"
forbid_regex "build/schema-markup-generator/references/schema-templates.md" '"(duration|prepTime|cookTime|totalTime)": "P(T)?[0-9]' "schema templates do not include literal fixed durations"
require_section_text "build/schema-markup-generator/references/validation-guide.md" "## Required and Recommended Properties" "FAQPage" "schema validation keeps FAQPage requirements"
require_section_text "build/schema-markup-generator/references/validation-guide.md" "## Required and Recommended Properties" "Product" "schema validation keeps Product requirements"
require_section_text "build/schema-markup-generator/references/validation-guide.md" "## Rich Result Policy Checks" "Content mismatch" "schema validation keeps content-mismatch policy"
require_section_text "build/schema-markup-generator/references/validation-guide.md" "## Testing Workflow" "Post-launch" "schema validation keeps post-launch monitoring"
require_section_text "build/schema-markup-generator/references/validation-guide.md" "## Maintenance Checklist" "dateModified" "schema validation keeps dateModified maintenance rule"

require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "clear evidence of risk" "backlink rubric keeps disavow evidence threshold"
require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "Low-DA sites with real content" "backlink rubric protects legitimate low-DA sites"
require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "Nofollow links" "backlink rubric protects nofollow links"
require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "Manually review flagged domains" "backlink rubric keeps manual review step"
require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "Attempt removal first" "backlink rubric keeps removal-before-disavow order"
require_section_text "monitor/backlink-analyzer/references/link-quality-rubric.md" "## 4. Disavow File Safety Guide" "backup" "backlink rubric keeps disavow backup/rollback"

require_section_text "optimize/internal-linking-optimizer/references/link-architecture-patterns.md" "## Model Selector" "Hub-and-Spoke" "internal linking keeps model selector"
require_section_text "optimize/internal-linking-optimizer/references/link-architecture-patterns.md" "## Migration Between Models" "Preserve existing equity" "internal linking keeps migration equity guard"
require_section_text "optimize/internal-linking-optimizer/references/link-architecture-patterns.md" "## Migration Between Models" "4-8 weeks" "internal linking keeps migration monitoring threshold"

require_section_text "optimize/content-refresher/references/refresh-templates.md" "## Republishing Strategy" "50%+" "content refresher keeps major-update threshold"
require_section_text "optimize/content-refresher/references/refresh-templates.md" "## Republishing Strategy" "20-50%" "content refresher keeps moderate-update threshold"
require_section_text "optimize/content-refresher/references/refresh-templates.md" "## Republishing Strategy" "dateModified" "content refresher keeps schema freshness check"
require_section_text "optimize/content-refresher/references/refresh-templates.md" "## Republishing Strategy" "lastmod" "content refresher keeps sitemap freshness check"

require_text "build/geo-content-optimizer/references/instructions-detail.md" "Source citations" "GEO analysis keeps source citation scoring"
require_text "build/geo-content-optimizer/references/instructions-detail.md" "Content freshness" "GEO analysis keeps content freshness scoring"
require_text "build/geo-content-optimizer/references/quotable-content-examples.md" "source and publication date" "GEO quotability keeps dated-source requirement"
require_text "build/geo-content-optimizer/references/quotable-content-examples.md" "current or explicitly labeled historical" "GEO quotability keeps currentness requirement"
require_text "build/geo-content-optimizer/references/ai-citation-patterns.md" "Updated within 12 months" "GEO citation patterns keep freshness threshold"

require_section_text "build/seo-content-writer/references/title-formulas.md" "## Rewrite Examples" "[X]%" "title examples keep proof claims as placeholders"
require_section_text "build/seo-content-writer/references/content-structure-templates.md" "## Shared Build Rules" "primary keyword early" "content structure keeps first-100-word keyword rule"
require_section_text "build/seo-content-writer/references/content-structure-templates.md" "## Shared Build Rules" "40-60 word definition block" "content structure keeps GEO definition requirement"
require_section_text "build/seo-content-writer/references/content-structure-templates.md" "## Blueprint Matrix" "FAQ rich results" "content structure keeps FAQ rich-result scope"
require_section_text "build/seo-content-writer/references/content-structure-templates.md" "## Implementation Checklist" "affiliate disclosure" "content structure keeps affiliate disclosure reminder"
require_section_text "build/seo-content-writer/references/seo-writing-checklist.md" "## On-Page Checklist" "Snippet targeting" "SEO writing checklist keeps snippet targeting"
require_section_text "build/seo-content-writer/references/seo-writing-checklist.md" "## Example Calibration Card" "CTA" "SEO writing checklist keeps CTA logic"
require_section_text "build/seo-content-writer/references/seo-writing-checklist.md" "## Final Self-Check" "source and date" "SEO writing checklist keeps source/date evidence check"

require_text "research/keyword-research/references/keyword-intent-taxonomy.md" "Verify final intent against the live SERP" "keyword intent taxonomy keeps live-SERP validation"
require_section_text "research/keyword-research/references/keyword-intent-taxonomy.md" "## Funnel Mapping" "Conversion potential" "keyword intent taxonomy keeps conversion expectations"
require_section_text "research/keyword-research/references/keyword-intent-taxonomy.md" "## Mixed Intent Handling" "answer the dominant question first" "keyword intent taxonomy keeps mixed-intent priority rule"

require_text "optimize/internal-linking-optimizer/references/linking-templates.md" "Exact match | 10-20%" "linking templates keep exact-match anchor threshold"
require_text "optimize/internal-linking-optimizer/references/linking-templates.md" "Partial match | 30-40%" "linking templates keep partial-match anchor threshold"
require_text "optimize/internal-linking-optimizer/references/linking-templates.md" "Orphan pages | [X] | 0" "linking templates keep orphan-page zero target"
require_text "optimize/internal-linking-optimizer/references/linking-templates.md" "Over-optimized anchors | [X]% | <10%" "linking templates keep over-optimization threshold"

require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "Sitemap directive" "technical audit example keeps robots sitemap directive"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "Only indexable URLs" "technical audit example keeps sitemap indexability check"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "lastmod accuracy" "technical audit example keeps lastmod check"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "HSTS enabled" "technical audit example keeps HSTS check"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "INP" "technical audit example keeps INP metric"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "Structured Data" "technical audit example keeps structured-data section"
require_text "optimize/technical-seo-checker/references/technical-audit-example.md" "Errors / missing opportunities" "technical audit example keeps structured-data missing-opportunity field"
require_section_text "optimize/technical-seo-checker/references/technical-audit-example.md" "## Reporting Rules" "robots.txt, sitemap, lastmod, HSTS, INP" "technical audit example keeps protected reporting fields"

require_text "research/competitor-analysis/references/battlecard-template.md" "**Confidence**: [High/Medium/Low]" "battlecard keeps confidence field"
require_text "research/competitor-analysis/references/battlecard-template.md" "| Domain authority | [score + source/date] | [score + source/date]" "battlecard keeps source/date on both authority metrics"
require_text "research/competitor-analysis/references/battlecard-template.md" "| AI citation frequency | [High/Med/Low + source/date] | [High/Med/Low + source/date]" "battlecard keeps source/date on both AI citation metrics"

echo ""
echo "Protected runtime contracts"
echo "---------------------------"

require_text "references/skill-contract.md" "Handoff Summary Format" "skill contract keeps handoff schema"
require_text "references/skill-contract.md" "Termination rules for Next Best Skill chains" "skill contract keeps chain termination rules"
require_text "references/skill-contract.md" "Protocol Layer vs Execution Layer" "skill contract keeps layer model"
require_text "references/skill-contract.md" "Gate Verdicts" "skill contract keeps auditor verdict model"

require_text "references/state-model.md" "Sole writer" "state model keeps memory sole-writer rule"
require_text "references/state-model.md" "HOT" "state model keeps HOT tier"
require_text "references/state-model.md" "WARM" "state model keeps WARM tier"
require_text "references/state-model.md" "COLD" "state model keeps COLD tier"
require_text "references/state-model.md" "Project isolation" "state model keeps project isolation"

require_text "hooks/hooks.json" "SessionStart" "hooks keep SessionStart behavior"
require_text "hooks/hooks.json" "PostToolUse" "hooks keep PostToolUse behavior"
require_text "hooks/hooks.json" "Stop" "hooks keep Stop guard"
require_text "hooks/hooks.json" "stop_hook_active" "hooks guard Stop re-entry"
require_text "hooks/hooks.json" "Respond only with JSON" "hooks specify Stop response schema"
require_text "hooks/hooks.json" "\\\"ok\\\": true" "hooks keep Stop allow-only response"
require_text "hooks/hooks.json" "Stop hook never initiates memory writes" "hooks document Stop no-write contract"
forbid_regex "hooks/hooks.json" "Save these results for future sessions\\?|Wiki wrap-up|Auditor archiving" "hooks forbid legacy interactive Stop prompts"
require_text "hooks/hooks.json" "class: auditor-output" "hooks keep auditor archive guard"

require_text "cross-cutting/memory-management/SKILL.md" "Sole writer of wiki" "memory-management keeps sole-writer contract"
require_text "cross-cutting/memory-management/SKILL.md" "HOT/WARM/COLD" "memory-management keeps memory lifecycle"
require_text "cross-cutting/memory-management/SKILL.md" "Auditor handoff archiving" "memory-management keeps auditor archive contract"
require_text "cross-cutting/memory-management/SKILL.md" "PostToolUse" "memory-management keeps hook delegation"

require_text "cross-cutting/entity-optimizer/SKILL.md" "Profile schema" "entity-optimizer keeps canonical profile schema contract"
require_text "cross-cutting/entity-optimizer/SKILL.md" "entity-geo-handoff-schema" "entity-optimizer keeps downstream schema reference"
require_text "cross-cutting/entity-optimizer/SKILL.md" "Next Best Skill" "entity-optimizer keeps handoff contract"

current_lines="$(find "$ROOT" \
  -path "$ROOT/.git" -prune -o \
  -path "$ROOT/.claude" -prune -o \
  -path "$ROOT/.docs" -prune -o \
  -type f \( -name '*.md' -o -name '*.json' -o -name '*.yml' -o -name '*.yaml' -o -name '*.sh' -o -name '*.cff' \) \
  -print0 | xargs -0 wc -l | tail -1 | awk '{print $1}')"

if [ -n "${current_lines:-}" ] && [ "$current_lines" -lt 20000 ]; then
  pass "repository line budget stays under 20000"
else
  fail "repository line budget stays under 20000 (current counted lines: ${current_lines:-unknown})"
fi

echo ""
echo "Current counted lines: ${current_lines:-unknown}"
echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
