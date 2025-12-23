#!/usr/bin/env python3
import os
import glob
import json
from datetime import datetime
from collections import defaultdict

class LeetCodeStats:
    def __init__(self):
        self.total_solutions = 0
        self.categories = defaultdict(int)
        self.all_files = []
        
    def scan_repository(self):
        """Scan for all C++ solution files"""
        # Get all .cpp files
        cpp_files = glob.glob("**/*.cpp", recursive=True)
        self.total_solutions = len(cpp_files)
        self.all_files = cpp_files
        
        # Categorize by folder
        for file_path in cpp_files:
            folder = os.path.dirname(file_path)
            if folder:
                self.categories[folder] += 1
            else:
                self.categories["root"] += 1
        
        return self
    
    def generate_stars(self):
        """Generate star visualization"""
        stars_count = min(self.total_solutions // 10, 20)
        return "⭐" * stars_count + f" ({self.total_solutions})"
    
    def generate_structure(self):
        """Generate folder structure tree"""
        structure_lines = []
        
        def build_tree(path, prefix=""):
            items = []
            try:
                items = os.listdir(path)
            except:
                return
            
            items = [i for i in items if not i.startswith('.')]
            items.sort()
            
            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last = (i == len(items) - 1)
                
                if os.path.isdir(item_path):
                    structure_lines.append(f"{prefix}{'└── ' if is_last else '├── '}📂 {item}/")
                    build_tree(item_path, prefix + ("    " if is_last else "│   "))
                elif item.endswith('.cpp'):
                    structure_lines.append(f"{prefix}{'└── ' if is_last else '├── '}📄 {item}")
        
        structure_lines.append("LeetCode-CPP/")
        build_tree(".")
        return "\n".join(structure_lines)
    
    def generate_file_list(self):
        """Generate detailed file list"""
        file_lines = []
        for file_path in sorted(self.all_files):
            size = os.path.getsize(file_path)
            modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
            file_lines.append(f"{file_path:<40} | {size:>6} bytes | {modified}")
        
        return "\n".join(file_lines) if file_lines else "No .cpp files found"
    
    def generate_progress_bars(self):
        """Generate progress bars for categories"""
        bars = {}
        targets = {
            "Arrays": 80, "Strings": 60, "Dynamic_Programming": 70,
            "Trees": 50, "Graphs": 40, "Backtracking": 30
        }
        
        for category, target in targets.items():
            count = self.categories.get(category, 0)
            percent = min(int((count / target) * 100), 100)
            bar = "█" * (percent // 5) + "░" * (20 - (percent // 5))
            bars[category] = {
                "count": count,
                "bar": bar,
                "percent": percent
            }
        
        return bars
    
    def update_readme(self):
        """Update README.md with current stats"""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace placeholders
        replacements = {
            "<TOTAL>": str(self.total_solutions),
            "<SOLUTION_STARS>": self.generate_stars(),
            "<FOLDER_STRUCTURE>": self.generate_structure(),
            "<FILE_LIST>": self.generate_file_list(),
            "<STREAK>": self.calculate_streak(),
        }
        
        # Add category counts
        bars = self.generate_progress_bars()
        for category, data in bars.items():
            key = f"<{category.upper()}_COUNT>"
            if key in content:
                content = content.replace(key, str(data["count"]))
            key = f"<{category.upper()}_PROGRESS>"
            if key in content:
                content = content.replace(key, f"{data['bar']} {data['percent']}%")
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Update last commit badge
        last_commit = datetime.now().strftime("%Y-%m-%d")
        content = content.replace("<LAST_COMMIT>", last_commit)
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Updated! Total solutions: {self.total_solutions}")
        print("📊 Category breakdown:")
        for cat, count in sorted(self.categories.items()):
            if cat != "root":
                print(f"   {cat}: {count}")
    
    def calculate_streak(self):
        """Calculate coding streak from git commits"""
        try:
            # Try to get commit history
            import subprocess
            result = subprocess.run(
                ["git", "log", "--oneline", "--format=%cd", "--date=short"],
                capture_output=True, text=True
            )
            dates = result.stdout.strip().split('\n')
            
            if dates:
                unique_dates = set(dates)
                return str(len(unique_dates))
        except:
            pass
        
        return "7"  # Default value

def main():
    print("📡 Scanning repository for LeetCode solutions...")
    stats = LeetCodeStats().scan_repository()
    stats.update_readme()
    print("🎉 README updated successfully!")

if __name__ == "__main__":
    main()
