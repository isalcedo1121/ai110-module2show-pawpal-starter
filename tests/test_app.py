from datetime import time
from pathlib import Path

from streamlit.testing.v1 import AppTest

from pawpal_system import Owner, Pet, Task


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def element(app, kind, label):
    return next(widget for widget in getattr(app, kind) if widget.label == label)


def click(app, label):
    element(app, "button", label).click().run()
    assert not app.exception


def add_task(app, name, duration, priority, due_time):
    element(app, "text_input", "Task name").set_value(name)
    element(app, "number_input", "Duration (minutes)").set_value(duration)
    element(app, "selectbox", "Priority").set_value(priority)
    element(app, "time_input", "Due time").set_value(due_time)
    click(app, "Add task")


def task_table(app):
    return app.table[1].value


def test_edit_task_handles_no_tasks():
    app = AppTest.from_file(str(APP_PATH)).run()

    assert not app.exception
    assert any(message.value == "No tasks to edit. Add a task above." for message in app.info)
    assert not any(widget.label == "Task to edit" for widget in app.selectbox)
    assert not any(widget.label == "Save changes" for widget in app.button)

    click(app, "Add pet")

    assert len(app.session_state["owner"].pets) == 1
    assert any(message.value == "No tasks to edit. Add a task above." for message in app.info)


def test_edit_priority_updates_original_task_and_schedule():
    app = AppTest.from_file(str(APP_PATH)).run()
    click(app, "Add pet")
    add_task(app, "Grooming", 10, "Medium", time(7, 0))
    add_task(app, "Feeding", 10, "Low", time(8, 0))
    owner = app.session_state["owner"]
    grooming, feeding = owner.pets[0].tasks
    element(app, "number_input", "Available minutes today").set_value(10)
    click(app, "Generate schedule")
    assert app.table[2].value["Task"].tolist() == ["Grooming"]

    element(app, "selectbox", "Task to edit").set_value(1).run()
    element(app, "selectbox", "New priority").set_value("High")
    click(app, "Save changes")

    assert app.session_state["owner"] is owner
    assert owner.pets[0].tasks[1] is feeding
    assert len(owner.pets[0].tasks) == 2
    assert feeding.priority == 3
    assert grooming.priority == 2
    assert task_table(app)["Priority"].tolist() == ["Medium", "High"]
    assert any(message.value == "Updated 'Feeding'." for message in app.success)
    click(app, "Generate schedule")
    assert app.table[2].value["Task"].tolist() == ["Feeding"]
    assert app.table[2].value["Priority"].tolist() == ["High"]

    app.run()
    assert feeding.priority == 3
    assert element(app, "selectbox", "New priority").value == "High"


def test_edit_duration_changes_schedule_fit():
    app = AppTest.from_file(str(APP_PATH)).run()
    click(app, "Add pet")
    add_task(app, "Walk", 20, "High", time(8, 0))
    walk = app.session_state["owner"].pets[0].tasks[0]
    element(app, "number_input", "Available minutes today").set_value(10)
    click(app, "Generate schedule")
    assert any("None of the tasks fit" in message.value for message in app.warning)

    element(app, "number_input", "New duration (minutes)").set_value(10)
    click(app, "Save changes")

    assert app.session_state["owner"].pets[0].tasks[0] is walk
    assert walk.duration == 10
    assert task_table(app)["Duration (min)"].tolist() == [10]
    click(app, "Generate schedule")
    assert app.table[2].value["Task"].tolist() == ["Walk"]
    assert app.table[2].value["Duration (min)"].tolist() == [10]
    assert any("10 of 10 minutes used" in message.value for message in app.success)


def test_edit_selection_loads_values_and_updates_only_selected_pet_task():
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", 3)
    luna = Pet("Luna", "cat", 5)
    mochi_task = Task("Feeding", 5, 1, "08:00")
    luna_task = Task("Feeding", 15, 3, "08:00")
    mochi.add_task(mochi_task)
    luna.add_task(luna_task)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    app = AppTest.from_file(str(APP_PATH))
    app.session_state["owner"] = owner
    app.run()

    assert not app.exception
    assert "Mochi" in element(app, "selectbox", "Task to edit").options[0]
    assert "Luna" in element(app, "selectbox", "Task to edit").options[1]
    assert element(app, "number_input", "New duration (minutes)").value == 5
    assert element(app, "selectbox", "New priority").value == "Low"
    element(app, "selectbox", "Task to edit").set_value(1).run()
    assert element(app, "number_input", "New duration (minutes)").value == 15
    assert element(app, "selectbox", "New priority").value == "High"

    element(app, "number_input", "New duration (minutes)").set_value(10)
    element(app, "selectbox", "New priority").set_value("Medium")
    click(app, "Save changes")

    assert mochi.tasks[0] is mochi_task
    assert luna.tasks[0] is luna_task
    assert len(mochi.tasks) == len(luna.tasks) == 1
    assert (mochi_task.duration, mochi_task.priority) == (5, 1)
    assert (luna_task.duration, luna_task.priority) == (10, 2)
    assert any("Conflict on" in message.value for message in app.warning)
    element(app, "selectbox", "Task to edit").set_value(0).run()
    assert element(app, "number_input", "New duration (minutes)").value == 5
    assert element(app, "selectbox", "New priority").value == "Low"
    element(app, "selectbox", "Task to edit").set_value(1).run()
    assert element(app, "number_input", "New duration (minutes)").value == 10
    assert element(app, "selectbox", "New priority").value == "Medium"
