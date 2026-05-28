# Bash Scripting

> **Tags:** `bash` `shell` `scripting` `linux` `automation` `devops`
> **Level:** Intermediate | **Prerequisite:** `terminal/01-terminal-basics.md`

---

## 1. Script Basics & Best Practices

```bash
#!/usr/bin/env bash
# Always use env to find bash (not /bin/bash — may differ on macOS)

# Strict mode (ALWAYS use this!)
set -euo pipefail
# -e: exit immediately on error
# -u: treat unset variables as errors
# -o pipefail: pipeline fails if any command fails (not just last)

# Debug mode (shows each command before executing)
set -x    # Enable
set +x    # Disable

# Track errors with line numbers
trap 'echo "Error on line $LINENO"' ERR

# Cleanup on exit
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT    # Runs always when script exits

echo "Temp directory: $TMPDIR"
```

---

## 2. Variables & Quoting

```bash
# Variables
name="Alice"
echo "$name"        # "Alice" — always quote variables!
echo "${name}"      # Explicit — use when adjacent to other chars
echo "${name}Jr"    # ✅ "AliceJr"

# Double quotes: expand variables, keep spaces
# Single quotes: literal, no expansion

path="/home/user/my file.txt"
ls "$path"    # ✅ Works (quotes preserve space)
ls $path      # ❌ ls /home/user/my file.txt — treated as 2 args

# Command substitution
today=$(date +%Y-%m-%d)
user=$(whoami)
files=$(ls -la | wc -l)

# Arithmetic
count=5
((count++))
count=$((count + 10))
result=$(echo "scale=2; 10/3" | bc)   # Floating point

# Default values
name="${1:-World}"                  # Use "World" if $1 unset or empty
file="${INPUT_FILE:?'INPUT_FILE is required'}"  # Error if unset

# String operations
str="Hello, World!"
echo ${#str}              # Length: 13
echo ${str:7}             # World! (substring from index 7)
echo ${str:7:5}           # World (substring 5 chars)
echo ${str/World/Bash}    # Hello, Bash! (replace first)
echo ${str//l/L}          # HeLLo, WorLd! (replace all)
echo ${str^^}             # HELLO, WORLD! (uppercase)
echo ${str,,}             # hello, world! (lowercase)

# Path manipulation
file="/home/user/script.sh"
echo ${file##*/}      # script.sh (basename)
echo ${file%/*}       # /home/user (dirname)
echo ${file%.sh}      # /home/user/script (remove extension)
echo ${file##*.}      # sh (extension)

# Arrays
fruits=("apple" "banana" "cherry")
echo "${fruits[0]}"          # apple
echo "${fruits[@]}"          # All elements
echo "${#fruits[@]}"         # Count: 3
fruits+=("date")             # Append
fruits[1]="blueberry"        # Modify

# Iterate array
for fruit in "${fruits[@]}"; do
  echo "$fruit"
done

# Associative arrays (bash 4+)
declare -A config
config[host]="localhost"
config[port]="5432"
config[db]="myapp"

echo "${config[host]}"
for key in "${!config[@]}"; do
  echo "$key = ${config[$key]}"
done
```

---

## 3. Conditionals

```bash
# if/elif/else
if [ "$1" = "help" ]; then
  echo "Usage: script.sh [option]"
elif [ "$1" = "version" ]; then
  echo "v1.0.0"
else
  echo "Unknown option: $1"
fi

# [[ ]] — modern, more features (preferred over [ ])
name="Alice"
if [[ "$name" == "Alice" ]]; then echo "Hi Alice"; fi
if [[ "$name" =~ ^[A-Z] ]]; then echo "Starts with uppercase"; fi
if [[ -z "$name" ]]; then echo "Empty"; fi    # -z: empty string
if [[ -n "$name" ]]; then echo "Not empty"; fi

# File tests
if [[ -f "$file" ]]; then echo "Is regular file"; fi
if [[ -d "$dir" ]]; then echo "Is directory"; fi
if [[ -e "$path" ]]; then echo "Exists"; fi
if [[ -r "$file" ]]; then echo "Readable"; fi
if [[ -w "$file" ]]; then echo "Writable"; fi
if [[ -x "$file" ]]; then echo "Executable"; fi
if [[ -s "$file" ]]; then echo "Non-empty"; fi

# Numeric comparisons
num=42
if [[ $num -gt 10 ]]; then echo "Greater than 10"; fi
if [[ $num -le 100 ]]; then echo "Less or equal to 100"; fi
# -eq -ne -gt -ge -lt -le

# Logical operators
if [[ -f "$file" && -r "$file" ]]; then echo "File exists and readable"; fi
if [[ $1 == "yes" || $1 == "y" ]]; then echo "Confirmed"; fi

# Single-line shortcuts
[[ -d "$dir" ]] || mkdir -p "$dir"      # Create if not exists
[[ -n "$var" ]] && echo "var is set"    # Execute if condition true

# case statement
case "$1" in
  start)
    echo "Starting service..."
    ;;
  stop|halt)    # Multiple patterns
    echo "Stopping service..."
    ;;
  restart)
    $0 stop
    $0 start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}" >&2
    exit 1
    ;;
esac
```

