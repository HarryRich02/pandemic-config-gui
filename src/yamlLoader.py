import yaml
import traceback
from collections import defaultdict
from PyQt5 import QtWidgets, QtCore


def log(message):
    print(f"[JUNEbug] {message}", flush=True)


def load_config(file_path, config_panel, graph_widget):
    log(f"Loading configuration from: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        log(f"Error opening YAML file: {e}")
        return

    disease = data.get("disease", {})
    if not disease:
        log("Error: YAML file does not contain a 'disease' section.")
        return

    # 1. Update Config Panel
    try:
        _update_config_panel(config_panel, disease)
    except Exception as e:
        log(f"Error updating config panel: {e}")

    # 2. Update Node Graph
    try:
        _update_graph(graph_widget, disease)
        log("Graph updated and layout complete.")
    except Exception as e:
        log(f"Critical error updating graph: {e}")
        traceback.print_exc()


def _update_config_panel(panel, disease):
    panel.name_entry.setText(disease.get("name", ""))

    settings = disease.get("settings", {})
    if "default_lowest_stage" in settings:
        panel.dls_combo.setCurrentText(settings["default_lowest_stage"])
    if "max_mild_symptom_tag" in settings:
        panel.mmst_combo.setCurrentText(settings["max_mild_symptom_tag"])

    trans = disease.get("transmission", {})
    if "type" in trans:
        panel.trans_type_combo.setCurrentText(trans["type"])

    for key, editor in panel.trans_editors.items():
        if key in trans:
            dist_data = trans[key]
            dist_type = dist_data.get("type", "constant")
            editor.type_combo.setCurrentText(dist_type)
            for param, value in dist_data.items():
                if param == "type":
                    continue
                if param in editor.inputs:
                    editor.inputs[param].setText(str(value))


def _update_graph(graph_widget, disease):
    graph = graph_widget.graph
    graph.clear_session()

    symptom_tags = disease.get("symptom_tags", [])
    tag_name_to_value = {t["name"]: t["value"] for t in symptom_tags}
    trajectories = disease.get("trajectories", [])

    is_source = set()
    is_target = set()
    all_active_tags = set()

    for traj in trajectories:
        stages = traj.get("stages", [])
        for i, stage in enumerate(stages):
            tag = stage.get("symptom_tag")
            all_active_tags.add(tag)
            if i < len(stages) - 1:
                is_source.add(tag)
            if i > 0:
                is_target.add(tag)

    nodes_cache = {}

    for tag in all_active_tags:
        if tag in is_source and tag in is_target:
            node_type = "symptoms.TransitionNode"
        elif tag in is_source:
            node_type = "symptoms.DefaultLowestStage"
        else:
            node_type = "symptoms.TerminalStage"

        node = graph.create_node(node_type, push_undo=False)
        node.set_name(tag)

        numeric_val = tag_name_to_value.get(tag, 0)
        try:
            node.set_property("tag", str(numeric_val), push_undo=False)
        except Exception:
            pass

        nodes_cache[tag] = node

    time_nodes_cache = defaultdict(list)

    for t_idx, traj in enumerate(trajectories):
        stages = traj.get("stages", [])
        previous_node = None
        trajectory_tag_counts = defaultdict(int)

        for i, stage in enumerate(stages):
            tag = stage.get("symptom_tag")

            trajectory_tag_counts[tag] += 1
            count = trajectory_tag_counts[tag]

            if count == 1:
                current_node = nodes_cache.get(tag)
            else:
                if i < len(stages) - 1:
                    node_type = "symptoms.TransitionNode"
                else:
                    node_type = "symptoms.TerminalStage"

                current_node = graph.create_node(node_type, push_undo=False)
                new_name = f"{tag} {count}"
                current_node.set_name(new_name)

                numeric_val = tag_name_to_value.get(tag, 0)
                try:
                    current_node.set_property("tag", str(numeric_val), push_undo=False)
                except:
                    pass
                current_node.set_color(40, 150, 250)

            if not current_node:
                previous_node = None
                continue

            if previous_node:
                prev_name = previous_node.name()
                curr_name = current_node.name()

                prev_stage_data = stages[i - 1]
                comp_data = prev_stage_data.get("completion_time", {})

                cache_key = (prev_name, curr_name)

                existing_time_node = None
                candidates = time_nodes_cache[cache_key]

                for node_obj, original_data in candidates:
                    if _is_data_equal(comp_data, original_data):
                        existing_time_node = node_obj
                        break

                if existing_time_node:
                    pass
                else:
                    time_node = _create_time_node(graph_widget, comp_data)
                    time_node.set_name(f"{prev_name} -> {curr_name}")

                    time_nodes_cache[cache_key].append((time_node, comp_data))

                    try:
                        previous_node.output(0).connect_to(
                            time_node.input(0), push_undo=False
                        )
                        time_node.output(0).connect_to(
                            current_node.input(0), push_undo=False
                        )
                    except Exception:
                        pass

                QtWidgets.QApplication.processEvents()

            previous_node = current_node

    try:
        graph.auto_layout_nodes()
    except Exception as e:
        log(f"Auto-Layout failed: {e}")

    graph.viewer().update()

    # 4. FINAL VISIBILITY REFRESH
    # Call a helper that iterates ALL nodes and updates visibility.
    # Delay by 200ms to ensure graph is fully settled.
    QtCore.QTimer.singleShot(200, lambda: _finalize_visibility(graph_widget))


def _finalize_visibility(graph_widget):
    log("Running final visibility refresh...")
    graph = graph_widget.graph
    for node in graph.all_nodes():
        if node.type_ == "transitions.UniversalTimeNode":
            if hasattr(graph_widget, "update_node_visibility"):
                graph_widget.update_node_visibility(node)


def _create_time_node(graph_widget, comp_data):
    graph = graph_widget.graph
    node = graph.create_node("transitions.UniversalTimeNode", push_undo=False)

    dist_type = comp_data.get("type", "constant")
    if dist_type not in [
        "constant",
        "normal",
        "lognormal",
        "beta",
        "gamma",
        "exponweib",
    ]:
        dist_type = "constant"
    node.set_property("type", dist_type, push_undo=False)

    for k, v in comp_data.items():
        if k == "type":
            continue

        prop_name = k
        if k == "value":
            prop_name = "Val"
        elif k == "loc" and dist_type in ["normal", "constant"]:
            prop_name = "Val"

        try:
            node.set_property(prop_name, str(v), push_undo=False)
        except Exception:
            pass

    return node


def _is_data_equal(data_a, data_b):
    if data_a.get("type") != data_b.get("type"):
        return False
    keys_a = set(k for k in data_a.keys() if k != "type")
    keys_b = set(k for k in data_b.keys() if k != "type")
    if keys_a != keys_b:
        return False
    for k in keys_a:
        val_a, val_b = data_a[k], data_b[k]
        if val_a == val_b:
            continue
        try:
            if abs(float(val_a) - float(val_b)) > 1e-7:
                return False
        except:
            if str(val_a) != str(val_b):
                return False
    return True
