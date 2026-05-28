# LABS - Module 01: LINUX BASICS

> **Mục tiêu:** Master 50+ Linux commands thông qua hands-on practice
>
> **Thời gian:** 3-5 giờ
>
> **Prerequisites:** Module 00 completed (WSL2 Ubuntu installed)

---

## 📋 Danh sách Labs

| Lab | Tên | Thời gian | Độ khó |
|-----|-----|-----------|--------|
| Lab 1 | File System Navigation | 20 phút | ⭐☆☆☆☆ |
| Lab 2 | File & Directory Operations | 30 phút | ⭐⭐☆☆☆ |
| Lab 3 | Text File Manipulation | 25 phút | ⭐⭐☆☆☆ |
| Lab 4 | Searching & Finding Files | 20 phút | ⭐⭐☆☆☆ |
| Lab 5 | File Permissions | 30 phút | ⭐⭐⭐☆☆ |
| Lab 6 | Process Management | 25 phút | ⭐⭐☆☆☆ |
| Lab 7 | Package Management | 20 phút | ⭐⭐☆☆☆ |
| Lab 8 | Basic Shell Scripting | 40 phút | ⭐⭐⭐☆☆ |
| Lab 9 | System Information & Monitoring | 20 phút | ⭐⭐☆☆☆ |

**Tổng thời gian:** ~3.5 giờ

---

## Lab 1: File System Navigation

### Objectives

- Hiểu Linux file system hierarchy
- Navigate directories với `cd`, `ls`, `pwd`
- Understand absolute vs relative paths

### Instructions

#### Step 1.1: Check Current Location

```bash
# Where am I?
pwd
```

**Expected Output:**

```
/home/username
```

**Explanation:**

- `pwd` = Print Working Directory
- Always shows absolute path từ root (/)

#### Step 1.2: List Home Directory Contents

```bash
# List files
ls
```

**Expected Output:**

```
(có thể empty nếu fresh install)
```

```bash
# List với details
ls -l
```

**Expected Output:**

```
total 0
```

```bash
# List ALL (including hidden files)
ls -la
```

**Expected Output:**

```
total 28
drwxr-xr-x 4 username username 4096 Dec 25 10:00 .
drwxr-xr-x 3 root     root     4096 Dec 24 09:00 ..
-rw-r--r-- 1 username username  220 Dec 24 09:00 .bash_logout
-rw-r--r-- 1 username username 3771 Dec 24 09:00 .bashrc
drwxr-xr-x 3 username username 4096 Dec 25 10:00 .config
-rw-r--r-- 1 username username  807 Dec 24 09:00 .profile
drwxr-xr-x 2 username username 4096 Dec 25 11:00 .ssh
```

**Understanding the output:**

```
drwxr-xr-x  4  username  username  4096  Dec 25 10:00  .config
│           │  │         │         │     │             │
│           │  │         │         │     │             └─ Filename
│           │  │         │         │     └─ Modification time
│           │  │         │         └─ Size (bytes)
│           │  │         └─ Group owner
│           │  └─ User owner
│           └─ Number of hard links
└─ Permissions (d = directory, - = file)
```

#### Step 1.3: Explore Root Directory

```bash
# Go to root
cd /

# Check location
pwd
```

**Expected Output:**

```
/
```

```bash
# List root contents
ls
```

**Expected Output:**

```
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
```

**Explore key directories:**

```bash
# System binaries
ls /bin
# Output: ls, cat, cp, mv, rm, ...

# Configuration files
ls /etc
# Output: passwd, hosts, hostname, ...

# User home directories
ls /home
# Output: username/

# Temporary files
ls /tmp
# Output: (various temp files)
```

#### Step 1.4: Practice Absolute Paths

```bash
# Absolute path - always starts with /
cd /home/username
pwd
# Output: /home/username

cd /usr/bin
pwd
# Output: /usr/bin

cd /etc
pwd
# Output: /etc

# Back to home (any of these work)
cd ~
cd $HOME
cd  # (cd with no args = go home)
pwd
# Output: /home/username
```

#### Step 1.5: Practice Relative Paths

```bash
# Start from home
cd ~
pwd
# Output: /home/username

# Create test structure
mkdir -p projects/web/frontend
mkdir -p projects/api/backend
```

**Navigate with relative paths:**

```bash
# From /home/username to projects
cd projects
pwd
# Output: /home/username/projects

# From projects to web
cd web
pwd
# Output: /home/username/projects/web

# Up one level (..)
cd ..
pwd
# Output: /home/username/projects

# Up two levels (../..)
cd ../..
pwd
# Output: /home/username

# Relative path from home to frontend
cd projects/web/frontend
pwd
# Output: /home/username/projects/web/frontend

# Back to home
cd ~
```

#### Step 1.6: Special Paths

```bash
# Current directory
ls .
# Same as: ls

# Parent directory
ls ..

# Home directory
ls ~

# Previous directory
cd /etc
cd /tmp
cd -  # Go back to /etc
pwd
# Output: /etc

cd -  # Toggle back to /tmp
pwd
# Output: /tmp
```

#### Step 1.7: Tab Completion Practice

```bash
# Type this, then press TAB:
cd /u[TAB]
# Completes to: cd /usr/

cd /usr/b[TAB]
# Completes to: cd /usr/bin/

# Multiple matches - press TAB twice:
cd /usr/[TAB][TAB]
# Shows: bin/ games/ include/ lib/ local/ sbin/ share/ src/
```

#### Step 1.8: Verification Exercise

**Exercise:** Navigate to `/usr/local/bin` using:

1. Absolute path
2. Relative path (from home)
3. Tab completion

**Solutions:**

```bash
# 1. Absolute
cd /usr/local/bin
pwd

# 2. Relative (from home)
cd ~
cd ../../usr/local/bin
pwd

# 3. Tab completion
cd /u[TAB]l[TAB]b[TAB]
pwd
```

**All should output:**

```
/usr/local/bin
```

✅ **Lab 1 Complete!** You can now navigate like a pro!

---

## Lab 2: File & Directory Operations

### Objectives

- Create, copy, move, delete files and directories
- Understand wildcards and globbing
- Practice safe file operations

### Instructions

#### Step 2.1: Setup Lab Environment

```bash
# Go to home
cd ~

# Create lab directory
mkdir linux-lab
cd linux-lab

# Verify
pwd
```

**Expected Output:**

```
/home/username/linux-lab
```

#### Step 2.2: Create Files

**Create empty files:**

```bash
# Method 1: touch
touch file1.txt
touch file2.txt file3.txt  # Multiple files

# Method 2: redirect
echo "Hello" > file4.txt
echo "World" > file5.txt

# Method 3: cat with redirect
cat > file6.txt
This is line 1
This is line 2
[Ctrl + D to finish]

# Verify
ls -l
```

**Expected Output:**

```
-rw-r--r-- 1 username username    0 Dec 25 10:00 file1.txt
-rw-r--r-- 1 username username    0 Dec 25 10:00 file2.txt
-rw-r--r-- 1 username username    0 Dec 25 10:00 file3.txt
-rw-r--r-- 1 username username    6 Dec 25 10:00 file4.txt
-rw-r--r-- 1 username username    6 Dec 25 10:00 file5.txt
-rw-r--r-- 1 username username   28 Dec 25 10:00 file6.txt
```

**View file contents:**

```bash
cat file4.txt
# Output: Hello

cat file5.txt
# Output: World

cat file6.txt
# Output:
# This is line 1
# This is line 2
```

#### Step 2.3: Create Directories

```bash
# Single directory
mkdir documents

# Multiple directories
mkdir images videos

# Nested directories (without -p = error)
mkdir projects/python/scripts
# Error: mkdir: cannot create directory 'projects/python/scripts': No such file or directory

# With -p (create parent directories)
mkdir -p projects/python/scripts
mkdir -p projects/nodejs/{src,tests,docs}

# Verify structure
ls -R projects
```

**Expected Output:**

```
projects:
nodejs  python

projects/nodejs:
docs  src  tests

projects/nodejs/docs:

projects/nodejs/src:

projects/nodejs/tests:

projects/python:
scripts

projects/python/scripts:
```

#### Step 2.4: Copy Files

```bash
# Copy single file
cp file1.txt file1_backup.txt

# Copy with different name
cp file2.txt documents/file2_copy.txt

# Copy multiple files to directory
cp file3.txt file4.txt file5.txt documents/

# Copy with verbose output
cp -v file6.txt documents/
```

**Expected Output (verbose):**

```
'file6.txt' -> 'documents/file6.txt'
```

```bash
# Verify
ls documents/
```

**Expected Output:**

```
file2_copy.txt  file3.txt  file4.txt  file5.txt  file6.txt
```

**Copy directories:**

```bash
# Copy directory (MUST use -r for recursive)
cp documents documents_backup
# Error: cp: -r not specified; omitting directory 'documents'

# Correct:
cp -r documents documents_backup

# Verify
ls -l
```

