# QUIZ - Module 00: SETUP

> **Purpose:** Assess environment setup knowledge
> **Questions:** 20 | **Passing Score:** 80% (16/20)
> **Time Limit:** 15 minutes

---

## Multiple Choice Questions

### Q1. What does WSL stand for?

A) Windows Server Linux  
B) Windows Subsystem for Linux ✓  
C) Web Service Layer  
D) Windows System Library

**Answer:** B

---

### Q2. Which WSL version should be used for DevOps work?

A) WSL 1  
B) WSL 2 ✓  
C) Both are equally good  
D) Neither, use VM instead

**Answer:** B - WSL 2 provides better performance and full system call compatibility

---

### Q3. Which command checks Git configuration?

A) git show config  
B) git list  
C) git config --list ✓  
D) git settings

**Answer:** C

---

### Q4. What is the recommended SSH key type for GitHub?

A) RSA 2048-bit  
B) DSA  
C) ED25519 ✓  
D) ECDSA

**Answer:** C - ED25519 is modern, secure, and efficient

---

### Q5. Which file stores Zsh configuration?

A) ~/.bashrc  
B) ~/.zshrc ✓  
C) /etc/zsh/config  
D) ~/.zsh_config

**Answer:** B

---

### Q6. To set Git default branch to 'main', use

A) git config init.branch main  
B) git config --global init.defaultBranch main ✓  
C) git branch --default main  
D) git set-default main

**Answer:** B

---

### Q7. Which extension is essential for using VS Code with WSL?

A) WSL Helper  
B) Remote - WSL ✓  
C) Linux Connector  
D) Ubuntu Plugin

**Answer:** B

---

### Q8. What does `eval "$(ssh-agent -s)"` do?

A) Creates SSH key  
B) Starts SSH agent ✓  
C) Deletes SSH agent  
D) Tests SSH connection

**Answer:** B

---

### Q9. How to test SSH connection to GitHub?

A) ssh github.com  
B) ssh -t <git@github.com>  
C) ssh -T <git@github.com> ✓  
D) ping github.com

**Answer:** C

---

### Q10. Which file should contain custom bash aliases?

A) ~/.aliases  
B) ~/.bashrc ✓  
C) /etc/aliases  
D) ~/.profile

**Answer:** B - Can also use ~/.bash_aliases if sourced in ~/.bashrc

---

## True/False Questions

### Q11. WSL 2 uses a lightweight VM

**Answer:** TRUE ✓

---

### Q12. You need to restart WSL after installing it

**Answer:** TRUE ✓

---

### Q13. SSH keys must have passphrase

**Answer:** FALSE - Passphrase is optional but recommended

---

### Q14. Git requires email and name to be configured

**Answer:** TRUE ✓

---

### Q15. VS Code can only connect to one WSL distribution

**Answer:** FALSE - Can connect to multiple distros

---

## Fill in the Blank

### Q16. The command to check WSL version is: `wsl ________`

**Answer:** `--version` or `-v`

---

### Q17. SSH keys are stored in `~/.______` directory

**Answer:** `ssh`

---

### Q18. The default Git editor can be set with: `git config --global core.______`

**Answer:** `editor`

---

## Practical Questions

### Q19. What command would you use to

1. Generate ED25519 SSH key
2. Add it to SSH agent  
3. Display public key

**Answer:**

```bash
1. ssh-keygen -t ed25519 -C "email@example.com"
2. ssh-add ~/.ssh/id_ed25519
3. cat ~/.ssh/id_ed25519.pub
```

---

### Q20. Write commands to configure Git with

- Name: "John Doe"
- Email: "<john@example.com>"
- Default branch: main

**Answer:**

```bash
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
git config --global init.defaultBranch main
```

---

## Scoring

- **18-20:** Excellent! Ready for next module
- **16-17:** Pass - Review weak areas
- **14-15:** Study more, retake quiz
- **<14:** Please review module content

---

## Answer Key

1. B  |  6. B  | 11. TRUE  | 16. --version
2. B  |  7. B  | 12. TRUE  | 17. ssh
3. C  |  8. B  | 13. FALSE | 18. editor
4. C  |  9. C  | 14. TRUE  | 19-20. See above
5. B  | 10. B  | 15. FALSE |

---

> **Need to score 80%+ to proceed to Module 01!** 🎯
