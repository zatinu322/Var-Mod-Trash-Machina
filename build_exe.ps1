Copy-Item .\main.exe .\main.exe.bak -Verbose -Force

poetry run nuitka `
--standalone `
--onefile `
--follow-imports `
--plugin-enable=pylint-warnings `
src/main.py `
--output-dir=dist `
--include-data-dir=src/localisation=localisation `
--include-data-dir=src/assets=assets `
--windows-company-name="PAVLIKRPG" `
--windows-product-name="Ex Machina Randomizer" `
--windows-file-version=1.3.0 `
--windows-file-description="Randomizer for Ex Machina" `
--windows-console-mode=disable `
--windows-icon-from-ico=".\src\assets\rpg_logo.ico" 

Move-Item .\dist\main.exe .\main.exe -Verbose -Force