**Expected Output:**

```
drwxr-xr-x 2 username username 4096 Dec 25 10:05 documents
drwxr-xr-x 2 username username 4096 Dec 25 10:06 documents_backup
```

#### Step 2.5: Move/Rename Files

```bash
# Rename file
mv file1.txt renamed_file.txt

# Move file to directory
mv file2.txt documents/

# Move multiple files
mv file3.txt file4.txt file5.txt images/

# Move and rename
mv file6.txt documents/important.txt

# Move directory
mv documents_backup old_documents

# Verify
ls
ls documents/
ls images/
ls old_documents/
```

#### Step 2.6: Delete Files & Directories

**⚠️ WARNING: No trash/recycle bin in Linux! Deleted = gone forever!**

```bash
# Delete single file
rm renamed_file.txt

# Delete multiple files
cd images/
rm file3.txt file4.txt

# Delete with confirmation (-i = interactive)
rm -i file5.txt
# Prompt: rm: remove regular file 'file5.txt'? 
# Type: y

cd ..

# Cannot delete directory with rm
rm images
# Error: rm: cannot remove 'images': Is a directory

# Delete empty directory
rmdir images
# Success (images was empty after deleting files)

# Delete non-empty directory (MUST use -r)
rm -r old_documents

# Safe delete with verbose + confirm
rm -riv documents
# Prompts for each file:
# rm: descend into directory 'documents/'? y
# rm: remove regular file 'documents/file2.txt'? y
# ...
```

**Create test for wildcards:**

```bash
# Create test files
touch test1.txt test2.txt test3.log test4.log report.pdf

# List all
ls
```

#### Step 2.7: Wildcards (Globbing)

```bash
# * = zero or more characters
ls *.txt
# Output: test1.txt test2.txt

ls *.log
# Output: test3.log test4.log

ls test*
# Output: test1.txt test2.txt test3.log test4.log

# ? = exactly one character
touch file1.txt file2.txt file10.txt

ls file?.txt
# Output: file1.txt file2.txt (NOT file10.txt)

ls file??.txt
# Output: file10.txt

# [] = character set
touch data1.txt data2.txt data3.txt dataA.txt dataB.txt

ls data[123].txt
# Output: data1.txt data2.txt data3.txt

ls data[A-Z].txt
# Output: dataA.txt dataB.txt

# Delete with wildcards (BE CAREFUL!)
rm test*.log
# Deletes: test3.log test4.log

# Verify
ls
```

#### Step 2.8: Practice Exercise

**Exercise:** Create this structure:

```
workspace/
├── frontend/
│   ├── src/
│   ├── public/
│   └── README.md
├── backend/
│   ├── api/
│   ├── db/
│   └── README.md
└── docs/
    └── setup.md
```

**Solution:**

```bash
cd ~/linux-lab

mkdir -p workspace/{frontend/{src,public},backend/{api,db},docs}

touch workspace/frontend/README.md
touch workspace/backend/README.md
touch workspace/docs/setup.md

# Verify with tree (install if needed: sudo apt install tree)
tree workspace

# Or verify with find
find workspace -type f  # Files only
find workspace -type d  # Directories only
```

**Expected tree output:**

```
workspace/
├── backend
│   ├── api
│   ├── db
│   └── README.md
├── docs
│   └── setup.md
└── frontend
    ├── public
    ├── README.md
    └── src
```

✅ **Lab 2 Complete!** You can create and manage files like a boss!

---

## Lab 3: Text File Manipulation

### Objectives

- View file contents với various tools
- Search trong files
- Edit files với nano
- Redirect input/output

### Instructions

#### Step 3.1: Create Sample Files

```bash
cd ~/linux-lab
mkdir text-lab
cd text-lab

# Create multi-line file
cat > sample.txt << 'EOF'
Linux is awesome!
DevOps is the future.
Shell scripting is powerful.
Docker containers rock.
Kubernetes orchestrates.
EOF

# Create log file
cat > app.log << 'EOF'
2024-12-25 10:00:00 INFO Server started
2024-12-25 10:01:15 INFO User alice logged in
2024-12-25 10:02:30 WARN High memory usage: 85%
2024-12-25 10:03:45 ERROR Connection timeout
2024-12-25 10:04:00 INFO User bob logged in
2024-12-25 10:05:10 ERROR Database connection failed
2024-12-25 10:06:20 INFO Server shutdown
EOF
```

#### Step 3.2: View File Contents

**cat - Display entire file:**

```bash
cat sample.txt
```

**Expected Output:**

```
Linux is awesome!
DevOps is the future.
Shell scripting is powerful.
Docker containers rock.
Kubernetes orchestrates.
```

**Show line numbers:**

```bash
cat -n sample.txt
```

**Expected Output:**

```
     1  Linux is awesome!
     2  DevOps is the future.
     3  Shell scripting is powerful.
     4  Docker containers rock.
     5  Kubernetes orchestrates.
```

**head - First lines:**

```bash
head -n 3 sample.txt
```

**Expected Output:**

```
Linux is awesome!
DevOps is the future.
Shell scripting is powerful.
```

**tail - Last lines:**

```bash
tail -n 2 sample.txt
```

**Expected Output:**

```
Docker containers rock.
Kubernetes orchestrates.
```

**less - Page through file:**

```bash
# For large files
less app.log

# Navigation in less:
# Space = next page
# b = previous page
# / = search
# q = quit
```

#### Step 3.3: Search in Files with grep

```bash
# Basic search
grep "ERROR" app.log
```

**Expected Output:**

```
2024-12-25 10:03:45 ERROR Connection timeout
2024-12-25 10:05:10 ERROR Database connection failed
```

```bash
# Case-insensitive search
grep -i "info" app.log
```

**Expected Output:**

```
2024-12-25 10:00:00 INFO Server started
2024-12-25 10:01:15 INFO User alice logged in
2024-12-25 10:04:00 INFO User bob logged in
2024-12-25 10:06:20 INFO Server shutdown
```

```bash
# Count matches
grep -c "INFO" app.log
```

**Expected Output:**

```
4
```

```bash
# Show line numbers
grep -n "User" app.log
```

**Expected Output:**

```
2:2024-12-25 10:01:15 INFO User alice logged in
5:2024-12-25 10:04:00 INFO User bob logged in
```

```bash
# Inverted match (lines NOT containing)
grep -v "INFO" app.log
```

**Expected Output:**

```
2024-12-25 10:02:30 WARN High memory usage: 85%
2024-12-25 10:03:45 ERROR Connection timeout
2024-12-25 10:05:10 ERROR Database connection failed
```

```bash
# Search multiple files
echo "test error message" > test.log
grep -r "ERROR" .
```

**Expected Output:**

```
./app.log:2024-12-25 10:03:45 ERROR Connection timeout
./app.log:2024-12-25 10:05:10 ERROR Database connection failed
./test.log:test error message
```

#### Step 3.4: Text Manipulation with sed, awk, cut

**sed - Stream editor:**

```bash
# Replace text
sed 's/Linux/Unix/' sample.txt
```

**Expected Output:**

```
Unix is awesome!        ← Changed
DevOps is the future.
Shell scripting is powerful.
Docker containers rock.
Kubernetes orchestrates.
```

**Note:** Original file unchanged! Use `-i` to edit in-place

```bash
# Replace all occurrences (global)
echo "cat cat cat" | sed 's/cat/dog/g'
# Output: dog dog dog

# Delete lines matching pattern
sed '/Docker/d' sample.txt
```

**Expected Output:**

```
Linux is awesome!
DevOps is the future.
Shell scripting is powerful.
Kubernetes orchestrates.
← Docker line deleted
```

**awk - Pattern scanning:**

```bash
# Print specific columns (space-separated)
echo "John 25 Engineer" > people.txt
echo "Alice 30 Manager" >> people.txt
echo "Bob 28 Designer" >> people.txt

awk '{print $1, $3}' people.txt
```

**Expected Output:**

```
John Engineer
Alice Manager
Bob Designer
```

```bash
# Extract time from logs
awk '{print $2}' app.log
```

**Expected Output:**

```
10:00:00
10:01:15
10:02:30
...
```

**cut - Extract columns:**

```bash
# CSV file
echo "name,age,city" > data.csv
echo "Alice,25,NYC" >> data.csv
echo "Bob,30,LA" >> data.csv

# Get first column
cut -d ',' -f 1 data.csv
```

**Expected Output:**

```
name
Alice
Bob
```

```bash
# Get columns 1 and 3
cut -d ',' -f 1,3 data.csv
```

**Expected Output:**

```
name,city
Alice,NYC
Bob,LA
```

#### Step 3.5: Edit Files with nano

```bash
# Open file in nano
nano sample.txt
```

**Inside nano:**

