from skilllogboard.core.events import Event


def test_minimal_event_serialization():
    event = Event(type="lifecycle", key="start")
    data = event.to_dict()

    assert data["type"] == "lifecycle"
    assert data["key"] == "start"
    assert data["value"] is None
    assert data["step"] is None
    assert data["path"] is None
    assert data["metadata"] == {}
    assert data["timestamp"]


def test_full_event_serialization():
    event = Event(
        type="artifact",
        key="checkpoint",
        value={"epoch": 1},
        step=1,
        path="artifacts/best.ckpt",
        metadata={"copy": True},
    )
    data = event.to_dict()

    assert data["type"] == "artifact"
    assert data["key"] == "checkpoint"
    assert data["value"] == {"epoch": 1}
    assert data["step"] == 1
    assert data["path"] == "artifacts/best.ckpt"
    assert data["metadata"] == {"copy": True}
