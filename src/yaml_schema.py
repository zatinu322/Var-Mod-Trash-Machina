from jsonschema import validate, ValidationError
import yaml

MANIFEST_SCHEMA = {
    "type": "object",
    "properties": {
        "version_validation": {"type": ["boolean", "string", "array"]},
        "resources_validation": {"type": "array"},
        "FolderToCopy": {"type": "string"},
        
    },
    "required": []
}

with open("/home/lypavel/Desktop/ExMachina/Var-Mod-Trash-Machina/resources/manifests/manifest_steam.yaml", "r", encoding="utf-8")as stream:
    data = yaml.safe_load(stream)

print(len(data.keys()))

try:
    validate(data, MANIFEST_SCHEMA)
except ValidationError as e:
    print(e)