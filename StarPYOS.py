import os
import time
import sys
from colorama import Fore, Back, Style, init
import random
import shutil
import math  # Added math import at the top
init(autoreset=True)

class SimpleShell:
    def _clear_screen(self):
        """Clear terminal - use cls on Windows, clear on Unix."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def __init__(self):
        self.current_dir = "/home/user"
        self.filesystem, self.files = self._get_initial_state()
        self.username = "user"
        self.hostname = "Star-PY-OS"
        self.is_root = False
        self.installed_packages = ["python", "nano", "vim", "htop", "btop", "cowsay", "fastfetch", "lynx", "cmatrix", "cava"]
        self.terminal_width = 160
        self.terminal_height = 45

    def _get_initial_state(self):
        """Return fresh (filesystem, files) for guest OS reset/format/reboot. Does not touch host."""
        readme_content = """╔═══════════════════════════════════════════════════════════════════════════════════╗
║                          WELCOME TO STAR PY OS                                    ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
Welcome to Star PY OS, it's a simulated GNU/Linux terminal box
based off Python. Pretty cool right?
Type 'help' to view all commands!
📦 View on GitHub: https://github.com/Brdyyy8-0298/Star-PY-OS
💻 Written in: Python
🔧 Customizable: You can modify all the code or ask an AI to view
all features via GitHub!
💬 Feedback: If you give feedback, I might not respond cuz you can
update it yourself! Feel free to fork and customize.
⚠️  Note: Memory is NOT persistent - changes are lost on exit.
Features:
• Full simulated Linux filesystem
• Package manager (pkg)
• File editors (nano, vim)
• System monitors (htop, btop)
• Fun stuff (nyancat, cowsay, hollywood, cmatrix, cava)
• Web browser (lynx - fully functional TUI browser)
• Root access via sudo
• Sound simulation (beep, cava)
• Prank tools (virus, trojan, ransomware generators)
• Enhanced Midnight Commander with full features
• And much more!
Enjoy exploring Star PY OS! ⭐
"""
        filesystem = {
            "/": ["home", "usr", "etc", "var", "tmp", "root"],
            "/home": ["user"],
            "/home/user": ["Documents", "Downloads", "Pictures", "README.txt"],
            "/home/user/Documents": [],
            "/home/user/Downloads": [],
            "/home/user/Pictures": [],
            "/usr": ["bin", "lib"],
            "/usr/bin": [],
            "/usr/lib": [],
            "/etc": [],
            "/var": ["log"],
            "/var/log": [],
            "/tmp": [],
            "/root": []
        }
        files = {"/home/user/README.txt": readme_content}
        return filesystem, files

    def boot_screen(self):
        self._clear_screen()
        print(Fore.MAGENTA + Style.BRIGHT + "Starting Star PY OS...".center(self.terminal_width) + Style.RESET_ALL)
        time.sleep(0.5)
        boot_msgs = [
            "[    0.000000] Linux version 6.17.0-star-py-1",
            "[    0.100000] Command line: BOOT_IMAGE=/vmlinuz-star root=/dev/sda1",
            "[    0.250000] Star PY OS based on GNU/Linux",
            "[    0.500000] Memory: 16384MB available",
            "[    1.000000] PCI: Using configuration type 1",
            "[    1.500000] ACPI: Core revision 20230331",
            "[    2.000000] NET: Registered PF_INET protocol family",
            "[    2.500000] Freeing unused kernel memory: 2048K",
        ]
        for msg in boot_msgs:
            print(Fore.WHITE + Style.DIM + msg + Style.RESET_ALL)
            time.sleep(0.1)
        time.sleep(0.3)
        print()
        systemd_msgs = [
            "[  OK  ] Started Emergency Shell.",
            "[  OK  ] Reached target Basic System.",
            "[  OK  ] Started D-Bus System Message Bus.",
            "[  OK  ] Started Network Manager.",
            "[  OK  ] Reached target Network.",
            "[  OK  ] Reached target Multi-User System.",
            "[  OK  ] Reached target Graphical Interface.",
        ]
        for msg in systemd_msgs:
            print(Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL)
            time.sleep(0.15)
        time.sleep(0.5)
        print()
        print(Fore.MAGENTA + "Star PY OS 6.17.0-star-py-1 (tty1)".center(self.terminal_width) + Style.RESET_ALL)
        print()
        time.sleep(0.3)
        print(Fore.WHITE + f"{self.hostname} login: " + Fore.CYAN + self.username + Style.RESET_ALL)
        time.sleep(0.2)
        print(Fore.GREEN + "Last login: Sun Feb  8 16:00:00 2026 on tty1" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "💡 Tip: Type 'cat README.txt' to get started!" + Style.RESET_ALL)
        print()
        time.sleep(0.5)

    def get_prompt(self):
        cwd = self.current_dir
        if cwd.startswith("/home/user"):
            cwd = "~" + cwd[10:]
        user_color = Fore.RED if self.is_root else Fore.GREEN
        user_name = "root" if self.is_root else self.username
        prompt_char = "#" if self.is_root else "$"
        return f"{user_color}{user_name}@{self.hostname}{Style.RESET_ALL}:{Fore.BLUE}{cwd}{Style.RESET_ALL}{prompt_char} "

    def resolve_path(self, path):
        path = path.rstrip("/") or "/"  # Normalize trailing slashes
        if path.startswith("/"):
            return path.rstrip("/") or "/"
        elif path == "~":
            return "/home/user"
        elif path.startswith("~/"):
            return "/home/user" + path[1:].rstrip("/") or "/home/user"
        elif path == "..":
            if self.current_dir == "/":
                return "/"
            parts = self.current_dir.rstrip("/").split("/")
            new_parts = parts[:-1]
            if not new_parts:
                return "/"
            return "/" + "/".join(new_parts)
        elif path == ".":
            return self.current_dir
        else:
            if self.current_dir == "/":
                return "/" + path
            return self.current_dir.rstrip("/") + "/" + path


    def ls(self, args):
        path = self.current_dir
        if args:
            path = self.resolve_path(args[0])

        if path not in self.filesystem:
            print(f"ls: cannot access '{path}': No such file or directory") # Use resolved path
            return

        items = self.filesystem[path][:]

        # Find files directly inside the *resolved* path
        file_items = []
        for filepath in self.files:
             # Check if the file is directly under the target directory
             dir_part, sep, filename = filepath.rpartition('/')
             if dir_part == path and sep: # Ensure it's a direct child
                 file_items.append(filename)
             elif path == "/" and '/' not in filepath: # Special case for files at root if any existed
                 file_items.append(filepath)


        for item in items:
            print(Fore.BLUE + Style.BRIGHT + item + "/" + Style.RESET_ALL, end="  ")
        for item in file_items:
            print(Fore.WHITE + item + Style.RESET_ALL, end="  ")
        if items or file_items:
            print()


    def cd(self, args):
        if not args:
            self.current_dir = "/home/user"
            return
        new_path = self.resolve_path(args[0])
        if new_path not in self.filesystem:
            print(f"cd: {args[0]}: No such file or directory")
            return
        self.current_dir = new_path

    def mkdir(self, args):
        if not args:
            print("mkdir: missing operand")
            return
        path = self.resolve_path(args[0])
        parent_path = os.path.dirname(path) # Use os.path for robustness
        dirname = os.path.basename(path)

        if parent_path not in self.filesystem:
            print(f"mkdir: cannot create directory '{args[0]}': No such file or directory")
            return
        if path in self.filesystem or path in self.files: # Check both dirs and files
            print(f"mkdir: cannot create directory '{args[0]}': File exists")
            return

        self.filesystem[parent_path].append(dirname)
        self.filesystem[path] = [] # Initialize new directory

    def touch(self, args):
        if not args:
            print("touch: missing file operand")
            return
        path = self.resolve_path(args[0])
        if path in self.files:
            # Update timestamp conceptually (not implemented here)
            pass
        else:
            # Check if parent directory exists
            parent_dir = os.path.dirname(path)
            if parent_dir not in self.filesystem:
                 print(f"touch: cannot create file '{args[0]}': No such file or directory")
                 return
            self.files[path] = ""

    def rm(self, args):
        if not args:
            print("rm: missing operand")
            return
        path = self.resolve_path(args[0])

        if path in self.files:
            del self.files[path]
        elif path in self.filesystem:
            if path == "/":
                print(f"rm: cannot remove '{args[0]}': Is a directory")
                return
            parent_path = os.path.dirname(path)
            dirname = os.path.basename(path)

            if parent_path in self.filesystem and dirname in self.filesystem[parent_path]:
                # Remove any files under this directory
                to_remove = [p for p in self.files if p == path or p.startswith(path + "/")]
                for p in to_remove:
                    del self.files[p]
                # Remove this dir and all subdirs (deepest first)
                subpaths = [p for p in self.filesystem if p == path or p.startswith(path + "/")]
                subpaths.sort(key=len, reverse=True)
                for p in subpaths:
                    parent = os.path.dirname(p)
                    name = os.path.basename(p)
                    if parent in self.filesystem and name in self.filesystem[parent]:
                        self.filesystem[parent].remove(name)
                    del self.filesystem[p]
            else:
                print(f"rm: cannot remove '{args[0]}': No such file or directory")
        else:
            print(f"rm: cannot remove '{args[0]}': No such file or directory")


    def cat(self, args):
        if not args:
            print("cat: missing operand")
            return
        path = self.resolve_path(args[0])
        if path not in self.files:
            print(f"cat: {args[0]}: No such file or directory")
            return
        print(self.files[path])

    def echo(self, args):
        if not args:
            print()
            return
        # Check redirects first (>> before > so ">>" is not matched as ">")
        if ">>" in args:
            try:
                idx = args.index(">>")
                text = " ".join(args[:idx])
                filename = args[idx + 1]
                if not filename:
                    raise IndexError
                path = self.resolve_path(filename)
                parent = os.path.dirname(path)
                if parent and parent not in self.filesystem:
                    print(f"echo: cannot create '{filename}': No such file or directory")
                    return
                if path in self.files:
                    self.files[path] += "\n" + text
                else:
                    self.files[path] = text
            except IndexError:
                print("echo: '>>' requires a filename")
                return
        elif ">" in args:
            try:
                idx = args.index(">")
                text = " ".join(args[:idx])
                filename = args[idx + 1]
                if not filename:
                    raise IndexError
                path = self.resolve_path(filename)
                parent = os.path.dirname(path)
                if parent and parent not in self.filesystem:
                    print(f"echo: cannot create '{filename}': No such file or directory")
                    return
                self.files[path] = text
            except IndexError:
                print("echo: '>' requires a filename")
                return
        else:
            print(" ".join(args))


    def mv(self, args):
        if len(args) < 2:
            print("mv: missing operand")
            return
        src = self.resolve_path(args[0])
        dst = self.resolve_path(args[1])

        # Check if source exists as file or directory
        src_exists_as_file = src in self.files
        src_exists_as_dir = src in self.filesystem

        if src_exists_as_file:
            self.files[dst] = self.files[src]
            del self.files[src]
        elif src_exists_as_dir:
             if dst in self.filesystem or dst in self.files: # Destination exists
                  print(f"mv: cannot move '{args[0]}': Destination '{args[1]}' exists")
                  return
             # Check if destination parent exists
             dst_parent = os.path.dirname(dst)
             if dst_parent not in self.filesystem:
                  print(f"mv: cannot move '{args[0]}': Cannot create directory '{args[1]}': No such file or directory")
                  return

             # Perform the move
             self.filesystem[dst] = self.filesystem[src] # Copy directory structure
             dst_parent_list = self.filesystem.get(dst_parent, [])
             dst_basename = os.path.basename(dst)
             if dst_basename not in dst_parent_list:
                 dst_parent_list.append(dst_basename)
                 self.filesystem[dst_parent] = dst_parent_list # Update parent list

             src_parent = os.path.dirname(src)
             src_basename = os.path.basename(src)
             src_parent_list = self.filesystem.get(src_parent, [])
             if src_basename in src_parent_list:
                 src_parent_list.remove(src_basename)
                 self.filesystem[src_parent] = src_parent_list # Update old parent list
             del self.filesystem[src] # Delete old directory entry

             # Move any files associated with the directory if needed (currently no specific file storage per dir beyond structure)
             # For this simple model, moving the structure is sufficient if no unique files per sub-dir are managed separately.

        else:
            print(f"mv: cannot stat '{args[0]}': No such file or directory")


    def clear(self, args):
        self._clear_screen()

    def pwd(self, args):
        print(self.current_dir)

    def whoami(self, args):
        if self.is_root:
            print("root")
        else:
            print(self.username)

    def id(self, args):
        if self.is_root:
            print("uid=0(root) gid=0(root) groups=0(root)")
        else:
            print(f"uid=1000({self.username}) gid=1000({self.username}) groups=1000({self.username}),4(adm),24(cdrom),27(sudo)")

    def sudo(self, args):
        if not args:
            print("sudo: no command specified")
            return
        print(f"[sudo] password for {self.username}: ", end="")
        sys.stdout.flush()
        time.sleep(0.5)
        print()
        old_root = self.is_root
        self.is_root = True
        cmd = args[0]
        cmd_args = args[1:]
        if hasattr(self, cmd):
            getattr(self, cmd)(cmd_args)
        else:
            print(f"{cmd}: command not found")
        self.is_root = old_root

    def beep(self, args):
        if len(args) < 2:
            print("beep: usage: beep <duration_ms> <frequency_hz>")
            return
        try:
            duration = int(args[0])
            frequency = int(args[1])
            print(f"{Fore.YELLOW}🔊 BEEP! Duration: {duration}ms, Frequency: {frequency}Hz{Style.RESET_ALL}")
            beep_chars = ["♪", "♫", "♬", "♩"]
            iterations = max(1, duration // 100)
            for i in range(iterations):
                sys.stdout.write(f"\r{Fore.CYAN}{random.choice(beep_chars) * (i % 10 + 1)}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
            print(f"\r{Fore.GREEN}Beep complete!{Style.RESET_ALL}" + " " * 20)
        except ValueError:
            print("beep: invalid arguments, must be integers")

    def trojan(self, args):
        self._clear_screen()
        print(Fore.RED + Style.BRIGHT + "╔═══════════════════════════════════════════════════════════════════════════════════╗" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "║                         TROJAN VIRUS GENERATOR v2.5                               ║" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "╚═══════════════════════════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "⚠️  WARNING: This is a SIMULATION - no actual malware will be created!" + Style.RESET_ALL)
        print()
        trojan_name = f"Trojan.Win32.Agent.{random.randint(100000, 999999)}"
        print(Fore.MAGENTA + f"Generating Trojan: {trojan_name}" + Style.RESET_ALL)
        print()
        time.sleep(0.5)
        stages = [
            ("Initializing malware framework", 15),
            ("Loading polymorphic engine", 20),
            ("Compiling payload shellcode", 25),
            ("Obfuscating binary signature", 30),
            ("Encrypting command & control URLs", 35),
            ("Injecting process hollowing code", 40),
            ("Adding rootkit components", 45),
            ("Implementing keylogger module", 50),
            ("Setting up backdoor listener", 55),
            ("Creating persistence registry keys", 60),
            ("Packing with UPX compressor", 65),
            ("Adding anti-debugging checks", 70),
            ("Implementing VM detection", 75),
            ("Encrypting strings with XOR", 80),
            ("Generating fake digital signature", 85),
            ("Building command execution module", 90),
            ("Adding screen capture functionality", 92),
            ("Implementing file exfiltration", 94),
            ("Creating auto-update mechanism", 96),
            ("Finalizing trojan binary", 98),
            ("Signing malware with stolen certificate", 100),
        ]
        for stage, progress in stages:
            bar_len = int(progress * 0.8)
            bar = "█" * bar_len + "░" * (80 - bar_len)
            color = Fore.GREEN if progress < 50 else Fore.YELLOW if progress < 80 else Fore.RED
            print(f"\r{Fore.CYAN}[{color}{bar}{Fore.CYAN}] {progress}% {Style.RESET_ALL}{stage}...".ljust(120), end="")
            sys.stdout.flush()
            time.sleep(0.3)
        print("\n")
        time.sleep(0.5)
        print(Fore.GREEN + "✓ Trojan successfully generated!" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "Trojan capabilities:" + Style.RESET_ALL)
        capabilities = [
            "• Remote access and control",
            "• Keystroke logging",
            "• Screen capture and monitoring",
            "• File system access and exfiltration",
            "• Registry manipulation",
            "• Process injection and hiding",
            "• Network traffic interception",
            "• Webcam and microphone access",
            "• Credential harvesting",
            "• Reverse shell establishment"
        ]
        for cap in capabilities:
            print(Fore.WHITE + cap + Style.RESET_ALL)
        time.sleep(0.1)
        print()
        print(Fore.RED + "⚠️  DEPLOYING TROJAN..." + Style.RESET_ALL)
        time.sleep(1)
        for i in range(5):
            sys.stdout.write(f"\r{Fore.RED}{'█' * (i * 20)}{'░' * (100 - i * 20)}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.3)
        print()
        print()
        print(Fore.RED + "ERROR: System breach detected!" + Style.RESET_ALL)
        time.sleep(0.5)
        print(Fore.RED + "ERROR: Unauthorized access established!" + Style.RESET_ALL)
        time.sleep(0.5)
        print(Fore.RED + "ERROR: Backdoor installed successfully!" + Style.RESET_ALL)
        time.sleep(1)
        print()
        print(Fore.GREEN + Style.BRIGHT + "JUST KIDDING! 😂" + Style.RESET_ALL)
        print(Fore.CYAN + "This was a harmless simulation. Your system is completely safe!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Educational purposes only - never create or use real malware!" + Style.RESET_ALL)
        print()

    def ransomware(self, args):
        self._clear_screen()
        print(Fore.RED + Style.BRIGHT + "╔═══════════════════════════════════════════════════════════════════════════════════╗" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "║                      RANSOMWARE ENCRYPTION ENGINE v3.2                            ║" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "╚═══════════════════════════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "⚠️  SIMULATION MODE - No files will actually be encrypted!" + Style.RESET_ALL)
        print()
        ransomware_name = f"Ransomware.Crypto.Locker.{random.randint(1000, 9999)}"
        decryption_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        print(Fore.MAGENTA + f"Initializing: {ransomware_name}" + Style.RESET_ALL)
        print()
        time.sleep(0.5)
        stages = [
            ("Loading encryption modules", 5),
            ("Generating RSA-4096 key pair", 10),
            ("Creating AES-256 session keys", 15),
            ("Scanning filesystem for targets", 20),
            ("Identifying encryption candidates", 25),
            ("Blacklisting system files", 30),
            ("Preparing encryption queue", 35),
            ("Disabling shadow copies", 40),
            ("Terminating antivirus processes", 45),
            ("Encrypting: Documents folder", 50),
            ("Encrypting: Pictures folder", 55),
            ("Encrypting: Videos folder", 60),
            ("Encrypting: Desktop files", 65),
            ("Encrypting: Downloads folder", 70),
            ("Encrypting: Database files", 75),
            ("Encrypting: Backup archives", 80),
            ("Overwriting file headers", 85),
            ("Deleting recovery points", 88),
            ("Destroying volume shadow copies", 91),
            ("Wiping file slack space", 94),
            ("Generating ransom note", 96),
            ("Establishing C2 connection", 98),
            ("Finalizing encryption process", 100),
        ]
        for stage, progress in stages:
            bar_len = int(progress * 0.8)
            bar = "█" * bar_len + "░" * (80 - bar_len)
            color = Fore.GREEN if progress < 50 else Fore.YELLOW if progress < 80 else Fore.RED
            print(f"\r{Fore.CYAN}[{color}{bar}{Fore.CYAN}] {progress}% {Style.RESET_ALL}{stage}...".ljust(120), end="")
            sys.stdout.flush()
            time.sleep(0.2)
        print("\n")
        time.sleep(0.5)
        print()
        print(Fore.RED + Style.BRIGHT + "╔═══════════════════════════════════════════════════════════════════════════════════╗" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "║                           ⚠️  ALL FILES ENCRYPTED  ⚠️                              ║" + Style.RESET_ALL)
        print(Fore.RED + Style.BRIGHT + "╚═══════════════════════════════════════════════════════════════════════════════════╝" + Style.RESET_ALL)
        print()
        encrypted_count = random.randint(15000, 50000)
        print(Fore.YELLOW + f"Total files encrypted: {encrypted_count}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Encryption algorithm: AES-256-CBC + RSA-4096" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Ransomware family: {ransomware_name}" + Style.RESET_ALL)
        print()
        print(Fore.CYAN + "To decrypt your files, you need the decryption key." + Style.RESET_ALL)
        print(Fore.CYAN + "A file has been created with the key hidden in its FILENAME!" + Style.RESET_ALL)
        print()
        # Create the key file with code in filename
        key_filename = f"DECRYPT_KEY_{decryption_code}.txt"
        key_path = f"/home/user/Downloads/{key_filename}"
        self.files[key_path] = f"""╔═══════════════════════════════════════════════════════════════╗
