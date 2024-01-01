from realdebridmanager.database import database
from realdebridmanager.rd.RealDebrid import RealDebrid


def check_blackhole_task(debrid_client, task):
    new_torrent_info = debrid_client.get_torrent_info(task['id'])
    if new_torrent_info['status'] == "waiting_files_selection":
        debrid_client.select_files(task['id'], ["all"])
        new_torrent_info = debrid_client.get_torrent_info(task['id'])
    if new_torrent_info['status'] == "downloaded":
        database.update_task(task['id'], 'rdstatus', new_torrent_info['status'])
        database.update_task(task['id'], 'rdprogressdownload', new_torrent_info['progress'])
        if new_torrent_info['progress'] == 100:
            database.update_task(task['id'], 'completed', 1)
    if new_torrent_info['status'] in ("magnet_error", "error", "magnet_conversion", "virus", "dead"):
        database.update_task(task['id'], 'rderror', 1)
        database.update_task(task['id'], 'completed', 1)

def check_tasks_for_completion():
    tasks = database.get_tasks()
    settings = database.get_all_settings()
    debrid_api_key = settings.get('rdapikey', None)
    if debrid_api_key is None:
        print("No RD API Key set, skipping task check")
        return
    debrid_client = RealDebrid(api_token=debrid_api_key)
    incomplete_tasks = [t for t in tasks if t['completed'] == '0']
    for task in incomplete_tasks:
        if task['task_type'] == 'blackhole':
            check_blackhole_task(debrid_client, task)
