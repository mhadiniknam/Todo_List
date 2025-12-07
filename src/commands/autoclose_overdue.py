# (Imports and other functions in this file remain the same)
import threading
import time
import schedule
import datetime
from db.session import get_db_session
from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from services.task_service import TaskService

_shutdown_event = threading.Event()

def _overdue_check_job():
    """The self-contained job to check for overdue tasks."""
    # This function is correct and does not need to change.
    print("\n[Scheduler]: Running background check for overdue tasks...")
    with get_db_session() as db:
        try:
            task_repo = TaskRepository(db)
            project_repo = ProjectRepository(db)
            task_service = TaskService(task_repo, project_repo)
            
            closed_tasks = task_service.close_all_overdue_tasks()
            
            if closed_tasks:
                print(f"[Scheduler]: ✅ Closed {len(closed_tasks)} overdue task(s). (Type a command to refresh prompt)")
            else:
                print("[Scheduler]: No overdue tasks found. (Type a command to refresh prompt)")
        except Exception as e:
            print(f"\n[Scheduler]: ❌ Error during background check: {e}")

def _run_scheduler_loop():
    """
    This function runs in a separate thread. It executes pending jobs
    in a loop until the دshutdown event is set.
    این عملا لوپی هست که ترد ما تمام اسکریپت های رانش رو اینجا قرار میدیم
    """
    # --- Configure the schedule ---
    schedule.every().minute.do(_overdue_check_job)
    
    print("[Scheduler]: Performing initial startup check for overdue tasks...")
    _overdue_check_job()
    
    try:
        if schedule.jobs:
            next_run_time = schedule.jobs[0].next_run
            print(f"[Scheduler]: Initial check complete. Next check at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}.")
        else:
            print("[Scheduler]: Initial check complete. No further jobs are scheduled.")
    except Exception as e:
        print(f"[Scheduler]: Could not determine next run time. Error: {e}")

    while not _shutdown_event.is_set():
        schedule.run_pending()
        time.sleep(60)
    
    print("\n[Scheduler]: Background scheduler has been shut down.")

def start_background_scheduler():
    """Starts the scheduler loop in a new background daemon thread."""
    scheduler_thread = threading.Thread(target=_run_scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("[Scheduler]: Background thread for checking tasks has started.")
    return scheduler_thread

def stop_background_scheduler():
    """Signals the background scheduler thread to shut down."""
    print("\n[Scheduler]: Signaling background thread to shut down...")
    _shutdown_event.set()