```
  GNU nano 6.2                  sample.txt                          Modified

Linux is awesome!
DevOps is the future.
Shell scripting is powerful.
Docker containers rock.
Kubernetes orchestrates.


[Add new line here ↓]





^G Help     ^O Write Out   ^W Where Is    ^K Cut
^X Exit     ^R Read File   ^\ Replace     ^U Paste
```

**Practice editing:**

1. Arrow keys to move
2. Type: "Text editors are essential."
3. Ctrl + K to cut line
4. Ctrl + U to paste
5. Ctrl + W to search ("Docker")
6. Ctrl + \ to find and replace ("is" → "IS")
7. Ctrl + O to save (Write Out)
   - Prompt: "File Name to Write: sample.txt"
   - Press Enter
8. Ctrl + X to exit

**Verify changes:**

```bash
cat sample.txt
```

#### Step 3.6: Redirection & Pipes

**Output redirection:**

```bash
# Overwrite file ( > )
echo "New content" > output.txt
cat output.txt
# Output: New content

echo "Replace content" > output.txt
cat output.txt
# Output: Replace content (previous lost)

# Append to file ( >> )
echo "Line 1" > output.txt
echo "Line 2" >> output.txt
echo "Line 3" >> output.txt
cat output.txt
```

**Expected Output:**

```
Line 1
Line 2
Line 3
```

**Pipes ( | ):**

```bash
# Chain commands
cat app.log | grep "ERROR" | wc -l
# Output: 2

# Sort and unique
cat > names.txt << EOF
Alice
Bob
Alice
Charlie
Bob
EOF

cat names.txt | sort | uniq
```

**Expected Output:**

```
Alice
Bob
Charlie
```

```bash
# Count word frequency
cat sample.txt | tr ' ' '\n' | sort | uniq -c | sort -rn
# Output:
#   2 is
#   1 Shell
#   1 scripting
#   ...
```

**Stderr redirection:**

```bash
# Redirect errors to file
ls /nonexistent 2> error.log
cat error.log
# Output: ls: cannot access '/nonexistent': No such file or directory

# Redirect both stdout and stderr
ls /nonexistent > output.txt 2>&1
# Both output and errors in output.txt

# Discard output (/dev/null = black hole)
ls /nonexistent 2> /dev/null
# No output, no error shown
```

#### Step 3.7: Exercise - Log Analysis

**Exercise:** Analyze `app.log`:

1. Count ERROR entries
2. Extract all timestamps of ERRORs
3. Find unique log levels
4. Create report file

**Solutions:**

```bash
# 1. Count ERRORs
grep -c "ERROR" app.log
# Output: 2

# 2. Extract ERROR timestamps
grep "ERROR" app.log | awk '{print $1, $2}'
```

**Expected Output:**

```
2024-12-25 10:03:45
2024-12-25 10:05:10
```

```bash
# 3. Unique log levels
awk '{print $3}' app.log | sort | uniq
```

**Expected Output:**

```
ERROR
INFO
WARN
```

```bash
# 4. Create report
cat > report.txt << 'EOF'
Log Analysis Report
===================
EOF

echo "" >> report.txt
echo "Total lines: $(wc -l < app.log)" >> report.txt
echo "ERROR count: $(grep -c ERROR app.log)" >> report.txt
echo "WARN count: $(grep -c WARN app.log)" >> report.txt
echo "INFO count: $(grep -c INFO app.log)" >> report.txt

cat report.txt
```

**Expected Output:**

```
Log Analysis Report
===================

Total lines: 7
ERROR count: 2
WARN count: 1
INFO count: 4
```

✅ **Lab 3 Complete!** You're a text manipulation wizard!

---

## Lab 4: Searching & Finding Files

### Objectives

- Find files với `find` command
- Locate files với `locate`
- Search in files với advanced `grep`

### Instructions

#### Step 4.1: Setup

```bash
cd ~/linux-lab
mkdir find-lab
cd find-lab

# Create test structure
mkdir -p projects/{web,api,mobile}
touch projects/web/{index.html,style.css,app.js}
touch projects/api/{server.py,database.py,config.yaml}
touch projects/mobile/{App.java,MainActivity.java}
echo "secret key" > projects/api/.env
chmod 600 projects/api/.env  # Secret file
```

#### Step 4.2: Find by Name

```bash
# Find all .js files
find . -name "*.js"
```

**Expected Output:**

```
./projects/web/app.js
```

```bash
# Case-insensitive search
find . -iname "*.JAVA"
```

**Expected Output:**

```
./projects/mobile/App.java
./projects/mobile/MainActivity.java
```

```bash
# Find directories only
find . -type d
```

**Expected Output:**

```
.
./projects
./projects/web
./projects/api
./projects/mobile
```

```bash
# Find files only
find . -type f
```

**Expected Output:**

```
./projects/web/index.html
./projects/web/style.css
./projects/web/app.js
./projects/api/server.py
./projects/api/database.py
./projects/api/config.yaml
./projects/api/.env
./projects/mobile/App.java
./projects/mobile/MainActivity.java
```

#### Step 4.3: Find by Size

```bash
# Create test files
dd if=/dev/zero of=small.txt bs=1K count=10   # 10KB
dd if=/dev/zero of=medium.txt bs=1M count=5   # 5MB
dd if=/dev/zero of=large.txt bs=1M count=50   # 50MB

# Find files > 1MB
find . -type f -size +1M
```

**Expected Output:**

```
./medium.txt
./large.txt
```

```bash
# Find files < 100KB
find . -type f -size -100k
```

```bash
# Find files between 1MB and 10MB
find . -type f -size +1M -size -10M
```

**Expected Output:**

```
./medium.txt
```

#### Step 4.4: Find by Time

```bash
# Find files modified in last 5 minutes
find . -type f -mmin -5

# Find files modified more than 1 hour ago
find . -type f -mmin +60

# Find files accessed today
find . -type f -atime 0

# Find files modified in last 7 days
find . -type f -mtime -7
```

#### Step 4.5: Find by Permissions

```bash
# Find executable files
find . -type f -perm /u+x

# Find files with permission 644
find . -type f -perm 644

# Find world-writable files (security check!)
find . -type f -perm /o+w
```

#### Step 4.6: Execute Commands on Find Results

```bash
# List details of .py files
find . -name "*.py" -exec ls -lh {} \;
```

**Expected Output:**

```
-rw-r--r-- 1 username username 0 Dec 25 10:00 ./projects/api/server.py
-rw-r--r-- 1 username username 0 Dec 25 10:00 ./projects/api/database.py
```

```bash
# Delete old files (BE CAREFUL!)
# Create old test file
touch -d "2020-01-01" old-file.txt

# Find and delete files older than 1000 days
find . -name "old-file.txt" -mtime +1000 -exec rm {} \;

# Safer: ask confirmation  
find . -name "*.bak" -exec rm -i {} \;
```

```bash
# Copy all HTML files to backup directory
mkdir backup
find . -name "*.html" -exec cp {} backup/ \;
```

#### Step 4.7: Advanced Find

```bash
# Combine conditions với -and/-or
find . -name "*.js" -or -name "*.py"

# Find empty files
touch empty.txt
find . -type f -empty
```

**Expected Output:**

```
./empty.txt
./projects/web/index.html
./projects/web/style.css
...
```

```bash
# Find hidden files (start with .)
find . -name ".*"
```

**Expected Output:**

```
./projects/api/.env
```

```bash
# Find and count
find . -type f | wc -l
# Output: (number of files)
```

#### Step 4.8: locate Command (Fast Alternative)

```bash
# Update locate database (first time)
sudo updatedb

# Find files containing "config"
locate config
```

**Note:** `locate` is faster but searches system-wide database (updated periodically)

```bash
# Case-insensitive
locate -i CONFIG

# Count results
locate -c python

# Limit results
locate -l 10 .py
```

#### Step 4.9: which & whereis

```bash
# Find command location
which python3
```

**Expected Output:**

```
/usr/bin/python3
```

```bash
# Find binary, source, manual
whereis python3
```

**Expected Output:**

```
python3: /usr/bin/python3 /usr/bin/python3.10 /usr/lib/python3 /etc/python3 /usr/share/man/man1/python3.1.gz
```

#### Step 4.10: Practice Exercise

**Exercise:** Find all files trong `~/linux-lab`:

1. Modified trong last 30 minutes
2. Larger than 1MB
3. Have `.txt` extension
4. Save list to `large-recent-txt-files.txt`

**Solution:**

```bash
cd ~/linux-lab

find . -type f -mmin -30 -size +1M -name "*.txt" > large-recent-txt-files.txt

cat large-recent-txt-files.txt
```

**Expected Output:**

```
./find-lab/large.txt
./find-lab/medium.txt
```

✅ **Lab 4 Complete!** You can find anything now!

---

## Lab 5: File Permissions

### Objectives

