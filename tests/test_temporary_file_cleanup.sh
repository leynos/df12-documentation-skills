#!/bin/sh
# Exercise the exact cleanup functions documented in the canonical workflows.
# The bounded-model cases run only through guarded unlink/rmdir shims, which
# refuse operands outside TEST_ROOT. Fixture teardown is deliberately separate
# from the model and uses find -delete only after all assertions complete.

set -eu

fail() {
  printf '%s\n' "FAIL: $*" >&2
  exit 1
}

assert_file() {
  test -f "$1" || fail "expected file to remain: $1"
}

assert_directory() {
  test -d "$1" || fail "expected directory to remain: $1"
}

assert_absent() {
  test ! -e "$1" && test ! -L "$1" || fail "expected path to be absent: $1"
}

teardown_fixture() {
  # This is test-fixture disposal, not a model of either cleanup function.
  if test -n "${TEST_ROOT:-}" && test -d "$TEST_ROOT"; then
    find "$TEST_ROOT" -depth -delete
  fi
}

TEST_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/temporary-cleanup-tests.XXXXXX")
TEST_ROOT=$(CDPATH= cd -- "$TEST_ROOT" && pwd -P)
trap teardown_fixture EXIT HUP INT TERM

# Preserve the original command path for the guarded command shims below.
SAFE_PATH=$PATH
export SAFE_PATH TEST_ROOT
MOCK_BIN=$TEST_ROOT/mock-bin
mkdir "$MOCK_BIN"

cat > "$MOCK_BIN/unlink" << 'ENDOFUNLINK'
#!/bin/sh
set -eu

operand=${1-}
if test -z "$operand"; then
  exit 64