---

## 4. Loops

```bash
# for loop
for i in {1..10}; do
  echo "Number: $i"
done

for i in {0..20..2}; do   # 0, 2, 4, ..., 20 (step 2)
  echo "$i"
done

for file in /etc/*.conf; do
  echo "Config: $file"
done

# C-style for loop
for (( i=0; i<10; i++ )); do
  echo "$i"
done

# while loop
count=0
while [[ $count -lt 10 ]]; do
  echo "$count"
  ((count++))
done

# Read file line by line
while IFS= read -r line; do    # IFS= preserves leading whitespace
  echo "Line: $line"
done < file.txt

# Read command output
while IFS= read -r user; do
  echo "Processing user: $user"
done < <(getent passwd | cut -d: -f1)   # Process substitution

# until loop (continue until condition is true)
until [[ $count -ge 10 ]]; do
  ((count++))
done

# Loop control
for i in {1..100}; do
  [[ $i -eq 50 ]] && break     # Exit loop
  [[ $i -lt 10 ]] && continue  # Skip to next iteration
  echo "$i"
done
```

---

## 5. Functions

```bash
# Function definition
greet() {
  local name="$1"    # local = function-scoped
  local greeting="${2:-Hello}"  # Default value for second arg
  echo "$greeting, $name!"
}

greet "Alice"           # "Hello, Alice!"
greet "Bob" "Hi"        # "Hi, Bob!"

# Return value (via echo + command substitution)
get_user_count() {
  local db="$1"
  psql -t -c "SELECT COUNT(*) FROM users" "$db" 2>/dev/null | tr -d '[:space:]'
}

count=$(get_user_count "myapp")
echo "Users: $count"

# Return status (0=success, 1-255=error)
file_exists() {
  [[ -f "$1" ]]   # Returns 0 if true, 1 if false
}

if file_exists "/etc/hosts"; then
  echo "File exists"
fi

# Passing arrays to functions
process_files() {
  local -n files_ref=$1   # nameref: reference to array by name
  
  for file in "${files_ref[@]}"; do
    echo "Processing: $file"
  done
}

my_files=("a.txt" "b.txt" "c.txt")
process_files my_files  # Pass array by name

# Error handling in functions
deploy() {
  local env="$1"
  
  if [[ -z "$env" ]]; then
    echo "Error: environment required" >&2
    return 1
  fi
  
  echo "Deploying to $env..."
  # ... deployment logic
}

deploy "production" || { echo "Deploy failed!"; exit 1; }
```

---

## 6. Input & Output

```bash
# Read user input
read -p "Enter your name: " name
read -s -p "Enter password: " password   # -s: silent (no echo)
echo ""  # Newline after silent input

# Input with timeout
if read -t 10 -p "Continue? (y/n) " answer; then
  [[ "$answer" == "y" ]] && echo "Continuing..."
else
  echo "Timeout — defaulting to no"
fi

# Redirect
command > output.txt      # Stdout to file (overwrite)
command >> output.txt     # Stdout to file (append)
command 2> error.txt      # Stderr to file
command 2>&1 | less       # Stderr to stdout, pipe to less
command > output.txt 2>&1 # Both stdout and stderr to file
command &> output.txt     # Shorthand for above
command 2>/dev/null       # Discard stderr

# Heredoc (multi-line string)
cat << EOF
This is a
multi-line
string
EOF

# Heredoc into file
cat > /tmp/config.yaml << 'EOF'
# Single quotes prevent variable expansion
database:
  host: ${DB_HOST}    # Literal — not expanded!
  port: 5432
EOF

# Tee (write to file AND stdout)
make build 2>&1 | tee build.log

# Process substitution
diff <(ls dir1) <(ls dir2)    # Compare outputs of two commands

# printf (preferred over echo for complex formatting)
printf "%-20s %5.2f\n" "Product name" 9.99
printf "Error: %s (code %d)\n" "$msg" "$code" >&2
```

---

## 7. Error Handling & Logging