- Understand Linux permission system
- Change file permissions với `chmod`
- Change ownership với `chown`
- Work với special permissions (setuid, setgid, sticky bit)

### Instructions

#### Step 5.1: Understanding Permissions

```bash
cd ~/linux-lab
mkdir permissions-lab
cd permissions-lab

# Create test file
touch testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rw-r--r-- 1 username username 0 Dec 25 10:00 testfile.txt
```

**Understanding the permission string:**

```
-rw-r--r--
│││││││││└ Other: read (r)
││││││││└─ Other: write (-)
│││││││└── Other: execute (-)
││││││└─── Group: read (r)
│││││└──── Group: write (-)
││││└───── Group: execute (-)
│││└────── User: read (r)
││└─────── User: write (w)
│└──────── User: execute (-)
└───────── File type (- = file, d = directory)
```

**Permission values:**

```
r (read)    = 4
w (write)   = 2
x (execute) = 1
- (none)    = 0

rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-- = 4+0+0 = 4
r-x = 4+0+1 = 5
```

#### Step 5.2: Change Permissions with chmod (Symbolic)

```bash
# Add execute permission for user
chmod u+x testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rwxr--r-- 1 username username 0 Dec 25 10:00 testfile.txt
   ↑ (x added)
```

```bash
# Remove write permission for user
chmod u-w testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-r-xr--r-- 1 username username 0 Dec 25 10:00 testfile.txt
  ↑ (w removed)
```

```bash
# Add write back
chmod u+w testfile.txt

# Add execute for group
chmod g+x testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rwxr-xr-- 1 username username 0 Dec 25 10:00 testfile.txt
       ↑ (x added for group)
```

```bash
# Add write for group and other
chmod go+w testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rwxrwxrw- 1 username username 0 Dec 25 10:00 testfile.txt
       ↑  ↑ (w added)
```

```bash
# Set exact permissions untuk all (symbolic = )
chmod u=rwx,g=rx,o=r testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rwxr-xr-- 1 username username 0 Dec 25 10:00 testfile.txt
```

#### Step 5.3: Change Permissions with chmod (Numeric)

```bash
# 755 = rwxr-xr-x
chmod 755 testfile.txt
ls -l testfile.txt
```

**Expected Output:**

```
-rwxr-xr-x 1 username username 0 Dec 25 10:00 testfile.txt
```

**Common permission modes:**

```bash
# 644 = rw-r--r-- (files: owner read/write, others read-only)
chmod 644 testfile.txt

# 755 = rwxr-xr-x (executables: owner full, others read+execute)
chmod 755 testfile.txt

# 600 = rw------- (secrets: only owner access)
chmod 600 testfile.txt

# 777 = rwxrwxrwx (everyone full access - DANGEROUS!)
chmod 777 testfile.txt

# 400 = r-------- (read-only for owner)
chmod 400 testfile.txt
```

**Verify:**

```bash
ls -l testfile.txt
```

#### Step 5.4: Directory Permissions

```bash
# Create test directory
mkdir testdir
ls -ld testdir
```

**Expected Output:**

```
drwxr-xr-x 2 username username 4096 Dec 25 10:00 testdir
```

**Directory permissions meaning:**

```
r (read)    = List contents (ls)
w (write)   = Create/delete files inside
x (execute) = Enter directory (cd)
```

**Test permissions:**

```bash
# Remove execute from directory
chmod u-x testdir
cd testdir
```

**Expected Output:**

```
bash: cd: testdir: Permission denied
```

```bash
# Add back
chmod u+x testdir
cd testdir
# Success!
cd ..

# Remove read
chmod u-r testdir
ls testdir
```

**Expected Output:**

```
ls: cannot open directory 'testdir': Permission denied
```

```bash
# But can still enter (has x)
cd testdir
pwd
# Output: /home/username/linux-lab/permissions-lab/testdir

cd ..

# Fix permissions
chmod 755 testdir
```

#### Step 5.5: Recursive Permissions

```bash
# Create structure
mkdir -p project/{src,docs,tests}
touch project/README.md
touch project/src/{main.py,utils.py}
touch project/docs/guide.md

# Set all files to 644
find project -type f -exec chmod 644 {} \;

# Set all directories to 755
find project -type d -exec chmod 755 {} \;

# Or simply:
chmod -R 755 project  # Sets 755 for ALL (files and dirs)

# Better approach:
chmod -R u=rwX,g=rX,o=rX project
# X (capital) = execute only if file is directory or already has execute
```

**Verify:**

```bash
ls -lR project
```

#### Step 5.6: Change Ownership (chown)

**Note:** Need sudo for chown to other users

```bash
# Create test file
touch myfile.txt
ls -l myfile.txt
```

**Expected Output:**

```
-rw-r--r-- 1 username username 0 Dec 25 10:00 myfile.txt
                │         │
                user    group
```

```bash
# Change owner (need sudo)
sudo chown root myfile.txt
ls -l myfile.txt
```

**Expected Output:**

```
-rw-r--r-- 1 root username 0 Dec 25 10:00 myfile.txt
                │
              changed
```

```bash
# Change both owner and group
sudo chown root:root myfile.txt
ls -l myfile.txt
```

**Expected Output:**

```
-rw-r--r-- 1 root root 0 Dec 25 10:00 myfile.txt
```

```bash
# Change back to yourself
sudo chown username:username myfile.txt

# Recursive ownership change
sudo chown -R username:username project/
```

#### Step 5.7: Special Permissions

**setuid (SUID) - Run as file owner:**

```bash
# Example: /usr/bin/passwd lets normal users change password
ls -l /usr/bin/passwd
```

**Expected Output:**

```
-rwsr-xr-x 1 root root 68208 Nov 29 10:15 /usr/bin/passwd
   ↑ (s = setuid)
```

**Create SUID example:**

```bash
#!/bin/bash
# test-suid.sh
echo "Running as: $(whoami)"
echo "Real user: $USER"

chmod 755 test-suid.sh
chmod u+s test-suid.sh  # Set SUID
ls -l test-suid.sh
```

**Expected Output:**

```
-rwsr-xr-x 1 username username 0 Dec 25 10:00 test-suid.sh
   ↑ s
```

**setgid (SGID) - Inherit group:**

```bash
mkdir shared-folder
chmod g+s shared-folder
ls -ld shared-folder
```

**Expected Output:**

```
drwxr-sr-x 2 username username 4096 Dec 25 10:00 shared-folder
      ↑ s
```

**Sticky bit - Only owner can delete:**

```bash
# /tmp has sticky bit
ls -ld /tmp
```

**Expected Output:**

```
drwxrwxrwt 20 root root 4096 Dec 25 10:00 /tmp
        ↑ t (sticky bit)
```

```bash
# Set sticky bit
mkdir temp-shared
chmod +t temp-shared
ls -ld temp-shared
```

**Expected Output:**

```
drwxr-xr-t 2 username username 4096 Dec 25 10:00 temp-shared
        ↑ t
```

#### Step 5.8: umask - Default Permissions

```bash
# Check current umask
umask
```

**Expected Output:**

```
0002
```

**Understanding umask:**

```
Default file permissions:    666 (rw-rw-rw-)
umask:                      -002
Result:                      664 (rw-rw-r--)

Default directory:           777 (rwxrwxrwx)
umask:                      -002
Result:                      775 (rwxrwxr-x)
```

```bash
# Test
umask 0002
touch test-umask.txt
mkdir test-umask-dir

ls -l test-umask.txt
# Expected: -rw-rw-r--

ls -ld test-umask-dir
# Expected: drwxrwxr-x

# Change umask
umask 0022
touch test-umask2.txt

ls -l test-umask2.txt
# Expected: -rw-r--r--
```

#### Step 5.9: Practice Exercise

**Exercise:** Create secure project structure:

1. Create `secure-project/` directory
2. Inside: `private/`, `shared/`, `public/`
3. `private/`: Only you (700)
4. `shared/`: You and group (750)
5. `public/`: Everyone read (755)
6. Create `secret.txt` in `private/` (600)

**Solution:**

```bash
cd ~/linux-lab/permissions-lab

mkdir -p secure-project/{private,shared,public}

chmod 700 secure-project/private
chmod 750 secure-project/shared
chmod 755 secure-project/public

touch secure-project/private/secret.txt
chmod 600 secure-project/private/secret.txt

# Verify
ls -ld secure-project/*/
ls -l secure-project/private/
```

**Expected Output:**

```
drwx------ 2 username username 4096 Dec 25 10:00 secure-project/private/
drwxr-x--- 2 username username 4096 Dec 25 10:00 secure-project/shared/
drwxr-xr-x 2 username username 4096 Dec 25 10:00 secure-project/public/

-rw------- 1 username username 0 Dec 25 10:00 secret.txt
```

✅ **Lab 5 Complete!** You understand Linux security model!

---

## Lab 6-9: [Continued in next message due to length]

**Labs 6-9 will cover:**

