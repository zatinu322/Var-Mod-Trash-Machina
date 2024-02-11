LOG("Setting randomizer globals...")

RAND_DWELLER = false
RAND_GUNS = false
RAND_VEH = false
RAND_PLAYER_VEH = false

RAND_GUNS_1 = {}
RAND_GUNS_2 = {}

RAND_VEH_1 = {}
RAND_VEH_2 = {}
RAND_VEH_3 = {}

RAND_DWELLER_1 = {}

LOG("Randomizer globals set.")

EXECUTE_SCRIPT "data\\scripts\\randomizer.lua"