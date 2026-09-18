from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]


def test_windows_launcher_delegates_to_shared_cli_host() -> None:
    source = (PROJECT_ROOT / "launcher/cgcli.cmd").read_text(encoding="utf-8")

    assert "CongGuoCliHost.exe" in source
    assert '"%APP_HOST%" --cgcli %*' in source
    assert "CGCLI_APP_PATH" in source
    assert "exit /b %ERRORLEVEL%" in source


def test_windows_installer_records_host_and_updates_user_path() -> None:
    source = (PROJECT_ROOT / "scripts/install-launcher-windows.ps1").read_text(
        encoding="utf-8"
    )

    assert "cgcli-app-path.txt" in source
    assert "CongGuoCliHost.exe" in source
    assert '--cgcli --version' in source
    assert 'SetEnvironmentVariable("Path", $UpdatedPath, "User")' in source