- Lab 6: Process Management
- Lab 7: Package Management
- Lab 8: Basic Shell Scripting
- Lab 9: System Information & Monitoring

**These labs are equally detailed with step-by-step instructions!**

---

✅ **Labs 1-5 Complete!** Great progress! Continuing with Labs 6-9...

---

## Lab 6: Process Management

### Objectives

- View running processes
- Monitor system resources
- Control processes (start, stop, kill)
- Manage background jobs
- Understand process hierarchy

### Instructions

#### Step 6.1: View Processes with ps

```bash
cd ~/linux-lab
mkdir process-lab
cd process-lab

# View your processes
ps
```

**Expected Output:**

```
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:00 ps
```

```bash
# View all processes (full format)
ps aux | head -20
```

**Expected Output:**

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1   2312  1024 ?        Sl   10:00   0:01 /init
root        10  0.0  0.0   2312     4 ?        Ss   10:00   0:00 /init
username  1234  0.0  0.2  10980  5340 pts/0    Ss   10:15   0:00 -bash
root      5678  0.0  0.1   8892  3120 pts/0    R+   11:30   0:00 ps aux
...
```

**Understanding columns:**

```
USER    - Process owner
PID     - Process ID
%CPU    - CPU usage percentage
%MEM    - Memory usage percentage
VSZ     - Virtual memory size (KB)
RSS     - Physical memory size (KB - Resident Set Size)
TTY     - Terminal
STAT    - Process state (R=running, S=sleeping, Z=zombie)
START   - Start time
TIME    - CPU time consumed
COMMAND - Command that started process
```

```bash
# Show process tree
ps auxf

# Or use pstree
pstree

# Show processes for specific user
ps -u username
```

### Step 6.2: Real-Time Monitoring with top

```bash
# Launch top
top
```

**Inside top:**

```
top - 11:30:15 up 5 days,  3:25,  2 users,  load average: 0.50, 0.80, 1.20
Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.2 us,  2.1 sy,  0.0 ni, 92.4 id,  0.2 wa,  0.0 hi,  0.1 si,  0.0 st
MiB Mem :   7850.0 total,   3125.5 free,   2100.3 used,   2624.2 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   5412.7 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 username  20   0   10980   5340   3456 S   1.0   0.1   0:01.23 bash
 5678 username  20   0    8892   3120   2780 R   0.3   0.0   0:00.15 top
```

**top commands:**

```
q     - Quit
1     - Show per-CPU stats
M     - Sort by memory
P     - Sort by CPU
k     - Kill process (enter PID)
r     - Renice process (change priority)
h     - Help
```

```bash
# Alternative: htop (better UI, install first)
sudo apt install htop -y
htop
```

#### Step 6.3: Background and Foreground Jobs

**Start process in background:**

```bash
# Long-running task
sleep 100 &
```

**Expected Output:**

```
[1] 9876
```

- `[1]` = Job number
- `9876` = Process ID

**View background jobs:**

```bash
jobs
```

**Expected Output:**

```
[1]+  Running                 sleep 100 &
```

**Start in foreground then background:**

```bash
# Run sleep
sleep 200

# Press Ctrl + Z to suspend
# [Ctrl + Z pressed]
```

**Expected Output:**

```
[2]+  Stopped                 sleep 200
```

```bash
# Continue in background
bg

# Check jobs
jobs
```

**Expected Output:**

```
[1]-  Running                 sleep 100 &
[2]+  Running                 sleep 200 &
```

**Bring to foreground:**

```bash
# Bring job 1 to foreground
fg %1

# [Ctrl + C to kill]
```

#### Step 6.4: Kill Processes

**Create test process:**

```bash
# Infinite loop
sleep 1000 &
SLEEP_PID=$!
echo "Sleep PID: $SLEEP_PID"
```

**Kill by PID:**

```bash
# Graceful kill (SIGTERM)
kill $SLEEP_PID

# Check if still running
ps -p $SLEEP_PID
# Output: (nothing, process killed)
```

**Force kill:**

```bash
# Start another
sleep 2000 &
SLEEP_PID=$!

# Force kill (SIGKILL)
kill -9 $SLEEP_PID

# Or
kill -SIGKILL $SLEEP_PID
```

**Kill by name:**

```bash
# Start multiple sleeps
sleep 3000 &
sleep 3001 &
sleep 3002 &

# Kill all sleep processes
pkill sleep

# Or killall
killall sleep

# Check
ps aux | grep sleep
```

**Common signals:**

```
1  SIGHUP   - Hangup (reload config)
2  SIGINT   - Interrupt (Ctrl+C)
9  SIGKILL  - Force kill (cannot be caught)
15 SIGTERM  - Terminate gracefully (default)
18 SIGCONT  - Continue if stopped
19 SIGSTOP  - Stop process
```

#### Step 6.5: Process Priority (nice/renice)

**nice values: -20 (highest priority) to 19 (lowest)**

```bash
# Start process with low priority
nice -n 19 sleep 500 &

# Check priority
ps -l
```

**Expected Output:**

```
F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY        TIME CMD
0 S  1000  1234  1233  0  99  19 -  1234 -      pts/0  00:00:00 sleep
                            ↑ NI (nice value = 19)
```

```bash
# Change priority of running process (need sudo for negative values)
SLEEP_PID=$(pgrep sleep)
sudo renice -n -10 -p $SLEEP_PID

# Verify
ps -l -p $SLEEP_PID
```

#### Step 6.6: Monitor System Resources

**CPU usage:**

```bash
# Overall CPU info
lscpu
```

**Expected Output:**

```
Architecture:            x86_64
CPU(s):                  4
Model name:              Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
...
```

```bash
# CPU usage by process
top -bn1 | grep "Cpu(s)"
```

**Memory usage:**

```bash
free -h
```

**Expected Output:**

```
              total        used        free      shared  buff/cache   available
Mem:          7.7Gi       2.0Gi       3.5Gi        10Mi       2.2Gi       5.4Gi
Swap:         2.0Gi          0B       2.0Gi
```

```bash
# Detailed memory
cat /proc/meminfo | head
```

**Disk I/O:**

```bash
# Install iostat
sudo apt install sysstat -y

# View I/O stats
iostat -x 1 3  # Every 1 second, 3 times
```

#### Step 6.7: Practice Exercise

**Exercise:**

1. Start a `sleep 1000` process in background
2. Find its PID
3. Check its priority
4. Lower its priority to 15
5. Kill it gracefully
6. Verify it's killed

**Solution:**

```bash
# 1. Start process
sleep 1000 &
```

**Expected Output:**

```
[1] 12345
```

```bash
# 2. Find PID (or use $! for last background process)
SLEEP_PID=$!
echo "PID: $SLEEP_PID"

# Alternative methods:
# pgrep sleep
# pidof sleep
# ps aux | grep sleep

# 3. Check priority
ps -l -p $SLEEP_PID | tail -1
```

**Expected Output:**

```
0 S  1000 12345  1234  0  80   0 -  1234 -      pts/0  00:00:00 sleep
                            ↑ Priority=80, Nice=0
```

```bash
# 4. Lower priority
renice -n 15 -p $SLEEP_PID

# Verify
ps -l -p $SLEEP_PID | tail -1
```

**Expected Output:**

```
0 S  1000 12345  1234  0  95  15 -  1234 -      pts/0  00:00:00 sleep
                            ↑ Nice=15
```

```bash
# 5. Kill gracefully
kill $SLEEP_PID

# 6. Verify
ps -p $SLEEP_PID
```

**Expected Output:**

```
(nothing - process dead)
```

✅ **Lab 6 Complete!** You can manage processes like a pro!

---

## Lab 7: Package Management

### Objectives

- Understand APT package manager
- Install, update, remove packages
- Search for packages
- Manage repositories

### Instructions

#### Step 7.1: Update Package Lists

```bash
# Update package index
sudo apt update
```

**Expected Output:**

```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
Get:3 http://archive.ubuntu.com/ubuntu jammy-security InRelease [110 kB]
Fetched 25.3 MB in 8s (3,165 kB/s)
Reading package lists... Done
Building dependency tree... Done
All packages are up to date.
```

#### Step 7.2: Search for Packages

```bash
# Search for package
apt search nginx
```

**Expected Output:**

```
Sorting... Done
Full Text Search... Done
nginx/jammy-updates 1.18.0-6ubuntu14.4 all
  small, powerful, scalable web/proxy server

nginx-common/jammy-updates 1.18.0-6ubuntu14.4 all
  small, powerful, scalable web/proxy server - common files
...
```

```bash
# Show package information
apt show nginx
```

**Expected Output:**

```
Package: nginx
Version: 1.18.0-6ubuntu14.4
Priority: optional
Section: web
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Installed-Size: 44.0 kB
Depends: nginx-core (>= 1.18.0-6ubuntu14.4) | nginx-full ...
Homepage: https://nginx.org
Description: small, powerful, scalable web/proxy server
 Nginx is a web server with a strong focus on high concurrency,
 performance and low memory usage...
