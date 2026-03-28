import json, sys, os, csv
from datetime import datetime
# json → used to export tasks into JSON format
# sys → used to read command-line arguments
# os → checks if file exists
# csv → export tasks to CSV
# datetime → handle dates (created time, deadline)
    #Class Definition
    # This class manages all task operations
class Task:
    def __init__(self):
        self.f = "MyTasks.txt"
        self.MyTasks = self.load_tasks()

    def load_tasks(self): # Function to read tasks from text file
        """Load tasks from plain text file"""
        tasks = []
        if os.path.exists(self.f): # Check if file exists
            try:
                with open(self.f, "r") as file:
                    for line in file:
                        if line.strip():
                            # Parse each line: id|description|priority|created|deadline|completed
                            parts = line.strip().split("|")
                            if len(parts) == 6:
                                tasks.append({
                                    "id": int(parts[0]),
                                    "description": parts[1],
                                    "priority": parts[2],
                                    "created": parts[3],
                                    "deadline": parts[4] if parts[4] != "None" else None,
                                    "completed": parts[5] == "True"
                                })
            except:
                pass
        return tasks

    def save(self):
        """Save tasks to plain text file"""
        with open(self.f, "w") as file:
            for t in self.MyTasks:
                # Format: id|description|priority|created|deadline|completed
                line = f"{t['id']}|{t['description']}|{t['priority']}|{t['created']}|{t.get('deadline', 'None')}|{t['completed']}\n"
                file.write(line)

    def add(self, d, p="medium", dl=None):
        try: 
            dl = datetime.strptime(dl, "%Y-%m-%d").date() if dl else None
        except: 
            dl = None
        
        new_id = max([t["id"] for t in self.MyTasks], default=0) + 1
        
        self.MyTasks.append({
            "id": new_id,
            "description": d, 
            "priority": p, 
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": str(dl) if dl else None, 
            "completed": False           
        })
        self.save()
        print(f"✓ Added: {d} (Created: {datetime.now().strftime('%Y-%m-%d %H:%M')})")

    def show(self):
        if not self.MyTasks:
            print("No tasks found")
            return
        
        print("\n📋 MY TASKS:")
        print("-" * 70)
        for t in self.MyTasks:
            status = '✓' if t['completed'] else '○'
            prio_icon = {"high":"🔴","medium":"🟡","low":"🟢"}.get(t['priority'], "⚪")
            created = t.get('created', 'N/A')[:16]
            deadline = f" | Due: {t['deadline']}" if t.get('deadline') else ""
            print(f"{status} {prio_icon} [{t['id']}] {t['description']} (Created: {created}){deadline}")
        print("-" * 70)

    def completed(self, i):
        for t in self.MyTasks:
            if t["id"] == i:
                t["completed"] = True
                self.save()
                print(f"✓ Task {i} completed at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                return
        print("❌ Task not found")

    def delete(self, i):
        self.MyTasks = [t for t in self.MyTasks if t["id"] != i]
        # Reindex IDs
        for idx, task in enumerate(self.MyTasks, 1):
            task["id"] = idx
        self.save()
        print(f"🗑️ Task {i} deleted")

    def export_json(self):
        """Export tasks to JSON file"""
        if not self.MyTasks:
            print("No tasks to export")
            return
        filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.MyTasks, f, indent=2)
        print(f"📁 Exported {len(self.MyTasks)} tasks to {filename}")

    def export_csv(self):
        """Export tasks to CSV file"""
        if not self.MyTasks:
            print("No tasks to export")
            return
        filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as f:
            # Use dictionary keys as headers
            w = csv.DictWriter(f, fieldnames=self.MyTasks[0].keys())
            w.writeheader()
            w.writerows(self.MyTasks)
        print(f"📁 Exported {len(self.MyTasks)} tasks to {filename}")

    def export(self, format="csv"):
        """Main export method - supports csv or json"""
        if format.lower() == "json":
            self.export_json()
        elif format.lower() == "csv":
            self.export_csv()
        else:
            print("❌ Invalid format. Use 'csv' or 'json'")

# -------- CLI --------
t = Task() # Create object
c = sys.argv[1] if len(sys.argv)>1 else "" # Read command

if c=="add": 
    t.add(sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "medium", sys.argv[4] if len(sys.argv)>4 else None)
elif c=="list": 
    t.show()
elif c=="completed": 
    t.completed(int(sys.argv[2]))
elif c=="delete": 
    t.delete(int(sys.argv[2]))
elif c=="export":
    format_type = sys.argv[2] if len(sys.argv)>2 else "csv"
    t.export(format_type)
else:  # Show help menu
    print("Help Commands:")
    print("  add 'task' [priority] [deadline]  - Add new task")
    print("  list                              - Show all tasks")
    print("  completed <id>                    - Mark task as done")
    print("  delete <id>                       - Remove task")
    print("  export [csv|json]                 - Export tasks (default: csv)")