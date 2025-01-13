import obspython as S
import threading
import time
import keyboard

is_holding = False
processing = False
source_not_found_logged = False

def set_visibility(visible):
    global source_not_found_logged
    if not text_MapImage.txt.strip():
        S.script_log(S.LOG_WARNING, "Source name is empty. Skipping visibility change.")
        return
    current_scene_source = S.obs_frontend_get_current_scene()
    if not current_scene_source:
        S.script_log(S.LOG_WARNING, "No current scene found.")
        return
    current_scene = S.obs_scene_from_source(current_scene_source)
    if not current_scene:
        S.script_log(S.LOG_WARNING, "Unable to retrieve the current scene.")
        S.obs_source_release(current_scene_source)
        return
    scene_item = S.obs_scene_find_source(current_scene, text_MapImage.txt)
    if scene_item:
        S.obs_sceneitem_set_visible(scene_item, visible)
        S.script_log(S.LOG_INFO, f"Source '{text_MapImage.txt}' visibility set to: {visible}")
        source_not_found_logged = False
    else:
        if not source_not_found_logged:
            S.script_log(S.LOG_WARNING, f"Source '{text_MapImage.txt}' not found in the scene.")
            source_not_found_logged = True
    S.obs_source_release(current_scene_source)

def send_f16():
    try:
        keyboard.send('f16')
        S.script_log(S.LOG_INFO, "Simulated pressing F16 successfully.")
    except Exception as e:
        S.script_log(S.LOG_ERROR, f"Error simulating F16: {e}")

def handle_keypress():
    global is_holding, processing
    while True:
        if keyboard.is_pressed('g'):
            if not is_holding and not processing:
                is_holding = True
                processing = True
                S.script_log(S.LOG_INFO, "G key pressed. Showing source.")
                set_visibility(True)
        else:
            if is_holding:
                is_holding = False
                S.script_log(S.LOG_INFO, "G key released. Waiting 1 second before hiding.")
                time.sleep(1)
                set_visibility(False)
                send_f16()
                processing = False
        time.sleep(0.01)

text_MapImage = type("text", (object,), {"txt": ""})()

def script_description():
    return (
        "Just made a simplified version of the OG Rust Hide Map Script.\n"
        "Add the image source name below.\n"
        "Script by Ōzen_VR."
    )

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_text(props, "rust_map_source_name", "Source Name:", S.OBS_TEXT_DEFAULT)
    return props

def script_update(settings):
    text_MapImage.txt = S.obs_data_get_string(settings, "rust_map_source_name")
    S.script_log(S.LOG_INFO, f"Updated settings: source_name={text_MapImage.txt}")

def script_load(settings):
    threading.Thread(target=handle_keypress, daemon=True).start()
    script_update(settings)
    S.script_log(S.LOG_INFO, "Script loaded successfully.")
    S.script_log(S.LOG_INFO, "Script by Ōzen_VR.")