```

```bash
# Search installed packages
apt list --installed | grep git
```

**Expected Output:**

```
git/jammy-updates,now 1:2.34.1-1ubuntu1.10 amd64 [installed]
git-man/jammy-updates,now 1:2.34.1-1ubuntu1.10 all [installed,automatic]
```

#### Step 7.3: Install Packages

```bash
# Install single package
sudo apt install tree -y
```

**Expected Output:**

```
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  tree
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 43.0 kB of archives.
After this operation, 115 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu jammy/universe amd64 tree amd64 2.0.2-1 [43.0 kB]
Fetched 43.0 kB in 1s (43.0 kB/s)
Selecting previously unselected package tree.
Setting up tree (2.0.2-1) ...
```

```bash
# Verify installation
tree --version
```

**Expected Output:**

```
tree v2.0.2 (c) 1996 - 2022 by Steve Baker
```

```bash
# Test tree command
cd ~/linux-lab
tree -L 2
```

**Expected Output:**

```
.
├── find-lab
│   ├── backup
│   ├── large.txt
│   └── projects
├── permissions-lab
│   ├── secure-project
│   └── testfile.txt
└── text-lab
    └── app.log
```

**Install multiple packages:**

```bash
sudo apt install curl wget net-tools -y
```

#### Step 7.4: Upgrade Packages

```bash
# Upgrade all packages
sudo apt upgrade -y
```

**Expected Output:**

```
Reading package lists... Done
Building dependency tree... Done
Calculating upgrade... Done
The following packages will be upgraded:
  package1 package2 package3
3 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Need to get 15.2 MB of archives.
After this operation, 123 kB disk space will be freed.
...
```

```bash
# Full upgrade (may remove packages if needed)
sudo apt full-upgrade -y

# Distribution upgrade (major version)
sudo apt dist-upgrade -y
```

#### Step 7.5: Remove Packages

```bash
# Install test package
sudo apt install fortune-mod -y

# Test it
fortune
```

**Expected Output:**

```
A witty message appears here...
```

```bash
# Remove package (keep config files)
sudo apt remove fortune-mod -y
```

**Expected Output:**

```
The following packages will be REMOVED:
  fortune-mod
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
After this operation, 245 kB disk space will be freed.
Removing fortune-mod (1:1.99.1-7.1) ...
```

```bash
# Remove package + config files
sudo apt purge fortune-mod -y

# Remove unused dependencies
sudo apt autoremove -y
```

**Expected Output:**

```
The following packages will be REMOVED:
  fortunes-min
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
```

#### Step 7.6: Clean Package Cache

```bash
# Clean downloaded package files
sudo apt clean

# Remove old package versions
sudo apt autoclean

# Check disk usage
du -sh /var/cache/apt/archives/
```

#### Step 7.7: Add PPA Repository

**PPA (Personal Package Archive) - Ubuntu-specific**

```bash
# Add PPA (example: Git stable releases)
sudo add-apt-repository ppa:git-core/ppa -y

# Update package list
sudo apt update

# Install from PPA
sudo apt install git -y
```

**Remove PPA:**

```bash
sudo add-apt-repository --remove ppa:git-core/ppa -y
```

#### Step 7.8: Hold/Unhold Packages

**Prevent package from being upgraded:**

```bash
# Hold package
sudo apt-mark hold git

# Try to upgrade
sudo apt upgrade
# Git will NOT be upgraded

# Show held packages
apt-mark showhold
```

**Expected Output:**

```
git
```

```bash
# Unhold
sudo apt-mark unhold git
```

#### Step 7.9: Install .deb Files

```bash
# Download .deb file (example: VSCode if not installed via snap)
# wget https://az764295.vo.msecnd.net/stable/xxxxx/code_x.xx.x-xxxxx_amd64.deb

# Install .deb file
# sudo dpkg -i code_x.xx.x-xxxxx_amd64.deb

# Fix dependencies if any errors
# sudo apt install -f
```

#### Step 7.10: Practice Exercise

**Exercise:**

1. Search for package `htop`
2. Install it
3. Run it to verify
4. Check its version
5. Remove it

**Solution:**

```bash
# 1. Search
apt search htop
```

**Expected Output:**

```
htop/jammy 3.0.5-7build2 amd64
  interactive processes viewer
```

```bash
# 2. Install
sudo apt install htop -y
```

**Expected Output:**

```
...
Setting up htop (3.0.5-7build2) ...
```

```bash
# 3. Run
htop
# [Press q to quit]

# 4. Check version
htop --version
```

**Expected Output:**

```
htop 3.0.5
```

```bash
# 5. Remove
sudo apt remove htop -y
sudo apt autoremove -y
```

**Expected Output:**

```
The following packages will be REMOVED:
  htop
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
```

✅ **Lab 7 Complete!** You can manage packages efficiently!

---

## Lab 8: Basic Shell Scripting

### Objectives

- Write and execute shell scripts
- Use variables and user input
- Implement conditionals and loops
- Create practical automation scripts

### Instructions

#### Step 8.1: Your First Script

```bash
cd ~/linux-lab
mkdir scripts
cd scripts

# Create script
nano hello.sh
```

**Type in nano:**

```bash
#!/bin/bash
# My first shell script

echo "Hello, World!"
echo "Today is: $(date)"
echo "Current user: $USER"
echo "Current directory: $(pwd)"
```

**Save:** Ctrl + O, Enter, Ctrl + X

**Make executable:**

```bash
chmod +x hello.sh
```

**Run script:**

```bash
./hello.sh
```

**Expected Output:**

```
Hello, World!
Today is: Wed Dec 25 11:30:00 UTC 2024
Current user: username
Current directory: /home/username/linux-lab/scripts
```

#### Step 8.2: Variables

**Create script:**

```bash
nano variables.sh
```

**Type:**

```bash
#!/bin/bash

# Variables
NAME="DevOps"
VERSION=1.0
IS_ACTIVE=true

# Using variables
echo "Project: $NAME"
echo "Version: $VERSION"
echo "Active: $IS_ACTIVE"

# Command substitution
CURRENT_DATE=$(date +%Y-%m-%d)
echo "Date: $CURRENT_DATE"

FILES_COUNT=$(ls -1 | wc -l)
echo "Files in directory: $FILES_COUNT"

# Arrays
FRUITS=("Apple" "Banana" "Orange")
echo "First fruit: ${FRUITS[0]}"
echo "All fruits: ${FRUITS[@]}"
echo "Number of fruits: ${#FRUITS[@]}"
```

**Save, make executable, run:**

```bash
chmod +x variables.sh
./variables.sh
```

**Expected Output:**

```
Project: DevOps
Version: 1.0
Active: true
Date: 2024-12-25
Files in directory: 2
First fruit: Apple
All fruits: Apple Banana Orange
Number of fruits: 3
```

#### Step 8.3: User Input

**Create script:**

```bash
nano input.sh
```

**Type:**

```bash
#!/bin/bash

echo "What is your name?"
read NAME

echo "How old are you?"
read AGE

echo ""
echo "Hello, $NAME!"
echo "You are $AGE years old."

# Read with prompt (single line)
read -p "Enter your city: " CITY
echo "You live in $CITY"

# Read password (silent)
read -sp "Enter password: " PASSWORD
echo ""
echo "Password length: ${#PASSWORD}"
```

**Save, make executable, run:**

```bash
chmod +x input.sh
./input.sh
```

**Interactive session:**

```
What is your name?
Alice
How old are you?
25

Hello, Alice!
You are 25 years old.
Enter your city: New York
You live in New York
Enter password: [typed but not shown]
Password length: 8
```

#### Step 8.4: Conditionals (if/else)

**Create script:**

```bash
nano conditionals.sh
```

**Type:**

```bash
#!/bin/bash

read -p "Enter a number: " NUM

# Simple if
if [ $NUM -gt 10 ]; then
    echo "$NUM is greater than 10"
fi

# if-else
if [ $NUM -eq 100 ]; then
    echo "Exactly 100!"
else
    echo "Not 100"
fi

# if-elif-else
if [ $NUM -lt 0 ]; then
    echo "Negative number"
elif [ $NUM -eq 0 ]; then
    echo "Zero"
elif [ $NUM -lt 10 ]; then
    echo "Single digit (1-9)"
else
    echo "Two or more digits"
fi

# String comparison
read -p "Enter yes or no: " ANSWER
if [ "$ANSWER" = "yes" ]; then
    echo "You said yes!"
elif [ "$ANSWER" = "no" ]; then
    echo "You said no!"
else
    echo "Invalid answer"
fi

# File tests
if [ -f "hello.sh" ]; then
    echo "hello.sh exists and is a file"
fi

if [ -d "../scripts" ]; then
    echo "../scripts exists and is a directory"
