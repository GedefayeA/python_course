# 📝 Task Manager CLI
A simple command-line task manager with priorities, deadlines, and CSV export.
## 🚀 Quick Start
# Add a task
python cli_task_manager.py add "Finish Python course" high 2026-04-20
# List all tasks
python cli_task_manager.py list
# Complete a task
python cli_task_manager.py complete 1
# Delete a task
python cli_task_manager.py delete 1
# Export to CSV
python cli_task_manager.py export
**📋 Commands**
**Command**                               **Description**
add "task" [priority] [deadline optional]         	Add new task
list	                                    Show all tasks
complete <id>	                            Mark task as done
delete <id>	                              Remove task
export	                                  Export to CSV