fi
parent=$(dirname "$operand")
base=$(basename "$operand")
absolute=$(CDPATH= cd -P -- "$parent" 2>/dev/null && pwd -P)/$base
case "$absolute" in
  "$TEST_ROOT" | "$TEST_ROOT"/*) ;;
  *)
    printf '%s\n' "refused unlink outside fixture: $operand" >&2
    exit 64
    ;;
esac
PATH=$SAFE_PATH command unlink "$operand"
ENDOFUNLINK

cat > "$MOCK_BIN/rmdir" << 'ENDOFRMDIR'
#!/bin/sh
set -eu

operand=${1-}
if test -z "$operand"; then
  exit 64
fi
parent=$(dirname "$operand")
base=$(basename "$operand")
absolute=$(CDPATH= cd -P -- "$parent" 2>/dev/null && pwd -P)/$base
case "$absolute" in
  "$TEST_ROOT" | "$TEST_ROOT"/*) ;;
  *)
    printf '%s\n' "refused rmdir outside fixture: $operand" >&2
    exit 64
    ;;
esac
PATH=$SAFE_PATH command rmdir "$operand"
ENDOFRMDIR
chmod +x "$MOCK_BIN/unlink" "$MOCK_BIN/rmdir"
PATH=$MOCK_BIN:$PATH
export PATH

# Reproduced from skills/commit-message/SKILL.md.
cleanup_commit_message() {
  if [ -e "$COMMIT_MSG_DIR/COMMIT_MSG.md" ] || [ -L "$COMMIT_MSG_DIR/COMMIT_MSG.md" ]; then
    unlink "$COMMIT_MSG_DIR/COMMIT_MSG.md"
  fi
  rmdir "$COMMIT_MSG_DIR"
}

# Reproduced from skills/pr-creation/SKILL.md.
cleanup_pr_body() {
  if [ -e "$PR_BODY_DIR/body.md" ] || [ -L "$PR_BODY_DIR/body.md" ]; then
    unlink "$PR_BODY_DIR/body.md"
  fi
  rmdir "$PR_BODY_DIR"
}

run_cleanup() {
  cleanup_kind=$1
  cleanup_value=$2
  case "$cleanup_kind" in
    commit)
      COMMIT_MSG_DIR=$cleanup_value
      cleanup_commit_message
      ;;
    pr)
      PR_BODY_DIR=$cleanup_value
      cleanup_pr_body
      ;;
    *) fail "unknown cleanup kind: $cleanup_kind" ;;
  esac
}

artifact_name() {
  case "$1" in
    commit) printf '%s\n' COMMIT_MSG.md ;;
    pr) printf '%s\n' body.md ;;
    *) fail "unknown cleanup kind: $1" ;;
  esac
}

assert_outer_sentinels() {
  assert_file "$1/parent.sentinel"
  assert_file "$1/sibling/sibling.sentinel"
  assert_file "$TEST_ROOT/outer.sentinel"
  assert_directory "$1/sibling"
}

run_exact_cleanup_case() {
  cleanup_kind=$1
  case_root=$TEST_ROOT/exact-$cleanup_kind
  target=$case_root/temporary
  artifact=$(artifact_name "$cleanup_kind")
  mkdir -p "$target" "$case_root/sibling"
  printf '%s\n' parent > "$case_root/parent.sentinel"
  printf '%s\n' sibling > "$case_root/sibling/sibling.sentinel"
  printf '%s\n' artefact > "$target/$artifact"

  run_cleanup "$cleanup_kind" "$target"

  assert_absent "$target/$artifact"
  assert_absent "$target"
  assert_outer_sentinels "$case_root"
}

run_bounded_case() {
  cleanup_kind=$1
  case_name=$2
  directory_value=$3
  invocation_directory=$4
  target=$5
  expect_artifact=$6
  case_root=$TEST_ROOT/bounded-$cleanup_kind-$case_name
  artifact=$(artifact_name "$cleanup_kind")

  mkdir -p "$case_root/sibling" "$invocation_directory"
  printf '%s\n' parent > "$case_root/parent.sentinel"
  printf '%s\n' sibling > "$case_root/sibling/sibling.sentinel"

  if test "$expect_artifact" = yes; then
    mkdir -p "$target"
    printf '%s\n' artefact > "$target/$artifact"
    # A non-empty target must make rmdir fail rather than delete recursively.
    printf '%s\n' keep > "$target/keep.sentinel"
  fi

  set +e
  cleanup_output=$(
    (
      CDPATH= cd -- "$invocation_directory" || exit 1
      run_cleanup "$cleanup_kind" "$directory_value"
    ) 2>&1
  )
  cleanup_status=$?
  set -e

  printf '%s/%s: expected non-zero rmdir status, got %s\n' \
    "$cleanup_kind" "$case_name" "$cleanup_status"
  test "$cleanup_status" -ne 0 || fail "expected non-empty cleanup to fail: $cleanup_kind/$case_name: $cleanup_output"
  assert_outer_sentinels "$case_root"

  if test "$expect_artifact" = yes; then
    assert_absent "$target/$artifact"
    assert_file "$target/keep.sentinel"
    assert_directory "$target"
  fi
}

printf '%s\n' outer > "$TEST_ROOT/outer.sentinel"

for cleanup_kind in commit pr; do
  run_exact_cleanup_case "$cleanup_kind"

  normal_root=$TEST_ROOT/bounded-$cleanup_kind-normal
  mkdir -p "$normal_root/work"
  normal_target=$(mktemp -d "$normal_root/work/generated.XXXXXX")
  run_bounded_case "$cleanup_kind" normal "$normal_target" "$normal_root/work" "$normal_target" yes

  empty_root=$TEST_ROOT/bounded-$cleanup_kind-empty
  empty_work=$empty_root/work
  run_bounded_case "$cleanup_kind" empty '' "$empty_work" "$empty_work/not-created" no

  dot_root=$TEST_ROOT/bounded-$cleanup_kind-dot
  dot_target=$dot_root/work/dot-target
  run_bounded_case "$cleanup_kind" dot . "$dot_target" "$dot_target" yes

  parent_root=$TEST_ROOT/bounded-$cleanup_kind-parent
  parent_target=$parent_root/work/parent-target
  parent_work=$parent_target/nested
  run_bounded_case "$cleanup_kind" parent .. "$parent_work" "$parent_target" yes

  absolute_root=$TEST_ROOT/bounded-$cleanup_kind-absolute
  absolute_target=$absolute_root/work/absolute-target
  run_bounded_case "$cleanup_kind" absolute "$absolute_target" "$absolute_root/work" "$absolute_target" yes

  whitespace_root=$TEST_ROOT/bounded-$cleanup_kind-whitespace
  whitespace_target="$whitespace_root/work/with whitespace"
  run_bounded_case "$cleanup_kind" whitespace "$whitespace_target" "$whitespace_root/work" "$whitespace_target" yes

  relative_root=$TEST_ROOT/bounded-$cleanup_kind-relative
  relative_work=$relative_root/work
  relative_target=$relative_work/nested/relative-target
  run_bounded_case "$cleanup_kind" relative nested/relative-target "$relative_work" "$relative_target" yes
done

printf '%s\n' 'Temporary file cleanup tests passed.'
