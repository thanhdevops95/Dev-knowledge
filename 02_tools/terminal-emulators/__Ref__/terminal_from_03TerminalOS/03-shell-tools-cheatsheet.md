# 🛠️ Shell Tools Cheatsheet — Tra cứu nhanh công cụ CLI

> `[BEGINNER → INTERMEDIATE]` — Bảng tra nhanh các công cụ command-line phổ biến nhất.
> Prerequisite: `01-terminal-basics.md`

---

## 1. Navigation & File Management

```bash
# ── Di chuyển & Xem ──
pwd                     # Print working directory
ls -la                  # List all files (long format)
ls -lh                  # Human-readable sizes
ls -lt                  # Sort by modification time
tree -L 2               # Directory tree, 2 levels deep
cd -                    # Go to previous directory
pushd /tmp && popd      # Stack-based directory navigation

# ── Tạo & Xóa ──
mkdir -p a/b/c          # Create nested directories
touch file.txt          # Create empty file
cp -r src/ dst/         # Copy recursively
mv old.txt new.txt      # Move/rename
rm -rf dir/             # ⚠️ Force remove directory
ln -s target link       # Symbolic link

# ── Tìm kiếm file ──
find . -name "*.py"                        # By name
find . -name "*.log" -mtime -7             # Modified in last 7 days
find . -size +100M                         # Files > 100MB
find . -name "*.tmp" -delete               # Find & delete
find . -type f -name "*.js" -not -path "*/node_modules/*"

# fd — faster find (Rust-based)
fd "\.py$"              # Find Python files
fd -e md                # Find by extension
fd -H "\.env"           # Include hidden files
```

---

## 2. Text Processing — Xử lý văn bản

```bash
# ── cat / bat ──
cat file.txt                   # Print file
cat file1 file2 > merged.txt   # Concatenate
bat file.txt                   # cat with syntax highlighting (install: cargo install bat)
head -20 file.txt              # First 20 lines
tail -20 file.txt              # Last 20 lines
tail -f app.log                # Follow log in real-time ⭐

# ── grep — Tìm kiếm text ──
grep "error" app.log                       # Basic search
grep -r "TODO" ./src                       # Recursive search
grep -i "warning" app.log                  # Case insensitive
grep -n "function" file.js                 # Show line numbers
grep -c "error" app.log                    # Count matches
grep -v "debug" app.log                    # Invert (exclude)
grep -E "error|warning|critical" app.log   # Extended regex (OR)
grep -l "TODO" **/*.py                     # List files only

# ripgrep (rg) — faster grep ⭐
rg "TODO" ./src                # Recursive, respects .gitignore
rg -t py "import"              # Search only Python files
rg -i "error" --json           # JSON output
rg "func\w+" -o                # Only show matches

# ── sed — Stream editor ──
sed 's/old/new/' file.txt                  # Replace first occurrence per line
sed 's/old/new/g' file.txt                 # Replace ALL occurrences
sed -i 's/old/new/g' file.txt             # In-place edit ⚠️
sed -n '10,20p' file.txt                   # Print lines 10-20
sed '/^#/d' file.txt                       # Delete comment lines

# ── awk — Column processing ──
awk '{print $1}' file.txt                  # Print first column
awk -F',' '{print $2}' data.csv            # CSV second column
awk '{sum += $1} END {print sum}' nums.txt # Sum first column
awk '/error/ {count++} END {print count}' log  # Count errors
df -h | awk 'NR>1 {print $5, $6}'         # Disk usage: % + mount

# ── sort & uniq ──
sort file.txt                     # Sort alphabetically
sort -n file.txt                  # Sort numerically
sort -r file.txt                  # Reverse sort
sort -t',' -k2 file.csv           # Sort CSV by column 2
sort file.txt | uniq              # Remove duplicates
sort file.txt | uniq -c | sort -rn  # Count + sort by frequency ⭐

# ── wc — Word count ──
wc -l file.txt          # Line count
wc -w file.txt          # Word count
find . -name "*.py" | xargs wc -l | tail -1  # Total lines of Python code

# ── cut & paste ──
cut -d',' -f1,3 data.csv        # Extract columns 1,3 from CSV
cut -c1-10 file.txt             # First 10 characters per line
paste file1 file2               # Merge files side by side
```

---

## 3. Piping & Redirection

```bash
# ── Pipes (|) ──
cat app.log | grep "error" | sort | uniq -c | sort -rn | head -10
#  1. Read log  2. Filter    3. Sort  4. Count  5. Top 10 errors

# ── Redirection ──
command > file.txt      # Stdout → file (overwrite)
command >> file.txt     # Stdout → file (append)
command 2> error.log    # Stderr → file
command &> all.log      # Both stdout + stderr → file
command < input.txt     # File → stdin
command1 | tee file.txt | command2  # Split output ⭐

# ── Here document ──
cat << 'EOF' > config.yaml
name: my-app
version: 1.0
debug: false
EOF
```

---

## 4. Process Management

