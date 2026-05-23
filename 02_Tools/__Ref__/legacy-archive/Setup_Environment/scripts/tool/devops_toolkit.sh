#!/bin/bash

# ===================================================================================
# DevOps Toolkit v2.0
#
# A unified script to manage DevOps tools and applications.
#
# Features:
# - External tool list via `tools.conf`
# - OS Detection (macOS & Debian-based Linux)
# - Platform-specific installation (Homebrew for macOS, APT for Linux)
# ===================================================================================


# ===================================================================================
# I. CONFIGURATION & CORE LOGIC
# ===================================================================================

# --- UI & Utility Functions ---
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

print_header() { echo -e "\n${BLUE}=======================================================${NC}"; echo -e "${BLUE}  $1${NC}"; echo -e "${BLUE}=======================================================${NC}\n"; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}i $1${NC}"; }

# --- Dynamic Tool Configuration ---
TOOLS_DISPLAY_NAMES=()
TOOLS_TYPES=()
TOOLS_PACKAGE_NAMES=()
TOOL_IS_INSTALLED=()

# --- OS Detection ---
OS_TYPE=""
PACKAGE_MANAGER=""
UPDATE_CMD=""
INSTALL_CMD=""
UNINSTALL_CMD=""

detect_os() {
    case "$(uname -s)" in
        Darwin)
            OS_TYPE="macos"
            if ! command -v brew &> /dev/null; then
                print_error "Homebrew is required on macOS but not found. Please install it first."
                exit 1
            fi
            PACKAGE_MANAGER="brew"
            INSTALL_CMD="brew install"
            UNINSTALL_CMD="brew uninstall"
            ;; 
        Linux)
            if [ -f /etc/debian_version ]; then
                OS_TYPE="linux_debian"
                if ! command -v apt-get &> /dev/null; then
                    print_error "apt-get is required on Debian/Ubuntu but not found."
                    exit 1
                fi
                PACKAGE_MANAGER="apt"
                UPDATE_CMD="sudo apt-get update"
                INSTALL_CMD="sudo apt-get install -y"
                UNINSTALL_CMD="sudo apt-get remove -y"
            else
                print_error "Unsupported Linux distribution. Only Debian-based distros are supported for now."
                exit 1
            fi
            ;; 
        *)
            print_error "Unsupported operating system: $(uname -s)"
            exit 1
            ;; 
    esac
    print_info "Detected OS: $OS_TYPE"
}