```bash
# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

log_info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $*" >&2; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_debug()   { [[ "${DEBUG:-}" == "true" ]] && echo -e "${BLUE}[DEBUG]${NC} $*"; }

# Robust error handling
set -euo pipefail

handle_error() {
  local exit_code=$?
  local line_no=$1
  log_error "Script failed on line $line_no with exit code $exit_code"
  cleanup
  exit $exit_code
}

cleanup() {
  log_info "Cleaning up..."
  [[ -n "${TMPFILE:-}" && -f "$TMPFILE" ]] && rm -f "$TMPFILE"
}

trap 'handle_error $LINENO' ERR
trap cleanup EXIT

# Retry function
retry() {
  local max_attempts=$1
  local delay=$2
  shift 2
  
  local attempt=1
  while (( attempt <= max_attempts )); do
    if "$@"; then
      return 0
    fi
    
    log_warn "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
    sleep "$delay"
    ((attempt++))
    delay=$((delay * 2))    # Exponential backoff
  done
  
  log_error "All $max_attempts attempts failed"
  return 1
}

# Usage
retry 3 5 curl -f "https://api.example.com/health"
retry 5 10 kubectl rollout status deployment/api
```

---

## 8. Practical Scripts

```bash
# Deploy script
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEPLOY_ENV="${1:?Usage: deploy.sh <environment>}"
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)
readonly LOG_FILE="/var/log/deploys/deploy_${TIMESTAMP}.log"

source "${SCRIPT_DIR}/lib/common.sh"   # Load shared functions

# Validate
if [[ ! "$DEPLOY_ENV" =~ ^(staging|production)$ ]]; then
  log_error "Invalid environment: $DEPLOY_ENV (must be staging or production)"
  exit 1
fi

# Require confirmation for production
if [[ "$DEPLOY_ENV" == "production" ]]; then
  read -p "Deploy to PRODUCTION? Type 'yes' to confirm: " confirm
  [[ "$confirm" != "yes" ]] && { log_info "Aborted"; exit 0; }
fi

log_info "Starting deploy to $DEPLOY_ENV"

# Run tests
log_info "Running tests..."
npm test 2>&1 | tee -a "$LOG_FILE"

# Build
log_info "Building..."
docker build -t "myapp:${TIMESTAMP}" -f Dockerfile . 2>&1 | tee -a "$LOG_FILE"

# Push
log_info "Pushing image..."
docker push "registry.example.com/myapp:${TIMESTAMP}" 2>&1 | tee -a "$LOG_FILE"

# Deploy (with rollback on failure)
PREVIOUS=$(kubectl get deployment/api -o jsonpath='{.spec.template.spec.containers[0].image}')

log_info "Deploying image..."
kubectl set image deployment/api api="myapp:${TIMESTAMP}" -n "$DEPLOY_ENV"

if ! kubectl rollout status deployment/api -n "$DEPLOY_ENV" --timeout=300s; then
  log_error "Deployment failed! Rolling back to $PREVIOUS"
  kubectl set image deployment/api api="$PREVIOUS" -n "$DEPLOY_ENV"
  exit 1
fi

log_info "Deploy to $DEPLOY_ENV completed successfully!"
log_info "Log: $LOG_FILE"
```

---

## 9. Useful One-Liners & Patterns

```bash
# Find and process files
find . -name "*.log" -mtime +7 -exec rm {} \;     # Delete logs older than 7 days
find . -name "*.ts" | xargs grep -l "TODO"        # Find TS files with TODO
find . -type f -newer reffile                      # Files newer than reference

# CSV processing with awk
awk -F, '{print $1, $3}' data.csv                 # Print columns 1 and 3
awk -F, 'NR>1 {sum += $2} END {print sum}' data.csv  # Sum column 2, skip header

# JSON with jq
cat response.json | jq '.data.users[] | {id, name}'
cat response.json | jq -r '.items[] | "\(.id),\(.name)"' > export.csv

# Parallel execution
for server in server1 server2 server3; do
  ssh "$server" "systemctl restart nginx" &   # Run in background
done
wait    # Wait for all background jobs

# Or with GNU parallel
echo "server1 server2 server3" | tr ' ' '\n' | parallel ssh {} "systemctl restart nginx"

# Check if command succeeds silently
if command -v docker &>/dev/null; then
  echo "Docker is installed"
fi

# Lock file (prevent concurrent runs)
LOCKFILE="/tmp/myscript.lock"
exec 9>"$LOCKFILE"
if ! flock -n 9; then
  echo "Script is already running" >&2
  exit 1
fi
# ... rest of script
```

---

*Tài liệu liên quan: `terminal/01-terminal-basics.md` | `terminal/03-shell-tools.md` | `cicd/01-github-actions.md`*