fi

if [ -x "hello.sh" ]; then
    echo "hello.sh is executable"
fi
```

**Comparison operators:**

```
Numbers:
-eq  Equal
-ne  Not equal
-lt  Less than
-le  Less than or equal
-gt  Greater than
-ge  Greater than or equal

Strings:
=    Equal
!=   Not equal
-z   Empty string
-n   Not empty

Files:
-f   Is file
-d   Is directory
-e   Exists
-r   Readable
-w   Writable
-x   Executable
```

**Run:**

```bash
chmod +x conditionals.sh
./conditionals.sh
```

#### Step 8.5: Loops

**Create script:**

```bash
nano loops.sh
```

**Type:**

```bash
#!/bin/bash

echo "=== For loop with range ==="
for i in {1..5}; do
    echo "Number: $i"
done

echo ""
echo "=== For loop with list ==="
for COLOR in Red Green Blue; do
    echo "Color: $COLOR"
done

echo ""
echo "=== For loop with files ==="
for FILE in *.sh; do
    echo "Script: $FILE"
done

echo ""
echo "=== While loop ==="
COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done

echo ""
echo "=== Until loop ==="
NUM=1
until [ $NUM -gt 5 ]; do
    echo "Number: $NUM"
    NUM=$((NUM + 1))
done

echo ""
echo "=== C-style for loop ==="
for ((i=1; i<=5; i++)); do
    echo "i = $i"
done

echo ""
echo "=== Loop with break ==="
for i in {1..10}; do
    if [ $i -eq 6 ]; then
        echo "Breaking at $i"
        break
    fi
    echo $i
done

echo ""
echo "=== Loop with continue ==="
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        echo "Skipping 3"
        continue
    fi
    echo $i
done
```

**Run:**

```bash
chmod +x loops.sh
./loops.sh
```

**Expected Output:**

```
=== For loop with range ===
Number: 1
Number: 2
Number: 3
Number: 4
Number: 5

=== For loop with list ===
Color: Red
Color: Green
Color: Blue
...
```

#### Step 8.6: Functions

**Create script:**

```bash
nano functions.sh
```

**Type:**

```bash
#!/bin/bash

# Simple function
greet() {
    echo "Hello from function!"
}

# Function with parameters
greet_user() {
    local NAME=$1  # $1 = first parameter
    local AGE=$2   # $2 = second parameter
    echo "Hello, $NAME! You are $AGE years old."
}

# Function with return value
add() {
    local RESULT=$(( $1 + $2 ))
    echo $RESULT  # Return via echo
}

# Function returning status code
is_even() {
    if [ $(( $1 % 2 )) -eq 0 ]; then
        return 0  # Success (true)
    else
        return 1  # Failure (false)
    fi
}

# Usage
echo "=== Simple function ==="
greet

echo ""
echo "=== Function with parameters ==="
greet_user "Alice" 25
greet_user "Bob" 30

echo ""
echo "=== Function with return value ==="
SUM=$(add 10 20)
echo "10 + 20 = $SUM"

echo ""
echo "=== Function with status code ==="
if is_even 4; then
    echo "4 is even"
fi

if ! is_even 7; then
    echo "7 is not even"
fi
```

**Run:**

```bash
chmod +x functions.sh
./functions.sh
```

#### Step 8.7: Practical Script - Backup Tool

**Create script:**

```bash
nano backup.sh
```

**Type:**

```bash
#!/bin/bash

# Simple backup script

# Configuration
SOURCE_DIR="$HOME/linux-lab"
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.tar.gz"

# Create backup directory if not exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Check if source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Create backup
echo "Starting backup..."
echo "Source: $SOURCE_DIR"
echo "Destination: $BACKUP_DIR/$BACKUP_FILE"

tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$SOURCE_DIR" 2>/dev/null

if [ $? -eq 0 ]; then
    SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "Backup completed successfully!"
    echo "Backup file: $BACKUP_FILE"
    echo "Size: $SIZE"
else
    echo "Backup failed!"
    exit 1
fi

# Keep only last 5 backups
echo ""
echo "Cleaning old backups (keeping last 5)..."
cd "$BACKUP_DIR"
ls -t backup_*.tar.gz | tail -n +6 | xargs -r rm
echo "Done!"
```

**Run:**

```bash
chmod +x backup.sh
./backup.sh
```

**Expected Output:**

```
Creating backup directory: /home/username/backups
Starting backup...
Source: /home/username/linux-lab
Destination: /home/username/backups/backup_20241225_113000.tar.gz
Backup completed successfully!
Backup file: backup_20241225_113000.tar.gz
Size: 52M

Cleaning old backups (keeping last 5)...
Done!
```

**Verify:**

```bash
ls -lh ~/backups/
```

#### Step 8.8: Practical Script - System Monitor

**Create script:**

```bash
nano sysmonitor.sh
```

**Type:**

```bash
#!/bin/bash

# System monitoring script

echo "======================================"
echo "  System Monitoring Report"
echo "  Date: $(date)"
echo "======================================"
echo ""

# CPU info
echo "=== CPU Information ==="
echo "CPU Cores: $(nproc)"
echo "Load Average: $(uptime | awk '{print $(NF-2), $(NF-1), $NF}')"
echo ""

# Memory info
echo "=== Memory Usage ==="
free -h | grep -E "Mem:|Swap:"
echo ""

# Disk usage
echo "=== Disk Usage ==="
df -h / | tail -1
echo ""

# Top 5 CPU processes
echo "=== Top 5 CPU Processes ==="
ps aux --sort=-%cpu | head -6
echo ""

# Top 5 Memory processes
echo "=== Top 5 Memory Processes ==="
ps aux --sort=-%mem | head -6
echo ""

# Network info
echo "=== Network Interfaces ==="
ip -br addr | grep -v lo
echo ""

# System uptime
echo "=== System Uptime ==="
uptime
```

**Run:**

```bash
chmod +x sysmonitor.sh
./sysmonitor.sh
```

#### Step 8.9: Practice Exercise

**Exercise:** Create a script `user-manager.sh` that:

1. Displays a menu:
   - 1) List users
   - 1) Show current user
   - 1) Exit
2. Accepts user choice
3. Performs the action
4. Loops until user chooses exit

**Solution:**

```bash
nano user-manager.sh
```

**Type:**

```bash
#!/bin/bash

while true; do
    echo ""
    echo "======================================"
    echo "  User Management Menu"
    echo "======================================"
    echo "1) List all users"
    echo "2) Show current user"
    echo "3) Show logged in users"
    echo "4) Exit"
    echo ""
    read -p "Enter your choice [1-4]: " CHOICE
    
    case $CHOICE in
        1)
            echo ""
            echo "All users:"
            cut -d: -f1 /etc/passwd | column
            ;;
        2)
            echo ""
            echo "Current user: $USER"
            echo "UID: $UID"
            echo "Home: $HOME"
            ;;
        3)
            echo ""
            echo "Logged in users:"
            who
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1-4."
            ;;
    esac
    
    read -p "Press Enter to continue..."
done
```

**Run:**

```bash
chmod +x user-manager.sh
./user-manager.sh
```

**Test all menu options!**

✅ **Lab 8 Complete!** You can write shell scripts!

---

## Lab 9: System Information & Monitoring

### Objectives

- Gather system information
- Monitor disk usage
- Check network status
- View system logs
- Create monitoring scripts

### Instructions

#### Step 9.1: System Information

**Hostname:**

```bash
hostname
```

**Expected Output:**

```
DESKTOP-ABC123
```

```bash
# Full hostname
hostname -f

# IP address
hostname -I
```

**OS Information:**

```bash
# OS details
cat /etc/os-release
```

**Expected Output:**

```
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
ID=ubuntu
PRETTY_NAME="Ubuntu 22.04.3 LTS"
...
```

```bash
# Kernel version
uname -r
```

**Expected Output:**

```
5.15.90.1-microsoft-standard-WSL2
```

```bash
# All system info
uname -a
```

**Expected Output:**

```
Linux DESKTOP-ABC123 5.15.90.1-microsoft-standard-WSL2 #1 SMP Fri Jan 27 02:56:13 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

**Hardware info:**

```bash
# CPU info
lscpu | head -20
```

**Expected Output:**

```
Architecture:                    x86_64
CPU(s):                          4
Thread(s) per core:  2
Core(s) per socket:              2
Model name:                      Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
...
```

```bash
# Memory info
lsmem | grep "Total online memory"

# Detailed memory
cat /proc/meminfo | head -10
```

#### Step 9.2: Disk Usage

**Disk space:**

```bash
df -h
```

**Expected Output:**

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd        251G   35G  204G  15% /
tmpfs           3.9G     0  3.9G   0% /mnt/wsl
...
```

```bash
# Specific filesystem
df -h /

# Inodes usage
df -i
```

**Directory sizes:**

```bash
# Current directory
du -sh