# --- Tool Loading ---
load_tools_from_config() {
    local config_file
    config_file="$(dirname "$0")/tools.conf"
    if [ ! -f "$config_file" ]; then
        print_error "Configuration file not found: $config_file"
        exit 1
    fi

    # Reset arrays
    TOOLS_DISPLAY_NAMES=()
    TOOLS_TYPES=()
    TOOLS_PACKAGE_NAMES=()

    while IFS=';' read -r display_name type brew_name apt_name; do
        # Ignore comments and empty lines
        [[ "$display_name" =~ ^# ]] && continue
        [ -z "$display_name" ] && continue
        
        local package_name=""
        if [ "$OS_TYPE" = "macos" ]; then
            package_name="$brew_name"
        elif [ "$OS_TYPE" = "linux_debian" ]; then
            package_name="$apt_name"
        fi

        # Skip tools that don't have a package for the current OS
        [ -z "$package_name" ] && continue

        # On Linux, casks are not a concept, treat as cli
        local effective_type="$type"
        if [ "$OS_TYPE" = "linux_debian" ] && [ "$type" = "cask" ]; then
            effective_type="cli"
        fi

        TOOLS_DISPLAY_NAMES+=("$display_name")
        TOOLS_TYPES+=("$effective_type")
        TOOLS_PACKAGE_NAMES+=("$package_name")
    done < "$config_file"
}

# --- Core Check/Install/Uninstall Logic ---

check_all_tools_status() {
    print_info "Checking tool and application status..."
    TOOL_IS_INSTALLED=()
    for i in "${!TOOLS_DISPLAY_NAMES[@]}"; do
        local type="${TOOLS_TYPES[i]}"
        local name="${TOOLS_PACKAGE_NAMES[i]}"
        local is_installed=0

        if [ "$OS_TYPE" = "macos" ] && [ "$type" = "cask" ]; then
            # Hybrid check for macOS casks
            if brew list --cask | grep -q "^$name$"; then
                is_installed=1
            else
                # Fallback for manually installed apps
                local app_name_map=("visual-studio-code:Visual Studio Code.app" "docker:Docker.app" "iterm2:iTerm.app" "rectangle:Rectangle.app")
                for mapping in "${app_name_map[@]}"; do
                    if [[ "${mapping%%:*}" == "$name" ]]; then
                        local app_name="${mapping#*:}"
                        if [ -d "/Applications/$app_name" ]; then
                            is_installed=1
                        fi
                        break
                    fi
                done
            fi
        elif [ "$PACKAGE_MANAGER" = "apt" ]; then
             # Check for apt packages more reliably
            if dpkg-query -W -f='${Status}' "$name" 2>/dev/null | grep -q "ok installed"; then
                 is_installed=1
            fi
        else
            # Generic check for CLI tools
            if command -v "$name" &> /dev/null; then
                is_installed=1
            fi
        fi
        TOOL_IS_INSTALLED[i]=$is_installed
    done
}


do_install() {
    local index=$1
    local name="${TOOLS_PACKAGE_NAMES[index]}"
    local type="${TOOLS_TYPES[i]}"

    if [ "${TOOL_IS_INSTALLED[index]}" -eq 1 ]; then
        print_success "$name is already installed."
        return 0
    fi

    print_info "Installing $name..."
    local cmd
    if [ "$OS_TYPE" = "macos" ] && [ "$type" = "cask" ]; then
        cmd="$INSTALL_CMD --cask $name"
    else
        cmd="$INSTALL_CMD $name"
    fi
    
    # Run update before first install on Linux
    if [ "$OS_TYPE" = "linux_debian" ] && ! $did_update; then
        print_info "Running apt-get update first..."
        eval "$UPDATE_CMD"
        did_update=true
    fi

    print_info "Running command: $cmd"
    eval "$cmd"

    if [ $? -eq 0 ]; then
        print_success "Successfully installed $name."
        TOOL_IS_INSTALLED[index]=1
    else
        print_error "Failed to install $name."
    fi
}

do_uninstall() {
    local index=$1
    local name="${TOOLS_PACKAGE_NAMES[index]}"
    local type="${TOOLS_TYPES[i]}"

    if [ "${TOOL_IS_INSTALLED[index]}" -eq 0 ]; then
        print_success "$name is not installed."
        return 0
    fi

    print_info "Uninstalling $name..."
    local cmd
    if [ "$OS_TYPE" = "macos" ] && [ "$type" = "cask" ]; then
        cmd="$UNINSTALL_CMD --cask $name"
    else
        cmd="$UNINSTALL_CMD $name"
    fi

    print_info "Running command: $cmd"
    eval "$cmd"

    if [ $? -eq 0 ]; then
        print_success "Successfully uninstalled $name."
        TOOL_IS_INSTALLED[index]=0
    else
        print_error "Failed to uninstall $name."
    fi
}


# ===================================================================================
# II. MENU & UI FUNCTIONS
# ===================================================================================

show_management_menu() {
    local action="$1"
    local did_update=false
    
    while true; do
        clear
        if [ "$action" = "install" ]; then
            print_header "Tool Installer"
        else
            print_header "Tool Uninstaller"
        fi
        
        check_all_tools_status
        echo "Select a tool to $action. Current status is shown."
        
        for i in "${!TOOLS_DISPLAY_NAMES[@]}"; do
            local display_name="${TOOLS_DISPLAY_NAMES[i]}"
            local status_str
            if [ "${TOOL_IS_INSTALLED[i]}" -eq 1 ]; then
                status_str="${GREEN}[installed]${NC}"
            else
                status_str="${RED}[missing]${NC}"
            fi
            printf "%2d. %-25s %b\n" "$((i+1))" "$display_name" "$status_str"
        done

        local tool_count=${#TOOLS_DISPLAY_NAMES[@]}
        echo "-------------------------------------------------------"
        echo "$((tool_count + 1))). $action ALL tools"
        echo "$((tool_count + 2))). Back to Main Menu"
        echo
        read -p "Enter your choice: " choice

        if [[ "$choice" -eq $((tool_count + 2)) ]]; then
            break
        elif [[ "$choice" -eq $((tool_count + 1)) ]]; then
            print_info "Processing all tools for '$action'..."
            for i in "${!TOOLS_DISPLAY_NAMES[@]}"; do
                if [ "$action" = "install" ]; then do_install "$i";
                else do_uninstall "$i"; fi
            done
            print_success "Finished processing all tools."
        elif [[ "$choice" -gt 0 && "$choice" -le "$tool_count" ]]; then
            local index_to_process=$((choice - 1))
            if [ "$action" = "install" ]; then do_install "$index_to_process";
            else do_uninstall "$index_to_process"; fi
        else
            print_error "Invalid choice."
        fi
        echo; read -n 1 -s -r -p "Press any key to continue..."
    done
}


run_generate_ssh_key() {
    # This function is unchanged for now
    print_header "SSH Key Generation Helper"
    read -p "Enter your GitHub/GitLab email address: " email
    if [ -z "$email" ]; then print_error "Email address cannot be empty."; return 1; fi
    
    local key_path="$HOME/.ssh/id_ed25519_devops_toolkit"
    ssh-keygen -t ed25519 -C "$email" -f "$key_path" -N ""
    
    print_success "SSH key generated. Public key:"
    cat "${key_path}.pub"
    if command -v pbcopy &> /dev/null; then
        cat "${key_path}.pub" | pbcopy
        print_success "Public key has been copied to your clipboard."
    fi
}


# ===================================================================================
# III. MAIN MENU
# ===================================================================================
main_menu() {
    # Run setup tasks
    detect_os
    load_tools_from_config

    while true; do
        clear
        print_header "DevOps Toolkit v2.0"
        
        local choice
        if command -v gum &> /dev/null; then
            choice=$(gum choose "Install Tools" "Uninstall Tools" "Generate a New SSH Key" "Exit")
        else
            echo "1. Install Tools"
            echo "2. Uninstall Tools"
            echo "3. Generate a New SSH Key"
            echo "4. Exit"
            echo
            read -p "Enter your choice [1-4]: " choice
            # Map number to string for case statement
            case "$choice" in
                1) choice="Install Tools" ;;
                2) choice="Uninstall Tools" ;;
                3) choice="Generate a New SSH Key" ;;
                4) choice="Exit" ;;
            esac
        fi

        case "$choice" in
            "Install Tools") show_management_menu "install" ;;
            "Uninstall Tools") show_management_menu "uninstall" ;;
            "Generate a New SSH Key") clear; run_generate_ssh_key ;; 
            "Exit") echo "Goodbye!"; exit 0 ;; 
            *) print_error "Invalid choice." ;; 
        esac
        echo
        read -n 1 -s -r -p "Press any key to return to the main menu..."
    done
}

# --- Script Entry Point ---
main_menu