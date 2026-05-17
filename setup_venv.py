#!/usr/bin/env python3
"""
AFRO Hacker - Virtual Environment Setup Script
Run this ONCE to create venv and install dependencies
Usage: python setup_venv.py

This script:
1. Creates a Python virtual environment
2. Installs all required dependencies
3. Creates a launcher script for easy startup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class VenvSetup:
    """Virtual environment setup manager"""

    def __init__(self):
        self.venv_dir = Path("venv")
        self.platform = platform.system()
        self.python_exe = sys.executable

    def print_header(self):
        """Print setup header"""
        print("\n" + "=" * 70)
        print("AFRO HACKER - VIRTUAL ENVIRONMENT SETUP")
        print("=" * 70)
        print(f"Python: {sys.version}")
        print(f"Platform: {self.platform}")
        print(f"Working Directory: {os.getcwd()}")
        print("=" * 70 + "\n")

    def print_status(self, message: str, icon: str = "ℹ"):
        """Print status message"""
        print(f"{icon} {message}")

    def check_venv_exists(self) -> bool:
        """Check if venv already exists"""
        return self.venv_dir.exists() and (self.venv_dir / "bin").exists() or (self.venv_dir / "Scripts").exists()

    def create_venv(self) -> bool:
        """Create virtual environment"""
        self.print_status("Creating virtual environment...")
        try:
            subprocess.check_call([self.python_exe, "-m", "venv", str(self.venv_dir)])
            self.print_status("✓ Virtual environment created successfully", "✓")
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"✗ Failed to create venv: {e}", "✗")
            return False
        except Exception as e:
            self.print_status(f"✗ Error: {e}", "✗")
            return False

    def get_pip_executable(self) -> Path:
        """Get path to pip executable in venv"""
        if self.platform == "Windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"

    def get_python_executable(self) -> Path:
        """Get path to python executable in venv"""
        if self.platform == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"

    def install_requirements(self) -> bool:
        """Install requirements using pip"""
        self.print_status("Installing dependencies...")
        
        requirements = [
            "pillow>=11.3.0",
            "numpy>=2.3.3",
            "pyinstaller>=6.16.0"
        ]

        pip_exe = self.get_pip_executable()

        if not pip_exe.exists():
            self.print_status(f"✗ pip not found at {pip_exe}", "✗")
            return False

        try:
            # Upgrade pip first
            self.print_status("  Upgrading pip...")
            subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])

            # Install each requirement
            for req in requirements:
                self.print_status(f"  Installing {req}...")
                subprocess.check_call([str(pip_exe), "install", req])

            self.print_status("✓ All dependencies installed successfully", "✓")
            return True

        except subprocess.CalledProcessError as e:
            self.print_status(f"✗ Failed to install dependencies: {e}", "✗")
            return False
        except Exception as e:
            self.print_status(f"✗ Error: {e}", "✗")
            return False

    def create_launcher_scripts(self) -> bool:
        """Create launcher scripts for easy startup"""
        self.print_status("Creating launcher scripts...")

        python_exe = self.get_python_executable()

        try:
            if self.platform == "Windows":
                # Create Windows batch file
                launcher_path = Path("run.bat")
                batch_content = f"""@echo off
"{python_exe}" main.py
pause
"""
                with open(launcher_path, 'w') as f:
                    f.write(batch_content)
                self.print_status(f"✓ Created launcher: run.bat", "✓")

            else:
                # Create Unix shell script
                launcher_path = Path("run.sh")
                shell_content = f"""#!/bin/bash
"{python_exe}" main.py
"""
                with open(launcher_path, 'w') as f:
                    f.write(shell_content)
                
                # Make executable
                os.chmod(launcher_path, 0o755)
                self.print_status(f"✓ Created launcher: run.sh", "✓")

            return True

        except Exception as e:
            self.print_status(f"⚠ Failed to create launcher: {e}", "⚠")
            return False

    def create_requirements_txt(self) -> bool:
        """Create requirements.txt if it doesn't exist"""
        req_path = Path("requirements.txt")

        if req_path.exists():
            self.print_status("requirements.txt already exists")
            return True

        try:
            requirements_content = """pillow>=11.3.0
numpy>=2.3.3
pyinstaller>=6.16.0
"""
            with open(req_path, 'w') as f:
                f.write(requirements_content)
            self.print_status("✓ Created requirements.txt", "✓")
            return True
        except Exception as e:
            self.print_status(f"⚠ Failed to create requirements.txt: {e}", "⚠")
            return False

    def test_venv(self) -> bool:
        """Test virtual environment works"""
        self.print_status("Testing virtual environment...")

        python_exe = self.get_python_executable()

        try:
            # Try importing key modules
            result = subprocess.run(
                [str(python_exe), "-c", "import tkinter, PIL, numpy; print('All imports OK')"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                self.print_status("✓ Virtual environment test passed", "✓")
                return True
            else:
                self.print_status(f"⚠ Import test failed: {result.stderr}", "⚠")
                return False

        except subprocess.TimeoutExpired:
            self.print_status("⚠ Test timed out", "⚠")
            return False
        except Exception as e:
            self.print_status(f"⚠ Test failed: {e}", "⚠")
            return False

    def run_setup(self) -> bool:
        """Run complete setup"""
        self.print_header()

        # Check if already setup
        if self.check_venv_exists():
            self.print_status("Virtual environment already exists!")
            self.print_status("To reinstall, delete the 'venv' folder and run this script again.")
            return True

        # Step 1: Create venv
        if not self.create_venv():
            return False

        # Step 2: Create requirements file
        self.create_requirements_txt()

        # Step 3: Install requirements
        if not self.install_requirements():
            self.print_status("⚠ Continuing despite installation issues...", "⚠")

        # Step 4: Create launcher scripts
        self.create_launcher_scripts()

        # Step 5: Test venv
        self.test_venv()

        return True

    def print_final_instructions(self):
        """Print final setup instructions"""
        print("\n" + "=" * 70)
        print("SETUP COMPLETE!")
        print("=" * 70)

        if self.platform == "Windows":
            print("\nTo run the application:")
            print("  Double-click: run.bat")
            print("  OR")
            print("  Command line: python main.py")
        else:
            print("\nTo run the application:")
            print("  ./run.sh")
            print("  OR")
            print("  python main.py")

        print("\nNext steps:")
        print("  1. File → Open ROM")
        print("  2. Select a Pokemon Fire Red ROM (BPRE/BPGE)")
        print("  3. View → Map Editor to see the map")

        print("\nNotes:")
        print("  - Virtual environment is in the 'venv' folder (don't delete)")
        print("  - To reinstall dependencies, delete 'venv' and run setup_venv.py again")
        print("  - The app requires Pokemon Fire Red US (BPRE) or EU (BPGE) ROM")

        print("\n" + "=" * 70 + "\n")


def main():
    """Main entry point"""
    setup = VenvSetup()

    try:
        success = setup.run_setup()

        if success:
            setup.print_final_instructions()
            return 0
        else:
            print("\n✗ Setup failed. Please check the errors above.")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠ Setup cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())