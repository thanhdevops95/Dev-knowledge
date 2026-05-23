# CHEATSHEET - Module 01: LINUX BASICS

---

## File System Navigation

```bash
pwd                    # Print working directory
cd /path              # Change directory (absolute)
cd ../folder          # Change directory (relative)
cd ~                  # Go to home
cd -                  # Go to previous directory
ls                    # List files
ls -la                # List all with details
ls -lh                # Human-readable sizes
tree                  # Show directory tree
```

## File Operations

```bash
touch file.txt        # Create empty file
mkdir dir             # Create directory
mkdir -p a/b/c        # Create nested directories
cp file1 file2        # Copy file
cp -r dir1 dir2       # Copy directory recursively
mv file1 file2        # Move/rename file
rm file               # Delete file
rm -rf dir            # Delete directory recursively (DANGEROUS!)
cat file              # Display file content
head -n 10 file       # First 10 lines
tail -n 10 file       # Last 10 lines
tail -f file          # Follow file (live updates)
less file             # Page through file
```

## Text Processing

```bash
grep "pattern" file           # Search in file
grep -r "pattern" dir         # Recursive search
grep -i "pattern" file        # Case-insensitive
grep -v "pattern" file        # Invert match
grep -c "pattern" file        # Count matches

sed 's/old/new/g' file        # Replace text
awk '{print $1}' file         # Print first column
cut -d',' -f1 file           # Cut CSV column
sort file                     # Sort lines
uniq file                     # Remove duplicates
wc -l file                    # Count lines
tr 'a-z' 'A-Z' < file        # Transform characters
```

## Permissions

```bash
chmod 755 file        # rwxr-xr-x
chmod 644 file        # rw-r--r--
chmod 600 file        # rw------- (private)
chmod +x file         # Add execute
chmod u+x file        # User execute only
chmod -R 755 dir      # Recursive

chown user file       # Change owner
chown user:group file # Change owner and group
chgrp group file      # Change group only

# Permission values:
# r=4, w=2, x=1
# 7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---
```

## Process Management

```bash
ps                    # Your processes
ps aux                # All processes
ps aux | grep name    # Find process
top                   # Live process monitor
htop                  # Better process monitor
kill PID              # Kill process
kill -9 PID           # Force kill
killall name          # Kill by name
pkill name            # Kill by pattern
jobs                  # Background jobs
bg                    # Resume in background
fg                    # Bring to foreground
nohup cmd &           # Run detached
```

## Package Management (apt)

```bash
sudo apt update                # Update package list
sudo apt upgrade              # Upgrade packages
sudo apt install package      # Install package
sudo apt remove package       # Remove package
sudo apt purge package        # Remove with config
sudo apt autoremove           # Remove unused
apt search keyword            # Search packages
apt show package              # Package info
```

## File Searching

```bash
find . -name "*.txt"          # Find by name
find . -type f                # Find files only
find . -type d                # Find directories only
find . -size +10M             # Files > 10MB
find . -mtime -7              # Modified last 7 days
find . -name "*.log" -delete  # Find and delete

locate filename               # Quick search (updatedb first)
which command                 # Find command location
whereis command               # Find binary/source/manual
```

## Redirection & Pipes

```bash
cmd > file            # Redirect output (overwrite)
cmd >> file           # Redirect output (append)
cmd 2> file           # Redirect errors
cmd &> file           # Redirect all
cmd < file            # Input from file
cmd1 | cmd2           # Pipe output
cmd > /dev/null       # Discard output
```

## Archives

```bash
tar -czf archive.tar.gz dir/  # Create compressed archive
tar -xzf archive.tar.gz       # Extract
tar -tzf archive.tar.gz       # List contents
zip -r archive.zip dir/       # Create zip
unzip archive.zip             # Extract zip
```

## Networking

```bash
ip addr               # Show IP addresses
ip route              # Show routes
ping host             # Test connectivity
curl url              # HTTP request
wget url              # Download file
netstat -tuln         # Show listening ports
ss -tuln              # Socket statistics
```

## System Info

```bash
uname -a              # System info
hostname              # Hostname
whoami                # Current user
id                    # User ID and groups
uptime                # System uptime
free -h               # Memory usage
df -h                 # Disk usage
du -sh dir            # Directory size
lscpu                 # CPU info
```

## Shortcuts

```bash
Ctrl + C              # Kill process
Ctrl + Z              # Suspend process
Ctrl + D              # Exit shell
Ctrl + L              # Clear screen
Ctrl + R              # Search history
Ctrl + A              # Start of line
Ctrl + E              # End of line
Ctrl + U              # Delete line
Tab                   # Auto-complete
!!                    # Last command
sudo !!               # Last command with sudo
```

## Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias update='sudo apt update && sudo apt upgrade -y'
alias ports='netstat -tulanp'
alias meminfo='free -h'
alias diskinfo='df -h'
```

---

> **Print this page and keep it near your desk!** 🖨️