║              RANSOMWARE DECRYPTION INSTRUCTIONS               ║
╚═══════════════════════════════════════════════════════════════╝
Your system has been encrypted by {ransomware_name}
IMPORTANT: The decryption code is hidden in this FILE'S NAME!
Look at the filename carefully - it contains the key you need.
This is a SIMULATION - no actual encryption occurred.
All your files are completely safe.
Educational demonstration only - never create or deploy ransomware!
To "decrypt" (end simulation), find the code in the filename above.
"""
        # File is in self.files so it will show in ls automatically
        print(Fore.GREEN + f"💡 Hint: Check /home/user/Downloads/" + Style.RESET_ALL)
        print(Fore.GREEN + f"💡 The decryption key is in the FILENAME, not the file contents!" + Style.RESET_ALL)
        print()
        time.sleep(2)
        print(Fore.YELLOW + "Attempting to contact C2 server..." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.RED + "Connection failed!" + Style.RESET_ALL)
        time.sleep(0.5)
        print()
        print(Fore.GREEN + Style.BRIGHT + "SIMULATION COMPLETE! 😄" + Style.RESET_ALL)
        print(Fore.CYAN + "This was completely harmless - your system is safe!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Remember: Ransomware is illegal and devastating - never use it!" + Style.RESET_ALL)
        print()

    def lynx(self, args):
        if not args:
            url = "https://example.com"
        else:
            url = args[0]
        self._clear_screen()
        print(Fore.CYAN + f"Lynx/2.9.0dev.12 - Text-based Web Browser".center(self.terminal_width) + Style.RESET_ALL)
        print(Fore.BLUE + "=" * self.terminal_width + Style.RESET_ALL)
        print()
        # Simulated web pages
        pages = {
            "https://example.com": {
                "title": "Example Domain",
                "content": """
