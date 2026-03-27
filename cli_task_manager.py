import json, sys, os, csv
from datetime import datetime

class Task:
    def __init__(self):
        self.f = "MyTasks.json"
        self.MyTasks = json.load(open(self.f)) if os.path.exists(self.f) else []

    def save(self):
        json.dump(self.MyTasks, open(self.f, "w"), indent=2)

    def add(self, d, p="medium", dl=None):
        try: 
            dl = datetime.strptime(dl, "%Y-%m-%d").date() if dl else None
        except: 
            dl = None
        
        self.MyTasks.append({
            "id": max([t["id"] for t in self.MyTasks], default=0)+1,
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

    def export(self):
        if not self.MyTasks:
            print("No tasks to export")
            return
        with open("MyTasks.csv","w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=self.MyTasks[0].keys())
            w.writeheader()
            w.writerows(self.MyTasks)
        print(f"📁 Exported {len(self.MyTasks)} tasks to MyTasks.csv")

# -------- CLI --------
t = Task()
c = sys.argv[1] if len(sys.argv)>1 else ""

if c=="add": 
    t.add(sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "medium", sys.argv[4] if len(sys.argv)>4 else None)
elif c=="list": 
    t.show()
elif c=="completed": 
    t.completed(int(sys.argv[2]))
elif c=="delete": 
    t.delete(int(sys.argv[2]))
elif c=="export": 
    t.export()
else: 
    print("Commands: add 'task' [priority] [deadline] | list | completed <id> | delete <id> | export")