# Subdirectories
du -sh *

#Top 10 largest in home
du -h ~ | sort -rh | head -10
```

**Expected Output:**

```
52M     /home/username/linux-lab
15M     /home/username/projects
...
```

**Find large files:**

```bash
# Files > 10MB in home
find ~ -type f -size +10M -exec ls -lh {} \; 2>/dev/null
```

#### Step 9.3: Network Status

**IP configuration:**

```bash
# All interfaces
ip addr

# Specific interface
ip addr show eth0

# Brief format
ip -br addr
```

**Expected Output:**

```
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             172.24.xxx.xxx/20
```

**Routing table:**

```bash
ip route
```

**Expected Output:**

```
default via 172.24.0.1 dev eth0
172.24.0.0/20 dev eth0 proto kernel scope link src 172.24.xxx.xxx
```

**Active connections:**

```bash
# All connections
ss -tuln
```

**Expected Output:**

```
Netid  State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port
tcp    LISTEN  0       128     0.0.0.0:22            0.0.0.0:*
tcp    LISTEN  0       128     [::]:22               [::]:*
```

**Network statistics:**

```bash
# Interface statistics
ip -s link

# Connection counts
ss -s
```

**Expected Output:**

```
Total: 180
TCP:   6 (estab 2, closed 0, orphaned 0, timewait 0)
...
```

#### Step 9.4: System Logs

**View system logs:**

```bash
# System log (if journald not available)
sudo tail -f /var/log/syslog

# Or with journalctl (systemd)
sudo journalctl -n 20
```

**Expected Output:**

```
Dec 25 11:30:00 hostname systemd[1]: Started Session 1 of user username.
Dec 25 11:30:15 hostname sshd[1234]: Accepted publickey for username from 192.168.1.1
...
```

**Authentication logs:**

```bash
# Login attempts
sudo tail /var/log/auth.log

# Failed logins
sudo grep "Failed" /var/log/auth.log
```

**Follow logs in real-time:**

```bash
# Follow system log
sudo journalctl -f

# Specific service
sudo journalctl -u ssh -f

# Last 100 lines
sudo journalctl -n 100

# Since time
sudo journalctl --since "1 hour ago"
sudo journalctl --since "2024-12-25 10:00:00"
```

#### Step 9.5: Process Monitoring

**System resource usage snapshot:**

```bash
# Create script
nano ~/linux-lab/scripts/snapshot.sh
```

**Type:**

```bash
#!/bin/bash

echo "System Resource Snapshot"
echo "Date: $(date)"
echo "========================"
echo ""

# CPU
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "CPU Load: " 100 - $1"%"}'
echo ""

# Memory
echo "Memory Usage:"
free -h | awk 'NR==2{printf "Used: %s / %s (%.2f%%)\n", $3,$2,$3*100/$2 }'
echo ""

# Disk
echo "Disk Usage:"
df -h / | awk 'NR==2{printf "Used: %s / %s (%s)\n", $3,$2,$5}'
echo ""

# Top 5 processes by CPU
echo "Top 5 CPU Processes:"
ps aux --sort=-%cpu | awk 'NR<=6{printf "%-10s %-6s %-6s %s\n", $1,$2,$3,$11}'
echo ""

# Top 5 processes by Memory
echo "Top 5 Memory Processes:"
ps aux --sort=-%mem | awk 'NR<=6{printf "%-10s %-6s %-6s %s\n", $1,$2,$4,$11}'
```

**Save, make executable, run:**

```bash
chmod +x ~/linux-lab/scripts/snapshot.sh
~/linux-lab/scripts/snapshot.sh
```

**Expected Output:**

```
System Resource Snapshot
Date: Wed Dec 25 11:30:00 UTC 2024
========================

CPU Usage:
CPU Load: 12.5%

Memory Usage:
Used: 2.1G / 7.7G (27.27%)

Disk Usage:
Used: 35G / 251G (15%)

Top 5 CPU Processes:
USER       PID    %CPU   COMMAND
root       1      0.1    /init
username   1234   0.0    -bash
...
```

#### Step 9.6: Automated Monitoring with Cron

**Create monitoring script that saves to file:**

```bash
nano ~/linux-lab/scripts/auto-monitor.sh
```

**Type:**

```bash
#!/bin/bash

LOG_DIR="$HOME/monitor-logs"
LOG_FILE="$LOG_DIR/monitor_$(date +%Y%m%d).log"

# Create log directory
mkdir -p "$LOG_DIR"

# Append to daily log
echo "=== $(date) ===" >> "$LOG_FILE"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')" >> "$LOG_FILE"
echo "MEM: $(free -h | awk 'NR==2{print $3 "/" $2}')" >> "$LOG_FILE"
echo "DISK: $(df -h / | awk 'NR==2{print $5}')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
```

**Make executable:**

```bash
chmod +x ~/linux-lab/scripts/auto-monitor.sh
```

**Add to crontab (run every 5 minutes):**

```bash
crontab -e
```

**Add this line:**

```
*/5 * * * * /home/username/linux-lab/scripts/auto-monitor.sh
```

**Verify crontab:**

```bash
crontab -l
```

**Expected Output:**

```
*/5 * * * * /home/username/linux-lab/scripts/auto-monitor.sh
```

**Wait 5 minutes, check logs:**

```bash
ls ~/monitor-logs/
cat ~/monitor-logs/monitor_*.log
```

#### Step 9.7: Practice Exercise

**Exercise:** Create `health-check.sh` that:

1. Checks if CPU usage > 80%
2. Checks if Memory usage > 90%
3. Checks if Disk usage > 90%
4. Sends alert (echo to console) if any threshold exceeded
5. Logs result to file

**Solution:**

```bash
nano ~/linux-lab/scripts/health-check.sh
```

**Type:**

```bash
#!/bin/bash

# Thresholds
CPU_THRESHOLD=80
MEM_THRESHOLD=90
DISK_THRESHOLD=90

# Log file
LOG_FILE="$HOME/health-check.log"

# Get metrics
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}' | cut -d. -f1)
MEM_USAGE=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')

# Log timestamp
echo "=== $(date) ===" >> "$LOG_FILE"

# Initialize alert flag
ALERT=false

# Check thresholds
if [ $CPU_USAGE -gt $CPU_THRESHOLD ]; then
    echo "⚠️  ALERT: CPU usage is ${CPU_USAGE}% (threshold: ${CPU_THRESHOLD}%)" | tee -a "$LOG_FILE"
    ALERT=true
fi

if [ $MEM_USAGE -gt $MEM_THRESHOLD ]; then
    echo "⚠️  ALERT: Memory usage is ${MEM_USAGE}% (threshold: ${MEM_THRESHOLD}%)" | tee -a "$LOG_FILE"
    ALERT=true
fi

if [ $DISK_USAGE -gt $DISK_THRESHOLD ]; then
    echo "⚠️  ALERT: Disk usage is ${DISK_USAGE}% (threshold: ${DISK_THRESHOLD}%)" | tee -a "$LOG_FILE"
    ALERT=true
fi

if [ "$ALERT" = false ]; then
    echo "✅ All systems healthy" | tee -a "$LOG_FILE"
    echo "   CPU: ${CPU_USAGE}%, Memory: ${MEM_USAGE}%, Disk: ${DISK_USAGE}%" | tee -a "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
```

**Save, make executable, run:**

```bash
chmod +x ~/linux-lab/scripts/health-check.sh
~/linux-lab/scripts/health-check.sh
```

**Expected Output:**

```
✅ All systems healthy
   CPU: 5%, Memory: 27%, Disk: 15%
```

**View log:**

```bash
cat ~/health-check.log
```

✅ **Lab 9 Complete!** You can monitor systems!

---

## 🎉 ALL LABS COMPLETE

### Module 01 Final Checklist

Congratulations! You've completed all 9 labs covering:

- [x] Lab 1: File System Navigation
- [x] Lab 2: File & Directory Operations  
- [x] Lab 3: Text File Manipulation
- [x] Lab 4: Searching & Finding Files
- [x] Lab 5: File Permissions
- [x] Lab 6: Process Management
- [x] Lab 7: Package Management
- [x] Lab 8: Basic Shell Scripting
- [x] Lab 9: System Information & Monitoring

### Skills Acquired

You now know how to:
✅ Navigate Linux filesystem confidently
✅ Create, copy, move, delete files and directories
✅ Manipulate text files with grep, sed, awk
✅ Find files with various criteria
✅ Manage file permissions and ownership
✅ Monitor and control processes
✅ Install and manage packages
✅ Write shell scripts for automation
✅ Monitor system resources and health

### Next Steps

**Ready for Module 02: GIT & GITHUB!**

Keep practicing Linux commands daily. The more you use them, the more natural they become!

---

> **"With great power comes great responsibility. Use `rm -rf` wisely!"** 🐧💪
