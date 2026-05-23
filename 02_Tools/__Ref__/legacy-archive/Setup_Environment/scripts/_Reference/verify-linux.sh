#!/bin/bash

# DevOps Training - Environment Verification Script
# For: Linux / WSL (Ubuntu/Debian)
# Version: 1.0.0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emoji
CHECK="✅"
CROSS="❌"
WARN="⚠️"

# Print header
print_header() {
    echo -e "${BLUE}====================================${NC}"
    echo -e "${BLUE}DevOps Training - Environment Check${NC}"
    echo -e "${BLUE}====================================${NC}"
    echo ""
}

# Print section
print_section() {
    echo -e "${YELLOW}Checking $1...${NC}"
}

# Check pass
check_pass() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

# Check fail
check_fail() {
    echo -e "${RED}${CROSS} $1${NC}"
}

# Check warn
check_warn() {
    echo -e "${YELLOW}${WARN} $1${NC}"
}

# Main verification
main() {
    print_header
    
    # Track overall status
    all_passed=true
    
    # 1. Check OS
    print_section "operating system"
    if [ -f /etc/os-release ]; then
        os_name=$(grep "^PRETTY_NAME=" /etc/os-release | cut -d'"' -f2)
        
        # Check if WSL
        if grep -qi microsoft /proc/version; then
            check_pass "OS: $os_name (WSL2)"
        else
            check_pass "OS: $os_name (Native Linux)"
        fi
    else
        check_fail "OS: Cannot detect OS version"
        all_passed=false
    fi
    echo ""
    
    # 2. Check shell
    print_section "shell"
    if [ -n "$BASH_VERSION" ]; then
        check_pass "Shell: bash $BASH_VERSION"
    elif [ -n "$ZSH_VERSION" ]; then
        check_pass "Shell: zsh $ZSH_VERSION"
    else
        check_warn "Shell: Unknown shell ($SHELL)"
    fi
    echo ""
    
    # 3. Check VS Code
    print_section "VS Code"
    if command -v code &> /dev/null; then
        code_version=$(code --version | head -n 1)
        check_pass "VS Code: version $code_version"
    else
        check_fail "VS Code: Command 'code' not found"
        check_fail "Install VS Code and ensure it's in PATH"
        all_passed=false
    fi
    echo ""
    
    # 4. Check internet connectivity
    print_section "internet connection"
    if ping -c 1 google.com &> /dev/null; then
        check_pass "Internet: Connected (ping google.com OK)"
    else
        check_fail "Internet: Cannot reach google.com"
        check_fail "Check your network connection"
        all_passed=false
    fi
    echo ""
    
    # 5. Check disk space
    print_section "disk space"
    # Get home directory disk usage
    disk_free=$(df -h ~ | awk 'NR==2 {print $4}')
    disk_free_gb=$(df -B GB ~ | awk 'NR==2 {print $4}' | sed 's/GB//')
    
    if [ "$disk_free_gb" -gt 20 ]; then
        check_pass "Disk: $disk_free free (sufficient)"
    elif [ "$disk_free_gb" -gt 10 ]; then
        check_warn "Disk: $disk_free free (low - recommend 20GB+)"
    else
        check_fail "Disk: $disk_free free (insufficient - need 20GB+)"
        all_passed=false
    fi
    echo ""
    
    # 6. Check course materials
    print_section "course materials"
    
    # Try common locations
    material_paths=(
        "$HOME/DevOps/DevOpsTraining"
        "/mnt/c/DevOps/DevOpsTraining"
        "$HOME/Desktop/DevOpsTraining"
        "$HOME/Downloads/DevOpsTraining"
    )
    
    material_found=false
    material_path=""
    
    for path in "${material_paths[@]}"; do
        if [ -d "$path/FOUNDATION" ]; then
            material_found=true
            material_path="$path"
            break
        fi
    done
    
    if [ "$material_found" = true ]; then
        check_pass "Materials: Found at $material_path"
        
        # Check structure
        if [ -d "$material_path/FOUNDATION" ] && [ -d "$material_path/ADVANCED" ]; then
            check_pass "Structure: FOUNDATION/ and ADVANCED/ folders present"
        else
            check_warn "Structure: Missing some folders (may be incomplete download)"
        fi
    else
        check_fail "Materials: Not found in common locations"
        check_fail "Download from: https://github.com/thanhlehoang0107/DevOpsTraining"
        all_passed=false
    fi
    echo ""
    
    # 7. Print summary
    echo -e "${BLUE}====================================${NC}"
    if [ "$all_passed" = true ]; then
        echo -e "${GREEN}ENVIRONMENT STATUS: ${CHECK} READY${NC}"
        echo ""
        echo -e "${GREEN}🎉 Congratulations! You're ready for Module 01!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Read Module 01 README"
        echo "2. Complete Module 01 labs"
        echo "3. Join Discord: https://discord.gg/devops-training"
    else
        echo -e "${RED}ENVIRONMENT STATUS: ${CROSS} NOT READY${NC}"
        echo ""
        echo -e "${YELLOW}Please fix the issues marked with ${CROSS} above${NC}"
        echo ""
        echo "Need help?"
        echo "- Check FAQ: FOUNDATION/00_SETUP/FAQ.md"
        echo "- Troubleshooting: FOUNDATION/00_SETUP/README.md#troubleshooting"
        echo "- Ask in Discord: https://discord.gg/devops-training"
    fi
    echo -e "${BLUE}====================================${NC}"
    echo ""
    
    # Optional checks (not required but recommended)
    echo -e "${YELLOW}Optional checks (for future modules):${NC}"
    echo ""
    
    # Check Git (will install in Module 02)
    if command -v git &> /dev/null; then
        git_version=$(git --version | awk '{print $3}')
        check_pass "Git: version $git_version (installed)"
    else
        echo -e "${BLUE}ℹ️ Git: Not installed yet (will install in Module 02)${NC}"
    fi
    
    # Check Docker (will install in Module 05)
    if command -v docker &> /dev/null; then
        docker_version=$(docker --version | awk '{print $3}' | sed 's/,//')
        check_pass "Docker: version $docker_version (installed)"
    else
        echo -e "${BLUE}ℹ️ Docker: Not installed yet (will install in Module 05)${NC}"
    fi
    
    echo ""
    echo "Happy learning! 🚀"
    echo ""
}

# Run main function
main