Example Domain
This domain is for use in illustrative examples in documents.
You may use this domain in literature without prior coordination
or asking for permission.
[More information...]
Links:
• About
• Contact
• Privacy Policy
"""
            },
            "https://github.com": {
                "title": "GitHub - Where the world builds software",
                "content": """
GitHub
Where the world builds software
Millions of developers and companies build, ship, and maintain
their software on GitHub—the largest and most advanced
development platform in the world.
Links:
• Sign in
• Sign up
• Explore
• Pricing
• Documentation
Featured Repositories:
• [linux] - Linux kernel source tree
• [python] - The Python programming language
• [react] - A JavaScript library for building user interfaces
"""
            },
            "https://github.com/Brdyyy8-0298/Star-PY-OS": {
                "title": "Star-PY-OS - Simulated Linux Terminal",
                "content": """
Star-PY-OS
A fully simulated GNU/Linux terminal environment written in Python
⭐ Star this repository
About:
Star PY OS is a complete simulation of a Linux terminal with
features including package management, file editing, system
monitors, web browsing, and more - all in pure Python!
Features:
• Full filesystem simulation
• Package manager (pkg)
• Text editors (nano, vim)
• System monitors (htop, btop)
• Web browser (lynx)
• Animations (nyancat, cmatrix, cava)
• Prank tools (virus simulators)
Installation:
1. Install Python 3.x
2. Install colorama: pip install colorama
3. Run: python star_py_os.py
Links:
• [README.md]
• [Issues]
• [Pull Requests]
• [License: MIT]
"""
            }
        }
        if url in pages:
            page = pages[url]
            print(Fore.GREEN + f"URL: {url}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Title: {page['title']}" + Style.RESET_ALL)
            print()
            print(page['content'])
        else:
            print(Fore.RED + f"Could not connect to {url}" + Style.RESET_ALL)
            print()
            print("Available pages:")
            print("• https://example.com")
            print("• https://github.com")
            print("• https://github.com/Brdyyy8-0298/Star-PY-OS")
            print()
            print(Fore.BLUE + "─" * self.terminal_width + Style.RESET_ALL)
            print(Fore.CYAN + "Commands: [Q]uit | [G]o to URL | [H]elp" + Style.RESET_ALL)
            print()
        try:
            while True:
                cmd = input(Fore.GREEN + "lynx> " + Style.RESET_ALL).strip().lower()
                if cmd == "q":
                    break
                elif cmd == "g":
                    new_url = input("Enter URL: ").strip()
                    self.lynx([new_url])
                    break
                elif cmd == "h":
                    print("\nLynx Help:")
                    print("  q - Quit")
                    print("  g - Go to URL")
                    print("  h - Help")
                    print()
                else:
                    print("Unknown command. Press 'h' for help.")
        except KeyboardInterrupt:
            print()
        self._clear_screen()

    def cmatrix(self, args):
        print(Fore.GREEN + "CMatrix - The Matrix Screensaver" + Style.RESET_ALL)
        print(Fore.YELLOW + "Press Ctrl+C to exit" + Style.RESET_ALL)
        time.sleep(1)
        cols = min(self.terminal_width, 120)
        rows = min(self.terminal_height, 30)
        drops = [0] * cols
        chars = ['0', '1', 'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク']
        # ANSI: hide cursor, then use cursor-home each frame to avoid clear flash
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            while True:
                # Update drops
                for i in range(cols):
                    if random.random() < 0.02:
                        drops[i] = 0
                    if drops[i] < rows:
                        drops[i] += 1
                    else:
                        drops[i] = 0
                # Build full frame then draw in one go (reduces flicker)
                sys.stdout.write(CURSOR_HOME)
                for j in range(rows):
                    line = ""
                    for i in range(cols):
                        if j == drops[i]:
                            line += Fore.WHITE + Style.BRIGHT + random.choice(chars)
                        elif drops[i] > 0 and j == drops[i] - 1:
                            line += Fore.GREEN + Style.BRIGHT + random.choice(chars)
                        elif drops[i] > 0 and 0 <= drops[i] - j <= 8:
                            line += Fore.GREEN + random.choice(chars)
                        else:
                            line += " "
                    sys.stdout.write(line + Style.RESET_ALL + "\n")
                sys.stdout.flush()
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        self._clear_screen()

    def cava(self, args):
        print(Fore.MAGENTA + "CAVA - Console Audio Visualizer" + Style.RESET_ALL)
        print(Fore.YELLOW + "Simulating audio visualization - Press Ctrl+C to exit" + Style.RESET_ALL)
        time.sleep(1)
        bars = 80
        max_height = 20
        header = Fore.CYAN + "♪ Now Playing: Simulated Audio Track ♪".center(self.terminal_width) + Style.RESET_ALL
        footer = Fore.CYAN + "Bass".ljust(20) + "Mid".ljust(40) + "Treble".rjust(20) + Style.RESET_ALL
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            beat = 0
            while True:
                # Generate simulated audio levels
                levels = []
                for i in range(bars):
                    base = int(max_height * abs(math.sin((i + beat) * 0.1)))
                    variation = random.randint(-3, 3)
                    level = max(0, min(max_height, base + variation))
                    levels.append(level)
                # Build full frame and draw in one go
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write(header + "\n\n")
                for h in range(max_height, 0, -1):
                    line = ""
                    for level in levels:
                        if level >= h:
                            if h > max_height * 0.7:
                                line += Fore.RED + "█"
                            elif h > max_height * 0.4:
                                line += Fore.YELLOW + "█"
                            else:
                                line += Fore.GREEN + "█"
                        else:
                            line += " "
                    sys.stdout.write(line + Style.RESET_ALL + "\n")
                sys.stdout.write("\n" + footer + "\n")
                sys.stdout.flush()
                beat += 1
                time.sleep(0.05)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        self._clear_screen()

    def mc(self, args):
        current_selection = 0
        scroll_offset = 0
        max_visible = 25  # Items visible on screen
        self._clear_screen()
        try:
            while True:
                self._clear_screen()
                # Header
                print(Back.BLUE + Fore.WHITE + Style.BRIGHT + " Midnight Commander ".ljust(self.terminal_width) + Style.RESET_ALL)
                print()
                # Current path
                print(Back.CYAN + Fore.BLACK + f" {self.current_dir} ".ljust(self.terminal_width) + Style.RESET_ALL)
                print()
                # Get items
                items = self.filesystem.get(self.current_dir, [])
                file_items = []
                for filepath in self.files:
                     dir_part, sep, filename = filepath.rpartition('/')
                     if dir_part == self.current_dir and sep:
                         file_items.append(filename)

                # Add parent directory
                all_items = [("../", True, True)]  # (name, is_dir, is_parent)
                all_items += [(item, True, False) for item in items]
                all_items += [(item, False, False) for item in file_items] # Use filename from loop

                # Calculate visible range
                visible_items = all_items[scroll_offset:scroll_offset + max_visible]
                # Display items
                for i, (item, is_dir, is_parent) in enumerate(visible_items):
                    actual_index = scroll_offset + i
                    if actual_index == current_selection:
                        # Selected item
                        if is_dir:
                            icon = "📁" if not is_parent else "⬆️ "
                            print(Back.CYAN + Fore.BLACK + f" {icon} {item:<75} " + Style.RESET_ALL)
                        else:
                            print(Back.CYAN + Fore.BLACK + f" 📄 {item:<75} " + Style.RESET_ALL)
                    else:
                        # Non-selected item
                        if is_dir:
                            icon = "📁" if not is_parent else "⬆️ "
                            print(f" {Fore.BLUE}{Style.BRIGHT}{icon} {item}{Style.RESET_ALL}")
                        else:
                            print(f" 📄 {item}")
                # Footer with commands
                print()
                print(Back.BLUE + Fore.WHITE + " F5 Copy | F6 Move | F7 NewDir | F8 Delete | F9 NewFile | ENTER Open | Q Quit ".ljust(self.terminal_width) + Style.RESET_ALL)
                print()
                # Get command
                cmd = input(Fore.GREEN + "mc> " + Style.RESET_ALL).strip().lower()
                if cmd == "q":
                    break
                elif cmd == "down" or cmd == "j":
                    if current_selection < len(all_items) - 1:
                        current_selection += 1
                        if current_selection >= scroll_offset + max_visible:
                            scroll_offset += 1
                elif cmd == "up" or cmd == "k":
                    if current_selection > 0:
                        current_selection -= 1
                        if current_selection < scroll_offset:
                            scroll_offset -= 1
                elif cmd == "enter" or cmd == "":
                    if current_selection < len(all_items):
                        selected_item, is_dir, is_parent = all_items[current_selection]
                        if is_parent:
                            self.cd([".."])
                            current_selection = 0
                            scroll_offset = 0
                        elif is_dir:
                            new_path = self.current_dir + ("/" if self.current_dir != "/" else "") + selected_item
                            if new_path in self.filesystem:
                                self.current_dir = new_path
                                current_selection = 0
                                scroll_offset = 0
                        else:
                            # View file
                            file_path = self.current_dir + "/" + selected_item
                            if file_path in self.files:
                                self._clear_screen()
                                print(Fore.CYAN + f"Viewing: {selected_item}" + Style.RESET_ALL)
                                print("=" * 80)
                                print(self.files[file_path])
                                print("=" * 80)
                                input("Press Enter to continue...")
                elif cmd == "f7" or cmd == "mkdir":
                    dirname = input("Enter directory name: ").strip()
                    if dirname:
                        self.mkdir([dirname])
                elif cmd == "f9" or cmd == "touch":
                    filename = input("Enter file name: ").strip()
                    if filename:
                        self.touch([filename])
                elif cmd == "f8" or cmd == "delete":
                    if current_selection < len(all_items):
                        selected_item, is_dir, is_parent = all_items[current_selection]
                        if not is_parent:
                            confirm = input(f"Delete {selected_item}? (y/n): ").lower()
                            if confirm == "y":
                                self.rm([selected_item])
                                current_selection = max(0, current_selection - 1)
        except KeyboardInterrupt:
            print("\n")
        self._clear_screen()

    def nano(self, args):
        if not args:
            print("nano: missing filename")
            return
        path = self.resolve_path(args[0])
        content = self.files.get(path, "")
        self._clear_screen()
        print(Fore.BLACK + Back.WHITE + f" GNU nano 7.2              {args[0]}".ljust(self.terminal_width) + Style.RESET_ALL)
        print()
        if content:
            print(content)
        lines = content.split("\n") if content else []
        print()
        print(Fore.BLACK + Back.WHITE + "^G Help    ^O Write Out ^W Where Is  ^K Cut       ^T Execute  ".ljust(self.terminal_width) + Style.RESET_ALL)
        print(Fore.BLACK + Back.WHITE + r"^X Exit    ^R Read File  ^\ Replace   ^U Paste     ^J Justify  ".ljust(self.terminal_width) + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "Enter text (type 'SAVE' on new line to save, 'EXIT' to quit without saving)" + Style.RESET_ALL)
        print()
        try:
            while True:
                line = input()
                if line == "SAVE":
                    self.files[path] = "\n".join(lines)
                    print(Fore.GREEN + f"[ Wrote {len(lines)} lines ]" + Style.RESET_ALL)
                    time.sleep(1)
                    break
                elif line == "EXIT":
                    print(Fore.YELLOW + "Exit without saving" + Style.RESET_ALL)
                    time.sleep(1)
                    break
                else:
                    lines.append(line)
        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "Exit without saving" + Style.RESET_ALL)
        self._clear_screen()

    def pkg(self, args):
        if not args:
            print("pkg: Star PY Package Manager")
            print("Usage:")
            print("  pkg install <package>   - Install a package")
            print("  pkg remove <package>    - Remove a package")
            print("  pkg list                - List installed packages")
            print("  pkg search <query>      - Search for packages")
            print("  pkg update              - Update package database")
            return
        cmd = args[0]
        if cmd == "list":
            print(Fore.CYAN + "Installed packages:" + Style.RESET_ALL)
            for pkg in self.installed_packages:
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {pkg}")
        elif cmd == "install" and len(args) > 1:
            pkg_name = args[1]
            if pkg_name in self.installed_packages:
                print(f"{Fore.YELLOW}Package '{pkg_name}' is already installed{Style.RESET_ALL}")
            else:
                print(f"Installing {pkg_name}...")
                time.sleep(0.5)
                print(f"Downloading {pkg_name}... [{'=' * 20}] 100%")
                time.sleep(0.3)
                print(f"Verifying package...")
                time.sleep(0.2)
                self.installed_packages.append(pkg_name)
                print(f"{Fore.GREEN}✓ Package '{pkg_name}' installed successfully!{Style.RESET_ALL}")
        elif cmd == "remove" and len(args) > 1:
            pkg_name = args[1]
            if pkg_name not in self.installed_packages:
                print(f"{Fore.RED}Package '{pkg_name}' is not installed{Style.RESET_ALL}")
            else:
                print(f"Removing {pkg_name}...")
                time.sleep(0.3)
                self.installed_packages.remove(pkg_name)
                print(f"{Fore.GREEN}✓ Package '{pkg_name}' removed successfully!{Style.RESET_ALL}")
        elif cmd == "search" and len(args) > 1:
            query = args[1]
            available = ["firefox", "chrome", "git", "docker", "nginx", "apache", "mysql", "nodejs", "gcc", "make"]
            results = [p for p in available if query.lower() in p.lower()]
            if results:
                print(Fore.CYAN + f"Search results for '{query}':" + Style.RESET_ALL)
                for pkg in results:
                    installed = pkg in self.installed_packages
                    status = f"{Fore.GREEN}[installed]{Style.RESET_ALL}" if installed else ""
                    print(f"  {pkg} {status}")
            else:
                print(f"No packages found matching '{query}'")
        elif cmd == "update":
            print("Updating package database...")
            time.sleep(0.5)
            print("Fetching package lists... [" + "=" * 25 + "] 100%")
            time.sleep(0.3)
            print(f"{Fore.GREEN}✓ Package database updated!{Style.RESET_ALL}")
        else:
            print(f"pkg: unknown command '{cmd}'")

    def virus(self, args):
        print(Fore.RED + Style.BRIGHT + "⚠️  VIRUS GENERATOR ⚠️" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "This is a PRANK tool - no actual harm will be done!" + Style.RESET_ALL)
        print()
        virus_types = [
            "Trojan.Generic.KD.12345678",
            "Worm.Win32.Conficker",
            "Ransomware.Cryptolocker.B",
            "Backdoor.Linux.Gafgyt",
            "Spyware.KeyLogger.XYZ",
        ]
        selected = random.choice(virus_types)
        print(f"Generating virus: {Fore.MAGENTA}{selected}{Style.RESET_ALL}")
        time.sleep(0.5)
        stages = [
            "Compiling malicious code...",
            "Obfuscating payload...",
            "Encrypting strings...",
            "Adding anti-detection...",
            "Creating persistence hooks...",
            "Finalizing executable...",
        ]
        for stage in stages:
            print(f"[+] {stage}", end="")
            time.sleep(0.3)
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
        print()
        print(Fore.RED + "⚠️  VIRUS GENERATED! ⚠️" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "Deploying virus..." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.RED + "ERROR: System32 corrupted!" + Style.RESET_ALL)
        time.sleep(0.5)
        print(Fore.RED + "ERROR: Bootloader compromised!" + Style.RESET_ALL)
        time.sleep(0.5)
        print(Fore.RED + "ERROR: All files encrypted!" + Style.RESET_ALL)
        time.sleep(1)
        print()
        print(Fore.GREEN + "Just kidding! 😂" + Style.RESET_ALL)
        print(Fore.CYAN + "This was a harmless prank. Your system is safe!" + Style.RESET_ALL)
        print()

    def tree(self, args):
        path = self.current_dir
        if args:
            path = self.resolve_path(args[0])
        if path not in self.filesystem:
            print(f"tree: {args[0] if args else path}: No such file or directory")
            return

        def print_tree(current_path, prefix="", is_last=True):
            items = self.filesystem.get(current_path, [])
            file_items = []
            for filepath in self.files:
                 dir_part, sep, filename = filepath.rpartition('/')
                 if dir_part == current_path and sep:
                     file_items.append(filename)

            all_items = [(d, True) for d in items] + [(f, False) for f in file_items]
            for i, (item, is_dir) in enumerate(all_items):
                is_last_item = (i == len(all_items) - 1)
                connector = "└── " if is_last_item else "├── "
                if is_dir:
                    print(prefix + connector + Fore.BLUE + item + Style.RESET_ALL)
                    new_prefix = prefix + ("    " if is_last_item else "│   ")
                    new_path = current_path + ("/" if current_path != "/" else "") + item
                    print_tree(new_path, new_prefix, is_last_item)
                else:
                    print(prefix + connector + Fore.WHITE + item + Style.RESET_ALL)

        print(Fore.BLUE + path + Style.RESET_ALL)
        print_tree(path)

    def fastfetch(self, args):
        logo = [
            "    ⭐ STAR  ",
            "   ⭐⭐⭐⭐  ",
            "  ⭐ PY OS ⭐ ",
            "   ⭐⭐⭐⭐  ",
            "    ⭐⭐⭐   ",
        ]
        info = [
            f"{Fore.MAGENTA}{self.username}@{self.hostname}{Style.RESET_ALL}",
            "-------------------",
            f"{Fore.MAGENTA}OS{Style.RESET_ALL}: Star PY OS x86_64",
            f"{Fore.MAGENTA}Based on{Style.RESET_ALL}: GNU/Linux",
            f"{Fore.MAGENTA}Kernel{Style.RESET_ALL}: 6.17.0-star-py-1",
            f"{Fore.MAGENTA}Uptime{Style.RESET_ALL}: 2 mins",
            f"{Fore.MAGENTA}Shell{Style.RESET_ALL}: python-shell",
            f"{Fore.MAGENTA}Terminal{Style.RESET_ALL}: /dev/tty1",
            f"{Fore.MAGENTA}CPU{Style.RESET_ALL}: Intel Core i7 (8) @ 3.6GHz",
            f"{Fore.MAGENTA}Memory{Style.RESET_ALL}: 2048MiB / 16384MiB",
        ]
        for i in range(max(len(logo), len(info))):
            logo_line = Fore.YELLOW + logo[i] + Style.RESET_ALL if i < len(logo) else " " * 15
            info_line = info[i] if i < len(info) else ""
            print(f"{logo_line}   {info_line}")

    def nyancat(self, args):
        frames = [
            [
                "   _____                ",
                "  /     \\               ",
                " | () () |   ∼∼∼∼      ",
                "  \\  ^  /   ∼∼∼∼       ",
                "   |||||    ∼∼∼∼       ",
                "   |||||               ",
            ],
            [
                "   _____                ",
                "  /     \\               ",
                " | () () |     ∼∼∼∼    ",
                "  \\  ^  /     ∼∼∼∼     ",
                "   |||||      ∼∼∼∼     ",
                "   |||||               ",
            ]
        ]
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        print("\n" + Fore.YELLOW + "Press Ctrl+C to stop" + Style.RESET_ALL + "\n")
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            frame_idx = 0
            color_idx = 0
            while True:
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write("\n")
                color = colors[color_idx % len(colors)]
                for line in frames[frame_idx]:
                    sys.stdout.write(color + line + Style.RESET_ALL + "\n")
                sys.stdout.write("\n" + Fore.CYAN + "~~ NYAN NYAN ~~" + Style.RESET_ALL + "\n")
                sys.stdout.flush()
                frame_idx = (frame_idx + 1) % len(frames)
                color_idx += 1
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        self._clear_screen()

    def vim(self, args):
        if not args:
            print("vim: missing filename")
            return
        path = self.resolve_path(args[0])
        content = self.files.get(path, "")
        print(Fore.GREEN + "--- VIM MODE ---" + Style.RESET_ALL)
        print(Fore.YELLOW + "Enter text (type ':wq' on new line to save and quit, ':q' to quit without saving)" + Style.RESET_ALL)
        print()
        if content:
            print(content)
        lines = content.split("\n") if content else []
        try:
            while True:
                line = input()
                if line == ":wq":
                    self.files[path] = "\n".join(lines)
                    print("File saved!")
                    break
                elif line == ":q":
                    print("Quit without saving")
                    break
                else:
                    lines.append(line)
        except KeyboardInterrupt:
            print("\nQuit without saving")

    def htop(self, args):
        print(Fore.YELLOW + "Press Ctrl+C to exit" + Style.RESET_ALL)
        time.sleep(1)
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            while True:
                lines = [Fore.GREEN + Style.BRIGHT + "htop - Interactive Process Viewer".center(self.terminal_width) + Style.RESET_ALL, ""]
                for i in range(8):
                    usage = random.randint(10, 95)
                    bar_len = int(usage / 5)
                    bar = "█" * bar_len + " " * (20 - bar_len)
                    color = Fore.GREEN if usage < 50 else Fore.YELLOW if usage < 80 else Fore.RED
                    lines.append(f"  {i+1} [{color}{bar}{Style.RESET_ALL}] {usage:>3}%")
                mem_usage = random.randint(20, 60)
                mem_bar = "█" * int(mem_usage / 5) + " " * (20 - int(mem_usage / 5))
                lines.extend(["", f"Mem[{Fore.CYAN}{mem_bar}{Style.RESET_ALL}] {mem_usage}% 4.2G/16.0G"])
                swap_usage = random.randint(0, 20)
                swap_bar = "█" * int(swap_usage / 5) + " " * (20 - int(swap_usage / 5))
                lines.append(f"  Swp[{Fore.YELLOW}{swap_bar}{Style.RESET_ALL}] {swap_usage}% 512M/8.0G")
                lines.extend(["", f"  Tasks: {Fore.CYAN}127{Style.RESET_ALL}, Load avg: {Fore.GREEN}1.2 1.5 1.8{Style.RESET_ALL}", f"  Uptime: {Fore.YELLOW}2:15:34{Style.RESET_ALL}", ""])
                lines.append(f"  {Fore.BLACK}{Back.CYAN}  PID USER      CPU% MEM%   TIME+ COMMAND            {Style.RESET_ALL}")
                processes = [
                    (1234, "user", random.randint(0, 15), random.randint(1, 5), "1:23.45", "python"),
                    (5678, "user", random.randint(0, 25), random.randint(2, 8), "0:45.12", "chrome"),
                    (9101, "root", random.randint(0, 5), random.randint(1, 3), "5:12.34", "systemd"),
                    (1121, "user", random.randint(0, 10), random.randint(1, 4), "0:15.67", "bash"),
                    (3141, "user", random.randint(0, 30), random.randint(3, 10), "2:34.89", "firefox"),
                    (5161, "root", random.randint(0, 5), random.randint(0, 2), "0:05.23", "sshd"),
                ]
                for pid, user, cpu, mem, ptime, cmd in processes:
                    lines.append(f"  {pid:>5} {user:<9} {cpu:>4}% {mem:>4}% {ptime:>7} {cmd:<20}")
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write("\n".join(lines) + "\n")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        self._clear_screen()

    def btop(self, args):
        print(Fore.YELLOW + "Press Ctrl+C to exit" + Style.RESET_ALL)
        time.sleep(1)
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            while True:
                lines = [
                    Fore.MAGENTA + Style.BRIGHT + "╔" + "═" * (self.terminal_width - 2) + "╗" + Style.RESET_ALL,
                    Fore.MAGENTA + Style.BRIGHT + "║" + "BTOP++ v1.2.13".center(self.terminal_width - 2) + "║" + Style.RESET_ALL,
                    Fore.MAGENTA + Style.BRIGHT + "╚" + "═" * (self.terminal_width - 2) + "╝" + Style.RESET_ALL,
                    "",
                    Fore.CYAN + "  CPU [8 cores]" + Style.RESET_ALL,
                ]
                for i in range(8):
                    usage = random.randint(5, 85)
                    graph = "".join([random.choice(["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]) for _ in range(80)])
                    color = Fore.GREEN if usage < 50 else Fore.YELLOW if usage < 75 else Fore.RED
                    lines.append(f"  {i+1}: {color}{graph}{Style.RESET_ALL} {usage}%")
                lines.append("")
                mem = random.randint(35, 65)
                mem_graph = "█" * int(mem * 0.8) + "░" * (80 - int(mem * 0.8))
                lines.append(f"  {Fore.BLUE}MEM [{mem_graph}] {mem}%{Style.RESET_ALL}")
                disk = random.randint(40, 70)
                disk_graph = "█" * int(disk * 0.8) + "░" * (80 - int(disk * 0.8))
                lines.append(f"  {Fore.YELLOW}DSK [{disk_graph}] {disk}%{Style.RESET_ALL}")
                net_up = random.randint(100, 999)
                net_down = random.randint(500, 2000)
                lines.extend(["", f"{Fore.GREEN}NET ↑{net_up}KB/s ↓{net_down}KB/s{Style.RESET_ALL}", ""])
                lines.append(Fore.CYAN + "  Top Processes:" + Style.RESET_ALL)
                procs = [
                    ("python", random.randint(5, 25)),
                    ("chrome", random.randint(10, 35)),
                    ("firefox", random.randint(8, 30)),
                    ("systemd", random.randint(1, 5)),
                ]
                for proc, cpu in procs:
                    bar = "█" * int(cpu) + "░" * (50 - int(cpu))
                    lines.append(f"    {proc:<12} [{Fore.GREEN}{bar}{Style.RESET_ALL}] {cpu}%")
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write("\n".join(lines) + "\n")
                sys.stdout.flush()
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        self._clear_screen()

    def cowsay(self, args):
        if not args:
            text = "Hello from Star PY OS!"
        else:
            text = " ".join(args)
        text_len = len(text)
        print(" " + "_" * (text_len + 2))
        print(f"< {text} >")
        print(" " + "-" * (text_len + 2))
        print(r"        \   ^__^")
        print(r"         \  (oo)\_______")
        print(r"            (__)\       )\/\ ")
        print(r"                ||----w |")
        print(r"                ||     ||")

    def hollywood(self, args):
        print(Fore.GREEN + "HOLLYWOOD HACKER MODE" + Style.RESET_ALL)
        print(Fore.YELLOW + "Press Ctrl+C to exit" + Style.RESET_ALL)
        time.sleep(1)
        CURSOR_HOME = "\033[H"
        CURSOR_HIDE = "\033[?25l"
        CURSOR_SHOW = "\033[?25h"
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self._clear_screen()
        try:
            iteration = 0
            while True:
                lines = [
                    Fore.GREEN + Style.BRIGHT + "╔" + "═" * (self.terminal_width - 2) + "╗" + Style.RESET_ALL,
                    Fore.GREEN + Style.BRIGHT + "║" + "CLASSIFIED HACKING OPERATION v4.7".center(self.terminal_width - 2) + "║" + Style.RESET_ALL,
                    Fore.GREEN + Style.BRIGHT + "╚" + "═" * (self.terminal_width - 2) + "╝" + Style.RESET_ALL,
                    "",
                    Fore.CYAN + "┌─ PORT SCANNER " + "─" * (self.terminal_width - 20) + "┐" + Style.RESET_ALL,
                ]
                for i in range(3):
                    port = random.randint(1000, 9999)
                    status = random.choice(["OPEN", "CLOSED", "FILTERED"])
                    color = Fore.GREEN if status == "OPEN" else Fore.RED
                    lines.append(f"│ Port {port}: {color}{status}{Style.RESET_ALL}")
                lines.extend([Fore.CYAN + "└" + "─" * (self.terminal_width - 2) + "┘" + Style.RESET_ALL, ""])
                lines.append(Fore.YELLOW + "┌─ NETWORK TRAFFIC " + "─" * (self.terminal_width - 22) + "┐" + Style.RESET_ALL)
                for i in range(3):
                    ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
                    packets = random.randint(100, 9999)
                    lines.append(f"│ {ip} → {packets} packets")
                lines.extend([Fore.YELLOW + "└" + "─" * (self.terminal_width - 2) + "┘" + Style.RESET_ALL, ""])
                lines.append(Fore.MAGENTA + "┌─ DECRYPTION ENGINE " + "─" * (self.terminal_width - 24) + "┐" + Style.RESET_ALL)
                for i in range(2):
                    hex_str = ''.join([random.choice('0123456789ABCDEF') for _ in range(32)])
                    lines.append(f"│ 0x{hex_str}")
                    progress = random.randint(60, 99)
                    bar_len = int(progress * 0.8)
                    bar = "█" * bar_len + "░" * (80 - bar_len)
                    lines.append(f"│ [{Fore.GREEN}{bar}{Style.RESET_ALL}] {progress}%")
                lines.extend([Fore.MAGENTA + "└" + "─" * (self.terminal_width - 2) + "┘" + Style.RESET_ALL, ""])
                lines.append(Fore.RED + "┌─ SYSTEM ACCESS " + "─" * (self.terminal_width - 20) + "┐" + Style.RESET_ALL)
                statuses = ["ATTEMPTING", "BYPASSING", "CRACKING", "ACCESSING"]
                for i in range(2):
                    status = random.choice(statuses)
                    target = random.choice(["firewall", "database", "mainframe", "server"])
                    lines.append(f"│ {status} {target}...")
                lines.extend([Fore.RED + "└" + "─" * (self.terminal_width - 2) + "┘" + Style.RESET_ALL, ""])
                lines.append(Fore.GREEN + f"STATUS: {'▓' * random.randint(10, 50)} BREACHING MAINFRAME..." + Style.RESET_ALL)
                sys.stdout.write(CURSOR_HOME)
                sys.stdout.write("\n".join(lines) + "\n")
                sys.stdout.flush()
                iteration += 1
                time.sleep(0.3)
        except KeyboardInterrupt:
            pass
        finally:
            sys.stdout.write(CURSOR_SHOW)
            sys.stdout.flush()
        print("\n" + Fore.RED + "OPERATION TERMINATED" + Style.RESET_ALL + "\n")

    def reboot(self, args):
        """Reboot the guest OS (Star PY OS) only. Host is not touched."""
        print(Fore.YELLOW + "Broadcast message from root@Star-PY-OS (tty1):" + Style.RESET_ALL)
        print(Fore.YELLOW + "  The system is going down for reboot NOW!" + Style.RESET_ALL)
        print()
        for msg in [
            "Stopping cron daemon...",
            "Stopping network manager...",
            "Unmounting /home...",
            "Unmounting /var...",
            "Unmounting /usr...",
            "Sending SIGTERM to all processes...",
            "Rebooting...",
        ]:
            print(Fore.CYAN + " [ OK ] " + Style.RESET_ALL + msg)
            time.sleep(0.12)
        time.sleep(0.3)
        # Restore guest OS state and show boot again (host unchanged)
        self.filesystem, self.files = self._get_initial_state()
        self.current_dir = "/home/user"
        self.is_root = False
        self.installed_packages = ["python", "nano", "vim", "htop", "btop", "cowsay", "fastfetch", "lynx", "cmatrix", "cava"]
        self._clear_screen()
        self.boot_screen()

    def shutdown(self, args):
        """Shut down the guest OS (exit Star PY OS). Host is not touched."""
        print(Fore.YELLOW + "Broadcast message from root@Star-PY-OS:" + Style.RESET_ALL)
        print(Fore.YELLOW + "  The system is going down for halt NOW!" + Style.RESET_ALL)
        print()
        for msg in [
            "Stopping user sessions...",
            "Stopping display manager...",
            "Stopping dbus...",
            "Unmounting filesystems...",
            "Deactivating swap...",
            "Saving system state...",
            "Power down.",
        ]:
            print(Fore.CYAN + " [ OK ] " + Style.RESET_ALL + msg)
            time.sleep(0.15)
        time.sleep(0.3)
        print(Fore.RED + "System halted." + Style.RESET_ALL)
        print(Fore.CYAN + "Star PY OS (guest) has shut down. Goodbye!" + Style.RESET_ALL)
        print()

    def format_drive(self, args):
        """Format the virtual drive (guest OS only). Restores filesystem to default. Usage: format [drive]"""
        drive = args[0] if args else "/dev/sda1"
        print(Fore.YELLOW + f"Formatting virtual drive {drive} (guest OS only)..." + Style.RESET_ALL)
        for pct in range(0, 101, 10):
            bar_len = int(pct * 0.5)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            print(f"\r{Fore.CYAN}[{bar}] {pct}%{Style.RESET_ALL}", end="")
            sys.stdout.flush()
            time.sleep(0.08)
        print()
        self.filesystem, self.files = self._get_initial_state()
        self.current_dir = "/home/user"
        print(Fore.GREEN + "Format complete. Virtual drive restored to default state." + Style.RESET_ALL)
        print()

    def reset(self, args):
        """Factory reset the guest OS. Restores filesystem, packages, and state. Host unchanged."""
        print(Fore.YELLOW + "Resetting Star PY OS (guest) to factory state..." + Style.RESET_ALL)
        for pct in range(0, 101, 12):
            bar_len = int(pct * 0.5)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            print(f"\r{Fore.CYAN}[{bar}] {pct}%{Style.RESET_ALL}", end="")
            sys.stdout.flush()
            time.sleep(0.1)
        print()
        self.filesystem, self.files = self._get_initial_state()
        self.current_dir = "/home/user"
        self.is_root = False
        self.installed_packages = ["python", "nano", "vim", "htop", "btop", "cowsay", "fastfetch", "lynx", "cmatrix", "cava"]
        print(Fore.GREEN + "System reset to factory state." + Style.RESET_ALL)
        print()

    def help(self, args):
        print(Fore.MAGENTA + "═" * self.terminal_width + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT + "STAR PY OS - Available Commands".center(self.terminal_width) + Style.RESET_ALL)
        print(Fore.MAGENTA + "═" * self.terminal_width + Style.RESET_ALL)
        print()
        cmds = [
            ("FILE MANAGEMENT", [
                ("ls", "List directory contents"),
                ("cd", "Change directory"),
                ("pwd", "Print working directory"),
                ("mkdir", "Make directory"),
                ("rm", "Remove file/directory"),
                ("touch", "Create empty file"),
                ("cat", "View file contents"),
                ("echo", "Print text (use > or >> to redirect)"),
                ("mv", "Move/rename file"),
                ("tree", "Display directory tree"),
                ("mc", "Midnight Commander file manager (enhanced)"),
            ]),
            ("TEXT EDITORS", [
                ("nano", "Edit file with nano"),
                ("vim", "Edit file with vim"),
            ]),
            ("SYSTEM INFO & MONITORING", [
                ("fastfetch", "Display system info"),
                ("htop", "Interactive process viewer"),
                ("btop", "Advanced resource monitor"),
                ("whoami", "Print current user"),
                ("id", "Print user ID info"),
            ]),
            ("NETWORK & WEB", [
                ("lynx", "Text-based web browser (functional!)"),
            ]),
            ("PACKAGE MANAGEMENT", [
                ("pkg", "Package manager (install/remove/search)"),
                ("sudo", "Execute command as root"),
            ]),
            ("FUN & ANIMATIONS", [
                ("nyancat", "Nyan cat animation"),
                ("cowsay", "Make cow say something"),
                ("hollywood", "Hollywood hacker mode"),
                ("cmatrix", "Matrix screensaver"),
                ("cava", "Console audio visualizer"),
                ("beep", "Make a beep sound (beep <ms> <hz>)"),
            ]),
            ("PRANK TOOLS (Educational Only!)", [
                ("virus", "Basic virus generator (PRANK)"),
                ("trojan", "Trojan simulator (LONG PAYLOAD)"),
                ("ransomware", "Ransomware simulator (CODE IN FILENAME)"),
            ]),
            ("SYSTEM (Guest OS only)", [
                ("reboot", "Reboot Star PY OS (guest only); shows boot screen again"),
                ("shutdown", "Shut down guest OS and exit (host unchanged)"),
                ("format", "Format virtual drive; restore filesystem to default (format [drive])"),
                ("reset", "Factory reset guest OS (filesystem, packages, state)"),
            ]),
            ("OTHER", [
                ("clear", "Clear screen"),
                ("help", "Show this help"),
                ("exit", "Exit shell"),
            ]),
        ]
        for category, commands in cmds:
            print(Fore.YELLOW + Style.BRIGHT + category + ":" + Style.RESET_ALL)
            for cmd, desc in commands:
                print(f"  {Fore.GREEN}{cmd:15}{Style.RESET_ALL} - {desc}")
            print()

    def run(self):
        self.boot_screen()
        while True:
            try:
                cmd_input = input(self.get_prompt())
                if not cmd_input.strip():
                    continue
                parts = cmd_input.split()
                cmd = parts[0]
                args = parts[1:]
                if cmd == "exit":
                    print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
                    break
                elif cmd == "ls":
                    self.ls(args)
                elif cmd == "cd":
                    self.cd(args)
                elif cmd == "pwd":
                    self.pwd(args)
                elif cmd == "mkdir":
                    self.mkdir(args)
                elif cmd == "rm":
                    self.rm(args)
                elif cmd == "touch":
                    self.touch(args)
                elif cmd == "cat":
                    self.cat(args)
                elif cmd == "echo":
                    self.echo(args)
                elif cmd == "mv":
                    self.mv(args)
                elif cmd == "clear":
                    self.clear(args)
                elif cmd == "tree":
                    self.tree(args)
                elif cmd == "whoami":
                    self.whoami(args)
                elif cmd == "id":
                    self.id(args)
                elif cmd == "sudo":
                    self.sudo(args)
                elif cmd == "beep":
                    self.beep(args)
                elif cmd == "nano":
                    self.nano(args)
                elif cmd == "pkg":
                    self.pkg(args)
                elif cmd == "virus":
                    self.virus(args)
                elif cmd == "trojan":
                    self.trojan(args)
                elif cmd == "ransomware":
                    self.ransomware(args)
                elif cmd == "lynx":
                    self.lynx(args)
                elif cmd == "cmatrix":
                    self.cmatrix(args)
                elif cmd == "cava":
                    self.cava(args)
                elif cmd == "fastfetch":
                    self.fastfetch(args)
                elif cmd == "nyancat":
                    self.nyancat(args)
                elif cmd == "vim":
                    self.vim(args)
                elif cmd == "htop":
                    self.htop(args)
                elif cmd == "btop":
                    self.btop(args)
                elif cmd == "cowsay":
                    self.cowsay(args)
                elif cmd == "hollywood":
                    self.hollywood(args)
                elif cmd == "mc":
                    self.mc(args)
                elif cmd == "reboot":
                    self.reboot(args)
                elif cmd == "shutdown":
                    self.shutdown(args)
                    return  # Exit guest OS (end run loop)
                elif cmd == "format" or cmd == "format-drive":
                    self.format_drive(args)
                elif cmd == "reset":
                    self.reset(args)
                elif cmd == "help":
                    self.help(args)
                else:
                    print(f"{cmd}: command not found")
            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                print()
                break

if __name__ == "__main__":
    shell = SimpleShell()
    shell.run()