```bash
# ── Xem processes ──
ps aux                  # All processes
ps aux | grep node      # Find node processes
top                     # Live process monitor
htop                    # Better top (interactive) ⭐
btop                    # Even better top (Rust-based)

# ── Kill processes ──
kill <PID>              # Graceful terminate (SIGTERM)
kill -9 <PID>           # Force kill (SIGKILL) ⚠️
killall node            # Kill all node processes
pkill -f "python app"   # Kill by command pattern

# ── Background & Jobs ──
command &               # Run in background
jobs                    # List background jobs
fg %1                   # Bring job 1 to foreground
bg %1                   # Resume job 1 in background
nohup command &         # Keep running after logout
Ctrl+Z                  # Suspend current process
Ctrl+C                  # Interrupt (SIGINT)

# ── Screen / Tmux ──
tmux new -s session1    # New named session
tmux attach -t session1 # Attach to session
tmux ls                 # List sessions
# Ctrl+B then D         # Detach
# Ctrl+B then C         # New window
# Ctrl+B then N         # Next window
# Ctrl+B then %         # Split vertical
# Ctrl+B then "         # Split horizontal
```

---

## 5. Network Tools

```bash
# ── HTTP requests ──
curl https://api.example.com              # GET request
curl -X POST -d '{"key":"val"}' -H "Content-Type: application/json" URL
curl -o file.zip URL                      # Download file
curl -I URL                               # Headers only
curl -s URL | jq .                        # Pretty print JSON ⭐

# HTTPie (friendlier curl)
http GET api.example.com/users
http POST api.example.com/users name=John
http --json POST URL key=value

# wget
wget URL                        # Download file
wget -r -l 2 URL                # Recursive download, 2 levels

# ── DNS & Network ──
ping google.com                 # Test connectivity
nslookup google.com             # DNS lookup
dig google.com                  # Detailed DNS
traceroute google.com           # Trace network path
ss -tlnp                        # Listening ports (Linux)
netstat -an | grep LISTEN       # Listening ports (macOS)
lsof -i :3000                  # Process using port 3000
```

---

## 6. Disk & System

```bash
# ── Disk usage ──
df -h                   # Filesystem usage (human-readable)
du -sh *                # Size of each item in current dir
du -sh . --max-depth=1  # Size of subdirectories
ncdu /                  # Interactive disk usage ⭐

# ── System info ──
uname -a                # System info
hostname                # Machine name
uptime                  # System uptime
free -h                 # Memory usage (Linux)
lscpu                   # CPU info

# ── Archives ──
tar -czf archive.tar.gz dir/    # Create gzip archive
tar -xzf archive.tar.gz         # Extract gzip archive
tar -xf archive.tar.bz2         # Extract bzip2
zip -r archive.zip dir/         # Create zip
unzip archive.zip               # Extract zip
```

---

## 7. Modern CLI Alternatives

| Classic | Modern | Language | Cải thiện |
|---|---|---|---|
| `find` | **fd** | Rust | 5x faster, sane defaults |
| `grep` | **ripgrep (rg)** | Rust | 10x faster, .gitignore respect |
| `cat` | **bat** | Rust | Syntax highlighting, line numbers |
| `ls` | **exa / eza** | Rust | Colors, git status, tree |
| `top` | **btop / htop** | C++/C | Interactive, visual |
| `du` | **ncdu / dust** | C/Rust | Interactive, visual |
| `cd` | **zoxide (z)** | Rust | Frecency-based autojump |
| `diff` | **delta** | Rust | Syntax-highlighted diffs |
| `man` | **tldr** | Multi | Simplified man pages |
| `jq` | **jq** | C | JSON processing ⭐ |

```bash
# Install (macOS)
brew install fd ripgrep bat eza zoxide btop delta tldr jq

# Install (Ubuntu)
sudo apt install fd-find ripgrep bat
```

---

## 8. jq — JSON Processing

```bash
# Pretty print
echo '{"name":"An","age":25}' | jq .

# Extract field
echo '{"name":"An","age":25}' | jq '.name'   # "An"

# Array operations
echo '[1,2,3,4,5]' | jq 'map(. * 2)'         # [2,4,6,8,10]

# Complex query
curl -s https://api.github.com/users/octocat/repos |
  jq '.[].name'                                # List repo names

curl -s https://api.github.com/users/octocat/repos |
  jq '.[] | {name: .name, stars: .stargazers_count}' |
  jq -s 'sort_by(.stars) | reverse | .[0:5]'  # Top 5 by stars
```

---

## Tài nguyên thêm

- [The Art of Command Line](https://github.com/jlevy/the-art-of-command-line) — Must-read CLI guide
- [explainshell.com](https://explainshell.com/) — Giải thích bất kỳ lệnh nào
- [tldr-pages](https://tldr.sh/) — Simplified man pages
- [Modern Unix](https://github.com/ibraheemdev/modern-unix) — Collection modern CLI tools
- [ShellCheck](https://www.shellcheck.net/) — Linter cho bash scripts
