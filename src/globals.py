AGENTS = ['Phoenix', 'Reyna', 'Jett', 'Raze', 'Yoru', 'Neon', 'Iso', 'Sova', 
          'Breach', 'Skye', r'KAY/O', 'Fade', 'Gekko', 'Clove', 'Brimstone', 'Viper', 
          'Omen', 'Astra', 'Harbor', 'Vyse', 'Sage', 'Cypher', 'Killjoy', 
          'Chamber', 'Deadlock']

X_COLUMNS = {
    "Agent_Type": ["Duelist", "Initiator", "Controller", "Sentinel"],
    "Playstyle": ["Balanced", "Aggressive", "Supportive", "Map-control", "Info-gathering"],
    "Difficulty": ["Easy", "Hard"],
    "Ability_Preference": ["Flashes/Stuns", "Smokes", "Healing", "Agility", "Information"],
    "Gun_Type": ["SMGs", "Shotguns", "Rifles", "Snipers", "Machine Guns"]
}

PREPROCESSED_X_COLUMNS = [
    'Difficulty',
    'Agent_Type_Duelist',
    'Agent_Type_Initiator',
    'Agent_Type_Sentinel',
    'Playstyle_Balanced',
    'Playstyle_Info-gathering',
    'Playstyle_Map-control',
    'Playstyle_Supportive',
    'Ability_Preference_Flashes/Stuns',
    'Ability_Preference_Healing',
    'Ability_Preference_Information',
    'Ability_Preference_Smokes',
    'Gun_Type_Rifles',
    'Gun_Type_SMGs',
    'Gun_Type_Shotguns',
    'Gun_Type_Snipers'
]

DIFFICULTY_MAPPINGS = {
    'Easy': 0.0,
    'Hard': 1.0
}

AGENT_MAPPINGS = [
    'Astra', 'Breach', 'Brimstone', 'Chamber', 'Clove', 'Cypher',
    'Deadlock', 'Fade', 'Gekko', 'Harbor', 'Iso', 'Jett', 'Killjoy',
    'Neon', 'Omen', 'Phoenix', 'Raze', 'Reyna', 'Sage', 'Skye',
    'Sova', 'Viper', 'Vyse', 'Yoru'
]