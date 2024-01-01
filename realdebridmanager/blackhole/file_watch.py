import os.path
import time

from realdebridmanager.database import database
from realdebridmanager.rd.RealDebrid import RealDebrid


def move_processed(file, dest_folder):
    head, tail = os.path.split(file)
    new_location = (head + "/" + dest_folder + "/" + tail)
    os.rename(file, new_location)


def post_process_torrent(debrid_client, torrent_id, file):
    new_torrent_info = debrid_client.get_torrent_info(torrent_id)
    if new_torrent_info['status'] == "waiting_files_selection":
        debrid_client.select_files(torrent_id, ["all"])
        new_torrent_info = debrid_client.get_torrent_info(torrent_id)
    if new_torrent_info['status'] in ("downloaded", "magnet_conversion"):
        database.add_task(new_torrent_info['id'],
                          'blackhole',
                          new_torrent_info['filename'],
                          new_torrent_info['status'],
                          new_torrent_info['progress'], attempts=1, rderror=0, completed=1)
        move_processed(file, "processed")
    elif new_torrent_info['status'] in ("magnet_error", "error", "virus", "dead"):
        database.add_task(new_torrent_info['id'],
                          'blackhole',
                          new_torrent_info['filename'],
                          new_torrent_info['status'],
                          new_torrent_info['progress'], attempts=1, rderror=1, completed=1)
        move_processed(file, "errored")
    else:
        database.add_task(new_torrent_info['id'],
                          'blackhole',
                          new_torrent_info['filename'],
                          new_torrent_info['status'],
                          new_torrent_info['progress'], attempts=1, rderror=0, completed=0)
        move_processed(file, "processed")


def process_torrent_file(file):
    print("Found torrent file: " + file)
    debrid_api_key = database.get_all_settings().get('rdapikey', None)
    debrid_client = RealDebrid(api_token=debrid_api_key)
    with open(file, 'rb') as finput:
        new_torrent = debrid_client.add_torrent(finput.read())
    time.sleep(2)
    post_process_torrent(debrid_client, new_torrent['id'], file)


def process_magnet_file(file):
    print("Found magnet file: " + file)
    debrid_api_key = database.get_all_settings().get('rdapikey', None)
    debrid_client = RealDebrid(api_token=debrid_api_key)
    with open(file, 'rb') as finput:
        new_torrent = debrid_client.add_torrent_magnet(finput.read())
    time.sleep(2)
    post_process_torrent(debrid_client, new_torrent['id'], file)


def watch_blackhole_folder():
    settings = database.get_all_settings()
    watch_path = settings.get('watchpath', None)
    path_exists = watch_path is not None and os.path.exists(watch_path)
    debrid_api_key = settings.get('rdapikey', None)
    if path_exists and debrid_api_key is not None:
        for file in os.listdir(watch_path):
            if file.endswith(".torrent"):
                process_torrent_file(os.path.join(watch_path, file))
            if file.endswith(".magnet"):
                process_magnet_file(os.path.join(watch_path, file))
    elif not path_exists:
        print(f"Watch path {watch_path} does not exist")
    elif debrid_api_key is None:
        print("Real Debrid API key is not set")
