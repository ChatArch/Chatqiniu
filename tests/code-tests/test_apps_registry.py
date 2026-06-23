from chatqiniu.apps import find_app, load_apps, remove_app, upsert_app


def test_app_registry_round_trip(tmp_path):
    registry = tmp_path / "apps.json"

    app = upsert_app(
        name="demo",
        endpoint="https://demo.example.com",
        title="Demo",
        description="Demo app",
        path=registry,
    )

    assert app.name == "demo"
    assert find_app("demo", registry) == app
    assert load_apps(registry) == [app]
    assert remove_app("demo", registry) is True
    assert load_apps(registry) == []
