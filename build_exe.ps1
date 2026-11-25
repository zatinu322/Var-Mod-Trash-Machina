$CompanyName = "PAVLIKRPG"
$ProductName = "Ex Machina Randomizer"
$FileVersion = "2.0.0"
$FileDescription = "Randomizer for Ex Machina / Hard Truck Apocalypse."

Copy-Item .\main.exe .\main.exe.bak -Verbose -Force

uv run nuitka `
--standalone `
--onefile `
--follow-imports `
--plugin-enable=pylint-warnings `
src/main.py `
--output-dir=dist `
--include-data-files=src/localisation.yaml=localisation.yaml `
--include-data-dir=src/assets=assets `
--windows-company-name="$CompanyName" `
--windows-product-name="$ProductName" `
--windows-file-version="$FileVersion" `
--windows-file-description="$FileDescription" `
--windows-console-mode=disable `
--windows-icon-from-ico=".\src\assets\rpg_logo.ico"

Move-Item .\dist\main.exe .\main.exe -Verbose -Force
